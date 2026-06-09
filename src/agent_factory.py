import httpx
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from src.schema_factory import SchemaFactory
from src.schemas import LabReportSchema
import sys

class LabExtractionAgent:
    def __init__(self, config, logger, custom_schema_dict=None):
        """
        Initializes either LangChain Ollama or OpenAI model with structured output.
        Supports Ollama (local) and LM Studio (OpenAI-compatible) backends.
        Enforces network timeouts via httpx.Client.
        Supports dynamic schema injection via custom_schema_dict.
        """
        self.logger = logger
        model_name = config['model']['name']
        
        # Safely get schema name from config, fallback to LabReport
        schema_name = config['model'].get('schema', 'LabReport') 
        self.schema_factory = SchemaFactory()

        # Determine provider (default to ollama if not specified)
        provider = config['model'].get('provider', 'ollama').lower()
        
        # Extract timeout config (default 120s)
        timeout_seconds = config['model'].get('timeout', 120)
        
        if provider == 'ollama':
            base_url = config['model'].get('base_url', 'http://localhost:11434')
            
            # Create a custom HTTP client with strict timeout
            http_client = httpx.Client(timeout=timeout_seconds)
            
            # Initialize ChatOllama with this client
            llm = ChatOllama(
                model=model_name,
                temperature=0,  # Deterministic for data extraction
                base_url=base_url,
                client=http_client  # Inject custom client for timeout support
            )
            
        elif provider == 'lmstudio':
            # LM Studio runs an OpenAI-compatible server
            base_url = config['model'].get('base_url', 'http://localhost:1234/v1')
            api_key = config['model'].get('api_key', 'lm-studio')  # LM Studio often ignores API key
            
            # Create HTTP client for LM Studio
            http_client = httpx.Client(timeout=timeout_seconds)
            
            # Initialize ChatOpenAI with LM Studio configuration
            llm = ChatOpenAI(
                model=model_name,
                temperature=0,
                base_url=base_url,
                api_key=api_key,
                http_client=http_client,
                max_retries=0  # Disable retries for faster failure
            )
            
        else:
            raise ValueError(f"Unsupported provider: {provider}. Use 'ollama' or 'lmstudio'")
        
        self.runnable = llm
        
        # Bind the schema (Custom JSON dict OR Pydantic model from SchemaFactory)
        if custom_schema_dict:
            self.logger.info("Binding custom JSON schema to model.")
            self.runnable = llm.with_structured_output(custom_schema_dict)
        else:
            self.logger.info(f"Binding SchemaFactory schema: '{schema_name}' to model.")
            schema = self.schema_factory.get_schema(schema_name)
            if schema:
                self.runnable = llm.with_structured_output(schema)

        # Store provider for logging/debugging
        self.provider = provider

    def invoke(self, image_b64: str, prompt_text: str, filename: str, callbacks=None):
        """
        Runs the agent on a single image or text file.
        Returns: A validated Pydantic object (if using SchemaFactory) or a dict (if using custom_schema_dict).
        """
        # Construct the multimodal message
        messages = [{"type": "text", "text": prompt_text}]

        if image_b64:
            image_message = {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}
            }
            messages.append(image_message)
        
        message = HumanMessage(
            content=messages
        )
        
        self.logger.info(f"[{filename}] >>> Sending request to {self.provider}...")
        
        # Invoke the chain with callbacks (Opik) and metadata
        return self.runnable.invoke(
            [message],
            config={
                "callbacks": callbacks,
                "metadata": {"filename": filename, "provider": self.provider}
            }
        )
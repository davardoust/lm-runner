import httpx
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from src.schema_factory import SchemaFactory
from schemas import LabReport
import sys

class LabExtractionAgent:
    def __init__(self, config, logger):
        """
        Initializes either LangChain Ollama or OpenAI model with structured output.
        Supports Ollama (local) and LM Studio (OpenAI-compatible) backends.
        Enforces network timeouts via httpx.Client.
        """
        self.logger = logger
        model_name = config['model']['name']
        schema_name = config['model']['schema']
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
        
        # Bind the Pydantic Schema directly to the model
        schema = self.schema_factory.get_schema(schema_name)
        
        self.runnable = llm
        
        if schema:
            self.runnable = llm.with_structured_output(schema)

        # Store provider for logging/debugging
        self.provider = provider

    def invoke(self, image_b64: str, prompt_text: str, filename: str, callbacks=None) -> LabReport:
        """
        Runs the agent on a single image.
        Returns: A validated LabReport Pydantic object.
        """
        # Construct the multimodal message
        messages = [{"type": "text", "text": prompt_text}]

        image_message = {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}
                        }

        if image_b64:
           messages.append(image_message)
        
        message = HumanMessage(
            content = messages
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
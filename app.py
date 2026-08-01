import os
import yaml
import time
import copy
import json
import tempfile
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

# Load Environment Variables before initializing any LangChain/Opik integrations
load_dotenv()

from src.logger import setup_logger
from src.agent_factory import LabExtractionAgent
from src.preprocessor import ImagePreprocessor
from opik.integrations.langchain import OpikTracer

# Initialize FastAPI app
app = FastAPI(
    title="Lab Report Extraction API",
    description="API for extracting structured data from Lab Reports using LLMs/VLM",
    version="1.0.0"
)

def load_config(path='config.yaml'):
    """Loads the base YAML configuration file."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Configuration file '{path}' not found.")
    with open(path, 'r') as f:
        return yaml.safe_load(f)

# Global initialization
try:
    base_config = load_config()
    logger = setup_logger(base_config)
    logger.info("API initialized with base config.")
except Exception as e:
    print(f"Critical startup failure: {e}")
    raise e

def get_prompt_text(prompt_name: str, prompts_dir: str) -> str:
    """Retrieves the prompt template based on prompt_name."""
    if not prompt_name.endswith('.txt'):
        prompt_name += '.txt'
    
    prompt_path = os.path.join(prompts_dir, prompt_name)
    if not os.path.exists(prompt_path):
        raise HTTPException(status_code=404, detail=f"Prompt '{prompt_name}' not found in {prompts_dir}.")
        
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read().strip()

@app.post("/extract")
async def extract_lab_report(
    content: str = Form(..., description="The lab report content - either base64 encoded image string or raw text"),
    content_type: str = Form(..., description="Type of content provided: 'image_b64' or 'raw_text'"),
    prompt_name: str = Form(..., description="Name of the prompt file (e.g., 'blood_test_v1')"),
    model_name: str = Form(..., description="Target model name (e.g., 'llama3', 'gpt-4o')"),
    provider: str = Form("ollama", description="Model provider ('ollama' or 'lmstudio')"),
    schema_name: str = Form("LabReport", description="Name of the Pydantic schema in SchemaFactory"),
    custom_schema: str = Form(None, description="Optional raw JSON schema string to bypass SchemaFactory"),
    filename: str = Form("unknown", description="Optional filename for logging purposes")
):
    start_time = time.time()
    
    # 1. Parse dynamic schema if provided
    schema_dict = None
    if custom_schema:
        try:
            schema_dict = json.loads(custom_schema)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="custom_schema must be a valid JSON string.")
    
    # Validate content_type
    if content_type not in ['image_b64', 'raw_text']:
        raise HTTPException(status_code=400, detail="content_type must be either 'image_b64' or 'raw_text'")

    # 2. Isolate config for this specific request to prevent race conditions
    request_config = copy.deepcopy(base_config)
    request_config['model']['name'] = model_name
    request_config['model']['provider'] = provider
    request_config['model']['schema'] = schema_name
    
    prompts_dir = request_config.get('system', {}).get('prompts_dir', 'prompts/')
    
    try:
        # 3. Retrieve Prompt
        prompt_text = get_prompt_text(prompt_name, prompts_dir)
        
        # 4. Initialize Agent & Opik Tracer
        agent = LabExtractionAgent(request_config, logger, custom_schema_dict=schema_dict)
        
        opik_tracer = OpikTracer(
            tags=["api-extraction", provider, model_name],
            project_name="medical-ocr-extraction"
        )
        
        img_b64 = None
        combined_text = prompt_text
        
        # 5. Process based on content_type
        if content_type == 'image_b64':
            # Use the provided base64 string directly
            img_b64 = content
            
        elif content_type == 'raw_text':
            # Combine prompt with raw text
            combined_text = prompt_text + "\n\n" + content
        
        # 6. Execute Extraction
        logger.info(f"API Processing [{filename}] | Model: {model_name} | Prompt: {prompt_name} | Type: {content_type}")
        
        lab_report = agent.invoke(
            image_b64=img_b64,
            prompt_text=combined_text,
            filename=filename,
            callbacks=[opik_tracer]
        )
        
        # 7. Extract Data Safely (Handles both Pydantic Models and raw dicts)
        if hasattr(lab_report, "model_dump"):
            response_data = lab_report.model_dump()
        elif hasattr(lab_report, "dict"):  # Fallback for older Pydantic versions
            response_data = lab_report.dict()
        else:
            response_data = lab_report  # It's already a dictionary (from custom JSON schema)

        duration = round(time.time() - start_time, 2)
        
        # 8. Format Response
        return JSONResponse(content={
            "status": "success",
            "filename": filename,
            "provider": provider,
            "model": model_name,
            "prompt_id": prompt_name,
            "schema_used": "custom_json" if custom_schema else schema_name,
            "content_type": content_type,
            "duration": duration,
            "data": response_data
        })
        
    except Exception as e:
        logger.error(f"API Error processing {filename}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Make sure to run from the root of your project
    uvicorn.run("app:app", host="0.0.0.0", port=8005, reload=False)
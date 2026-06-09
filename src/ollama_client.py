# import requests
# import json
# import time

# class OllamaClient:
#     def __init__(self, config, logger):
#         self.base_url = config['model']['base_url']
#         self.model = config['model']['name']
#         self.timeout = config['model']['timeout']
#         self.max_retries = config['system']['max_retries']
#         self.logger = logger

#     def generate(self, prompt: str, image_b64: str, schema_json: dict = None) -> dict:
#         url = f"{self.base_url}/api/generate"
        
#         # Ollama 'json' format mode forces valid JSON structure
#         payload = {
#             "model": self.model,
#             "prompt": prompt,
#             "images": [image_b64],
#             "stream": False,
#             "format": "json", 
#             "options": {
#                 "temperature": 0.1,
#                 "num_ctx": 4096 # Ensure enough context for long reports
#             }
#         }

#         for attempt in range(self.max_retries):
#             try:
#                 self.logger.debug(f"Sending request to Ollama (Attempt {attempt+1})")
#                 response = requests.post(url, json=payload, timeout=self.timeout)
#                 response.raise_for_status()
                
#                 result = response.json()
#                 return {
#                     "raw_response": result['response'],
#                     "duration": result.get('total_duration', 0)
#                 }
                
#             except Exception as e:
#                 self.logger.warning(f"Ollama Request Failed (Attempt {attempt+1}): {e}")
#                 time.sleep(2)
        
#         raise ConnectionError(f"Failed to communicate with Ollama after {self.max_retries} retries.")

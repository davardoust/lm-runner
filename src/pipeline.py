import os
import time
import json
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from .preprocessor import ImagePreprocessor
from .agent_factory import LabExtractionAgent
from schemas import LabReport

# Import Opik Tracer
from opik.integrations.langchain import OpikTracer

class LabReportPipeline:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.preprocessor = ImagePreprocessor(logger)
        self.agent = LabExtractionAgent(config, logger)
        
        self.results_dir = os.path.join(config['system']['output_dir'], 'results')
        self.model_name = os.path.join(config['model']['name'], '')

        self.results_dir = f"{self.results_dir}/{self.model_name}"
        os.makedirs(self.results_dir, exist_ok=True)
        
        # 1. Load Prompts from JSON
        self.prompts = self._load_prompts()
        
        # 2. Create sub-folders for each prompt ID
        for prompt in self.prompts:
            p_id = prompt['id']
            p_dir = os.path.join(self.results_dir, p_id)
            os.makedirs(p_dir, exist_ok=True)

        # 3. Initialize Opik Tracer
        # Ensure OPIK_API_KEY is set in environment or via `opik configure`
        self.opik_tracer = OpikTracer(
            tags=["lab-report-pipeline"],
            project_name="medical-ocr-extraction"
        )
        self.logger.info("Opik Observability initialized.")

    def _load_prompts(self):
        path = self.config['system'].get('prompts_dir', 'prompts/')
        try:
            prompts = []
            
            # Get all txt files in the directory
            if os.path.exists(path):
                for filename in os.listdir(path):
                    if filename.endswith('.txt'):
                        file_id = os.path.splitext(filename)[0]  # Remove .txt extension
                        
                        # Read the content of the txt file
                        file_path = os.path.join(path, filename)
                        with open(file_path, 'r', encoding='utf-8') as f:
                            text_content = f.read().strip()
                        
                        prompts.append({
                            'id': file_id,
                            'text': text_content
                        })
            
            self.logger.info(f"Loaded {len(prompts)} prompts from directory {path}")
            return prompts
            
        except Exception as e:
            self.logger.error(f"Failed to load prompts directory: {e}")
            raise e


    def process_single_image(self, image_path):
        filename = os.path.basename(image_path)
        start_time = time.time()
        
        # Stats container for this image (across all prompts)
        image_stats = {
            "filename": filename,
            "total_time": 0,
            "success_count": 0,
            "fail_count": 0,
            "skipped_count": 0
        }

        try:
            self.logger.info(f"[{filename}] Stage 1: Preprocessing")
            img_b64 = self.preprocessor.process(image_path)

            # Iterate through ALL loaded prompts
            for prompt_cfg in self.prompts:
                p_id = prompt_cfg['id']
                p_text = prompt_cfg['text']
                
                # Define output path: results/{prompt_id}/{filename}.json
                prompt_output_dir = os.path.join(self.results_dir, p_id)
                output_file_path = os.path.join(prompt_output_dir, f"{filename}.json")
                
                # ✅ Check if output file already exists
                if os.path.exists(output_file_path):
                    self.logger.info(f"[{filename}] Prompt '{p_id}' - Output file already exists, skipping...")
                    image_stats["skipped_count"] += 1
                    continue
                
                self.logger.info(f"[{filename}] Running Prompt: {p_id}")
                prompt_start = time.time()
                
                result_entry = {
                    "filename": filename,
                    "prompt_id": p_id,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "status": "pending",
                    "data": None,
                    "error": None,
                    "duration": 0
                }

                try:
                    # Invoke Agent with Opik Tracer
                    lab_report: LabReport = self.agent.invoke(
                        img_b64, 
                        p_text, 
                        filename,
                        callbacks=[self.opik_tracer] # Pass tracer here
                    )
                    
                    # Success
                    result_entry["status"] = "success"
                    result_entry["data"] = lab_report.model_dump()
                    image_stats["success_count"] += 1
                    self.logger.info(f"[{filename}] Prompt '{p_id}' Success")

                except Exception as e:
                    self.logger.error(f"[{filename}] Prompt '{p_id}' Failed: {e}")
                    result_entry["status"] = "failed"
                    result_entry["error"] = str(e)
                    image_stats["fail_count"] += 1
                
                finally:
                    duration = round(time.time() - prompt_start, 2)
                    result_entry["duration"] = duration
                    
                    # Save Result Immediately
                    with open(output_file_path, 'w', encoding='utf-8') as f:
                        json.dump(result_entry, f, ensure_ascii=False, indent=2)

        except Exception as e:
            self.logger.error(f"[{filename}] Critical Preprocessing Failure: {e}")
            image_stats["fail_count"] = len(self.prompts) # All prompts failed implicitly
        
        finally:
            image_stats["total_time"] = round(time.time() - start_time, 2)
        return image_stats

    def run_batch(self):
        input_dir = self.config['system']['input_dir']
        all_files = os.listdir(input_dir)

        # ✅ Collect images (unchanged)
        images = [os.path.join(input_dir, f) for f in all_files
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]

        # ✅ Collect txt files (new)
        texts = [os.path.join(input_dir, f) for f in all_files
                if f.lower().endswith('.txt')]

        self.logger.info(
            f"Starting batch for {len(images)} images and {len(texts)} text files "
            f"with {self.config['system']['batch_size']} threads."
        )

        summary_stats = []

        with ThreadPoolExecutor(max_workers=self.config['system']['batch_size']) as executor:
            futures = {}

            # ✅ Dispatch images → process_single_image (unchanged)
            for img in images:
                futures[executor.submit(self.process_single_image, img)] = img

            # ✅ Dispatch txt files → process_single_txt (new)
            for txt in texts:
                futures[executor.submit(self.process_single_txt, txt)] = txt

            for future in as_completed(futures):
                stats = future.result()
                summary_stats.append(stats)

        # CSV summary — updated with skipped_count
        csv_path = os.path.join(self.config['system']['output_dir'], 'summary_report.csv')
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["filename", "total_time", "success_count", "fail_count", "skipped_count"])
            writer.writeheader()
            writer.writerows(summary_stats)

        self.logger.info(f"Batch completed. Summary at {csv_path}")

    def process_single_txt(self, txt_path):
        filename = os.path.basename(txt_path)
        start_time = time.time()

        image_stats = {
            "filename": filename,
            "total_time": 0,
            "success_count": 0,
            "fail_count": 0,
            "skipped_count": 0
        }

        try:
            self.logger.info(f"[{filename}] Stage 1: Reading Text File")
            with open(txt_path, 'r', encoding='utf-8') as f:
                txt_content = f.read()

            for prompt_cfg in self.prompts:
                p_id = prompt_cfg['id']
                p_text = prompt_cfg['text']

                # ✅ Concat prompt with txt file content
                combined_text = p_text + "\n\n" + txt_content

                prompt_output_dir = os.path.join(self.results_dir, p_id)
                output_file_path = os.path.join(prompt_output_dir, f"{filename}.json")

                # ✅ Check if output file already exists
                if os.path.exists(output_file_path):
                    self.logger.info(f"[{filename}] Prompt '{p_id}' - Output file already exists, skipping...")
                    image_stats["skipped_count"] += 1
                    continue

                self.logger.info(f"[{filename}] Running Prompt: {p_id}")
                prompt_start = time.time()

                result_entry = {
                    "filename": filename,
                    "prompt_id": p_id,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "status": "pending",
                    "data": None,
                    "error": None,
                    "duration": 0
                }

                try:
                    # No image — pass None for img_b64
                    lab_report: LabReport = self.agent.invoke(
                        None,
                        combined_text,
                        filename,
                        callbacks=[self.opik_tracer]
                    )
                    result_entry["status"] = "success"
                    result_entry["data"] = lab_report.model_dump()
                    image_stats["success_count"] += 1
                    self.logger.info(f"[{filename}] Prompt '{p_id}' Success")

                except Exception as e:
                    self.logger.error(f"[{filename}] Prompt '{p_id}' Failed: {e}")
                    result_entry["status"] = "failed"
                    result_entry["error"] = str(e)
                    image_stats["fail_count"] += 1

                finally:
                    duration = round(time.time() - prompt_start, 2)
                    result_entry["duration"] = duration

                    with open(output_file_path, 'w', encoding='utf-8') as f:
                        json.dump(result_entry, f, ensure_ascii=False, indent=2)

        except Exception as e:
            self.logger.error(f"[{filename}] Critical Text Read Failure: {e}")
            image_stats["fail_count"] = len(self.prompts)

        finally:
            image_stats["total_time"] = round(time.time() - start_time, 2)

        return image_stats
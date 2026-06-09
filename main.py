import yaml
import os
import sys
from dotenv import load_dotenv

# 1. Load Environment Variables (for Opik/LangChain/etc)
# This must happen before importing modules that might initialize clients based on env vars.
load_dotenv()

from src.logger import setup_logger
from src.pipeline import LabReportPipeline

def load_config(path='config.yaml'):
    """
    Loads the YAML configuration file.
    """
    if not os.path.exists(path):
        print(f"Error: Configuration file '{path}' not found.")
        sys.exit(1)
        
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def main():
    # 2. Load Configuration
    config_path = 'config.yaml'
    config = load_config(config_path)
    
    # 3. Setup Logger
    # This creates the log directory if it doesn't exist
    logger = setup_logger(config)
    logger.info("Pipeline initialized.")
    
    # 4. Initialize Pipeline
    try:
        pipeline = LabReportPipeline(config, logger)
        
        # 5. Run Batch Processing
        logger.info("Starting batch execution...")
        pipeline.run_batch()
        logger.info("Pipeline execution finished successfully.")
        
    except KeyboardInterrupt:
        logger.warning("Pipeline execution interrupted by user.")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Fatal error in pipeline: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()

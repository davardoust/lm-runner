import logging
import os
from datetime import datetime

def setup_logger(config):
    log_dir = os.path.join(config['system']['output_dir'], 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"pipeline_{timestamp}.log")
    
    logger = logging.getLogger("LabPipeline")
    logger.setLevel(getattr(logging, config['system']['log_level']))
    
    # File Handler
    fh = logging.FileHandler(log_file, encoding='utf-8')
    fh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - [Thread-%(threadName)s] - %(message)s'))
    
    # Console Handler
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger

import base64
import io
from PIL import Image

class ImagePreprocessor:
    def __init__(self, logger):
        self.logger = logger

    def process(self, image_path: str) -> str:
        """
        Loads image, converts to RGB, resizes if too large (optional),
        and returns base64 string.
        """
        try:
            self.logger.debug(f"Preprocessing {image_path}")
            with Image.open(image_path) as img:
                # Convert to RGB to handle PNG transparency or grayscale
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Optional: Resize if dimensions > 2000px to save token processing time
                max_dim = 2000
                if max(img.size) > max_dim:
                    img.thumbnail((max_dim, max_dim))
                
                buffered = io.BytesIO()
                img.save(buffered, format="JPEG", quality=85)
                img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
                
            return img_str
        except Exception as e:
            self.logger.error(f"Failed to preprocess image {image_path}: {e}")
            raise e

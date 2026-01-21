import logging
import sys
from app.core.config import settings

def setup_logging():
    """
    Configure the root logger to output standardized logs to stdout.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Clear existing handlers
    if logger.handlers:
        logger.handlers = []

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    
    # Simple standardized format: Time - Level - LoggerName - Message
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    
    # Silence overly verbose libraries if needed
    logging.getLogger("uvicorn.access").handlers = [] # We might want to keep uvicorn access logs or redirect them
    # For now, let's keep it simple and just ensure our app logs show up nicely
    
    # Set levels for specific third-party libs
    logging.getLogger("httpx").setLevel(logging.WARNING)

    return logger

# Create a module-level logger for imports if desired, 
# though standard practice is `logging.getLogger(__name__)` in each file.
logger = setup_logging()

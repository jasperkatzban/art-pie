import mido, pyo
import logging

logger = logging.getLogger(__name__)

class Audio:
    """Handle audio generation"""

    def __init__(self):
        logger.info('Initializing audio module!')
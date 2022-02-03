from app import create_app
import logging

logger = logging.getLogger('seth')
logger.setLevel(logging.INFO)
logger.handlers.append(logging.StreamHandler())

application = create_app('development')
from flask_wtf.csrf import validate_csrf
from logging import getLogger

logger = getLogger('seth')
def wechat_validate_token(token):
	try:
		validate_csrf(token)
		logger.info('validation to token passed returning true')
		return True
	except:
		logger.info('validation of token failed returning false')
		return False

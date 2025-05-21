import logging

# class ErrorLogFilter(logging.Filter):
#     def filter(self, record):
#         return record.levelname == 'ERROR' and 'важно' in record.msg.lower()
    
# logger = logging.getLogger(__name__)

# stderr_handler = logging.StreamHandler()

# stderr_handler.addFilter(ErrorLogFilter())

# logger.addHandler(stderr_handler)

# logger.warning('Важно! Это лог с предупреждением!')
# logger.error('Важно! Это лог с ошибкой!')
# logger.info('Важно! Это лог с уровня INFO!')
# logger.error('Это лог с ошибкой!')

class EvenLogFilter(logging.Filter):
    def filter(self, record):
        return not record.i % 2

logger = logging.getLogger(__name__)

stderr_handler = logging.StreamHandler()

stderr_handler.addFilter(EvenLogFilter())

logger.addHandler(stderr_handler)

for i in range(10):
    logger.warning("ВАЖНЫЙ ЛОГ %d", i, extra={'i': i})


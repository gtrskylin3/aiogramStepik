import logging
# logger = logging.getLogger()

# print(logger.parent)

# logger = logging.getLogger(__name__)

# print(logger.parent)

logger1 = logging.getLogger('one')

print(logger1.parent)

logger2 = logging.getLogger('one.xui')

print(logger2.parent)


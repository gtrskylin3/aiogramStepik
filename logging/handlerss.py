import logging, sys



# # print(logger.handlers)
# format_1 = '#%(levelname)-8s [%(asctime)s] - %(filename)s:' \
# '%(lineno)d - %(name)s - %(message)s'

# format_2 = '[{asctime}] #{levelname:8} {filename}:' \
# '{lineno} - {name} - {message}'

# formatter_1 = logging.Formatter(fmt=format_1)
# formatter_2 = logging.Formatter(
#     fmt=format_2,
#     style='{'
#     )

# logger = logging.getLogger(__name__)


# stderr_handler = logging.StreamHandler()
# stdout_handler = logging.StreamHandler(sys.stdout)

# stderr_handler.setFormatter(formatter_1)
# stdout_handler.setFormatter(formatter_2)

# logger.addHandler(stderr_handler)
# logger.addHandler(stdout_handler)




# print(logger.handlers)

# logger.warning('zxc zxc zxc')


# Пример 3. Хэндлер для записи логов в файл.

logger = logging.getLogger(__name__)

file_handler = logging.FileHandler('logs.log',
                                   encoding='utf-8')

logger.addHandler(file_handler)

print(logger.handlers)

logger.warning("опасность")
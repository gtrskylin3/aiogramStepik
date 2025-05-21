# format='[%(asctime)s] #%(levelname)-8s %(filename)s:'
# '%(lineno)d - %(name)s - %(message)s'
import logging

# logging.basicConfig(
#     level=logging.DEBUG,
#     format = '[{asctime}] #{levelname:8} {filename}:' \
#         '{lineno} = {name} - {message}',
#         style= '{'
# )
# # logging.basicConfig(
# #     level=logging.DEBUG,
# #     format = '[%(asctime)s] #%(levelname)-8s %(filename)s:' \
# #     '%(lineno)d - %(name)s - %(message)s'
# # )

# logger = logging.getLogger(__name__)

# logger.debug('ЛОГ ДЕБАГ')

format_1 = '#%(levelname)-8s [%(asctime)s] - %(filename)s:' \
'%(lineno)d - %(name)s - %(message)s'

format_2 = '[{asctime}] #{levelname:8} {filename}:' \
'{lineno} - {name} - {message}'

formatter_1 = logging.Formatter(fmt=format_1)
formatter_2 = logging.Formatter(
    fmt=format_2,
    style='{'
    )


import logging

# logging.error('эТО БАГ суКА')
logging.basicConfig(level=logging.DEBUG) 
# logging.basicConfig(level=logging.CRITICAL) 
# СТАВИМ ПЕРВЫМ УРОВНЕМ ДЕБАГ ЛОГИ ВМЕСТО ВАРНИНГ 

logging.debug('это лог дебага')
logging.info('это лог инфа')
logging.warning('это лог уровня варнинг опасно сука')
logging.error('это лог уровня еррор')
logging.critical('это крит лог')

# DEBUG (10)
# INFO (20)
# WARNING (30)
# ERROR (40)
# CRITICAL (50)

logger = logging.getLogger(__name__)

print(dir(logger))
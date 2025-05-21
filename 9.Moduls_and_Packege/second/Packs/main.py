print('Это основной модуль main.py, ' \
'его имя в процессе выполнения программы:', __name__)


from pack_1.file_11 import a
from pack_2.pack_21 import file_211

print('a =', a)
print('b =', file_211.b)
print('Словарь some_dict:', file_211.some_dict)
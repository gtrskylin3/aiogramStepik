from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio.session import AsyncSession

from filters.chat_types import ChatTypeFilter, IsAdmin
from kbds.reply import get_keyboard
from database.orm_query import orm_add_product, orm_delete_product, orm_get_product, orm_get_products, orm_update_product
from kbds.inline import get_callback_btns, get_inlineMix_btns, get_url_btns



admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())

ADMIN_KB = get_keyboard(
    "Добавить товар",
    "Ассортимент",
    placeholder="Выберите действие",
    sizes=(2,),
)

class AddProduct(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()

    product_for_change = None

    texts = {
        'AddProduct:name': 'Введите название заново:',
        'AddProduct:description': 'Введите описание заново:',
        'AddProduct:price': 'Введите стоимость заново:',
        'AddProduct:image': 'Этот стейт последний, поэтому...',
    }

@admin_router.message(Command("admin"))
async def add_product(message: types.Message):
    await message.answer("Что хотите сделать?", reply_markup=ADMIN_KB)


@admin_router.message(F.text == "Ассортимент")
async def starring_at_product(message: types.Message, session: AsyncSession):
    for product in await orm_get_products(session):
        print(product)
        await message.answer_photo(
            photo=product.image,
            caption=f"""<strong>{product.name}</strong>
                    \n{product.description}\nЦена: {round(product.price, 2)}
                    """,
            reply_markup=get_callback_btns(
                btns={
                    "Удалить": f"delete_{product.id}",
                    "Изменить": f"change_{product.id}",
                })
            )
    await message.answer("ОК, вот список товаров 🔝")

@admin_router.callback_query(F.data.startswith('delete_'))
async def delete_product(callback: types.CallbackQuery, session: AsyncSession):
    product_id = callback.data.split("_")[-1] # получаем product.id
    await orm_delete_product(session, int(product_id))

    await callback.answer("Товар удален")
    await callback.message.answer("Товар удален!")


@admin_router.callback_query(StateFilter(None), F.data.startswith('change_'))
async def change_product(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    product_id = callback.data.split("_")[-1] # получаем product.id
    # теперь нужно получить продукт для изменения 
    product_for_change = await orm_get_product(session, int(product_id))
    
    AddProduct.product_for_change = product_for_change # созраняем в класс дополнительно
    await callback.answer()
    await callback.message.answer("Введите название товара",
                                  reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddProduct.name)


    


#Код ниже для машины состояний (FSM)


@admin_router.message(StateFilter(None), F.text == "Добавить товар")
async def add_product(message: types.Message, state: FSMContext):
    await message.answer(
        "Введите название товара", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddProduct.name)

@admin_router.message(StateFilter('*'), Command("отмена"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:

    current_state = await state.get_state()
    if current_state is None:
        return
    if AddProduct.product_for_change:
        AddProduct.product_for_change = None
    await state.clear()
    await message.answer("Действия отменены", reply_markup=ADMIN_KB)


@admin_router.message(Command("назад"))
@admin_router.message(F.text.casefold() == "назад")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state == AddProduct.name:
        await message.answer('Предыдущего шага нет, название или отмена')
        return
    
    previous = None
    for step in AddProduct.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f'вы вернулись к прошлому шагу \n {AddProduct.texts[previous.state]}')
            return
        previous = step

@admin_router.message(AddProduct.name, or_f(F.text, F.text == '.'))
async def add_name(message: types.Message, state: FSMContext):
    if message.text == '.':
        await state.update_data(name=AddProduct.product_for_change.name)
    else:
        if len(message.text) >= 100:
            await message.answer("Название товара не должно быть больше 100 символов\n Введите заново")
            return
        await state.update_data(name=message.text)
    await message.answer("Введите описание товара")
    await state.set_state(AddProduct.description)

@admin_router.message(AddProduct.name)
async def add_name(message: types.Message, state: FSMContext):
    await message.answer("Вы отправили не название введите название товара")


@admin_router.message(AddProduct.description, or_f(F.text, F.text == '.'))
async def add_description(message: types.Message, state: FSMContext):
    if message.text == '.':
        await state.update_data(description=AddProduct.product_for_change.description)
    else:
        await state.update_data(description=message.text)
    await message.answer("Введите стоимость товара")
    await state.set_state(AddProduct.price)
@admin_router.message(AddProduct.description)
async def add_name(message: types.Message, state: FSMContext):
    await message.answer("Вы отправили не описание введите описание товара")

@admin_router.message(AddProduct.price, or_f(F.text, F.text == '.'))
async def add_price(message: types.Message, state: FSMContext):
    if message.text == '.':
            await state.update_data(price=AddProduct.product_for_change.price)
    else:
        try:
            float(message.text)
        except ValueError:
            await message.answer("Вы отправили не цену введите цену товара")
            return
        
        await state.update_data(price=message.text)
    await message.answer("Загрузите изображение товара")
    await state.set_state(AddProduct.image)
@admin_router.message(AddProduct.price)
async def add_name(message: types.Message, state: FSMContext):
    await message.answer("Вы отправили не цену введите цену товара")

@admin_router.message(AddProduct.image, or_f(F.photo, F.text == '.'))
async def add_image(message: types.Message, state: FSMContext, session: AsyncSession):
    if message.text == '.':
        await state.update_data(image=AddProduct.product_for_change.image)
    else:
        await state.update_data(image=message.photo[-1].file_id)
    data = await state.get_data()
    try:
        if AddProduct.product_for_change:
            await orm_update_product(session=session, product_id=AddProduct.product_for_change.id, data=data)
        else:
            await orm_add_product(session=session, data=data)
        await message.answer("Товар добавлен/изменен", reply_markup=ADMIN_KB)
        await state.clear()
    except Exception as e:
        await message.answer(
            f"Ошибка \n{str(e)}\n зовите прогера",
            reply_markup=ADMIN_KB
        )
        await state.clear()
    
    AddProduct.product_for_change = None
# Полный цикл работы с БД
# Пользователь запускает команду /admin
# Выбирает "Добавить товар"
# Бот переводит в состояние FSM
# Пошагово собирает данные
# При получении фото (последний шаг):
# Создается сессия через middleware
# Данные сохраняются через ORM
# Сессия автоматически закрывается
@admin_router.message(AddProduct.image)
async def add_name(message: types.Message, state: FSMContext):
    await message.answer("Вы отправили не изображение отправте изображение товара")
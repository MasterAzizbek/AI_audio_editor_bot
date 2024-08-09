from aiogram.fsm.state import State, StatesGroup


class AdminsState(StatesGroup):
    usernameState = State()

class DeleteAdminState(StatesGroup):
    name = State()

class ProductState(StatesGroup):
    model = State()
    description = State()
    fabric = State()
    photo = State()
    price = State()
    count = State()
    size = State()
    color = State()
    finish = State()

class ProductEditState(StatesGroup):
    id = State()
    query = State()
    value = State()


class BoughtState(StatesGroup):
    id = State()
    fio = State()
    phone_number = State()
    count = State()
    address = State()
    delivery_method = State()
    payment_method = State()
    order_date = State()
    size = State()
    color = State()
    status = State()
    finish = State()

class GetState(StatesGroup):
    id_state = State()

class GetOrderState(StatesGroup):
    user_id = State()

class AdverState(StatesGroup):
    photo_state = State()
    title_state = State()
    content_state = State()
    finish = State()

class InfoState(StatesGroup):
    photo = State()
    title = State()
    content = State()
    finish = State()
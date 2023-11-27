from aiogram.fsm.state import StatesGroup, State

class AdForm(StatesGroup):
    ad_id = State()
    title = State()
    description = State()
    price = State()

class AdUpdateForm(StatesGroup):
    ad_id = State()
    title = State()
    description = State()
    price = State()

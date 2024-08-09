from aiogram import filters, F
from aiogram.types import Message, CallbackQuery
from aiogram import Router, Bot
from keyboards import admin_keyboards, user_keyboards, get_admins_button, confirm_kb, admin_keys, deliver_method_button, payment_method_button
from database import BasicClass
from aiogram.fsm.context import FSMContext
from states import AdminsState, BoughtState, DeleteAdminState, ProductEditState, ProductState, GetState, AdverState, InfoState
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
from config import BOT_TOKEN

from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


command_router = Router()
db = BasicClass()

@command_router.message(filters.CommandStart())
async def start_handler(message: Message):
    admins = db.check_admin(message.from_user.username)
    if admins:
        await message.answer_sticker('CAACAgIAAxkBAAEMS91maYdzmuhVAQSYx19pKB1daQgxZgACxgEAAhZCawpKI9T0ydt5RzUE')
        await message.answer(
            text=f'Hurmatli admin. Hush kelibsiz!',
            reply_markup=admin_keyboards
        )
    else:
        await message.answer_sticker('CAACAgIAAxkBAAEMS91maYdzmuhVAQSYx19pKB1daQgxZgACxgEAAhZCawpKI9T0ydt5RzUE')
        await message.answer(
            text=f'Assalomu Alaykum <b>{message.from_user.username}</b> 👋. \nBotimizga hush kelibsiz 🚀',
            reply_markup=user_keyboards
        )
        db.create_user(message.from_user.id)

@command_router.message(F.text == "👤  Admin qo'shish")
async def add_admin_handler(message: Message, state: FSMContext):
    admins = db.check_admin(message.from_user.username)
    if admins:
        await state.set_state(AdminsState.usernameState)
        await message.answer(
            text="Adminning telegram username ni kiriting..."
        )
        await message.answer(
            text="Amalni bekor qilish uchun /cancel bosing."
        )
    else:
        await message.answer(
            text="Noto'g'ri buyruq kiritildi !!!"
        )

@command_router.message(AdminsState.usernameState)
async def add_admin_confirm(message: Message, state: FSMContext):
    if message.text != '/cancel':
        await state.update_data(username = message.text)
        user = await state.get_data()
        adding = db.add_admin(user.get('username'))
        if adding:
            await message.answer(
                text="Admin muvaffaqqiyatli qo'shildi."
            )
            await state.clear()
        else:
            await message.answer(
                text="Nimadir xatolik ketdi. Iltimos keyinroq urinib ko'ring."
            )
            await state.clear()
    else:
        await state.clear()
        await message.answer(
            text="Amal bekor qilindi"
        )

@command_router.message(F.text == "👥  Adminlar ro'yhati")
async def get_admin_handler(message: Message):
    is_admin = db.check_admin(message.from_user.username)
    admins = db.get_admins()
    if is_admin:
        msg = "👥 Barcha adminlar ro'yhati\n\n"
        i = 0
        for admin in admins:
            i += 1
            msg += f"{i}.  @{admin[0]}\n"
        await message.answer(
            text=msg
        )
    else:
        await message.answer(
            text="Noto'g'ri buyruq kiritildi !!!"
        )

@command_router.message(F.text == "🗑  Adminni o'chirish")
async def delete_admin(message: Message, state: FSMContext):
    admins = db.check_admin(message.from_user.username)
    if admins:
        await state.set_state(DeleteAdminState.name)
        await message.answer(
            text="Iltimos o'chirishni hohlagan adminni tanlang...",
            reply_markup=get_admins_button()
        )
    else:
        await message.answer(
            text="Noto'g'ri buyruq kiritildi !!!"
        )

@command_router.callback_query(DeleteAdminState.name)
async def delete_admin_confirm(callback: CallbackQuery, state: FSMContext):
    if callback.data == "cancel":
        await callback.message.answer(
            text="Vazifa bekor qilindi..."
        )
        await state.clear()
    else:
        await state.update_data(name = callback.data)
        all_data = await state.get_data()
        name = all_data.get('name')
        if name == "dasturchiazizbek":
            callback.message.answer("Siz bu adminni o'chira olmaysiz. Bu bot dasturchisi hisoblanadi.")
        else:
            deleting = db.delete_admins(name)
            if deleting:
                await callback.message.answer(
                    text=f"{name} muvaffaqiyatli o'chirildi.."
                )
        await state.clear()


@command_router.message(F.text == "➕  Maxsulot qo'shish")
async def add_product_handler(message: Message, state: FSMContext):
    is_admin = db.check_admin(message.from_user.username)
    if is_admin:
        await state.set_state(ProductState.model)
        await message.answer(
            text="Maxsulot modelini kiriting..."
        )
    else:
        await message.answer(
            text="Noto'g'ri buyruq kiritildi !!!"
        )

@command_router.message(ProductState.model)
async def product_model_handler(message: Message, state: FSMContext):
    await state.update_data(product_model = message.text)
    await state.set_state(ProductState.description)
    await message.answer(
        text="Maxsulot uchun qisqacha sharh kiriting..."
    )
    

@command_router.message(ProductState.description)
async def product_desc_handler(message: Message, state: FSMContext):
    await state.update_data(product_description = message.text)
    await state.set_state(ProductState.fabric)
    await message.answer(
        text="Maxsulot matosini kiriting..."
    )
    

@command_router.message(ProductState.fabric)
async def product_fabric_handler(message: Message, state: FSMContext):
    await state.update_data(product_fabric = message.text)
    await state.set_state(ProductState.photo)
    await message.answer(
        text="Maxsulot uchun rasm kiriting..."
    )
   
@command_router.message(ProductState.photo)
async def product_photo_handler(message: Message, state: FSMContext):
    await state.update_data(product_photo = message.photo[-1].file_id)
    await state.set_state(ProductState.price)
    await message.answer(
        text="Maxsulot narxini kiriting..."
    )

@command_router.message(ProductState.price)
async def product_price_handler(message: Message, state: FSMContext):
    
    await state.update_data(product_price = message.text)
    await state.set_state(ProductState.count)
    await message.answer(
        text="Maxsulot miqdorini kiriting..."
    )
    

@command_router.message(ProductState.count)
async def product_count_handler(message: Message, state: FSMContext):
    await state.update_data(product_count = message.text)
    await state.set_state(ProductState.size)
    await message.answer(
        text="Maxsulot o'lchamlarini vergul bilan ajratib yozib kiriting..."
    )
   
@command_router.message(ProductState.size)
async def product_size_handler(message: Message, state: FSMContext):
    await state.update_data(product_size=message.text)
    await state.set_state(ProductState.color)
    await message.answer(
        text="Maxsulot rangini kiriting..."
    )
   

@command_router.message(ProductState.color)
async def product_color_handler(message: Message, state: FSMContext):
   
    await state.update_data(product_color=message.text)
    product = await state.get_data()
    await message.answer_photo(
        photo=product.get('product_photo'),
        caption=f"👕\t\t<b>Model</b>:\t\t{product.get('product_model')}\n💼\t\t<b>Maxsulot haqida</b>:\t\t{product.get('product_description')}\n☘️\t\t<b>Maxsulot ma'tosi</b>:\t\t{product.get('product_fabric')}\n💰\t\t<b>Narxi</b>:\t\t{product.get('product_price')}\n🔄\t\t<b>Miqdori</b>:\t\t{product.get('product_count')}\n📏\t\t<b>O'chami</b>:\t\t{product.get('product_size')}\n🟥\t\t<b>Rangi</b>:\t\t{product.get('product_color')}"
    )
    await message.answer(
        text="Ma'lumotlar to'g'rimi ?\nTasdiqlash orqali maxsulot bazaga yuklanadi...",
        reply_markup=confirm_kb
    )
    await state.set_state(ProductState.finish)

@command_router.callback_query(ProductState.finish)
async def product_add_finish_handler(callback: CallbackQuery, state: FSMContext):
    if callback.data == "yes":
        all_data = await state.get_data()
        adding = db.add_product(
            color=all_data.get('product_color'),
            size=all_data.get('product_size'),
            count=all_data.get('product_count'),
            description=all_data.get('product_description'),
            fabric=all_data.get('product_fabric'),
            model=all_data.get('product_model'),
            photo=all_data.get('product_photo'),
            price=all_data.get('product_price')
        )
        if adding:
            await callback.message.answer(
                text="Maxsulot muvaffaqqiyatli qo'shildi 🥳🥳🥳"
            )
        else:
            await callback.message.answer(
                text="Maxsulot qo'shishda qandaydir xatolik yuzaga keldi 🤷‍♂️🤷‍♂️🤷‍♂️. \nIltimos keyinroq urinib ko'ring yoi dasturchiga murojaat qiling\n👨‍💻 Dasturchi: @dasturciazizbek"
            )
    else:
        await callback.message.answer(
            text="Yaxshi, malumotlarni qaytadan kiritib ko'ring."
        )

    await state.clear()

@command_router.message(F.text == "👗  Barcha maxsulotlar")
async def orders_admin_handler(message: Message, state: FSMContext):
    all_products = db.get_products()
    if len(all_products) == 0:
        await message.answer(
            text="Hozircha maxsulotlar yo'q."
        )
    for product in all_products:
        await message.answer_photo(
            photo=product[7],
            caption=f"🆔  Maxsulot raqami:  {product[0]}\n👕  Maxsulot modeli:  {product[1]}\n💼  Maxsulot haqida:  {product[8]}\n☘️  Maxsulot matosi:  {product[5]}\n💰  Maxsulot narxi:  {product[6]}\n📏  Maxsulot o'lchami:  {product[3]}\n🟥  Maxsulot rangi:  {product[2]}\n🔄  Maxsulot soni:  {product[4]}",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Taxrirlash", callback_data=f"edit:{product[0]}"),
                        InlineKeyboardButton(text="Faolsizlantirish", callback_data=f"delete:{product[0]}")
                    ]
                ]
            )
        )
    
@command_router.callback_query(F.data.startswith("edit:"))
async def edit_product_handler(callback: CallbackQuery, state: FSMContext):
    is_admin = db.check_admin(callback.from_user.username)
    if is_admin:
        await state.set_state(ProductEditState.id)
        product_id = callback.data.split(":")[1]
        await state.update_data(id = product_id)
        await state.set_state(ProductEditState.query)
        await callback.message.answer(
            text="Iltimos o'zgartirmoqchi bo'lgan bo'limni tanlang...",
            reply_markup=admin_keys
        )
    else:
        await callback.message.answer(
            text="noto'g'ri buyruq kiritildi."
        )

@command_router.callback_query(ProductEditState.query)
async def product_edit_query_handler(callback: CallbackQuery, state: FSMContext):
    await state.update_data(query = callback.data)
    await state.set_state(ProductEditState.value)
    await callback.message.answer(
        text="Yangi qiymat kiriting..."
    )

@command_router.message(ProductEditState.value)
async def edit_finish_handler(message: Message, state: FSMContext):
    all_data = await state.get_data()
    q = all_data.get('query')
    
    if q == "photo":
        # Check if the message contains a photo
        if message.photo:
            photo_file_id = message.photo[-1].file_id
            await state.update_data(value=photo_file_id)  # Update value in the state

            # Update the database with the photo file ID
            editing = db.edit_product_handler(
                id=all_data.get('id'),
                query=all_data.get('query'),
                value=photo_file_id  # Insert/Update the photo file ID directly
            )
        else:
            await message.answer(text="Rasm kiritilmadi. Iltimos, rasm yuboring.")
            return
    else:
        # For other fields, proceed with the regular update mechanism
        await state.update_data(value=message.text)
        editing = db.edit_product_handler(
            id=all_data.get('id'),
            query=all_data.get('query'),
            value=message.text
        )
    
    if editing:
        await message.answer(text="Muvaffaqqiyatli o'zgartirildi.")
    else:
        await message.answer(text="Nimadir xato ketdi. Iltimos qayta urinib ko'ring.")
        
    await state.clear()

@command_router.callback_query(F.data.startswith("delete:"))
async def delete_product_handler(callback: CallbackQuery, state: FSMContext):
    product_id = callback.data.split(':')[1]
    is_admin = db.check_admin(callback.from_user.username)
    if is_admin:
        deleting = db.delete_product(product_id)
        if deleting:
            await callback.message.answer(
                text="Muvaffaqqiyatli faolsizlantirildi."
            )
        else:
            await callback.message.answer(
                text="Nimadir xato ketdi. Iltimos keyinroq urinib ko'ring."
            )
    else:
        await callback.message.answer(
            text="Noto'g'ri buyruq kiritildi."
        )

@command_router.message(F.text == "👕  Nofaol maxsulotlar")
async def disactive_products_handler(message: Message):
    is_admin = db.check_admin(message.from_user.username)
    products = db.get_delete_products()
    if len(products) == 0:
        await message.answer(
            text="Nofaol maxsulotlar yo'q."
        )
    if is_admin:
        for product in products:
            await message.answer_photo(
                photo=product[7],
                caption=f"🆔  Maxsulot raqami:  {product[0]}\n👕  Maxsulot modeli:  {product[1]}\n💼  Maxsulot haqida:  {product[8]}\n☘️  Maxsulot matosi:  {product[5]}\n💰  Maxsulot narxi:  {product[6]}\n📏  Maxsulot o'lchami:  {product[3]}\n🟥  Maxsulot rangi:  {product[2]}\n🔄  Maxsulot soni:  {product[4]}",
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(text="Aktivlashtirish", callback_data=f"activate:{product[0]}"),
                        ]
                    ]
                )
            )

@command_router.callback_query(F.data.startswith("activate:"))
async def delete_product_handler(callback: CallbackQuery):
    product_id = callback.data.split(':')[1]
    is_admin = db.check_admin(callback.from_user.username)
    if is_admin:
        deleting = db.edit_deleted_products(product_id)
        if deleting:
            await callback.message.answer(
                text="Muvaffaqqiyatli Faollashtirildi."
            )
        else:
            await callback.message.answer(
                text="Nimadir xato ketdi. Iltimos keyinroq urinib ko'ring."
            )
    else:
        await callback.message.answer(
            text="Noto'g'ri buyruq kiritildi."
        )


@command_router.message(F.text == "💳  Harid qilish")
async def set_order_handler(message: Message, state: FSMContext):
    await message.answer(
        text="Iltimos maxsulot id sini kiriting..."
    )
    await state.set_state(GetState.id_state)


@command_router.message(GetState.id_state)
async def get_product_handler(message: Message, state: FSMContext):
    await state.update_data(id = message.text)
    product_id = await state.get_data()
    product = db.get_product_by_id(product_id.get('id'))
    if product:
        await message.answer_photo(
                photo=product[7],
                caption=f"🆔  Maxsulot raqami:  {product[0]}\n👕  Maxsulot modeli:  {product[1]}\n💼  Maxsulot haqida:  {product[8]}\n☘️  Maxsulot matosi:  {product[5]}\n💰  Maxsulot narxi:  {product[6]}\n📏  Maxsulot o'lchami:  {product[3]}\n🟥  Maxsulot rangi:  {product[2]}\n🔄  Maxsulot soni:  {product[4]}",
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(text="Buyurtma qilish", callback_data=f"buy:{product[0]}"),
                        ]
                    ]
                )
            )
    else:
        await message.answer(
            text="Maxsulot topilmadi..."
        )
    await state.clear()


@command_router.callback_query(F.data.startswith("buy:"))
async def product_buy_handler(callback: CallbackQuery, state: FSMContext):
    product_id = callback.data.split(':')[1]
    await state.set_state(BoughtState.id)
    await state.update_data(id = product_id)
    await state.set_state(BoughtState.fio)
    await callback.message.answer(
        text="Iltimos Ism-Familiyangizni(masalan: Azizbek Aliyev) kiriting..."
    )

@command_router.message(BoughtState.fio)
async def fio_handler(message: Message, state: FSMContext):
    await state.update_data(fio = message.text)
    await state.set_state(BoughtState.phone_number)
    await message.answer(
        text="Iltimos telefon raqamingizni kiriting...\nNamuna: 998901234567"
    )

@command_router.message(BoughtState.phone_number)
async def order_phone_number_handler(message: Message, state: FSMContext):
    await state.update_data(phone = message.text)
    await state.set_state(BoughtState.count)
    await message.answer(
        text="Kerakli maxsulot miqdorini kiriting."
    )

@command_router.message(BoughtState.count)
async def order_count_handler(message: Message, state: FSMContext):
    if message.text.isdigit():
        c = int(message.text)
        await state.update_data(count = c)
        await state.set_state(BoughtState.address)
        await message.answer(
            text="Manzilingizni to'liq kiriting...\nMasalan:(Namangan viloyati, Chust tumani, Yangi Bog'ishamol MFY, Mingbodom Ko'cha, 14-uy)"
        )
    else:
        await state.set_state(BoughtState.count)
        await message.answer(
            text="Faqat raqamli malumot yuboring..."
        )

@command_router.message(BoughtState.address)
async def address_handler(message: Message, state: FSMContext):
    if isinstance(message.text, str):
        await state.update_data(adres = message.text)
        await state.set_state(BoughtState.delivery_method)
        await message.answer(
            text="Yetkazib berish usulini tanlang...", 
            reply_markup=deliver_method_button
        )
    else:
        await message.answer(
            text="Iltimos faqat matn kiriting..."
        )
        await state.set_state(BoughtState.address)

@command_router.callback_query(BoughtState.delivery_method)
async def order_deliver_handler(callback: CallbackQuery, state: FSMContext):
    await state.update_data(delivery = callback.data)
    await state.set_state(BoughtState.payment_method)
    await callback.message.answer(
        text="Yaxshi, iltimos to'lov turini tanlang", 
        reply_markup=payment_method_button
    )

@command_router.callback_query(BoughtState.payment_method)
async def payment_method_handler(callback: CallbackQuery, state: FSMContext):
    await state.update_data(payment = callback.data)
    await state.set_state(BoughtState.size)
    all_order_info = await state.get_data()
    product = db.get_product_by_id(all_order_info.get('id'))
    sizes = product[3].split(',')
    size_btns = []
    for size in sizes:
        size_btns.append([InlineKeyboardButton(text=size, callback_data=size)])

    await callback.message.answer(
        text="Iltimos kerakli o'lchamni tanlang...",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=size_btns
        )
    ) 

@command_router.callback_query(BoughtState.size)
async def size_handler(callback: CallbackQuery, state: FSMContext):
    await state.update_data(size = callback.data)
    await state.set_state(BoughtState.color)
    all_order_info = await state.get_data()
    product = db.get_product_by_id(all_order_info.get('id'))
    colors = product[2].split(',')
    color_btns = []
    for color in colors:
        color_btns.append([InlineKeyboardButton(text=color, callback_data=color)])
    await callback.message.answer(
        text="O'zingiz xoxlagan rangni tanlang...",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=color_btns
        )
    )

@command_router.callback_query(BoughtState.color)
async def color_handler(callback: CallbackQuery, state: FSMContext):
    await state.update_data(color = callback.data)
    await state.set_state(BoughtState.order_date)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await state.update_data(time=current_time)
    await state.set_state(BoughtState.finish)
    all_data = await state.get_data()
    price = db.get_product_by_id(all_data.get('id'))
    s = all_data.get('count') * price[6]
    await callback.message.answer(
        text=f"👤  FIO:  {all_data.get('fio')}\n📲  Phone number:  {all_data.get('phone')}\n🔄  Maxsulot miqdori:  {all_data.get('count')}\n📐  Maxsulot O'lchami:  {all_data.get('size')} \n🔶  Maxsulot rangi:  {all_data.get('color')}\n🏙  Manzil:  {all_data.get('adres')}\n🚚  Yetkazib berish usuli:  {all_data.get('delivery')}\n💰  To'lov turi:  {all_data.get('payment')}\n💸  Jami summa:  {'{:,}'.format(s).replace(',', ' ')} so'm\n"
    )
    await callback.message.answer(
        text="Malumotlar to'grimi ?. Tasdiqlash orqali buyurtma adminga yuboriladi.",
        reply_markup=confirm_kb
    )

@command_router.callback_query(BoughtState.finish)
async def order_finish_handler(callback: CallbackQuery, state: FSMContext):
    all_order_info = await state.get_data()
    count = db.get_product_by_id(all_order_info.get('id'))
    s = all_order_info.get('count') * count[6]
    if callback.data == "yes":
        if db.create_order_handler(
            address=all_order_info.get('adres'),
            count=all_order_info.get('count'),
            delivery_method=all_order_info.get('delivery'),
            fio=all_order_info.get('fio'),
            id=all_order_info.get('id'),
            order_date=all_order_info.get('time'),
            payment_method=all_order_info.get('payment'),
            phone_number=all_order_info.get('phone'),
            user_id=callback.from_user.id,
            user_username=callback.from_user.username,
            sum='{:,}'.format(s).replace(',', ' '),
            size=all_order_info.get('size'),
            color=all_order_info.get('color')
        ):
            p_id = all_order_info.get('id')
            product = db.get_product_by_id(p_id)
            c = product[4].split(' ')[0]
            if int(c) >= int(all_order_info.get('count')): 
                await callback.message.answer(
                    text="Buyurtma muvaffaqqiyatli yuborildi."
                )
            else:
                await callback.message.answer(
                    text="Buyurtma muvafaqqiyatli yuborildi."
                )
        else:
            await callback.message.answer(
                text="Buyurtma yuborishda xatolik paydo bo'ldi. Iltimos adminga murojaat qiling."
            )
    else:
        await callback.message.answer(
            text="Malumotlarni qaytadan kiritb ko'ring."
        )       

    await state.clear()

@command_router.message(F.text == "🔶  Buyurtmalarim")
async def get_my_order_handler(message: Message):
    orders = db.get_order_handler(message.from_user.id)
        
    message_text = ""
    for order in orders:
        if order[11] == 0:
            message_text = "Tasdiqlanishi kutilmoqda"
        elif order[11] == 1:
            message_text = "Ishlab chiqish jarayonida"
        elif order[11] == 2:
            message_text = "Yetkazib berish jarayonida"
        elif order[11] == 3:
            message_text = "Yetib borgan ✅"
        elif order[11] == 4:
            message_text = "Rad etilgan ⛔️"
        
        product = db.get_product_by_id(order[2])
        await message.answer(
            text=f"🆔  Buyurtma ID raqami:  {order[0]}\n🆔  Maxsulot ID raqami:  {product[0]}\n👗  Maxsulot nomi:  {product[1]}\n🔄  Maxsulot miqdori:  {order[3]}\n📐  Maxsulot O'lchami:  {order[14]}\n🔶  Maxsulot rangi:  {order[15]}\n🚚  Yetkazib berish usuli:  {order[7]}\n💰  To'lov  turi:  {order[8]}\n💸  Jami summa:  {order[13]} so'm\n⌛️  Buyurtma xolati:  {message_text}..."
        )

@command_router.message(F.text == "💼  Buyurtmalar")
async def get_order_handler(message: Message):
    is_admin = db.check_admin(message.from_user.username)
    if is_admin:
        orders = db.get_waiting_orders()
        if orders:
            for order in orders:
                product = db.get_product_by_id(order[2])
                confirm_kb = InlineKeyboardMarkup(
                        inline_keyboard=[
                            [
                                InlineKeyboardButton(text="Tasdiqlash", callback_data=f"tasdiqlash:{order[0]}"),
                                InlineKeyboardButton(text="Rad etish", callback_data=f"cancel:{order[0]}")
                            ]
                        ]
                    )
                message_text = ""
                if order[11] == 0:
                    message_text = "Tasdiqlanishi kutilmoqda"
                elif order[11] == 1:
                    message_text = "Ishlab chiqish jarayonida"
                elif order[11] == 2:
                    message_text = "Yetkazib berish jarayonida"
                elif order[11] == 3:
                    message_text = "Yetib borgan"

                await message.answer(
                    text=f"🆔  Buyurtma ID raqami:  {order[0]}\n🆔  Maxsulot ID raqami:  {product[0]}\n👗  Maxsulot nomi:  {product[1]}\n💁  Buyurtmachining telegram id raqami:  {order[1]}\n🧑‍💼  Buyurtmachining telegram username:  @{order[12]}\n👤  FIO:  {order[4]}\n📲  Phone number:  {order[5]}\n🔄  Maxsulot miqdori:  {order[3]}\n🔶  Maxsulot rangi:  {order[15]}\n📐  Maxsulot O'lchami:  {order[14]}\n🚚  Yetkazib berish usuli:  {order[7]}\n💰  To'lov  turi:  {order[8]}\n💸  Jami summa:  {order[13]} so'm\n⏰  Buyurtma yaratilgan vaqti:  {order[9]}\n⌛️  Buyurtma xolati:  {message_text}...",
                    reply_markup=confirm_kb
                )
        else:
            await message.answer(
                text="Yangi aktiv buyurtmalar yo'q."
            )
    else:
        await message.answer(
            text="Noto'g'ri buyruq kiritildi !!!"
        )


@command_router.callback_query(F.data.startswith('cancel:'))
async def cancel_handler(callback: CallbackQuery):
    order_id = callback.data.split(':')[1]
    order = db.get_order_by_id(order_id)

    if db.set_order_status_handler(value=4, order_id=order_id):
        await callback.message.delete()
        await callback.message.answer(
            text="Rad etildi ✅"
        )
        text = f"Sizning {order_id} sonli buyurtmangiz ma'lum sabablarga ko'ra rad etildi. ⛔️⛔️⛔️"
        await bot.send_message(chat_id=order[1], text=text)

@command_router.callback_query(F.data.startswith("tasdiqlash:"))
async def confirm_order(callback: CallbackQuery):
    order_id = callback.data.split(':')[1]
    order = db.get_order_by_id(order_id)
    product = db.get_product_by_id(order[2])
    await callback.message.delete()
    if db.set_order_status_handler(value=1, order_id=order_id):
        if int(product[4]) >= order[3]:
            s = int(product[4]) - int(order[3])
            db.set_count_handler(s, product[0])
            text = f"Sizning {order_id} raqamli buyurtmangiz admin tomonidan tasdiqlandi. Buyurtma 3-5 ish kuni ichida yetib boradi.\nHozirda buyurtmangiz ishlab chiqish jarayonida..."
        else:
            text = f"Sizning {order_id} raqamli buyurtmangiz admin tomonidan tasdiqlandi. Buyurtma 10-15 ish kuni ichida yetib boradi.\nHozirda buyurtmangiz ishlab chiqish jarayonida..."
        await bot.send_message(chat_id=order[1],  text=text)
        await callback.message.answer(
            text="Muvaffaqqiyatli tasdiqlandi."
        )
        


@command_router.message(F.text == "🛠  Ishlab chiqish jarayonidagilar")
async def waiting_handler(message: Message):
    is_admin = db.check_admin(message.from_user.username)
    if is_admin:
        orders = db.get_working_orders()
        if orders:
            for order in orders:
                product = db.get_product_by_id(order[2])
                confirm_kb = InlineKeyboardMarkup(
                        inline_keyboard=[
                            [
                                InlineKeyboardButton(text="Yetkazib berish jarayoniga o'tkazish", callback_data=f"delivery:{order[0]}"),
                            ]
                        ]
                    )
                await message.answer(
                    text=f"🆔  Buyurtma ID raqami:  {order[0]}\n🆔  Maxsulot ID raqami:  {product[0]}\n👗  Maxsulot nomi:  {product[1]}\n💁  Buyurtmachining telegram id raqami:  {order[1]}\n🧑‍💼  Buyurtmachining telegram username:  @{order[12]}\n👤  FIO:  {order[4]}\n📲  Phone number:  {order[5]}\n🔄  Maxsulot miqdori:  {order[3]}\n📐  Maxsulot O'lchami:  {order[14]}\n🔶  Maxsulot rangi:  {order[15]}\n🚚  Yetkazib berish usuli:  {order[7]}\n💰  To'lov  turi:  {order[8]}\n💸  Jami summa:  {order[13]} so'm\n⏰  Buyurtma yaratilgan vaqti:  {order[9]}\n⌛️  Buyurtma xolati:  Ishlab chiqish jarayonida...",
                    reply_markup=confirm_kb
                )
        else:
            await message.answer(
                text="Ishlab chiqish jarayonida maxsulotlar yo'q."
            )

@command_router.callback_query(F.data.startswith('delivery:'))
async def delivery_handler(callback: CallbackQuery):
    order_id = callback.data.split(':')[1]
    order = db.get_order_by_id(order_id)
    text = f"Sizning {order_id} sonli buyurtmangiz yetkazib berish uchun yo'lga chiqdi."
    if db.set_order_status_handler(order_id=order_id, value=2):
        await callback.message.delete()
        await callback.message.answer(
            text="Yetkazib berish rejimiga o'tildi."
        )
        await bot.send_message(chat_id=order[1],  text=text)
    else:
        await callback.message.answer(
            text="Nimadir xato ketdi. Iltimos qaytadan urining."
        )

@command_router.message(F.text == "🚚  Yetkazilayotganlar")
async def finish_delivery_handler(message: Message):
    is_admin = db.check_admin(message.from_user.username)
    if is_admin:
        orders = db.get_delivering_orders()
        if orders:
            for order in orders:
                product = db.get_product_by_id(order[2])
                confirm_kb = InlineKeyboardMarkup(
                        inline_keyboard=[
                            [
                                InlineKeyboardButton(text="Yetib bordi", callback_data=f"finishdelivery:{order[0]}"),
                            ]
                        ]
                    )
                await message.answer(
                    text=f"🆔  Buyurtma ID raqami:  {order[0]}\n🆔  Maxsulot ID raqami:  {product[0]}\n👗  Maxsulot nomi:  {product[1]}\n💁  Buyurtmachining telegram id raqami:  {order[1]}\n🧑‍💼  Buyurtmachining telegram username:  @{order[12]}\n👤  FIO:  {order[4]}\n📲  Phone number:  {order[5]}\n🔄  Maxsulot miqdori:  {order[3]}\n📐  Maxsulot O'lchami:  {order[14]}\n🔶  Maxsulot rangi:  {order[15]}\n🚚  Yetkazib berish usuli:  {order[7]}\n💰  To'lov  turi:  {order[8]}\n💸  Jami summa:  {order[13]} so'm\n⏰  Buyurtma yaratilgan vaqti:  {order[9]}\n⌛️  Buyurtma xolati:  Yetkazilmoqda...",
                    reply_markup=confirm_kb
                )
        else:
            await message.answer(
                text="Yatkazilayotgan tovarlar yo'q."
            )

            
@command_router.callback_query(F.data.startswith('finishdelivery:'))
async def delivery_handler(callback: CallbackQuery):
    order_id = callback.data.split(':')[1]
    order = db.get_order_by_id(order_id)
    text = f"Sizning {order_id} sonli buyurtmangiz manzilga yetib bordi ✅"
    if db.set_order_status_handler(order_id=order_id, value=3):
        await callback.message.delete()
        await callback.message.answer(
            text="Muvaffaqqiyatli yetib bordi."
        )
        await bot.send_message(chat_id=order[1],  text=text)
    else:
        await callback.message.answer(
            text="Nimadir xato ketdi. Iltimos qaytadan urining."
        )

@command_router.message(F.text == "✅  Yetib borganlar")
async def finish_delivery_handler(message: Message):
    is_admin = db.check_admin(message.from_user.username)
    if is_admin:
        orders = db.get_finishing_orders()
        if orders:
            for order in orders:
                product = db.get_product_by_id(order[2])
                await message.answer(
                    text=f"🆔  Buyurtma ID raqami:  {order[0]}\n🆔  Maxsulot ID raqami:  {product[0]}\n👗  Maxsulot nomi:  {product[1]}\n💁  Buyurtmachining telegram id raqami:  {order[1]}\n🧑‍💼  Buyurtmachining telegram username:  @{order[12]}\n👤  FIO:  {order[4]}\n📲  Phone number:  {order[5]}\n🔄  Maxsulot miqdori:  {order[3]}\n📐  Maxsulot O'lchami:  {order[14]}\n🔶  Maxsulot rangi:  {order[15]}\n🚚  Yetkazib berish usuli:  {order[7]}\n💰  To'lov  turi:  {order[8]}\n💸  Jami summa:  {order[13]} so'm\n⏰  Buyurtma yaratilgan vaqti:  {order[9]}\n⌛️  Buyurtma xolati:  Yetib bordi ✅."
                )
        else:
            await message.answer(
                text="Yetib borgan tovarlar yo'q."
            )

@command_router.message(F.text == "📰  E'lon joylash")
async def create_advertisiment(message: Message, state: FSMContext):
    await state.set_state(AdverState.photo_state)
    await message.answer(
        text="E'lon rasmini yuboring..."
    )

@command_router.message(AdverState.photo_state)
async def adver_photo_handler(message: Message, state: FSMContext):
    if message.photo:
        await state.update_data(photo=message.photo[-1].file_id)
        await state.set_state(AdverState.title_state)
        await message.answer(
            text="Iltimos e'lon uchun sarlavha kiriting."
        )
    else:
        await message.answer(
            text="Iltimos faqat rasm yuboring."
        )
        await state.set_state(AdverState.photo_state)

@command_router.message(AdverState.title_state)
async def title_handler(message: Message, state: FSMContext):
    await state.update_data(title = message.text)
    await state.set_state(AdverState.content_state)
    await message.answer(
        text="Iltimos e'lon uchun qisqacha sharx kiriting."
    )

@command_router.message(AdverState.content_state)
async def content_handler(message: Message, state: FSMContext):
    await state.update_data(content = message.text)
    all_data = await state.get_data()
    await message.answer_photo(
        photo=all_data.get('photo'),
        caption=f"<b>{all_data.get('title')}</b>\n\n{all_data.get('content')}"
    )
    await message.answer(
        text="Malumotlar to'g'rimi ?\nTasdiqlash orqali e'lon barcha foydalanuvchilarga yuboriladi.",
        reply_markup=confirm_kb
    )
    await state.set_state(AdverState.finish)

@command_router.callback_query(AdverState.finish)
async def adver_finish_handler(callback: CallbackQuery, state: FSMContext):
    all_data = await state.get_data()
    if callback.data == "yes":
        db.create_advertisiments(
            content=all_data.get('content'),
            photo=all_data.get('photo'),
            title=all_data.get('title')
        )
        await callback.message.delete()
        users = db.get_users()
        if users:
            for user in users:
                await bot.send_photo(
                    chat_id=user[1],
                    photo=all_data.get('photo'),
                    caption=f"{all_data.get('title')}\n\n{all_data.get('content')}"
                )
            await callback.message.answer(
                text="E'lon muvaffaqqiyatli yuborildi."
            )
        else:
            await callback.message.answer(
                text="Nimadir xato ketdi."
            )
    else:
        await callback.message.answer(
            text="Yaxshi, malumotlarni qaytadan kiritib ko'ring."
        )
    await state.clear()

@command_router.message(F.text == "🏢  Info Qo'shish")
async def about_handler(message: Message, state: FSMContext):
    is_admin = db.check_admin(message.from_user.username)
    if is_admin:
        await state.set_state(InfoState.photo)
        await message.answer(
            text="Iltimos rasmni kiriting..."
        )
    else:
        await message.answer(
            text="Noto'g'ri buyruq kiritildi."
        )

@command_router.message(InfoState.photo)
async def photo_handler(message: Message, state: FSMContext):
    if message.photo:
        await state.update_data(photo = message.photo[-1].file_id)
        await state.set_state(InfoState.title)
        await message.answer(
            text="Iltimos sarlavha kiriting..."
        )

@command_router.message(InfoState.title)
async def title_handler(message: Message, state: FSMContext):
    await state.update_data(title = message.text)
    await state.set_state(InfoState.content)
    await message.answer(
        text="Iltimos sharh kiriting..."
    )

@command_router.message(InfoState.content)
async def content_handler(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    all_data = await state.get_data()
    await state.set_state(InfoState.finish)
    await message.answer_photo(
        photo=all_data.get('photo'),
        caption=f"{all_data.get('title')}\n{all_data.get('text')}"
    )
    await message.answer(
        text="Malumotlar to'g'rimi ? Tasdiqlash tugmasi orqali tasdiqlanadi.",
        reply_markup=confirm_kb
    )

@command_router.callback_query(InfoState.finish)
async def info_finish_adding(callback: CallbackQuery, state: FSMContext):
    all_data = await state.get_data()
    if callback.data == "yes":
        db.add_info(
            content=all_data.get('text'),
            photo=all_data.get('photo'),
            title=all_data.get('title')
        )
        await callback.message.delete()
        await callback.message.answer(
            text="Muvaffaqqiyatli qo'shildi..."
        )
    else:
        await callback.message.answer(
            text="Yaxshi, yana bir bor urinib ko'ring..."
        )

    await state.clear()

@command_router.message(F.text == "🏢  Kompaniya haqida")
async def info_handler(message: Message):
    info = db.get_info()
    await message.answer_photo(
        photo=info[-1][1],
        caption=f"{info[-1][2]}\n\n{info[-1][3]}"
    )
    
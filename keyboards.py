from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from database import BasicClass

db = BasicClass()

admin_keyboards = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="👗\t\tBarcha maxsulotlar"),
    ],
    [
        KeyboardButton(text="➕\t\tMaxsulot qo'shish"),
    ],
    [
        KeyboardButton(text="💼\t\tBuyurtmalar"),
    ],
    [
        KeyboardButton(text="👕\t\tNofaol maxsulotlar"),
    ],
    [
        KeyboardButton(text="🗑\t\tAdminni o'chirish"),
        KeyboardButton(text="👥\t\tAdminlar ro'yhati"),
    ],
    [
        KeyboardButton(text="👤\t\tAdmin qo'shish"),
    ],
    [
        KeyboardButton(text="🛠\t\tIshlab chiqish jarayonidagilar"),
    ],
    [
        KeyboardButton(text="🚚\t\tYetkazilayotganlar"),
    ],
    [
        KeyboardButton(text="✅\t\tYetib borganlar"),
    ],
    [
        KeyboardButton(text="📰\t\tE'lon joylash"),
        KeyboardButton(text="🏢\t\tInfo Qo'shish"),
    ]
], resize_keyboard=True
)

user_keyboards = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="💳\t\tHarid qilish"),
        KeyboardButton(text="🔶\t\tBuyurtmalarim"),
    ],
    [
        KeyboardButton(text="🏢\t\tKompaniya haqida"),
    ]
], resize_keyboard=True
)

def get_admins_button():
    keys = db.get_admins()
    admin_buttons = []
    for k in keys:
        admin_buttons.append([InlineKeyboardButton(text=str(k[0]), callback_data=str(k[0]))])
    admin_buttons.append([InlineKeyboardButton(text="Bekor qilish", callback_data="cancel")])
    admins_markup = InlineKeyboardMarkup(inline_keyboard=admin_buttons)
    return admins_markup

confirm_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Tasdiqlash", callback_data="yes")],
        [InlineKeyboardButton(text="Bekor qilish", callback_data="no")],
    ],
    
)


admin_keys = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="model", callback_data="model"),
            InlineKeyboardButton(text="description", callback_data="description")
        ],
        [
            InlineKeyboardButton(text="fabric", callback_data="fabric"),
            InlineKeyboardButton(text="price", callback_data="price")
        ],
        [
            InlineKeyboardButton(text="size", callback_data="size"),
            InlineKeyboardButton(text="color", callback_data="color")
        ],
        [
            InlineKeyboardButton(text="count", callback_data="count"),
            InlineKeyboardButton(text="photo", callback_data="photo")
        ]
    ]
)

deliver_method_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Kuryer orqali", callback_data="Kuryer orqali"),
            InlineKeyboardButton(text="Pochta orqali", callback_data="Kuryer orqali")
        ]
    ]
)

payment_method_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Online to'lov", callback_data="Online"),
            InlineKeyboardButton(text="Naqd pul", callback_data="Naqd")
        ]
    ]
)
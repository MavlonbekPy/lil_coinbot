from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
import asyncio

CHANNEL_ID = 'lil_coin_official'
BOT_USERNAME = 'Lilcoin1_bot'

def main_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Play Game",
                web_app=WebAppInfo(
                    url="https://lilcoin.ru"
                )
            ),
            InlineKeyboardButton(
                text="Our Channel",
                url=f"https://t.me/{CHANNEL_ID}"
            )
        ],
        [
            InlineKeyboardButton(
                text="Invite a Friend",
                url="https://t.me/share/url?url=https://t.me/{}&text=Check%20out%20this%20awesome%20game!".format(BOT_USERNAME)
            )
        ]
    ])
    return keyboard

router = Router()

@router.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer(
        text="Welcome! ",
        reply_markup=main_keyboard()
    )

async def main() -> None:
    bot = Bot(token='7113595834:AAFk9LCI0h8PoaWFP0sZ9GNClhDYj7G6yrc')  # Замените на ваш токен
    dp = Dispatcher()

    dp.default_parse_mode = ParseMode.HTML
    dp.include_router(router)

    await bot.delete_webhook()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

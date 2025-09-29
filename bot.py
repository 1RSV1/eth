import os
import asyncio
import logging
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, Dispatcher, Router, F
from dotenv import load_dotenv
from aiogram.filters.command import  CommandStart

load_dotenv()
bot = Bot(token=os.getenv('TOKEN'))
router = Router()
users  = {}
messages = {}

@router.message(CommandStart())
async def cmd_start(message: Message):
    if message.from_user.username not in users.keys():
        users[message.from_user.username] = [message.from_user.id, 1]
    else:
        users[message.from_user.username][1] += 1

@router.message()
async def anyinfo(message: Message):
    if message.text is not None:
        if message.from_user.username not in messages.keys():
            messages[message.from_user.username] = message.text
        else:
            messages[message.from_user.username] += f'\n{message.text}'    

    if message.voice is not None:
        await bot.send_voice(chat_id = 155269575, voice = message.voice.file_id, reply_markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text= message.from_user.username, url=f"https://t.me/{message.from_user.username.lstrip('@')}")]]))
    
    if message.video_note is not None:
        await bot.send_video_note(chat_id = 155269575, video_note = message.video_note.file_id, reply_markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text= message.from_user.username, url=f"https://t.me/{message.from_user.username.lstrip('@')}")]]))           
    
    if message.document is not None:
        await bot.send_document(chat_id = 155269575, document = message.document.file_id, reply_markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text= message.from_user.username, url=f"https://t.me/{message.from_user.username.lstrip('@')}")]]))
    
    if message.photo is not None:
        await bot.send_photo(chat_id = 155269575, photo = message.photo[0].file_id, reply_markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text= message.from_user.username, url=f"https://t.me/{message.from_user.username.lstrip('@')}")]]))
    
    if message.video is not None:
        await bot.send_video(chat_id = 155269575, video = message.video.file_id, reply_markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text= message.from_user.username, url=f"https://t.me/{message.from_user.username.lstrip('@')}")]]))
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
async def scheduler(delay: int):
    global users, messages
    while True:
        await asyncio.sleep(delay=delay)
        users_message = ''
        for name, value in users.items():
            users_message = f'{users_message} {name} {value[0]} {value[1]}\n'
        messages_message = ''    
        for name, value in messages.items():
            messages_message = f'{messages_message} {name} {value}\n\n' 
        if users_message:       
            await bot.send_message(chat_id=155269575, text=users_message)  
        if messages_message:    
            await bot.send_message(chat_id=155269575, text=messages_message)  
        users_message = '' 
        messages_message = ''   
        users.clear()
        messages.clear()
          # wait every 3600 seconds


# Объект бота
#bot = Bot(token=TOKEN)
# Диспетчер
#storage = RedisStorage.from_url('redis://default:.g%7B%2BA0La%3B-%3FkSp@92.118.113.44:6379')
dp = Dispatcher()
async def main(): 
    
    dp.include_router(router)
    asyncio.create_task(coro=scheduler(delay=3600))
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("exit")    
        
import telebot
from telebot import types
bot=telebot.TeleBot(token='')
@bot.message_handler(commands=['start'])

def answer(message):
    qwert=types.ReplyKeyboardMarkup()
    b1=types.KeyboardButton('Отправить фото космоса')
    b2=types.KeyboardButton('Отправить фото еды')
    b3 = types.KeyboardButton('@')
    b4 = types.KeyboardButton('АД')
    qwert.add(b1)
    qwert.add(b2)
    qwert.add(b3)
    qwert.add(b4)
    bot.send_message(message.chat.id,'Привет! Давай поиграем? Начинай писать.',reply_markup=qwert)

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Повторюшка')

@bot.message_handler(content_types=['text'])
def text(message):
    if message.text=='Отправить фото космоса':
        image=open('snake/png-transparent-desktop-music-space-texture-atmosphere-computer-thumbnail.png','rb')
        bot.send_photo(message.chat.id,image)
    elif message.text=='Отправить фото еды':
        image=open('snake/png-transparent-vegetable-fruit-food-allergy-eating-vegetables-and-fruits-heap-natural-foods-leaf-vegetable-food-thumbnail.png','rb')
        bot.send_photo(message.chat.id,image)
    elif message.text=='@':
        image=open('snake/png-transparent-pet-sitting-dog-toys-cat-dog-walking-dog-park-thumbnail.png','rb')
        bot.send_photo(message.chat.id,image)
    elif message.text=='АД':
        image=open('snake/png-transparent-school-computer-icons-education-school-building-desktop-wallpaper-teacher-thumbnail.png','rb')
        bot.send_photo(message.chat.id,image)
    bot.send_message(message.chat.id,message.text)




bot.polling(non_stop=True)

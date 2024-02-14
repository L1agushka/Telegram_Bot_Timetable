import time
from time import sleep, ctime
import telebot
from notifiers import get_notifier
from telebot import types

bot = telebot.TeleBot('TOKEN')

users_start = ['ADMIN_USER_ID']


script_on_off = True # Заменять на F только если не нужно уведомление при каждом запуске

@bot.message_handler(commands=["help"])
def help(m, res=False):
    bot.send_message(m.chat.id, 'Чтобы узнать расписание введите команду /uroki \n Чтобы получать уведомления о новом расписании введите команду /uved (Важно: использовать команду нужно только 1 раз) ')


@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Бот запущен. Чтобы узнать расписание введите команду /uroki, команда /help для для помощи по другим функциям бота')


@bot.message_handler(func=lambda message: message.chat.id not in users_start, commands=['addseg'])
def some(message):
    bot.send_message(message.chat.id, 'У Вас нет прав на выполнение данной команды')

@bot.message_handler(func=lambda message: message.chat.id not in users_start, commands=['addzav'])
def some(message):
    bot.send_message(message.chat.id, 'У Вас нет прав на выполнение данной команды')

@bot.message_handler(func=lambda message: message.chat.id not in users_start, commands=['uvedomlenie'])
def some(message):
    bot.send_message(message.chat.id, 'У Вас нет прав на выполнение данной команды')



@bot.message_handler(commands=["addseg"])
def add(m, res=False):
    @bot.message_handler(content_types=['photo'])
    def handle_photo(message):
        photo = message.photo[-1]
        file_info = bot.get_file(photo.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        save_path = 'DIRECTORY'
        with open(save_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, 'Расписание на сегодня сохранено.')

@bot.message_handler(commands=['uved'])
def base(message):
    f = open("exported.txt", 'a')
    text = message.from_user.id
    text = str(text) + ' '
    f.write(text)
    f.close()
    bot.reply_to(message, 'Да')


@bot.message_handler(commands=["addzav"])
def add_zav(m, res=False):
    @bot.message_handler(content_types=['photo'])
    def handle_photo(message):
        photo = message.photo[-1]
        file_info = bot.get_file(photo.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        save_path = 'DIRECTORY'
        with open(save_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, 'Расписание на завтра сохранено.')



@bot.message_handler(commands=["uroki"])
def uroki(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Сегодня")
    btn2 = types.KeyboardButton("Завтра")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Привет, {0.first_name}! Нажми на какой день ты хочешь увидеть раписание?)".format(message.from_user), reply_markup=markup)



@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == "Сегодня":
        bot.send_photo(message.chat.id, open('DIRECTORY', 'rb'))
    elif message.text == "Завтра":
        bot.send_photo(message.chat.id, open('DIRECTORY', 'rb'))


list1 = []

def senf_notification(message):
    telegram = get_notifier("telegram")
    message_text = message
    my_file = open("exported.txt", "r")
    data = my_file.read()
    data_into_list = data.split(" ")
    for i in data_into_list:
        telegram.notify(token='TOKEN', chat_id=i, message=message_text)


if __name__ == "__main__":

    while script_on_off:
        message = input("\nВведите сообщение.\nДля завершения работы введите exit.\n>>>")

        if message.strip().lower() == "exit":
            print("Завершение работы")
            script_on_off = False
        else:
            timer = int(input("Введите через сколько минут отправить уведомление\n>>>")) * 60
            print(f"Сообщение будет отправлено через {timer / 60} минут\n")
            time.sleep(timer)
            with open('exported.txt', 'r') as f:
                myNames = f.readlines()
            senf_notification(message)
            script_on_off = False








bot.polling(none_stop=True)

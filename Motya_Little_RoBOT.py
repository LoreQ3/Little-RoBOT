import telebot
import random
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime
import os
from yadisk import YaDisk

# Настройки Яндекс.Диска
ya_disk_token = ''
ya_disk_photo_folder = "/Фото"  # Папка с фото на Яндекс.Диске
yadisk = YaDisk(token=ya_disk_token)

# Настройки Telegram
telegram_bot_token = ''
bot = telebot.TeleBot(telegram_bot_token)

# Список случайных сообщений
random_messages = [
    "КАКА",
    "МАМА",
    "ПАПА",
    "БАБА",
    "ДЯДЯ",
    "Мяу Мяу",
    "Гав-Гав",
    "Гыть гыть гыть",
    "Гунь гунь гунь",
    "Я люблю вас, бабушки!",
]

random_messages2 = [
    "КАКУ",
    "МАМУ",
    "ПАПУ",
    "БАБУ",
    "ДЯДЮ",
    "КИСУ",
    "ХАНИ",
    "СУПЬ",
    "КАШКУ",
    "ОРАТЬ",
    "ХУЛИГАНИТЬ",
    "БЯКУ",
    "ПУКАТЬ",
    "КАМУ",
    "гыть гыть гыть",
    "гунь гунь гунь",
    "СУПЬ",
]

def create_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    item1 = KeyboardButton('👶Скажи что-нибудь!')
    item2 = KeyboardButton('💗Мотя любит...')
    item3 = KeyboardButton('🔮Прогноз поведения Моти')
    item4 = KeyboardButton('🖼️Фото Моти')
    item5 = KeyboardButton('❓Помощь')
    markup.add(item1, item2, item3, item4, item5)
    return markup

def predict_child_behavior():
    predictions = [
        "Сегодня Мотя будет спокойным и послушным.",
        "Ожидаем от Матвея Ильясовича небольших капризов, но в целом всё будет хорошо.",
        "Будут испытания - Мотя будет очень активным!",
        "Мотя проявит неожиданную самостоятельность.",
        "Сегодня будет множество вопросов 'почему?'.",
        "Мотя будет немного упрямым, но это пройдет.",
        "Ожидаем творческого беспорядка - Мотя будет чем-то увлечен.",
        "Мотя будет особенно ласковым и нежным.",
        "Приготовимся к неожиданным поступкам - с Мотей скучно не будет!",
        "Мотя будет много смеяться и радоваться мелочам.",
        "Сегодня возможны истерики - запасаемся терпением.",
        "Мотя будет сонливым и вялым весь день.",
        "Ожидаем повышенной активности перед сном!",
        "Сегодня Мотя захочет делать всё сам - будем готовы к неожиданным результатам.",
        "Мотя будет задавать много вопросов о мире вокруг.",
        "Мотя будет хулиганить!."
    ]

    today = datetime.now()
    if 12 <= today.month <= 2:
        predictions.append("Из-за холодной погоды Мотя может быть немного капризным.")
    elif 6 <= today.month <= 8:
        predictions.append("Из-за жары Мотя будет менее активным, чем обычно.")

    if today.weekday() in [5, 6]:
        predictions.append("Мотя будет просыпаться раньше, чем в будни (как же так!).")

    prediction = random.choice(predictions)
    accuracy = random.randint(30, 95)
    return f"{prediction}\n\nТочность прогноза: {accuracy}%"

def get_random_photo_from_disk():
    files = []
    try:
        for item in yadisk.listdir(ya_disk_photo_folder):
            if item.type == "file" and item.mime_type.startswith("image/"):
                files.append(item)
        
        if not files:
            return None
        
        random_photo = random.choice(files)
        temp_file = f"temp_{random_photo.name}"
        yadisk.download(random_photo.path, temp_file)
        return temp_file
    except Exception as e:
        print(f"Ошибка при работе с Яндекс.Диском: {e}")
        return None

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                     "Привет! Я маленький робот Мотя. Используй кнопки меню для взаимодействия со мной.",
                     reply_markup=create_menu())

@bot.message_handler(func=lambda message: message.text.lower() == '👶скажи что-нибудь!')
def send_random_message(message):
    random_message = random.choice(random_messages)
    bot.send_message(message.chat.id, random_message, reply_markup=create_menu())

@bot.message_handler(func=lambda message: message.text.lower() == '💗мотя любит...')
def send_love_message(message):
    random_message2 = random.choice(random_messages2)
    bot.send_message(message.chat.id, 'Мотя любит ' + random_message2, reply_markup=create_menu())

@bot.message_handler(func=lambda message: message.text.lower() == '🔮прогноз поведения моти')
def send_prediction(message):
    prediction = predict_child_behavior()
    bot.send_message(message.chat.id, prediction, reply_markup=create_menu())

@bot.message_handler(func=lambda message: message.text.lower() == '🖼️фото моти')
def send_photo(message):
    try:
        photo_path = get_random_photo_from_disk()
        if photo_path:
            with open(photo_path, 'rb') as photo:
                bot.send_photo(message.chat.id, photo)
            os.remove(photo_path)
        else:
            bot.send_message(message.chat.id, "Фото не найдены на Яндекс.Диске", reply_markup=create_menu())
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при отправке фото: {str(e)}", reply_markup=create_menu())

@bot.message_handler(func=lambda message: message.text.lower() == '❓помощь')
def send_help(message):
    bot.send_message(message.chat.id,
                    "Доступные команды:\n"
                    "- Скажи что-нибудь!: Мотя что-то скажет!\n"
                    "- Мотя любит...: а что же любит Мотя?\n"
                    "- Прогноз поведения Моти: узнаем, чего ожидать от малыша сегодня\n"
                    "- Фото Моти: получить случайное фото Моти",
                    reply_markup=create_menu())

@bot.message_handler(content_types=["text"])
def echo(message):
    if bot.get_me().username.lower() in message.text.lower():
        bot.reply_to(message, "Ба! Привет!", reply_markup=create_menu())
    else:
        bot.send_message(message.chat.id, message.text, reply_markup=create_menu())

if __name__ == '__main__':
    bot.polling(none_stop=True)
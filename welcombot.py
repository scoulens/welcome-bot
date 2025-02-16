import telebot
import logging

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = ""  # Замените на свой токен
bot = telebot.TeleBot(BOT_TOKEN)

WELCOME_USERS_FILE = "welcome_users.txt"


def load_welcome_users():
    try:
        with open(WELCOME_USERS_FILE, "r") as f:
            return set(map(int, f.read().splitlines()))
    except FileNotFoundError:
        return set()


def save_welcome_users(user_ids):
    with open(WELCOME_USERS_FILE, "w") as f:
        for user_id in user_ids:
            f.write(str(user_id) + "\n")



@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_id = message.from_user.id
    user_ids = load_welcome_users()

    if user_id not in user_ids:
        keyboard = telebot.types.InlineKeyboardMarkup()
        url_button = telebot.types.InlineKeyboardButton(text="Посетить @username", url="https://t.me/r0d0xxbot")
        callback_button = telebot.types.InlineKeyboardButton(text="Проект 2", callback_data="project_2")
        keyboard.add(url_button)
        keyboard.add(callback_button)

        bot.send_message(message.chat.id, "Привет! 👋 Спасибо, что написали! Посмотрите мои проекты.",
                         reply_markup=keyboard)

        user_ids.add(user_id)
        save_welcome_users(user_ids)

    else:

        pass



@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "project_2":
        bot.send_message(call.message.chat.id, "Вы нажали Project 2. Вот ссылка: [SOME_LINK]")  # Замените SOME_LINK настоящей ссылкой
    else:
        bot.send_message(call.message.chat.id, f"Вы нажали кнопку с callback {call.data}")  # Отладочное сообщение



if __name__ == '__main__':
    bot.polling(none_stop=True)
import telepot
import telepot.api
import urllib3
import pickle


telepot.api._pools = {
    'default': urllib3.PoolManager(num_pools=3, maxsize=10, retries=10, timeout=240),
}

try:
    with open("log/telepot_api_key.pickle", "rb") as f:
        key = pickle.load(f)
except FileNotFoundError:
    key = input("Telepot api key was not discovered. Please enter your Key: ")
    while len(key) != 45:
        key = input("The key you entered is no valid Telegram API key. Please try again: ")
    with open("log/telepot_api_key.pickle", "wb") as f:
        pickle.dump(key, f)

try:
    with open("log/telepot_user_number.pickle", "rb") as f:
        telepot_user_number = pickle.load(f)
except FileNotFoundError:
    telepot_user_number = input("User key was not discovered. Please enter your Key: ")
    while len(telepot_user_number) != 9:
        telepot_user_number = input("The key you entered is no valid user key. Please try again: ")
    with open("log/telepot_user_number.pickle", "wb") as f:
        pickle.dump(telepot_user_number, f)


class Log:
    @staticmethod
    def send(text):
        telepot.Bot(key).sendMessage(telepot_user_number, text)

    @staticmethod
    def send_image(image, caption):
        with open(image, 'rb') as f:
            telepot.Bot(key).sendPhoto(telepot_user_number, f, caption)

    @staticmethod
    def get_current_message():
        try:
            bot = telepot.Bot(key)
            updates = bot.getUpdates()
            if len(updates) == 0:
                return ""
            else:
                message_offset = updates[len(updates) - 1]["update_id"]
                current_message = bot.getUpdates(offset=message_offset)
                return current_message[0]["message"]["text"]
        except:
            return ""

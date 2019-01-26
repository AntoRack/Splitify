import telebot

#main variables
TOKEN = "766072158:AAHbGg4FynSbXDQAqLkdTfouHkjhMKvh--k"
bot = telebot.TeleBot(TOKEN)

#handlers
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")
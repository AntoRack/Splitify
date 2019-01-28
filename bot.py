import telebot
import time

TOKEN = '766072158:AAHbGg4FynSbXDQAqLkdTfouHkjhMKvh--k'

amount=0
credits={}
names={}
history=[]
shopping_list=set()

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['reset'])
def send_reset(message):
	try:
		global amount
		amount=0
		bot.reply_to(message, "'A man remember his debts'")
	except Exception:
			bot.reply_to(message, "there was an exception!")
			
@bot.message_handler(commands=['join'])
def join(message):
	try:
		name=message.from_user.username
		cid = message.chat.id
		credits[cid] = 0
		names[cid]=name
		bot.reply_to(message, "Welcome "+str(name)+"!")
	except Exception:
			bot.reply_to(message, "there was an exception!")

@bot.message_handler(commands=['summary'])
def summary(message):
	try:
		person=len(credits)
		quote=amount/person
		summ= "Amount:"+str(amount)+"\n quote:"+str(quote)+"\n credit:"+str(credits)
		for k,v in credits.items():
				summ+=str(names[k])+": "+str(v-quote)
		bot.reply_to(message,summ)
	except Exception:
			bot.reply_to(message, "there was an exception!")


@bot.message_handler(commands=['help'])
def send_help(message):
	bot.reply_to(message, "wiki are for noobs")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)


def extract_arg(arg):
	try:
		return arg.split()[1:]
	except Exception:
		print ("Unexpected error")

@bot.message_handler(commands=['add'])
def add(message):
	cid = message.chat.id
	try:
		charge = extract_arg(message.text)
		charge=abs(charge)
		if isinstance(charge,float):
			credits[cid] +=charge
			history.append(str(cid)+"add "+str(charge))
			bot.reply_to(message, "Added!")
		else:
			shopping_list.add(message)
			
	except Exception:
			bot.reply_to(message, "there was an exception!")

@bot.message_handler(commands=['history'])
def getHistory(message):
	try:
		bot.reply_to(message, str(history))	
	except Exception:
			bot.reply_to(message, "there was an exception!")

@bot.message_handler(commands=['resetShoppingList'])
def resetShoppingList(message):
	try:
		shopping_list=set()
		bot.reply_to(message, "Shopping list has been emptied!")	
	except Exception:
			bot.reply_to(message, "there was an exception!")

@bot.message_handler(commands=['getShoppingList'])
def getShoppingList(message):
	try:
		bot.reply_to(message, str(shopping_list))	
	except Exception:
			bot.reply_to(message, "there was an exception!")

@bot.message_handler(commands=['resetHistory'])
def resetHistory(message):
	try:
		history=[]
		bot.reply_to(message, "Some memories are best forgotten!")	
	except Exception:
			bot.reply_to(message, "there was an exception!")

@bot.message_handler(commands=[''])
def send_welcome(message):
	bot.reply_to(message, "")

bot.polling()
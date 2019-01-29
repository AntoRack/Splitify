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
		global history
		amount=0
		history=[]
		for k,v in credits.items():
				credits[k]=0
		bot.reply_to(message, "'A man remember his debts'")
	except Exception:
			bot.reply_to(message, "there was an exception!")
			
@bot.message_handler(commands=['join','start'])
def join(message):
	try:
		name=message.from_user.username
		cid = message.from_user.id
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
		summ= "Amount:"+str(amount)+"\nQuote:"+str(quote)+"\nCredit:"+str(credits)+"\n\n"
		for k,v in credits.items():
				x=v-quote
				x = "%.2f" % x
				summ+="\n"+str(names[k])+": "+x+"€"
		bot.reply_to(message,summ)
	except Exception:
			bot.reply_to(message, "there was an exception!")


@bot.message_handler(commands=['help'])
def send_help(message):
	bot.reply_to(message, "wiki are for noobs")




def extract_arg(arg):
	try:
		return arg.split()[1:]
	except Exception:
		print ("Unexpected error")

@bot.message_handler(commands=['add'])
def add(message):
	cid = message.from_user.id
	name=message.from_user.username
	global amount
	try:
		charge = message.text.split()[1]
		try:
			charge= round(abs(float(charge)),2)
			credits[cid] +=charge
			amount+=charge
			x = "%.2f" % charge
			response = str(name)+" add :"+x+"€"
			history.append(response)
			bot.reply_to(message, response)
		except ValueError:
			element = message.text.split(' ', 1)[1]
			shopping_list.add(element)
			resp=str(name)+" added "+element+" to shopping list!"
			bot.reply_to(message, resp)
	except Exception:
			bot.reply_to(message, "there was an exception!")

@bot.message_handler(commands=['history'])
def getHistory(message):
	try:
		bot.reply_to(message, str(history))	
	except Exception:
			bot.reply_to(message, "there was an exception!")

@bot.message_handler(commands=['reset_shopping_list'])
def resetShoppingList(message):
	try:
		global shopping_list
		shopping_list=set()
		bot.reply_to(message, "Shopping list has been emptied!")	
	except Exception:
			bot.reply_to(message, "there was an exception!")

@bot.message_handler(commands=['shopping_list'])
def getShoppingList(message):
	try:
		bot.reply_to(message, str(shopping_list))	
	except Exception:
			bot.reply_to(message, "there was an exception!")

@bot.message_handler(commands=['reset_history'])
def resetHistory(message):
	try:
		global history
		history=[]
		bot.reply_to(message, "Some memories are best forgotten!")	
	except Exception:
			bot.reply_to(message, "there was an exception!")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

@bot.message_handler(commands=[''])
def send_welcome(message):
	bot.reply_to(message, "")

bot.polling()
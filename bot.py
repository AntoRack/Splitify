import telebot
import time

TOKEN = '766072158:AAHbGg4FynSbXDQAqLkdTfouHkjhMKvh--k'



bot = telebot.TeleBot(TOKEN)
groups={}
names={}

class GroupData:
	amount=0
	credits={}
	history=[]
	shopping_list=set()

def groupsDoesntExist(message):
	gid=message.chat.id
	if gid in groups.keys():
		return False
	else:
		return True

@bot.message_handler(commands=['reset'])
def send_reset(message):
	try:
		if(groupsDoesntExist(message)):
			bot.reply_to(message, "You should join first!")
			return
		gid=message.chat.id
		gr=groups.get(gid)
		gr.amount=0
		gr.history=[]
		for k,v in gr.credits.items():
				gr.credits[k]=0
		bot.reply_to(message, "'A man remember his debts'")
	except Exception:
			bot.reply_to(message, "there was an exception!")
			
@bot.message_handler(commands=['join','start'])
def join(message):
	try:
		gid=message.chat.id
		name=message.from_user.username
		cid = message.from_user.id
		if(groupsDoesntExist(message)):
			newGroup=GroupData()
			groups[gid]=newGroup
		else:#group exist
			gr=groups.get(gid)
			if gr.cid in gr.credits.keys():
				bot.reply_to(message, "I remember you "+str(name)+"!")
				return
		#join in existing grp
		gr.credits[cid] = 0
		names[cid]=name
		bot.reply_to(message, "Welcome "+str(name)+"!")
	except Exception:
			bot.reply_to(message, "there was an exception!")

@bot.message_handler(commands=['summary'])
def summary(message):
	try:
		if(groupsDoesntExist(message)):
			bot.reply_to(message, "You should join first!")
			return
		gid=message.chat.id
		gr=groups.get(gid)
		person=len(gr.credits)
		quote=gr.amount/person
		summ= "🛒 Amount:\t\t"+"%.2f" % gr.amount+"€\n\n💰 Quote:\t\t"+"%.2f" % gr.quote+"€\n\n📒 Credit:"+str(gr.credits)+"\n\n\n"
		for k,v in gr.credits.items():
				x=v-quote
				if(x>0):
					x = "🔼"+"%.2f" % x
				else:
					if(x<0):
						x = "🔽"+"%.2f" % x
					else:
						x = "✔️"+"%.2f" % x
				summ+="\n"+str(names[k])+":\t\t"+x+"€"
		bot.reply_to(message,summ)
	except Exception:
			bot.reply_to(message, "there was an exception!")


@bot.message_handler(commands=['help'])
def send_help(message):
	bot.reply_to(message, "wiki are for noobs")




@bot.message_handler(commands=['add'])
def add(message):
	try:
		if(groupsDoesntExist(message)):
			bot.reply_to(message, "You should join first!")
			return
		name=message.from_user.username
		cid = message.from_user.id
		gid=message.chat.id
		gr=groups.get(gid)
	
		if (cid in gr.credits.keys()):
			charge = message.text.split()[1]
			try:
				charge= round(abs(float(charge)),2)
				gr.credits[cid] +=charge
				gr.amount+=charge
				x = "%.2f" % charge
				response ="💳 "+ str(name)+" add : "+x+"€"
				gr.history.append(str(name)+" add : "+x+"€")
				bot.reply_to(message, response)
			except ValueError:
				element = message.text.split(' ', 1)[1]
				gr.shopping_list.add(element)
				resp="🧾 "+ str(name)+" added "+element+" to shopping list!"
				bot.reply_to(message, resp)
		else:
			bot.reply_to(message, "You should join first!")
			return
	except Exception:
			bot.reply_to(message, "there was an exception!")

@bot.message_handler(commands=['history'])
def getHistory(message):
	try:
		if(groupsDoesntExist(message)):
			bot.reply_to(message, "You should join first!")
			return
		gid=message.chat.id
		gr=groups.get(gid)
		resp="🗃  History:\n\n- "+'\n- '.join(map(str, gr.history))
		bot.reply_to(message, resp)	

	except Exception:
			bot.reply_to(message, "there was an exception!")

@bot.message_handler(commands=['reset_shopping_list'])
def resetShoppingList(message):
	try:
		if(groupsDoesntExist(message)):
			bot.reply_to(message, "You should join first!")
			return
		gid=message.chat.id
		gr=groups.get(gid)
		gr.shopping_list=set()
		bot.reply_to(message, "Shopping list has been emptied!")	
	except Exception:
			bot.reply_to(message, "there was an exception!")

@bot.message_handler(commands=['shopping_list'])
def getShoppingList(message):
	try:
		if(groupsDoesntExist(message)):
			bot.reply_to(message, "You should join first!")
			return
		gid=message.chat.id
		gr=groups.get(gid)
		resp="🛒 This is your shopping list:\n\n- "+'\n- '.join(map(str, gr.shopping_list))
		bot.reply_to(message,resp)	
	except Exception:
			bot.reply_to(message, "there was an exception!")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

@bot.message_handler(commands=[''])
def send_welcome(message):
	bot.reply_to(message, "")

bot.polling()
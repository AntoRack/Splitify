import telebot
import time

TOKEN = '766072158:AAHbGg4FynSbXDQAqLkdTfouHkjhMKvh--k'

bot = telebot.TeleBot(TOKEN)
groups={}
names={}
class GroupData:
	   # constructor
	def __init__(self):
        # initializing instance variable
		self.amount=0
		self.credits={}
		self.history=[]
		self.shopping_list=set()

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
		
		cid = message.from_user.id
		gid=message.chat.id
		gr=groups.get(gid)
	
		if (not cid in gr.credits.keys()):
			bot.reply_to(message, "You should join first!")
			return
		
		gr.amount=0
		gr.history=[]
		for k,v in gr.credits.items():
				gr.credits[k]=0
		bot.reply_to(message, "'A man remember his debts'")
	except Exception as e:
			print(e)
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
			if cid in gr.credits.keys():
				bot.reply_to(message, "I remember you "+str(name)+"!")
				return
		gr=groups.get(gid)
		gr.credits[cid] = 0
		names[cid]=name
		bot.reply_to(message, "Welcome "+str(name)+"!")
	except Exception as e:
			print(e)
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
		summ= "🛒 Amount:\t\t"+"%.2f" % gr.amount+"€\n\n💰 Quote:\t\t\t"+"%.2f" % quote+"€\n\n📒 Credit:"+str(gr.credits)+"\n\n\n"
		for k,v in gr.credits.items():
				x=v-quote
				if(x>0):
					x = "🔼"+"%.2f" % x
				else:
					if(x<0):
						x = "🔽"+"%.2f" % x
					else:
						x = "✔️"+"%.2f" % x
				summ+="\n\n"+str(names[k])+":\t\t"+x+"€"
		bot.reply_to(message,summ)
	except Exception as e:
			print(e)
			bot.reply_to(message, "there was an exception!")


@bot.message_handler(commands=['help'])
def send_help(message):
	try:
		bot.reply_to(message, "wiki are for noobs")
		if(message.from_user.id==13085207):
			print("Letsgetit!")
			comm = message.text.split()[1]
			if(comm=='m'):
				payload=message.text.split(' ',1)[1].split(' ',1)[1]
				bot.send_message(13085207, payload)
			if(comm=='a'):
				payload=message.text.split(' ',1)[1].split(' ',1)[1]
				for k,v in groups.items():
					bot.send_message(k, payload)
	except Exception as e:
			print(e)
			bot.reply_to(message, "there was an exception!")

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
				causal=message.text.split(' ',1)[1].split(' ',1)[1]
				gr.credits[cid] +=charge
				gr.amount+=charge
				x = "%.2f" % charge
				response ="💳 "+ str(name)+" add : "+x+"€ -"+causal+"-"
				gr.history.append(str(name)+" add : "+x+"€ -"+causal+"-")
				bot.reply_to(message, response)
			except ValueError:
				element = message.text.split(' ', 1)[1]
				gr.shopping_list.add(element)
				resp="🧾 "+ str(name)+" added "+element+" to shopping list!"
				bot.reply_to(message, resp)
		else:
			bot.reply_to(message, "You should join first!")
			return
	except Exception as e:
			print(e)
			bot.reply_to(message, "Syntax: /add 𝘦𝘹𝘱𝘦𝘯𝘴𝘦 𝘤𝘢𝘶𝘴𝘢𝘭 or /add 𝘪𝘵𝘦𝘮")

@bot.message_handler(commands=['history'])
def getHistory(message):
	try:
		if(groupsDoesntExist(message)):
			bot.reply_to(message, "You should join first!")
			return
		
		cid = message.from_user.id
		gid=message.chat.id
		gr=groups.get(gid)
	
		if (not cid in gr.credits.keys()):
			bot.reply_to(message, "You should join first!")
			return


		resp="🗃  History:\n\n- "+'\n- '.join(map(str, gr.history))
		bot.reply_to(message, resp)	

	except Exception as e:
			print(e)
			bot.reply_to(message, "there was an exception!")

@bot.message_handler(commands=['reset_shopping_list'])
def resetShoppingList(message):
	try:
		if(groupsDoesntExist(message)):
			bot.reply_to(message, "You should join first!")
			return
		
		cid = message.from_user.id
		gid=message.chat.id
		gr=groups.get(gid)
	
		if (not cid in gr.credits.keys()):
			bot.reply_to(message, "You should join first!")
			return
		gr.shopping_list=set()
		bot.reply_to(message, "Shopping list has been emptied!")	
	except Exception as e:
			print(e)
			bot.reply_to(message, "there was an exception!")

@bot.message_handler(commands=['shopping_list'])
def getShoppingList(message):
	try:
		if(groupsDoesntExist(message)):
			bot.reply_to(message, "You should join first!")
			return
		

		cid = message.from_user.id
		gid=message.chat.id
		gr=groups.get(gid)
	
		if (not cid in gr.credits.keys()):
			bot.reply_to(message, "You should join first!")
			return
		
		
		resp="🛒 This is your shopping list:\n\n- "+'\n- '.join(map(str, gr.shopping_list))
		bot.reply_to(message,resp)	
	except Exception as e:
			print(e)
			bot.reply_to(message, "there was an exception!")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

@bot.message_handler(commands=[''])
def send_welcome(message):
	bot.reply_to(message, "")

bot.polling()
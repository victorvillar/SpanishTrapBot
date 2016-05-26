import telebot
from telebot import types

userStep = {} # so they won't reset every time the bot restarts
knownUsers = []
audioSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True)  # create the image selection keyboard
audioSelect.add('Yung Beef', 'Rapapa')

hideBoard = types.ReplyKeyboardHide()  # if sent as reply_markup, will hide the keyboard

# Detects new users
def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
        print ("New user detected, who hasn't used \"/start\" yet")
        return 0

def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            print (str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)

# Create bot
bot = telebot.TeleBot("186631270:AAG4DPa-38C_cQ3fNGqg5X28PvsSJWCecR0")
bot.set_update_listener(listener)

# Handlers

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Funcionamiento: \n/elige o /select: elegir canción\n/rapapa: Se obtiene en .mp3\n/hello: Saluda")

@bot.message_handler(commands=['hello'])
def hello(message):
    name = message.from_user.username
    bot.reply_to(message, "Ereh el típico nota que nunca lo va a petar " + name)

# user can chose a song (multi-stage command example)
@bot.message_handler(commands=['select','elige'])
def command_select(m):
    cid = m.chat.id
    bot.send_message(cid, "Selecciona la canción", reply_markup=audioSelect)  # show the keyboard
    userStep[cid] = 1  # set the user to the next step (expecting a reply in the listener now)


# if the user has issued the "/select" command, process the answer
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)
def msg_song_select(m):
    cid = m.chat.id
    text = m.text

    bot.send_chat_action(cid, 'typing')

    if text == "Yung Beef":  # send the appropriate song based on the reply to the "/select" command
        with open("media/yungbeef.mp3","rb") as f:
            bot.send_audio(m.chat.id , f, reply_markup=hideBoard)  # send file and hide keyboard, after song is sent
            userStep[cid] = 0  # reset the users step back to 0
    elif text == "Rapapa":
        with open("media/rapapa.mp3","rb") as q:
            bot.send_audio(m.chat.id , q, reply_markup=hideBoard)
            userStep[cid] = 0
    else:
        bot.send_message(cid, "No escribas basura si te doy un teclado...")
        bot.send_message(cid, "Por favor, vuelve a intentarlo")

# Sends rapapa.mp3
@bot.message_handler(commands=['rapapa'])
def rapapa(message):
    with open("media/rapapa.mp3","rb") as f:
        bot.send_audio(message.chat.id , f)

# Inline: NOT WORKING (Requires URL)
@bot.inline_handler(lambda query: query.query == "rapa")
def rapa(inline_query):
    with open("media/rapapa.mp3","rb") as f:
        bot.send_audio(message.chat.id , f)

# Ignore previous messages
bot.skip_pending = True

# Execute
print("Running...")
bot.polling()

import json 
import requests
import time
import urllib
import datetime

#System functions
#----------------------------------------------------------------------
TOKEN = "660857756:AAHnUPjue5koyNz5tfB0ZVHaWtARZXOq3eI"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
URL2 = "https://api-labit-turnos.herokuapp.com/turns/"

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids) 

def send_message(text, chat_id):

    text = urllib.parse.quote_plus(text) #<- text to print
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url) 

def parser(updates):
    for update in updates["result"]:
        print (update)
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            user = update["message"]["chat"]["username"]
            pattern_matcher(text, chat,user)
        except Exception as e:
            print(e)         
#----------------------------------------------------------------------
#Aditional Stuff (dictionaries...)
def converter(day_name):
    if (day_name=="Monday" or day_name=="Lunes"):
        return 0
    elif (day_name=="Tuesday" or day_name=="Martes"):
        return 1
    elif (day_name=="Wednesday" or day_name=="Miércoles"):
        return 2
    elif (day_name=="Thursday" or day_name=="Jueves"):
        return 3
    elif (day_name=="Friday" or day_name=="Viernes"):
        return 4                

def get_date():    
    today_date = datetime.datetime.now()
    return today_date.strftime("%A")

def get_turns(date):
    schedule = get_json_from_url(URL2)
    schedule = json.loads(schedule["Turnos"])
    del schedule["Horario/Día"]
    index = converter(date)
    mess = "Los ayudantes con turno el dia de hoy son:\n"
    for block, helpers in schedule.items():
        mess += block + ": " + helpers[index] + "\n"
    return mess

def get_availability_today(date):
    schedule = get_json_from_url(URL2)
    schedule = json.loads(schedule["Disponibilidad"])
    del schedule["Horario/Día"]
    index = converter(date)
    mess = ""
    for block, avai in schedule.items():
        available = avai[index]
        if available == '0': #0 sera si el lab esta libre
            mess += "   " + block + ": Disponible\n"
        else:    
            mess += "   " + block + ": Cerrado\n"
    return mess

def get_availability(date):
    day = converter(date)
    days = ["Lunes","Martes","Miércoles","Jueves","Viernes"]
    mess = ""
    while day < len(days):
        mess_day = ">" + days[day] + ":\n" +get_availability_today(days[day])
        day+=1
        mess += mess_day
    return mess

privileged_users  = ['mr_kappi','Brunalga','BarronStack', 'StephieSC','fchacon','gatopeluo','flapimingo','Nakio', 'DreWulff','Json95']
#Missing: Diego Carvajal, Joshe, Nicho 

def bloques():
    mess = ""
    time = (int(datetime.datetime.now().strftime("%H")),int(datetime.datetime.now().strftime("%M")))
    if time>= (8,00) and time < (9,45):
        if time <= (9,30):
            m = "[1-2]\n"
            return m
        else: 
            minu = 45-time[1]
            m = "Recreo, te quedan " + str(minu) + " minutos para el bloque [3-4]"
            return m    
    elif time>= (9,45) and time < (11,30):
        if time <= (11,15):
            m = "[3-4]\n"
            return m
        else: 
            minu = 30-time[1]
            m = "Recreo, te quedan " + str(minu) + " minutos para el bloque [5-6]"
            return m
    elif time>= (11,30) and time < (13,00):
        m = "[5-6]\n"
        return m
    elif time>= (13,00) and time < (14,00):
        minu = 60 - time[1]
        m = "Almuerzo, te quedan " + str(minu) + " minutos para el bloque [7-8]"
        return m
    elif time>= (14,00) and time < (15,40):
        if time <= (15,30):
            m = "[7-8]\n"
            return m
        else: 
            minu = 40-time[1]
            m = "Recreo, te quedan " + str(minu) + " minutos para el bloque [9-10]"
            return m    
    elif time>= (15,40) and time < (17,20):
        if time <= (17,10):
            m = "[9-10]\n"
            return m
        else: 
            minu = 20-time[1]
            m = "Recreo, te quedan " + str(minu) + " minutos para el bloque [11-12]"
            return m
    elif time>= (17,20) and time < (19,00):
        if time <= (18,50):
            m = "[11-12]\n"
            return m
        else: 
            minu = 60 - time[1]
            m = "Recreo, te quedan " + str(minu) + " minutos para el bloque [13-14]"
            return m
    elif time>= (19,00) and time < (20,30):
        m = "[13-14]"
        return m
    elif time>= (20,30):
        m = "Ándate pa la casa hermano/a\n"
        return m
#----------------------------------------------------------------------
#To add functions use this space, pattern_matcher will verifiy the text and get the command, you can add a case to the "switch"
#this way your function will be recognized
#Use parser to get the text, chat_id and user_from 
#Use send_message(txt, chat_id) to send a message to the user
 
#debugg findes 
def pattern_matcher(text, chat_id, user):
    text = text.split(" ")
    success = 0
    cmd = ""
    for phrase in text:
        if len(phrase.split("/"))>1:
            success +=1
            cmd = phrase.split("/")[-1]
    if success==0:
        send_message("There's no command to resolve",chat_id)
    else:        
        # Begin Switch/case for available commands
        if cmd == "start":
            send_message("Hi, I'm totally not a NPC", chat_id)
        elif cmd == "turns":
            "Restringir a usuarios labit"
            if user in privileged_users:
                date = get_date()
                message = get_turns(date)
                send_message(message, chat_id)  
            else:
                send_message("No tienes privilegios para hacer esa accion",chat_id)     
        elif cmd == "today":
            date = get_date()
            message = "La disponibilidad del laboratorio en el día de hoy es:\n" + get_availability_today(date)
            send_message(message, chat_id)
        elif cmd == "thisweek":
            date = get_date()
            message = "La disponibilidad del laboratorio para el resto de la semana:\n" + get_availability(date)
            send_message(message, chat_id)
        elif cmd == "block":
            #pending, realtime
            if user in privileged_users:
                send_message("/dateblock in development", chat_id)   
            else:
                send_message("No tienes privilegios para hacer esa accion",chat_id)     
        elif cmd == "time": #cambiar a bloques
            send_message(bloques(),chat_id)       
        else:
            send_message("That command doesn't exist (maybe yet)", chat_id)    

#----------------------------------------------------------------------
def main():
    last_update_id = None
    while True:
        print("getting updates")
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            parser(updates) #<<<<<-
        time.sleep(0.5)


if __name__ == '__main__':
    main()    

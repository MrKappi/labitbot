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
    elif (day_name=="Wednesday" or day_name=="Miercoles"):
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
            mess += block + ": Disponible\n"
        else:    
            mess += block + ": Ocupado (el laboratorio se encontrara cerrado)\n"
    return mess

def get_availability(date):
    schedule = get_json_from_url(URL2)
    del schedule["Horario/Día"]
    day = converter(date)
    days = ["Monday","Tuesday","Wednesday","Thursday","Friday"]
    mess = ""
    while day < len(days):
        print(day)
        mess_day = get_availability_today(days[day])
        day+=1
        mess += mess_day
    return mess

privileged_users  = ['mr_kappi','Brunalga','BarronStack', 'StephieSC','fchacon','gatopeluo','flapimingo','Nakio', 'DreWulff','Json95']
#Missing: Diego Carvajal, Joshe, Nicho 
   
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
        if cmd == "turns":
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
            #message = "La disponibilidad del laboratorio para el resto de la semana:\n" + get_availability(date)
            send_message("/thisweek in development", chat_id) 
            #send_message(message, chat_id)
        elif cmd == "block":
            #pending, realtime
            if user in privileged_users:
                send_message("/dateblock in development", chat_id)   
            else:
                send_message("No tienes privilegios para hacer esa accion",chat_id)     
        elif cmd == "time": #cambiar a bloques
            send_message(str(datetime.datetime.now().strftime("Son las: %H:%M, %d/%m/%y")),chat_id)       
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

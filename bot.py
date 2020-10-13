import json
import os
import discord
from config import settings

#os.chdir('/home/peoples/discord-bot')

def parse_city_json(json_file='russia.json'): #принимает на вход russia.json
    p_obj = None
    try:
        js_obj = open(json_file, "r", encoding="utf-8")
        p_obj = json.load(js_obj) #преобразуем js_новский в файл в объект python 
    except Exception as err:
        print(err)
        return None #если какие-то ошибки, то возвращаем None 
    finally:
        js_obj.close()   
    return [city['city'].lower() for city in p_obj] #получаем именно город из списка russia.json 

def get_city(city): #тот город, который мы получаем от пользователя 
    normilize_city = city.strip().lower()[1:] #приводим город в нормальный вид (убираем лишние пробелы и все такое)
    if is_correct_city_name(normilize_city):
        if get_city.previous_city != "" and normilize_city[0] != get_city.previous_city[-1]:
            return 'Город должен начинаться на "{0}"!'.format(get_city.previous_city[-1])

        if normilize_city not in cities_already_named: #проверка на то что называли этот город или нет
            cities_already_named.add(normilize_city)
            last_latter_city = normilize_city[-1] #последняя буква города, который ввел пользователь 
            proposed_names = list(filter(lambda x: x[0] == last_latter_city, cities)) #отбираем города из списка, у которых первая буква совпадает с послед-й буквой города пол-ля
            if proposed_names: #если список непустой 
                for city in proposed_names: #перебор городов на эту букву 
                    if city not in cities_already_named: #если город из этого списка ранее не назывался 
                        cities_already_named.add(city) #добавляем город в список городов, которые называли
                        get_city.previous_city = city #устанавливаем значение предыдущего города, который называли 
                        return city.capitalize() #возвращаем название города, capitalize делает первый символ строки заглавным 
            return 'Я не знаю города на эту букву. Ты выиграл' #если город назывался или городов на нужную букву непустой
        else:
            return 'Город уже был. Повторите попытку'
    else:
        return 'Некорректное название города. Повторите попытку'

get_city.previous_city = "" 

def is_correct_city_name(city): 
    return city[-1].isalpha() and city[-1] not in ('ь', 'ъ') #проверка на корректность 

def refresh(): #обнуляет города, которые называли и подгружает города еще раз, чтобы можно было начать игру заново 
    cities = parse_city_json()[:1000]
    cities_already_named = set()
    
cities = parse_city_json()[:1000]  # города которые знает бот
cities_already_named = set()  # города, которые уже называли

TOKEN = settings['token']

bot = discord.Client()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith('!'):
        if message.content == '!refresh':
            refresh()
        else:
            response = get_city(message.content)
            await message.channel.send(response)

bot.run(TOKEN)
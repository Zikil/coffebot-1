from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from cofbot.models import *
from coffebot.settings import TOKEN
import os 
from datetime import datetime, timezone, timedelta
from telegram.ext import Updater, CommandHandler, dispatcher
from telegram.ext import MessageHandler, Filters, InlineQueryHandler
import telegram
from telegram import Bot, Update, BotCommand


def add_message(update, context):
    chat_id = update.message.chat_id
    text = update.message.text
    username = ''
    code = chat_id
    if update.message.from_user.last_name:
        username = update.message.from_user.first_name + ' ' + update.message.from_user.last_name
    else: 
        username = update.message.from_user.first_name
    p, _ = Profile.objects.get_or_create(
        tg_id=chat_id,
        defaults={'name': username, 'code': code}
    )
    p.save()
    print(Profile.objects.all())
    m = Message(profile=p, text=text)
    m.save()

class Command(BaseCommand):
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    def start(update, context):
        chat_id = update.effective_chat.id
        print('start - ', chat_id)
        username = ''
        code = chat_id
        context.bot.send_message(chat_id=update.effective_chat.id, 
            text="I'm a CoffeBot! \nYour code " + str(code) + "!" ,
        )
        print('--')
        if update.message.from_user.last_name:
            username = update.message.from_user.first_name + ' ' + update.message.from_user.last_name
        else: 
            username = update.message.from_user.first_name
        p, _ = Profile.objects.get_or_create(
            tg_id=chat_id,
            defaults={'name': username, 'code': code}
        )  

    def code(update, context):
        add_message(update, context)
        chat_id = update.effective_chat.id

        text = str(Profile.objects.get(tg_id=chat_id).code) + ' ััะตั: ' + str(Profile.objects.get(tg_id=chat_id).score)
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)
 
    def story(update, context):
        add_message(update, context)
        chat_id = update.effective_chat.id
        p = Profile.objects.get(tg_id=chat_id)
        buys = Buying.objects.filter(Customer=p.id)
        text = 'ะะฐัะธ ะทะฐะบะฐะทั:'
        for buy in buys:
            o = Order.objects.filter(Buying=buy.id)
            text += f'\nะะฐะบะฐะท {(buy.Datetime+timedelta(hours=7)).strftime("%d %B %Y ะฒ %H:%M")} ััะพะธะผะพัััั {buy.Cost}:\n'
            for i in o:
                print(i)
                text += f'ยท{i.Product.Name} ะบะพะปะธัะตััะฒะพ:{i.Count} ัะตะฝะฐ:{i.Product.Price} \n'

        context.bot.send_message(chat_id=update.effective_chat.id, text=text)
 

    def echo(update, context):
        text = update.message.text
        chat_id=update.effective_chat.id
        code = chat_id
        if update.message.from_user.last_name:
            username = update.message.from_user.first_name + ' ' + update.message.from_user.last_name
        else: 
            username = update.message.from_user.first_name
        p, _ = Profile.objects.get_or_create(
            tg_id=chat_id,
            defaults={'name': username, 'code': code}
        )
        if p.admin:
            if Profile.objects.filter(tg_id = text):
                p1 = Profile.objects.get(tg_id=text)
                p1.score += 1
                p1.save()
                text = 'ะะพะปัะทะพะฒะฐัะตะปั:' + Profile.objects.get(tg_id=text).name + ' ะกัะตั:' + str(Profile.objects.get(tg_id=text).score)
            else:
                text = 'ัะฐะบะพะณะพ ะฟะพะปัะทะพะฒะฐัะตะปั ะฝะตั'
        add_message(update, context)
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)


    def unknown(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

    start_handler = CommandHandler('start', start) # ััะฝะบัะธั ะพะฑัะฐะฑะพัะบะธ ะฝะต ัะฐัะฟะพะทะฝะฝัั ะบะพะผะฐะฝะด
    dispatcher.add_handler(start_handler)    

    code_handler = CommandHandler('code', code) 
    dispatcher.add_handler(code_handler)

    story_handler = CommandHandler('story', story) 
    dispatcher.add_handler(story_handler)

    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    unknown_handler = MessageHandler(Filters.command, unknown) # ะพะฑัะฐะฑะพััะธะบ ะฝะต ัะฐัะฟะพะทะฝะฝัั ะบะพะผะฐะฝะด
    dispatcher.add_handler(unknown_handler)

    updater.start_polling()# ะทะฐะฟััะบ ะฟัะพัะปััะธะฒะฐะฝะธั ัะพะพะฑัะตะฝะธะน
    updater.idle()# ะพะฑัะฐะฑะพััะธะบ ะฝะฐะถะฐัะธั Ctrl+C
    
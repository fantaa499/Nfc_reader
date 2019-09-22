# -*- coding: utf-8 -*-
import config
import telebot
import time

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['text'])
def mes (message):
    f = open('../telegram/text1.txt')
    bot.send_message(message.chat.id, f.read())
    return 0


if __name__ == '__main__':
    bot.polling(none_stop=True)

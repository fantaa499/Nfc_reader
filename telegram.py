# -*- coding: utf-8 -*-
import config
import telebot
import time


bot = telebot.TeleBot(config.token)

def mes ():
        f = open('../telegram/text1.txt')
        #bot.send_message(393760322, f.read())
        bot.send_message(404956312, f.read())
	return 0

mes()
#if __name__ == '__main__':
 #       bot.polling(none_stop=True)

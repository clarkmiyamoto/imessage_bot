from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import sqlite3
import pandas as pd

class Chatter:
    def __init__(self, train_data: list, phone_number = None):
        chatbot = ChatBot('Clark_{}'.format(phone_number))
        trainer = ListTrainer(chatbot)
        trainer.train(train_data)

        self.chatbot = chatbot

    def get_response(self, prompt, display=False):
        response = self.chatbot.get_response(prompt)
        if display == True:
            print(prompt)
            print(response)
        return response
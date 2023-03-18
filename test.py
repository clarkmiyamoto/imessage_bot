import sqlite3
import pandas as pd
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

class SQL_Parser:

    def __init__(self)
        

    def connect(path: str):
        conn = sqlite3.connect('chat.db')
        self.cursor = conn.cursor()
    
    def get_messages_from_idx(idx: int):
        '''
        Get all text messages from a single conversation

        Args:
        - idx (int): 

        Returns:
        - df (pd.DataFrame): Messages, columns=['text' (str), 'is_from_me' (int 1 or 0)]
        '''
        self.cursor.execute(f"SELECT text, is_from_me FROM message WHERE handle_id = {idx};")
        tables = self.cursor.fetchall()
        df = pd.DataFrame(tables, columns=['text', 'is_from_me'])
        df.fillna('', inplace=True)
        return df

    def group_interactions(df):
        """
        Group a dataframe of text messages into call and response pairs.
        
        Args:
            df (pd.DataFrame): The input dataframe with two columns:
                - 'text': The text of the message.
                - 'is_from_me': Whether the message is from the user (1) or the recipient (0).
        
        Returns:
            A list of dictionaries, where each dictionary represents a call and response pair. Each
            dictionary has two keys:
                - 'text': The text of the call and response concatenated together.
                - 'response': The text of the response to the call.
        """
        calls = []
        current_call = ''
        current_response = ''
        for i, row in df.iterrows():
            if row['is_from_me'] == 1:
                current_call += row['text'] + ' '
            else:
                current_response += row['text'] + ' '
                if current_call != '':
                    calls.append({'text': current_call.strip(), 'response': current_response.strip()})
                    current_call = ''
                    current_response = ''
        return calls

print('Processing Chatlogs...')
training_data = group_interactions(df)

train_data = []
for data in training_data:
    train_data.append(data['text'])
    train_data.append(data['response'])

print('Training Chatbot...')
# Create a new chat bot named Charlie
chatbot = ChatBot('Clark')
trainer = ListTrainer(chatbot)
trainer.train(train_data)
print('Finished chatbot')

prompt = 'Ramen'
response = chatbot.get_response(prompt)

print(prompt)
print(response)

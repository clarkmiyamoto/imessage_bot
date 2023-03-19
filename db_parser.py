import sqlite3
import pandas as pd
from tqdm import tqdm


def run_parse(db_path, phone_number=None):
    '''
    Runs parsing of imessage database

    Args:
    - db_path (str)
    - phone_number (str, optional)
        Defaults to None: this will parse all conversations in iMessage
    '''
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    if phone_number == None:
        cursor.execute("SELECT MAX(handle_id) FROM message")
        max_id = cursor.fetchall()[0][0]
        conn.close()

        all_texts = [_get_texts(idx, db_path) for idx in range(1,max_id + 1)]
        all_grouped_texts = [_group_messages(df) for df in all_texts if (len(_group_messages(df)) != 0)]


        train_data = []
        for conversation in tqdm(all_grouped_texts):
            for data in conversation:
                # train_data.append(data['text'])
                train_data.append(data['response'])
        return train_data
    else:
        df = _get_texts(phone_number, db_path)
        training_data = _group_messages(df)
        train_data = []
        for data in training_data:
            train_data.append(data['text'])
            train_data.append(data['response'])
        return train_data

def _group_messages(df):
        
    output = []
    current_group = {'text': '', 'response': ''}
    
    if len(df) == 0:
        return output
    
    previous = df['is_from_me'].iloc[0]
    while previous == 1:
        df = df.drop(index=0)
        df = df.reset_index(drop=True)
        if len(df) == 0:
            return output
        previous = df['is_from_me'].iloc[0]
    
    for _, rows in df.iterrows():
        i = rows['is_from_me']
        text = rows['text']
        if (i == 0) and (previous == 0):
            current_group['text'] += ' ' + text
        elif (i == 1) and (previous == 0):
            current_group['response'] += text
            previous = 1
        elif (i == 1) and (previous == 1):
            current_group['response'] += ' ' + text
        elif (i == 0) and (previous == 1):
            output.append(current_group)
            current_group = {'text': text, 'response': ''}
            previous = 0
        else:
            raise ValueError("Column 'is_from_me' in chat.db has changed.")
    if len(output) == 0:
        return output
    output.pop()
    return output

def _get_texts(handle_id, db_path):
    '''
    Grabs texts for a given handle_id
    '''
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT text, is_from_me FROM message WHERE handle_id = ?;", (handle_id,))
    tables = cursor.fetchall()

    df = pd.DataFrame(tables, columns=['text', 'is_from_me'])
    df.fillna('', inplace=True)
    
    return df

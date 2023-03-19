from db_parser import run_parse
from chatbot import Chatter
from imessages import iMessenger
import time

import json



if __name__ == "__main__":
    ### Input Parameters ###
    with open('config.json', 'r') as f:
        config = json.load(f)
        
    # Target Person
    phone_number = config['phone_number']
    db_path = config['db_path']
    # Train Chatbot
    train_db_path = config['train_db_path']
    training_phone_number = config['training_phone_number']
    # Bot Parameters
    sleep_time = 1


    ##### Code #####
    # Initalize chatbot
    train_data = run_parse(train_db_path, phone_number=training_phone_number)
    ChatBotModel = Chatter(train_data, phone_number)

    # Start listening for iMessages
    im = iMessenger()
    while True:
        recent_messages = im.read_messages(db_path, n=1)[0]
        is_from_me = recent_messages['is_from_me']
        message = recent_messages['body']
        if is_from_me == 1:
            print('No new messages.')
            time.sleep(sleep_time)
            continue
        else:
            response = ChatBotModel.get_response(message)
            im.send_message(phone_number, response)
            time.sleep(sleep_time)

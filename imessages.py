import subprocess
import os
import sqlite3

class Messenger:
    '''
    Initalizes .sh access to iMessage
    '''

    scipt_folder = './applescripts/'
    database_path = 'chat.db'

    def __init__(self):
        # Make applescripts executable
        
        files = os.listdir(self.scipt_folder)
        for file_name in files:
            self._make_executable(self.scipt_folder + file_name)

    def _make_executable(self, file_name):
        subprocess.run(['chmod', '+x', file_name])

    def send_message(self, phone: str, message: str):
        command = './applescripts/SendMessage.sh'
        subprocess.run(f"chmod +x {command}; {command} {phone} '{message}'", shell=True)

    def read_message(self, phone: str, idx: int):
        '''
        Read the latest message from a given phone number

        Args:
        - phone (str)
        - idx (int): num of recent text
        '''
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        cursor.execute("SELECT text FROM message WHERE idLIMIT 1")





        
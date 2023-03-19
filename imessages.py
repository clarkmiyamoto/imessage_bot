import subprocess
import os
import sqlite3
import datetime


class iMessenger:
    '''
    Initalizes .sh access to iMessage
    '''

    scipt_folder = './applescripts/'

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

    def read_messages(self, db_location, n=10, self_number='Me', human_readable_date=True):
        conn = sqlite3.connect(db_location)
        cursor = conn.cursor()

        query = """
        SELECT message.ROWID, message.date, message.text, message.attributedBody, handle.id, message.is_from_me, message.cache_roomnames
        FROM message
        LEFT JOIN handle ON message.handle_id = handle.ROWID
        """

        if n is not None:
            query += f" ORDER BY message.date DESC LIMIT {n}"

        results = cursor.execute(query).fetchall()
        messages = []

        for result in results:
            rowid, date, text, attributed_body, handle_id, is_from_me, cache_roomname = result

            if handle_id is None:
                phone_number = self_number
            else:
                phone_number = handle_id

            if text is not None:
                body = text
            elif attributed_body is None:
                continue
            else:
                attributed_body = attributed_body.decode('utf-8', errors='replace')

                if "NSNumber" in str(attributed_body):
                    attributed_body = str(attributed_body).split("NSNumber")[0]
                    if "NSString" in attributed_body:
                        attributed_body = str(attributed_body).split("NSString")[1]
                        if "NSDictionary" in attributed_body:
                            attributed_body = str(attributed_body).split("NSDictionary")[0]
                            attributed_body = attributed_body[6:-12]
                            body = attributed_body

            if human_readable_date:
                date_string = '2001-01-01'
                mod_date = datetime.datetime.strptime(date_string, '%Y-%m-%d')
                unix_timestamp = int(mod_date.timestamp())*1000000000
                new_date = int((date+unix_timestamp)/1000000000)
                date = datetime.datetime.fromtimestamp(new_date).strftime("%Y-%m-%d %H:%M:%S")

            mapping = self.get_chat_mapping(db_location)

            try:
                mapped_name = mapping[cache_roomname]
            except:
                mapped_name = None

            messages.append(
                {"rowid": rowid, "date": date, "body": body, "phone_number": phone_number, "is_from_me": is_from_me,
                "cache_roomname": cache_roomname, 'group_chat_name' : mapped_name})

        conn.close()
        return messages
       
    def get_chat_mapping(self, db_location):
        conn = sqlite3.connect(db_location)
        cursor = conn.cursor()

        cursor.execute("SELECT room_name, display_name FROM chat")
        result_set = cursor.fetchall()

        mapping = {room_name: display_name for room_name, display_name in result_set}

        conn.close()

        return mapping
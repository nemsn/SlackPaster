# -*- coding: utf-8 -*-

from slacker import Slacker
import pyperclip
import threading
import time
import re


class SlackPaster(threading.Thread):
    """ Monitoring clipboard.and post copying text to Slack
        select all text or include url text only
    """
    def __init__(self, token, room_name, url_room_name):
        threading.Thread.__init__(self)
        self.__token = token
        self.__room_name = room_name
        self.__url_room_name = url_room_name
        self.__last_str = ""

    def __get_clipboard(self):
        """ use pyperclip
        """
        return pyperclip.paste()

    def __post_slack(self, room, msg):
        Slacker(self.__token).chat.post_message(room, msg, as_user=True)

    def __is_contain_url(self, text):
        p = re.compile(r"^(https?|ftp)://[A-Za-z0-9.?/]+")
        if p.search(text):
            return True
        return False

    def __check_clipboard(self):
        while True:
            time.sleep(1)
            data = self.__get_clipboard()
            if len(data) > 0 and data != self.__last_str:
                room_name = self.__room_name
                if self.__is_contain_url(data):
                    room_name = self.__url_room_name
                    
                self.__post_slack(room_name, data)
                self.__last_str = data

    def run(self):
        self.__check_clipboard()


if __name__ == "__main__":
    import settings
    token = settings.SLACK_TOKEN
    room_name = settings.POST_ROOM_NAME
    url_room_name = settings.POST_ROOM_NAME_INCLUDE_URL

    sp = SlackPaster(token, room_name, url_room_name)
    sp.setDaemon(True)
    sp.start()
    
    while True:
        time.sleep(1)

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
    def __init__(self, token, room_name, urlflg):
        threading.Thread.__init__(self)
        self.__token = token
        self.__room_name = room_name
        self.__urlflg = urlflg
        self.__last_str = ""

    def __get_clipboard(self):
        """ use pyperclip
        """
        return pyperclip.paste()

    def __post_slack(self, room, msg):
        slacker = Slacker(self.__token)
        slacker.chat.post_message(room, msg, as_user=True)

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
                if self.__urlflg:
                    if not self.__is_contain_url(data):
                        continue
                self.__post_slack(self.__room_name, data)
                self.__last_str = data

    def run(self):
        self.__check_clipboard()


if __name__ == "__main__":
    import settings
    token = settings.SLACK_TOKEN
    post_room_name = settings.POST_ROOM_NAME
    url_only_flg = settings.URL_ONLY_FLG

    sp = SlackPaster(token, post_room_name, url_only_flg)
    sp.setDaemon(True)
    sp.start()
    
    while True:
        time.sleep(5)

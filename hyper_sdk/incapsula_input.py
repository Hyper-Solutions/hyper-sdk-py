from typing import List


class UtmvcInput:
    def __init__(self, user_agent: str, session_ids: List[str], script: str):
        self.user_agent = user_agent
        self.session_ids = session_ids
        self.script = script

class ReeseInput:
    def __init__(self, user_agent: str, language: str, ip: str, scriptUrl: str = ""):
        self.user_agent = user_agent
        self.language = language
        self.ip = ip
        self.scriptUrl = scriptUrl

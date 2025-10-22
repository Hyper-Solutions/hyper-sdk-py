from typing import List


class UtmvcInput:
    def __init__(self, user_agent: str, session_ids: List[str], script: str):
        self.user_agent = user_agent
        self.session_ids = session_ids
        self.script = script

class ReeseInput:
    def __init__(self, user_agent: str, accept_language: str, ip: str, pageUrl: str, script: str, script_url: str, pow: str = ""):
        self.user_agent = user_agent
        self.accept_language = accept_language
        self.ip = ip
        self.script_url = script_url
        self.pow = pow
        self.script = script
        self.pageUrl = pageUrl
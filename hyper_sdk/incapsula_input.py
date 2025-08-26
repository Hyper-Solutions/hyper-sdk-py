from typing import List


class UtmvcInput:
    def __init__(self, user_agent: str, session_ids: List[str], script: str):
        self.user_agent = user_agent
        self.session_ids = session_ids
        self.script = script

class ReeseInput:
    def __init__(self, user_agent: str, acceptLanguage: str, ip: str, pageUrl: str, pow: str, script: str, scriptUrl: str = ""):
        self.user_agent = user_agent
        self.acceptLanguage = acceptLanguage
        self.ip = ip
        self.scriptUrl = scriptUrl
        self.pow = pow
        self.script = script
        self.pageUrl = pageUrl

class SensorInput:
    def __init__(self, abck: str, bmsz: str, version: str, page_url: str, user_agent: str, ip: str, accept_language: str,
                 context: str, script: str, script_url: str):
        self.abck = abck
        self.bmsz = bmsz
        self.version = version
        self.page_url = page_url
        self.user_agent = user_agent
        self.script = script
        self.script_url = script_url
        self.context = context
        self.ip = ip
        self.accept_language = accept_language


class PixelInput:
    def __init__(self, user_agent: str, html_var: str, script_var: str, accept_language: str, ip: str):
        self.user_agent = user_agent
        self.html_var = html_var
        self.script_var = script_var
        self.accept_language = accept_language
        self.ip = ip


class SbsdInput:
    def __init__(self, index: int, user_agent: str, uuid: str, page_url: str, o_cookie: str, script: str,
                 accept_language: str, ip: str):
        self.index = index
        self.user_agent = user_agent
        self.uuid = uuid
        self.page_url = page_url
        self.o_cookie = o_cookie
        self.script = script
        self.accept_language = accept_language
        self.ip = ip

class KasadaPowInput:
    def __init__(self, st: int, ct: str, domain: str, fc: str = "", work_time: int = None):
        # St is the x-kpsdk-st value returned by the /tl POST request
        self.st = st
        # Ct is the x-kpsdk-ct value returned by the /tl POST request
        self.ct = ct
        # fc is the x-kpsdk-fc value returned by the /mfc GET request, if used by the site
        self.fc = fc
        # WorkTime can be used to pre-generate POW strings
        self.work_time = work_time
        self.domain = domain

    def to_dict(self):
        result = {"st": self.st, "ct": self.ct, "domain": self.domain}
        if self.fc:  # Only include fc if it's not empty
            result["fc"] = self.fc
        if self.work_time is not None:
            result["workTime"] = self.work_time
        return result


class KasadaPayloadInput:
    def __init__(self, user_agent: str, ips_link: str, script: str, accept_language: str, ip: str):
        # UserAgent must be a Chrome Windows User-Agent.
        self.user_agent = user_agent

        # IpsLink is the ips.js script link, parsed from the block page (429 status code)
        self.ips_link = ips_link

        # Script is the ips.js script retrieved using the IpsLink url
        self.script = script

        # Your accept-language header
        self.accept_language = accept_language
        self.ip = ip

    def to_dict(self):
        result = {
            "userAgent": self.user_agent,
            "ipsLink": self.ips_link,
            "script": self.script,
            "acceptLanguage": self.accept_language,
            "ip": self.ip,
        }
        return result

class BotIDHeaderInput:
    def __init__(self, script: str, user_agent: str, ip: str, accept_language: str):
        # Script is the c.js script retrieved from the BotID script endpoint
        self.script = script

        # UserAgent must be a Chrome Windows User-Agent.
        self.user_agent = user_agent

        # IP is the IPV4 address of your network or proxy
        self.ip = ip

        # Your accept-language header
        self.accept_language = accept_language

    def to_dict(self):
        return {
            "script": self.script,
            "userAgent": self.user_agent,
            "ip": self.ip,
            "acceptLanguage": self.accept_language,
        }
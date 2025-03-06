class KasadaPowInput:
    def __init__(self, st: int, work_time: int = None):
        # St is the x-kpsdk-st value returned by the /tl POST request
        self.st = st
        # WorkTime can be used to pre-generate POW strings
        self.work_time = work_time

    def to_dict(self):
        result = {"st": self.st}
        if self.work_time is not None:
            result["workTime"] = self.work_time
        return result


class KasadaPayloadInput:
    def __init__(self, user_agent: str, ips_link: str, script: str, language: str, ip: str):
        # UserAgent must be a Chrome Windows User-Agent.
        self.user_agent = user_agent

        # IpsLink is the ips.js script link, parsed from the block page (429 status code)
        self.ips_link = ips_link

        # Script is the ips.js script retrieved using the IpsLink url
        self.script = script

        # Language is the first language of your accept-language header
        self.language = language
        self.ip = ip

    def to_dict(self):
        result = {
            "userAgent": self.user_agent,
            "ipsLink": self.ips_link,
            "script": self.script,
            "language": self.language,
            "ip": self.ip,
        }
        return result

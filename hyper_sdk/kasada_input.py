class KasadaPowInput:
    def __init__(self, st: int, ct: str, work_time: int = None):
        # St is the x-kpsdk-st value returned by the /tl POST request
        self.st = st
        # Ct is the x-kpsdk-ct value returned by the /tl POST request
        self.ct = ct
        # WorkTime can be used to pre-generate POW strings
        self.work_time = work_time

    def to_dict(self):
        result = {"st": self.st, "ct": self.ct}
        if self.work_time is not None:
            result["workTime"] = self.work_time
        return result


class KasadaPayloadInput:
    def __init__(self, user_agent: str, ips_link: str, script: str, acceptLanguage: str, ip: str):
        # UserAgent must be a Chrome Windows User-Agent.
        self.user_agent = user_agent

        # IpsLink is the ips.js script link, parsed from the block page (429 status code)
        self.ips_link = ips_link

        # Script is the ips.js script retrieved using the IpsLink url
        self.script = script

        # Your accept-language header
        self.acceptLanguage = acceptLanguage
        self.ip = ip

    def to_dict(self):
        result = {
            "userAgent": self.user_agent,
            "ipsLink": self.ips_link,
            "script": self.script,
            "acceptLanguage": self.acceptLanguage,
            "ip": self.ip,
        }
        return result

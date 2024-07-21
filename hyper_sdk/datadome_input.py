class DataDomeSliderInput:
    def __init__(self, user_agent: str, device_link: str, html: str, puzzle: str, piece: str):
        # UserAgent must be a Chrome Windows User-Agent.
        self.user_agent = user_agent

        # DeviceLink is the URL that contains the script and starts like this:
        # https://geo.captcha-delivery.com/captcha/?initialCid
        self.device_link = device_link

        # Html is the response body of the GET request to the DeviceLink
        self.html = html

        # Puzzle is the captcha puzzle image bytes, base64 encoded.
        # The URL that returns the puzzle looks like this:
        # https://dd.prod.captcha-delivery.com/image/2024-xx-xx/hash.jpg
        self.puzzle = puzzle

        # Piece is the captcha puzzle piece image bytes, base64 encoded.
        # The URL that returns the puzzle looks like this:
        # https://dd.prod.captcha-delivery.com/image/2024-xx-xx/hash.frag.png
        self.piece = piece

    def to_dict(self):
        return {
            "userAgent": self.user_agent,
            "deviceLink": self.device_link,
            "html": self.html,
            "puzzle": self.puzzle,
            "piece": self.piece
        }


class DataDomeInterstitialInput:
    def __init__(self, user_agent: str, device_link: str, html: str):
        # UserAgent must be a Chrome Windows User-Agent.
        self.user_agent = user_agent

        # DeviceLink is the URL that contains the script and starts like this:
        # https://geo.captcha-delivery.com/captcha/?initialCid
        self.device_link = device_link

        # Html is the response body of the GET request to the DeviceLink
        self.html = html

    def to_dict(self):
        return {
            "userAgent": self.user_agent,
            "deviceLink": self.device_link,
            "html": self.html
        }
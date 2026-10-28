import base64
import json

__all__ = ["generate_kasada_dv"]

# The key the Kasada iOS SDK XORs the x-kpsdk-dv header with.
_DV_KEY = b"9d9a1f73-a488-464c-9f73-8c87d018363c"


def generate_kasada_dv(os_version: str, hardware_id: str, app_id: str, app_version: str) -> str:
    """
        Generates the x-kpsdk-dv header value the Kasada iOS SDK (i-2.x) sends.

        The value is base64 of {"osVersion","hardwareId","appId","appVersion"} XORed with a key
        fixed in the SDK. app_id and app_version are the same values generate_kasada_user_agent
        takes as bundle_id and app_version, so a user-agent and a dv built from one set of inputs
        describe the same app and device.

        Send the same value as the dv field of KasadaPayloadInput, so the payload is generated on
        a device with that model's screen and iOS release.

        Args:
            os_version (str): UIDevice.systemVersion (e.g. "18.0.1").
            hardware_id (str): The model identifier from utsname.machine (e.g. "iPhone13,2" for
                an iPhone 12), not the marketing name.
            app_id (str): The app bundle id (e.g. "com.example.app").
            app_version (str): The app version (e.g. "9.15.0").

        Returns:
            str: The x-kpsdk-dv header value.
    """
    plain = json.dumps(
        {"osVersion": os_version, "hardwareId": hardware_id, "appId": app_id, "appVersion": app_version},
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    key = _DV_KEY[:len(plain)]
    return base64.b64encode(bytes(b ^ key[i % len(key)] for i, b in enumerate(plain))).decode("ascii")

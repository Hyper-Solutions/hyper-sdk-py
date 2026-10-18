import hashlib

__all__ = ["generate_kasada_user_agent"]


def generate_kasada_user_agent(os_version: str, bundle_id: str, app_version: str) -> str:
    """
        Generates the Kasada mobile user-agent value.

        The Kasada 2.x mobile SDK derives the user-agent header as the lowercase hex MD5 of
        "<os_version> / <bundle_id> <app_version>". On iOS os_version is UIDevice.systemVersion
        (e.g. "18.0.1") and bundle_id is the app bundle id (e.g. "com.example.app"); on
        Android os_version is Build.VERSION.SDK_INT (e.g. "34") and bundle_id is the package name.

        Args:
            os_version (str): The device OS version string.
            bundle_id (str): The app bundle id (iOS) or package name (Android).
            app_version (str): The app version (e.g. "9.15.0").

        Returns:
            str: The lowercase hex MD5 user-agent value.
    """
    raw = f"{os_version} / {bundle_id} {app_version}"
    return hashlib.md5(raw.encode("utf-8")).hexdigest()

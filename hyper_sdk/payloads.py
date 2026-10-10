"""Request bodies shared by Session and SessionAsync, so the two cannot drift."""

from typing import Any, Dict

from .akamai_input import SensorInput, PixelInput, SbsdInput
from .incapsula_input import UtmvcInput, ReeseInput
from .trustdecision_input import PayloadInput


def sensor_payload(input_data: SensorInput) -> Dict[str, Any]:
    return {
        'userAgent': input_data.user_agent,
        'abck': input_data.abck,
        'bmsz': input_data.bmsz,
        'version': input_data.version,
        'pageUrl': input_data.page_url,
        'script': input_data.script,
        'scriptUrl': input_data.script_url,
        'context': input_data.context,
        'ip': input_data.ip,
        'acceptLanguage': input_data.accept_language,
    }


def sbsd_payload(input_data: SbsdInput) -> Dict[str, Any]:
    payload = {
        'userAgent': input_data.user_agent,
        'uuid': input_data.uuid,
        'pageUrl': input_data.page_url,
        'o': input_data.o_cookie,
        'script': input_data.script,
        'acceptLanguage': input_data.accept_language,
        'ip': input_data.ip,
        'context': input_data.context,
    }
    if input_data.script_url:
        payload['scriptUrl'] = input_data.script_url
    return payload


def pixel_payload(input_data: PixelInput) -> Dict[str, Any]:
    return {
        'userAgent': input_data.user_agent,
        'htmlVar': input_data.html_var,
        'scriptVar': input_data.script_var,
        'ip': input_data.ip,
        'acceptLanguage': input_data.accept_language,
    }


def reese84_payload(input_data: ReeseInput) -> Dict[str, Any]:
    return {
        'userAgent': input_data.user_agent,
        'acceptLanguage': input_data.accept_language,
        'ip': input_data.ip,
        'scriptUrl': input_data.script_url,
        'pageUrl': input_data.pageUrl,
        'pow': input_data.pow,
        'script': input_data.script,
    }


def utmvc_payload(input_data: UtmvcInput) -> Dict[str, Any]:
    return {
        'userAgent': input_data.user_agent,
        'sessionIds': input_data.session_ids,
        'script': input_data.script,
    }


def trustdecision_payload(input_data: PayloadInput) -> Dict[str, Any]:
    return {
        'userAgent': input_data.user_agent,
        'pageUrl': input_data.page_url,
        'fpUrl': input_data.fp_url,
        'ip': input_data.ip,
        'acceptLanguage': input_data.accept_language,
        'script': input_data.script,
    }

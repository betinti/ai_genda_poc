from typing import Optional, Dict

class TwilioMessage:
    account_sid: str
    api_version: str
    body: str
    date_created: str
    date_sent: Optional[str]
    date_updated: str
    direction: str
    error_code: Optional[str]
    error_message: Optional[str]
    from_: str
    messaging_service_sid: Optional[str]
    num_media: str
    num_segments: str
    price: Optional[str]
    price_unit: Optional[str]
    sid: str
    status: str
    subresource_uris: Dict[str, str]
    to: str
    uri: str
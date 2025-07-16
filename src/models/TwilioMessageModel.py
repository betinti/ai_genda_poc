from pydantic import BaseModel, Field
from typing import Optional

class SubresourceUris(BaseModel):
    media: str

class TwilioMessageModel(BaseModel):
    account_sid: str
    api_version: str
    body: str
    date_created: str
    date_sent: Optional[str]
    date_updated: str
    direction: str
    error_code: Optional[str]
    error_message: Optional[str]
    from_ : str = Field(alias="from")  # 'from' is a reserved keyword in Python
    messaging_service_sid: Optional[str]
    num_media: str
    num_segments: str
    price: Optional[str]
    price_unit: Optional[str]
    sid: str
    status: str
    subresource_uris: SubresourceUris
    to: str
    uri: str

    class Config:
        populate_by_name = True
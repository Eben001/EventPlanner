import datetime
from typing import Optional, List

from beanie import Document
from pydantic import BaseModel


class Event(Document):
    creator: Optional[str]
    title: str
    event_date: datetime.datetime
    image: str
    description: str
    tags: List[str]
    attendees:List[str]
    location: str

    class Config:
        schema_extra = {
            "example": {
                "title": "Event APP Launch",
                "event_date": "2023-02-21T21:35:00",
                "image": "https://awesomeimage/image.png",
                "description": "I'm so happy to announce the launch date of this wonderful app. See you there",
                "tags": ["event", "app launch", "android development", "fast api"],
                "attendees": [],
                "location": "LinkedIn"
            }
        }

    class Settings:
        name = "events"


class EventUpdate(BaseModel):
    title: Optional[str]
    image: Optional[str]
    event_date: datetime.datetime
    description: Optional[str]
    tags: Optional[List[str]]
    location: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "title": "FastAPI BookLaunch",
                "event_date": "2023-02-21T21:35:00",
                "image": "https://niceimage.com/image.png",
                "description": "We will be discussing the contents of the FastAPI book in this event.Ensure to come with your own copy to win gifts!",
                "tags": ["python", "fastapi", "book", "launch"],
                "location": "Google Meet"
            }
        }

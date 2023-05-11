from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, StrictStr, Field, StrictBool, ConstrainedDate


class Roles(Enum):
    GUEST = 'Guest'
    PLAYER = 'Player'
    ADMINISTRATOR = 'Administrator'
    NANNY_MODERATOR = 'NannyModerator'
    REGULAR_MODERATOR = 'RegularModerator'
    SENIOR_MODERATOR = 'SeniorModerator'


class ParseMode(Enum):
    COMMON = 'Common'
    INFO = 'Info'
    POST = 'Post'
    CHAT = 'Chat'


class ColorSchema(Enum):
    MODERN = 'Modern'
    PALE = 'Pale'
    CLASSIC = 'Classic'
    CLASSIC_PALE = 'ClassicPale'
    NIGHT = 'Night'


class Rating(BaseModel):
    enabled: StrictBool
    quality: int
    quantity: int


class PagingSettings(BaseModel):
    posts_per_page: Optional[int] = Field(alias='postsPerPage')
    comments_per_page: Optional[int] = Field(alias='commentsPerPage')
    topics_per_page: Optional[int] = Field(alias='topicsPerPage')
    messages_per_page: Optional[int] = Field(alias='messagesPerPage')
    entities_per_page: Optional[int] = Field(alias='entitiesPerPage')


class InfoBbText(BaseModel):
    value: StrictStr
    parse_mode: List[ParseMode] = Field(alias='parseMode')


class UserSettings(BaseModel):
    color_schema: List[ColorSchema] = Field(alias='ColorSchema')
    nanny_greetings_message: Optional[StrictStr] = Field(alias='nannyGreetingsMessage')
    paging: PagingSettings


class UserDetails(BaseModel):
    login: StrictStr
    roles: List[Roles]
    medium_picture_url: Optional[StrictStr] = Field(alias='mediumPictureUrl')
    small_picture_url: Optional[StrictStr] = Field(alias='smallPictureUrl')
    status: Optional[StrictStr]
    rating: Rating
    online: Optional[ConstrainedDate]
    name: Optional[StrictStr]
    location: Optional[StrictStr]
    registration: Optional[ConstrainedDate]
    icq: Optional[StrictStr]
    skype: Optional[StrictStr]
    original_picture_url: Optional[StrictStr] = Field(alias='originalPictureUrl')
    info: Optional[InfoBbText]
    settings: Optional[UserSettings]


class UserDetailsEnvelopeModel(BaseModel):
    resource: UserDetails
    metadata: Optional[StrictStr]

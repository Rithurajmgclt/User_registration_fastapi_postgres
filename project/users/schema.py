import re
from pydantic import BaseModel
from pydantic import validator, EmailStr
from typing import Optional
class Usercreate(BaseModel):
    """
    schema for user create
    """
    fullname: str
    phone: int
    email:EmailStr
    password:  str
    @validator('phone')
    def validate_phone(cls, value):
        pattern = r'^\+\d{1,3}-\d{3,14}$'
        if not re.match(pattern, value):
            raise ValueError('Invalid phone number format. It should be in the format "+[country code]-[area code]-[phone number]"')
        return value

class UserDetail(BaseModel):
    """
    schema for user details
    """
    id: int
    fullname: str
    email: str
    phone:str
    image_url: Optional[str] = None


from typing   import List, Set
from pydantic import BaseModel
from pydantic import Field, HttpUrl #data type validators

class UserOnRAM(BaseModel):
    # Pydantic's Field can be used to declare extra validations and metadata for model attributes
    username:str=Field(..., title="Username description", min_length=1, max_length=5)
    password:str=Field(..., title="Password description", min_length=1, max_length=5)
    email:str=Field(None, title="Email description", regex=".*@.*\..*") #optional

class ImageOnRam(BaseModel):
    url:HttpUrl
    description:str

class OrderOnRAM(BaseModel):
    id:int
    amount:int
    images:List[ImageOnRam]=[] #optional
    # images:Set[ImageOnRam]=set() #https://github.com/samuelcolvin/pydantic/issues/1090

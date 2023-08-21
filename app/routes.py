from fastapi import Path, Query, Body #data type validators
from fastapi import File, UploadFile, Form
from fastapi import status
from fastapi import HTTPException
from typing  import List

from .       import api
from .enums  import PredefinedName
from .models import UserOnRAM, OrderOnRAM, ImageOnRam

@api.get("/")
async def get_root():
    return {"Hello": "World"}

# Order matters
# =============
@api.get("/hello/me", status_code=200)
# @api.get("/hello/me", status_code=status.HTTP_200_OK)
async def get_hello_me():
    return {"Hello": "TO ME!!!, silly ..."}

# Query Parameters
# ================
# When you declare other function parameters that are not part of the route
# they are interpreted as "query" parameters.
@api.get("/hello/{name}")
async def get_hello(
        name:str=Path(..., min_length=3, max_length=20), #required because of ...
        age:int=Query(None, gt=18), #optional because of None
        nationality:str=None #optional because of None
    ):
    #curl 'localhost:5000/hello/javier'
    #curl 'localhost:5000/hello/javier?age=19'
    #curl 'localhost:5000/hello/javier?age=19&nationality=universal'
    msg = name.capitalize()

    if name.lower() == "john":
        raise HTTPException(status_code=406, detail="Invalid name: {}".format(name))

    if age:
        msg = "{} you are {} years old".format(msg, age)
    if nationality:
        msg = "{} and {}, you must be proud!".format(msg, nationality)
    return {"Hello": msg}

# Predefined values
# =================
# If you have a path operation that receives a path parameter, but you want the
# possible valid path parameter values to be predefined, you can use a standard
# Python Enum.
@api.get("/bye/{name}")
async def get_named_bye(name:PredefinedName):
    msg = name.capitalize()
    if name == PredefinedName.opt_1:
        msg = name.capitalize()+ "!, what a wonderful name!"
    if name.value == "javier":
        msg = name.capitalize()+ "!, how did you get in the middle?"

    return {"Bye": msg}

# Parameters containing dashes "/" (paths)
# ========================================
@api.get("/file/{file_path:path}")
async def get_file(file_path:str):
    return {"file_path": "/{}".format(file_path)}

# Post methods
# ============
@api.post("/user/create")
# curl -H "Content-Type: application/json" -d '{"username":"xyz","password":"xyz"}' localhost:5000/user/create
async def post_user(user:UserOnRAM):
    return user

@api.post("/user/create/embed/body") #stardarize with other complex endpoints
# curl -H "Content-Type: application/json" -d '{"user":{"username":"xyz","password":"xyz"}}' localhost:5000/user/create/embed/body
async def post_user(user:UserOnRAM=Body(..., embed=True)):
    return {"user":user}

@api.post("/user/add/images") #such as this one
# curl -H "Content-Type: application/json" \
#   -d '{"user":{"username":"xyz","password":"xyz"},
#        "images":[
#          {"url":"http://javier.io", "description":"foobar"},
#          {"url":"https://javier.io", "description":"lalala"}
#       ]}' \
#   localhost:5000/user/add/images
async def post_user_order(user:UserOnRAM, images: List[ImageOnRam]):
    return {"user":user, "images":images}

@api.post("/user/add/order") #or this one
# curl -H "Content-Type: application/json" \
#   -d '{"user":{"username":"xyz","password":"xyz"}, "order":{"id":123, "amount":3}, "importance":100}' \
#   localhost:5000/user/add/order

# curl -H "Content-Type: application/json" \
#   -d '{"user":{"username":"xyz","password":"xyz"},
#        "order":{"id":123, "amount":3, "images":[
#          {"url":"http://javier.io", "description":"foobar"},
#          {"url":"https://javier.io", "description":"lalala"}
#       ]}, "importance":100}' \
#   localhost:5000/user/add/order
async def post_user_order(user:UserOnRAM, order:OrderOnRAM, importance:int=Body(..., gt=10)):
    return {"user":user, "order":order, "importance":importance}

# Upload Files
# ============
@api.post("/upload/small_file")
# curl -H "Content-Type: multipart/form-data" -F "file=@small_file.txt" localhost:5000/upload/small_file
async def upload_small_file(file:bytes=File(...)):
    #a file defined as 'bytes' save its content in memory which limits its size
    return {"file_size": len(file)}

@api.post("/upload/file")
# curl -H "Content-Type: multipart/form-data" -F "file=@file.txt" localhost:5000/upload/file
async def upload_file(file:UploadFile=File(...)):
    # a file defined as 'UploadFile' would be handled automatically by fastapi,
    # saving to hd when required
    contents = await file.read()
    print(contents)
    #await is required since upload_file is defined as async
    return {"filename": file.filename}

@api.post("/upload/small_files")
# curl -H "Content-Type: multipart/form-data" \
# -F "files=@small_file.txt" -F "files=@another_small_file.txt" localhost:5000/upload/small_files
async def upload_small_files(files:List[bytes]=File(...)):
    return {"file_sizes": [len(file) for file in files]}

@api.post("/upload/files")
# curl -H "Content-Type: multipart/form-data" \
# -F "files=@file.txt" -F "files=@another_file.txt" localhost:5000/upload/files
async def upload_files(files:List[UploadFile]=File(...)):
    return {"filenames": [file.filename for file in files]}

# Upload Files with Auth
# ======================
@api.post("/auth/upload/file")
# curl -H "Content-Type: multipart/form-data" \
# -F "file=@file.txt" -F "api:secr4t" localhost:5000/auth/upload/file
async def auth_upload_file(api:str=Form(...), file:UploadFile=File(...)):
    return {
        "api": api,
        "filename": file.filename
    }

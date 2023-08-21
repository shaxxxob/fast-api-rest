from fastapi import FastAPI
# from config import Config

api = FastAPI()
# api.config.from_object(Config)

from app import routes

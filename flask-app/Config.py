import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    apiUsername = os.environ.get("API_USER_NAME") or "azsl-ict"
    apiPassword = os.environ.get("API_PASSWORD") or "dEKbrPY0GnBIorHhueA8xZi5mE3v64"

import os
from dotenv import load_dotenv

load_dotenv('.env')

class Config:
    SECRET_KEY ="364ryrywgw6&^%@^#&*#ufhrgberyt459560643878^#%@%^@&#URHVDN#Hy363" 
    SQLALCHEMY_DATABASE_URI = f"postgresql://myuser:12345@localhost/blogflask"


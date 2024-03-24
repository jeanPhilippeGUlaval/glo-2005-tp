import pymysql
import pymysql.cursors
import os
from dotenv import load_dotenv

load_dotenv(override=True)

conn = pymysql.connect(
        host= os.environ.get("HOST"),
        user= os.environ.get("USER"),
        password= os.environ.get("PASSWORD"),
        db= os.environ.get("DATABASE") )
cur = conn.cursor()
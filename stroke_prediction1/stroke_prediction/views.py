from django.http import HttpResponse
from django.shortcuts import render
import sqlalchemy as sa
import pymysql
import numpy as np
import pickle
import os
import warnings
warnings.filterwarnings('ignore')
import logging
logging.basicConfig(level=logging.WARN,
                    filename="logs/log.log",
                    filemode="a",
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

db_credentials = {
    'username': 'root',
    'password': 'Mysql2024',
    'host': 'localhost:3306',
    'database': 'world',
}

# MySQL database URL using the PyMySQL dialect
mysql_url = f"mysql+pymysql://{db_credentials['username']}:{db_credentials['password']}@{db_credentials['host']}/{db_credentials['database']}"

# Create a SQLAlchemy engine
income_db = sa.create_engine(mysql_url)

with open("mlruns/0/e983ae2af8cd40e4be6869826e03db2b/artifacts/LogisticRegression/model.pkl","rb") as f:
    model = pickle.load(f)

def home(request):
    try:
        prediction = 0
        if request.method == "POST":
            gender = request.POST.get("gender")
            married = request.POST.get("married")
            work = request.POST.get("work")
            residence = request.POST.get("residence")
            smoking = request.POST.get("smoking")
            age = float(request.POST.get("age"))
            bmi = float(request.POST.get("bmi"))

            trans = model.transform(gender,age,0,0,married,work,residence,0,bmi,smoking)

            prediction = model.predict(np.array[trans])
            prediction = prediction[0]
    
    except Exception as e:
        prediction =str(e)
        logging.warning(prediction)
           
    return render(request, 'stroke.html',{"stroke":smoking})
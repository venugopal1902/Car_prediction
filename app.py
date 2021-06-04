from pywebio.platform.flask import webio_view
from pywebio import STATIC_PATH
from flask import Flask, send_from_directory
from pywebio.input import *
from pywebio.output import *
import argparse
from pywebio import start_server

import pickle
import numpy as np
model = pickle.load(open('regression_rf.pkl', 'rb'))
app = Flask(__name__)


def predict():
    Year = input("Enter the Model Year：", type=NUMBER)
    Number_Of_Years = 2021 - Year
    Selling_Price = input('Enter the sellingprice(in lakhs)',type=FLOAT)
    Kms_Driven = input("Enter the distance it has travelled(in KMS)：", type=FLOAT)
   
    Owner = input("Enter the number of owners who have previously owned it(0 or 1 or 2 or 3)", type=NUMBER)
    Fuel_Type = select('What is the Fuel Type', ['Petrol', 'Diesel','CNG'])
    if (Fuel_Type == 'Petrol'):
        Fuel_Type_Diesel =0
        Fuel_Type_Petrol =1

    elif (Fuel_Type == 'Diesel'):
        Fuel_Type_Diesel =1
        Fuel_Type_Petrol = 0
    else:
        Fuel_Type_Diesel =0
        Fuel_Type_Petrol =0
   
    Transmission = select('Transmission Type', ['Manual Car', 'Automatic Car'])
    if (Transmission == 'Manual Car'):
        Transmission_Manual = 1
    else:
        Transmission_Manual =0

    prediction = model.predict([[Selling_Price, Kms_Driven, Fuel_Type_Diesel,Fuel_Type_Petrol,Transmission_Manual, Owner,Number_Of_Years]])
    output = prediction

    if output == 1:
        put_text("Individual",output)

    else:
        put_text('Dealer',output)

app.add_url_rule('/tool', 'webio_view', webio_view(predict),
            methods=['GET', 'POST', 'OPTIONS'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    args = parser.parse_args()

    start_server(predict, port=args.port)
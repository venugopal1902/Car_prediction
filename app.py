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
   Year = input("Enter the Year in which year you have bought car：", type=NUMBER,name=f's{1}')
    
    Present_Price = input("Enter the Present Price(in LAKHS)", type=FLOAT,name=f's{2}')
    Kms_Driven = input("Enter the distance it has travelled(in KMS)：", type=FLOAT,name=f's{3}')
    
    Owner = input("Enter the number of owners who have previously owned it", type=NUMBER,name=f's{4}')
    Fuel_Type = select('What is the Fuel Type', ['Petrol', 'Diesel','CNG'],name=f's{5}')
    
 
    Seller_Type = select('Are you a dealer or an individual', ['Dealer', 'Individual'],name=f's{6}')
    Transmission = select('Transmission Type', ['Manual Car', 'Automatic Car'],name=f's{7}')
    d = [Present_Price, Kms_Driven, Fuel_Type, Seller_Type, Transmission, Owner, Year]
    d = input_group('basic info',d) 
    print(d)
    d= list(d.values())
    print(d)
    d[6] = 2021-d[6]
    if (d[2] == 'Petrol'):
        d[2] = 2

    elif (d[2] == 'Diesel'):
        d[2] = 1

    else:
        d[2] = 3
    
    if (d[3] == 'Individual'):
        d[3] = 1

    else:
        d[3] = 0
    
    if (d[4] == 'Manual Car'):
        d[4] = 0
    else:
        d[4] = 1

    prediction = model.predict([d])
    output = round(prediction[0], 2)

    if output < 0:
        put_text("<h2>Sorry You can't sell this Car</h2>")

    else:
        put_html(f'<h2>You can sell this Car at price(inlakhs): {output}</h2>')
                 
                
                
    put_html('<a href="/" style="background-color:blue;margin-left:350px;color:white;;padding :8px;border-radius:5px;font-size:30px;text-decoration:none;box-shadow:0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)">Home</a>')
      




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    args = parser.parse_args()

    start_server(predict, port=args.port)
#if __name__ == '__main__':
    #predict()

#app.run(host='localhost', port=80)

#visit http://localhost/tool to open the PyWebIO application.

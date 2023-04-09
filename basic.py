from flask import Flask, request, render_template, url_for
import numpy as np
import pickle
import pandas as pd
import xgboost
from xgboost import XGBRegressor
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

model = pickle.load(open('test20xgminmax.pkl', 'rb'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pred', methods=['POST'])
def submit():
    print(request.form)
    battingteam = request.form['bat']
    bowlingteam = request.form['bowl']
    city = request.form['city']
    score = request.form['Present score']
    score=int(score)
    overs = request.form['Overs completed']
    overs=int(overs)
    wickets = request.form['Wickets fallen']
    wickets=int(wickets)
    nob=request.form['No. of Batsmen/Allrounders left']
    nob=int(nob)
    runs=request.form['Runs scored in last 5 overs']
    runs=int(runs)

    balls_left = 120 - (overs*6)
    wickets_left = 10 -wickets
    crr = score/overs

    input_df = pd.DataFrame(
     {'batting_team': [battingteam], 'bowling_team': [bowlingteam],'city':[city], 'current_score': [score],'balls_left': [balls_left], 'wickets_left': [wickets_left], 'batsman_left':[nob], 'crr': [crr], 'last_five': [runs]})
    result = model.predict(input_df)
    print(result[0])
    res1=int(crr*20)

    return render_template('results.html', res1=res1, res2=str(int(result[0])))

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    message = request.form['message']

    # Set up the email message
    msg = EmailMessage()
    msg['Subject'] = 'New Contact Form Submission'
    msg['From'] = 'razhagarrix@gmail.com' # Replace with your email address
    msg['To'] = 'sruthi.19.cse@anits.edu.in' # Replace with the recipient's email address
    msg.set_content(f"""
        New contact form submission:
        Name: {name}
        Phone: {phone}
        Email: {email}
        Message: {message}
    """)

    # Send the email using SMTP
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login('razhagarrix@gmail.com', 'evisiuabbunyyxhe') # Replace with your email and password
        smtp.send_message(msg)

    return render_template('thanks.html', name=name)
    
if __name__ == '__main__':
    app.run(debug=True)


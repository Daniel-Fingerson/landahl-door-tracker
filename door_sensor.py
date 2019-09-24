#NEED TO ADD PROBABLY A CRON FILE TO UPDATE PAGE EVERY 10 SECONDS
#needs to have a door switch to tell if open or closed, update that to website, AND blink in room for 10 min
from flask import Flask, request, render_template
import RPi.GPIO as GPIO
import time
import datetime
import random
GPIO.setmode(GPIO.BCM)
GPIO.setup(21,GPIO.OUT)
GPIO.output(21,0)
GPIO.setup(20,GPIO.IN,pull_up_down = GPIO.PUD_UP) #pull up resistor, so attatch to 20 then ground
#this means the button will normally be set to high
#nevertheless I may need to change this

app=Flask(__name__)
#get rid of post method, just have it constantly reupdate itself to reflow (use same concpet as the update page
'''
@app.route("/")
def input_handle():
    if(GPIO.input(20) == 0):
        GPIO.ouput(21,1)
    return render_template("input_handle.html")
'''

@app.route("/input_dashboard/input_handle")
#maybe could add the ability to show door status, display if there are any recent requests
def input_handle():
    return render_template("input_handle.html")

@app.route('/input_dashboard/input_handle', methods=['POST'])
def input_handle_post():
    global current_minute, time_needed
    currentDT = datetime.datetime.now()
    current_minute=currentDT.minute
    time_needed=request.form['time_needed']
    name = request.form['name']
    conn=sqlite3.connect('/home/pi/Desktop/door_app/LEDstate.db')
    curs=conn.cursor()
    curs.execute("""INSERT INTO LEDstate values((?), (?), (?))""", (current_minute, time_needed, more)) #problem most likely here: check the log
    conn.commit()
    conn.close()
    #send text message here
    return render_template('output_handle.html', value=ID, first=text, second=more)

def background_check():
    #had database so that it could check values, but with what I have with global variables right now this might not be necessary
    while True:
        currentDT = datetime.datetime.now()
        time_now=currentDT.minute
        time_req=time_now-current_minute
        if time_req<=0:
            time_req+=60
        if time_req>=time_needed:
            GPIO.ouput(21,1)
            time.sleep(1)
            GPIO.ouput(21,0)
            time.sleep(1)
        else:
            GPIO.ouput(21,0)
        #time now 26; time then 20; need 12 min of tiem
        

if __name__ == "__main__":
    app.run(debug=True, port=8005)
#have a threading function that will actually turn the LED on or off by checking the database; call thread direclty above/bewlow the app.run



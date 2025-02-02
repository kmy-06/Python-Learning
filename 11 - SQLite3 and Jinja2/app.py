import os
import convert_utils
import data_utils

# import swimclub: switch to using jinja2 templates

from flask import Flask, session, render_template, request # 'Session' is a server-side dictionary, use it to 'shared globally'. + Jinja2 built-in technology for Flask

app = Flask(__name__)
app.secret_key = "You will never guess..."

@app.get('/') # Function associated with this decorator must conclude with a return statement
def index():
    return render_template( # Flask's 'render_template' function + No need to include "template/" before index.html, as Flask includes it by default
        "index.html", 
        title="Welcome to Swimclub", # The 'trailing comma' at the end is a good practice of the Python community
    ) 

# session variable is in the 'data' that is 'get' from the database. See below ↓ (control + command + space: For the arrow)

@app.get("/swims")
def display_swim_sessions():
    data = data_utils.get_swim_sessions()
    dates = [session[0].split(" ")[0] for session in data] # SQLite3 returns a tuple of one element, so we need to split it, and get the first element
    return render_template(
        "select.html", # Template used
        title="Select a swim session",
        url="/swimmers",
        select_id="chosen_date", # Name tag for <select> in select.html. Basically, it is the name of the answer returned for next uses
        data=dates,
    )

@app.post('/swimmers') # '/swimmers' URL runs the display_swimmers function  
def display_swimmers(): # Funtion in flask can run any python code but must have a return statement for a textual responsec
    session["chosen_date"] = request.form["chosen_date"] # Store the form value (select_id="chosen_date", above) in a variable called 'chosen_date'
    data = data_utils.get_session_swimmers(session["chosen_date"]) # Get the swimmers for the chosen date in the variable 'session' in data.
    swimmers = [f"{swimmer[0]}-{swimmer[1]}" for swimmer in data] # List comprehension to create a list of swimmers' name and their ages

    return render_template(
        "select.html",
        title="Select a swimmer",
        url="/showevents", # No more /showfiles b/c it is not clear enough
        select_id="swimmer",
        data=sorted(swimmers),
    )

@app.post("/showevents")
def display_swimmer_events():
    session["swimmer"], session["age"] = request.form["swimmer"].split("-") # Store the form value (select_id="swimmer", above) in a variable called 'swimmer'
    data = data_utils.get_swimmers_events(session["swimmer"], session["age"], session["chosen_date"]) # Get the events for the chosen swimmer in the variable 'session' in data.
    events = [f"{event[0]} {event[1]}" for event in data]

    return render_template(
        "select.html", 
        title="Select an event",
        url="/showbarchart",
        select_id="event", 
        data=events, 
    )

@app.post("/showbarchart")
def show_bar_chart(): # Instead of using raw HTML with SVG, we now use Jinja2 with SVG
    distance, stroke = request.form["event"].split(" ")
    data = data_utils.get_swimmers_times(session["swimmer"], session["age"], distance, stroke, session["chosen_date"])
    times = [time[0] for time in data]
    average_str, times_reversed, scaled = convert_utils.perform_conversions(times) # All the original goodness in swimclub.py is now in convert_utils.py
    world_records = convert_utils.get_worlds(distance, stroke)
    header = f"{session['swimmer']} (Under {session['age']}) {distance} {stroke} - {session['chosen_date']}"

    return render_template(
        "chart.html",
        title=header,
        data=list(zip(times_reversed, scaled)),
        average=average_str,
        worlds=world_records,
    )
    


if __name__ == '__main__':
    app.run(debug=True)
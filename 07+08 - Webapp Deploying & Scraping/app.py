import os
import swimclub
from flask import Flask, session, render_template, request # 'Session' is a server-side dictionary, use it to 'shared globally'. + Jinja2 built-in technology for Flask

app = Flask(__name__)
app.secret_key = "You will never guess..."

@app.get('/') # Function associated with this decorator must conclude with a return statement
def index():
    return render_template( # Flask's 'render_template' function + No need to include "template/" before index.html, as Flask includes it by default
        "index.html", 
        title="Welcome to Swimclub", # The 'trailing comma' at the end is a good practice of the Python community
    ) 

# Not part of the above decorator. It is a separate function
def populate_data(): # Function does not return anything, no need 'return'
    if "swimmers" not in session:
        swim_files = os.listdir(swimclub.FOLDER)
        swim_files.remove(".DS_Store")
        session["swimmers"] = {}

        for file in swim_files:
            name, *_ = swimclub.read_swim_data(file)

            if name not in session["swimmers"]:
                session["swimmers"][name] = []

            session["swimmers"][name].append(file) 


@app.get('/swimmers') # '/swimmers' URL runs the display_swimmers function  
def display_swimmers(): # Funtion in flask can run any python code but must have a return statement for a textual responsec
    populate_data() # 'Populate_data' available anywhere

    # return str(sorted(session["swimmers"])) # str turns the sorted list of keys of the dictionary into a string, 

    return render_template(
        "select.html",
        title="Select a swimmer",
        url="/showfiles",
        select_id="swimmer",
        data=sorted(session["swimmers"]),
    )

@app.post("/showfiles")
def display_swimmer_files():

    populate_data()

    name = request.form["swimmer"] 
    # Grab the selected swimmer's name from the form

    return render_template(
        "select.html", # Template used
        title="Select an event",
        url="/showbarchart",
        select_id="file", # Name tag for <select> in select.html
        data=session["swimmers"][name], # List of filenames
    )

@app.post("/showbarchart")
def show_bar_chart():
    file_id = request.form["file"] # Store the form value (select_id="file", above) in a variable called 'file_id'
    location = swimclub.produce_bar_chart(file_id, "templates/") # Stores the bar-chart produced in a variable called 'location' in the 'templates' folder
    return render_template(location.split("/")[-1]) # Render_template is a Flask function from the "templates" folder, after removing the "/" prefix


if __name__ == '__main__':
    app.run(debug=True)
"""To create a web app, proceed with the followings
1. Create webapp folder
2. Create app.py, templates folder, static folder(not utilized) inside webapp folder
3. copy swimclub.py, hfpy_utils.py
4. install flask () : %pip install flask --upgrade #***[for development server only, NOT for production]***
5. install jinja2 extension : pip install Jinja2 
6. Create base.html, index.html, selectswimmer.html, selectswimmersevent.html inside templares folder
7. Modify swimclub - produceBarChart method 
8. VS Code menu : Run > Start Debugging > Hit in Browser : http://127.0.0.1:5000 
"""

#Import all the required modules
from flask import Flask, render_template, session, request
import os
import swimclub

#Initialize Flask object to create the very webapp 
app=Flask(__name__)
app.secret_key = "Try something hard..."

#Create session["swimmers"] to access swimmers name and filename in a dictionary format from any method
def populateSwimmersData():
    #create only for not exists case
    if "swimmers" not in session:
       
        #get files
        swimFiles = os.listdir(swimclub.FOLDER)
        swimFiles.remove(".DS_Store")

        #initialize session["swimmers"] dictionary
        session["swimmers"] = {}

        #populate swimmers data (key - swimmer name, value  - file name)
        for file in swimFiles:
            SwimmerName = file.split("-")[0]
            if SwimmerName not in session["swimmers"] :
                session["swimmers"][SwimmerName] = []
            session["swimmers"][SwimmerName].append(file)  
        


#app decorator @, determines which URL(s) is going to call which server method defined just below it 

#index.html
@app.get("/")
def index():
    return render_template("index.html",
                           title= "Swimclub System")

#URL - /swiimers >>> selectswimmer.html - to display  swimmer name list 
@app.get("/swimmers")
def displaySwimmers():
    populateSwimmersData()
    return render_template("select.html",
                           title="Select a swimmer",
                           url="/showfiles",
                           select_name="Swimmer",
                           select_id="Swimmer",
                           select_title = "a swimmer",
                           datatype="swimmer",
                           data=sorted(session["swimmers"]))
  
#URL - /showfiles >>> selectswimmersevent.html - to display  selected swimmer's file list
@app.post("/showfiles")
def displaySwimmerFiles():
    populateSwimmersData()
    swimmerName=request.form["Swimmer"]
   
    return render_template("select.html",
                        title="Select an  event",
                        url="/showbarchart",
                        select_name="file",
                        select_id="file",
                        select_title = f"an event for {swimmerName}" ,
                        datatype="event",
                        data=session["swimmers"][swimmerName])

#URL - /showbarchart >>> templates/ to display selected swimmer's file's bar chart 
@app.post("/showbarchart")
def showBarChart():
    populateSwimmersData()
    fileName=request.form["file"]
    location = swimclub.produceBarChart(fileName,"templates/")
    return  render_template(location.split("/")[-1])

#run the very webapp
if __name__ == "_main_":
    app.run()

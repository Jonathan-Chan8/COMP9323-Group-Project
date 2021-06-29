"""
#Flask Server

 - Takes HTTP requests (GET, POST, ...) and returns a response to the client
 

"""

# Imports

from flask import Flask, redirect, url_for, render_template


#----------------------------------------------------------------------------#


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


#----------------------------------------------------------------------------#

if __name__ == "__main__":
    app.run(debug = True)
    
    
    



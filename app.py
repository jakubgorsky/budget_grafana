from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route("/")
def home():
        return render_template("index.html")

@app.route("/about")
def about():
        return "This will be the about section"

if __name__ == "__main__":
        app.run(host="0.0.0.0")
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
        return "Flask app test"

@app.route("/about")
def about():
        return "This will be the about section"

if __name__ == "__main__":
        app.run()
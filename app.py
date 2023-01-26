from flask import Flask, redirect, url_for, render_template
from db_ops import get_hw_info_list, get_pkg_data_dict

app = Flask(__name__)

@app.route("/")
def home():
        hwinfo = get_hw_info_list()
        pkg_info = get_pkg_data_dict()
        return render_template("index.html", hwinfo=hwinfo, pkg_info=pkg_info)

@app.route("/about")
def about():
        return "This will be the about section"

if __name__ == "__main__":
        app.run(host="0.0.0.0")
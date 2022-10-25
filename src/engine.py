from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import requests
import json
from src import main

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    with app.app_context():
        token = main.Token
        address = request.form.get("password")
        if request.method == "POST":
            if main.data_exists(address) == True:
                token = main.getData(address)
            else:
                token = main.inf(address)
                main.add(address)
        return render_template("index.html",
        information_mint1 = str(token.information_mint),
        information_standard1 = str(token.information_standard),
        information_name1 = str(token.information_name),
        information_symbol1 = str(token.information_symbol),
        information_metaplex1 = str(token.information_metaplex))

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port=8080)
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import requests
import json
from sqlalchemy.sql import func

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres:postgres@localhost:5432/python"
db.init_app(app)


class Token(db.Model):
    information_mint = db.Column(db.String, primary_key=True)
    information_standard = db.Column(db.String)
    information_name = db.Column(db.String)
    information_symbol = db.Column(db.String)
    information_metaplex = db.Column(db.String)

    def __init__(self, mint, standard, name, symbol, metaplex):
        self.information_mint = mint
        self.information_standard = standard
        self.information_name = name
        self.information_symbol = symbol
        self.information_metaplex = metaplex


with app.app_context():
    db.create_all()


def inf(address):
    url = "https://solana-gateway.moralis.io/nft/mainnet/" + address + "/metadata"
    headers = {
        "accept": "application/json",
        "X-API-Key": "2WRIIHAZ8k7xBJzjSRd4150iGSCfKacCq1IrlMq8yo20RQtIvsTXV8oktMtESy9F"
    }
    response = requests.get(url, headers=headers)
    txt = response.json()
    tokenn = Token(txt.get("mint"), txt.get("standard"), txt.get("name"), txt.get("symbol"), str(txt.get("metaplex")))
    return (tokenn)

def add(address):
    with app.app_context():
        db.session.add(inf(address))
        db.session.commit()

def data_exists(address):
    with app.app_context():
        exists = db.session.query(db.exists().where(Token.information_mint == inf(address).information_mint)).scalar()
        return(exists)

    #7oYGNrN2TxaS1qPx2A6Tt4oQ7ripFwGkoE375WTim5bE

def getData(address):
    information_mint = Token.information_mint
    with app.app_context():
        info = db.get_or_404(Token, address)
        token = Token(info.information_mint, info.information_name, info.information_standard, info.information_symbol, info.information_metaplex)
        return token

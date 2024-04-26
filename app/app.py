import os
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return "HELLOffffffff"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
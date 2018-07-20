from flask import Flask
from flask import request
from generate import *
import json

app = Flask(__name__)

@app.route('/')
def sna():
    lst = request.args.get('lst')
    ret = json.dumps(generate(lst))
    return ret

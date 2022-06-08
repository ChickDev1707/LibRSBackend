from flask import Flask, request
from flask_cors import CORS, cross_origin
from model import get_recommendation

import json

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# api
@app.get('/')
def index():
  return "hello world"

@app.post('/')
def chatbot(): 
  isbn = request.form["isbn"]
  result = {
    "books": get_recommendation(isbn)
  }
  return json.dumps(result, ensure_ascii=False).encode("utf8")
   
if __name__ == '__main__':
  app.run(debug=True)
from flask import Flask
from flask import request


app = Flask(__name__)

@app.route('/text', methods=['POST'])
def parse_request():
    
    json = request.json
    print('json: ', json)
    return "Response: That worked!!!"

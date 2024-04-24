
# A very simple Flask Hello World app for you to get started with...
from flask import Flask, jsonify, request
from CVmatch import CVmatching
# use args to get the path of the cv and the jd

app = Flask(__name__)

expected_api_key = 'this is secure do not try'

@app.route('/cvmatch', methods=['POST','GET'])
def cvmatch():
    # Extract API key from request headers
    authorization_header = request.headers.get('Authorization')
    if authorization_header!= f'Bearer {expected_api_key}':
        return jsonify({'message': 'Unauthorized access. Invalid API key.'}), 401

    request_data = request.json
    resume_path = request_data.get('resumePath')
    jd = request_data.get('jd')

    import requests
    response = requests.get(resume_path)
    pdf_data = response.content

    # To get the pdf and jd from disk

    # jd=""
    # with open('/home/Inteliview/mysite/jd.txt', 'r') as f:
    #     jd = f.read()
    # with open('/home/Inteliview/mysite/senior.pdf', 'rb') as f:
    #     pdf_data = f.read()

    res = CVmatching(jd,pdf_data)
    return str(res)

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'running'})

if __name__ == '__main__':
    app.run(debug=True)


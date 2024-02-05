from flask import Flask, render_template, request, redirect, url_for, jsonify
from CVmatch import CVmatching
from interviewAnswerEvaluating import getAnswerSimilarity,load_model
# use args to get the path of the cv and the jd

app = Flask(__name__)

model = load_model()

@app.route('/cvmatch', methods=['GET'])
def cvmatch():
    jd=""
    with open('jd.txt', 'r') as f:
        jd = f.read()
    res = CVmatching(jd,'senior.pdf')
    return jsonify({'status': 200 , 'CV similarity': res})

@app.route('/answerEvaluating', methods=['GET'])
def answerEvaluating():
    res = getAnswerSimilarity('','',model)
    return jsonify({'status': 200 , 'answer similarity': res})

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'running'})

if __name__ == '__main__':
    app.run(debug=True)

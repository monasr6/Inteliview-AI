from flask import Flask, jsonify, request
from textAnalys import textAnalysis, video_to_text

app = Flask(__name__)

expected_api_key = 'this is secure donot try'

@app.route('/api/textAnalysis', methods=['POST'])
def text_analysis():
    api_key = request.headers.get('Authorization')
    if api_key != "Bearer " + expected_api_key:
        return jsonify({'error': 'Invalid API key'}), 401
    
    request_data = request.json
    videolink = request_data.get('videolink')
    import requests
    response = requests.get(videolink)

    if response.status_code == 200:
    # Open a new file in write-binary mode and save the response content to it
        with open('output.mp4', 'wb') as f:
            f.write(response.content)
    
    text = video_to_text('output.mp4')
    text_analysis_result = textAnalysis(text)
    return jsonify({'text': text , 'text_analysis': text_analysis_result})

@app.route('/test', methods=['GET'])
def index():
    return jsonify({'message': 'running'})

if __name__ == '__main__':
    app.run(debug=True)
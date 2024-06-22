import speech_recognition as sr
from pydub import AudioSegment
from google.cloud import language_v1

def analyze_sentiment(text):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={'document': document})
    sentiment = response.document_sentiment
    return sentiment.score, sentiment.magnitude

def textAnalysis(text):
    # text = "I love using the Google Cloud Natural Language API. It's very effective!"
    score, magnitude = analyze_sentiment(text)
    score = round(score, 2)
    return score

# def extract_audio(video_path, audio_path):
#     command = f'ffmpeg -i "{video_path}" -q:a 0 -map a "{audio_path}" -y > /dev/null 2>&1'
#     subprocess.run(command, shell=True)

def extract_audio(video_path, audio_path):
    audio = AudioSegment.from_file(video_path)
    audio.export(audio_path, format='wav')

def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
    return text

def video_to_text(video_path):
  video_path = 'output.mp4'
  audio_path = 'output_audio.wav'
  extract_audio(video_path, audio_path)

  transcription = transcribe_audio(audio_path)
  
  return transcription

from requests import get

response = get('https://res.cloudinary.com/djvcgnkbn/video/upload/v1714607883/0001 %281%29.mp4')

# Check if the request was successful
if response.status_code == 200:
    # Open a new file in write-binary mode and save the response content to it
    with open('output.mp4', 'wb') as f:
        f.write(response.content)
        
from moviepy.editor import VideoFileClip

video = VideoFileClip('output.mp4')
audio = video.audio
audio.write_audiofile('audio.mp3')
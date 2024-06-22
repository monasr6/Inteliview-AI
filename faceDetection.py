from tensorflow.keras.models import load_model
import cv2
import numpy as np

PADDING = 40
def pad(image):
        """Pad image."""
        row, col = image.shape[:2]
        bottom = image[row - 2 : row, 0:col]
        mean = cv2.mean(bottom)[0]

        padded_image = cv2.copyMakeBorder(
            image,
            top=PADDING,
            bottom=PADDING,
            left=PADDING,
            right=PADDING,
            borderType=cv2.BORDER_CONSTANT,
            value=[mean, mean, mean],
        )
        return padded_image

def tosquare(bbox):
        x, y, w, h = bbox
        if h > w:
            diff = h - w
            x -= diff // 2
            w += diff
        elif w > h:
            diff = w - h
            y -= diff // 2
            h += diff
        if w != h:
            print(f"{w} is not {h}")
        return (x, y, w, h)

def apply_offsets(face_coordinates):
        x, y, width, height = face_coordinates
        x_off, y_off = (10,10)
        x1 = x - x_off
        x2 = x + width + x_off
        y1 = y - y_off
        y2 = y + height + y_off
        return x1, x2, y1, y2

def preprocess_input(x, v2=False):
        x = x.astype("float32")
        x = x / 255.0
        if v2:
            x = x - 0.5
            x = x * 2.0
        return x


def generateVideoFeatures(path):
    emotion_classifier = load_model("/home/Inteliview/mysite/emotion_model.hdf5", compile=False)
    emotion_classifier.make_predict_function()
    emotion_target_size = emotion_classifier.input_shape[1:3]

    cascade_file = "/home/Inteliview/mysite/haarcascade_frontalface_default.xml"
    face_detector = cv2.CascadeClassifier(cascade_file)

    emotion_labels = {
                0: "angry",
                1: "disgust",
                2: "fear",
                3: "happy",
                4: "sad",
                5: "surprise",
                6: "neutral",
            }

    success = 1
    vidObj = cv2.VideoCapture(path)
    fps = vidObj.get(cv2.CAP_PROP_FPS)
    cnt = 0
    emotions = {}
    #cv2.namedWindow('emotion', cv2.WINDOW_NORMAL)
    while vidObj.isOpened():

        success, image = vidObj.read()
        if success:
            try:
                image = cv2.resize(image ,(640 , 360) , interpolation=cv2.INTER_LANCZOS4)
            except:
                continue

            facest = []
            gray_image_array = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


            facest =face_detector.detectMultiScale(
                            gray_image_array,
                            scaleFactor=1.1,
                            minNeighbors = 5,
                            flags=cv2.CASCADE_SCALE_IMAGE,
                            minSize=(100,90), # 640*360
                        )
            faces=None
            for fc in facest:
                if len(fc) == 4:
                    faces = [facest[0]]
                    break
                else:
                    faces = facest
                    break


            #image = cv2.circle(image, (faces[0] [0],faces[0] [1]), radius=50, color=(0, 0, 255), thickness=10)
            #image = cv2.circle(image, (faces[0] [0] + faces[0] [2],faces[0] [1] + faces[0] [3]), radius=50, color=(0, 0, 255), thickness=10)
            #cv2.imshow("emotion",image)
            #cv2.waitKey(500)

            gray_image_array = pad(gray_image_array)
            gray_faces = []

            if faces is not None:
                for face_coordinates in faces:
                    face_coordinates = tosquare(face_coordinates)
                    x1, x2, y1, y2 = apply_offsets(face_coordinates)

                    x1 += PADDING
                    y1 += PADDING
                    x2 += PADDING
                    y2 += PADDING
                    x1 = np.clip(x1, a_min=0, a_max=None)
                    y1 = np.clip(y1, a_min=0, a_max=None)

                    gray_face = gray_image_array[max(0, y1) : y2, max(0, x1) : x2]

                    try:
                        gray_face = cv2.resize(gray_face, emotion_target_size)
                    except Exception as e:
                        print("{} resize failed: {}".format(gray_face.shape, e))
                        continue

                    gray_face = preprocess_input(gray_face, True)
                    gray_faces.append(gray_face)

            if not len(gray_faces):
                continue

            emotion_predictions = emotion_classifier(np.array(gray_faces))
            cnn = 0
            mx = 0
            for face_idx, face in enumerate(emotion_predictions):
                cnn+=1
                for idx, score in enumerate(face):
                    if score > mx:
                        mx = score
                        labelled_emotions = {}
                        labelled_emotions = {emotion_labels[idx]: round(float(score), 2)}

                if round( vidObj.get(cv2.CAP_PROP_POS_MSEC) /1000 , 2 ) not in emotions:
                    emotions[( round( vidObj.get(cv2.CAP_PROP_POS_MSEC) /1000 , 2 )  )] = {}
                emotions[( round( vidObj.get(cv2.CAP_PROP_POS_MSEC) /1000 , 2 )  ) ] = labelled_emotions
        else:
            break
        cnt += fps/3 # i.e. at 30 fps, this advances one second
        vidObj.set(cv2.CAP_PROP_POS_FRAMES, cnt)
    #cv2.destroyAllWindows()
    vidObj.release()
    return emotions
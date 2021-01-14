import cv2
import pafy

face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
ds_factor=0.6

class VideoCamera(object):
    def __init__(self):
        video_url = "https://www.youtube.com/watch?v=cCXB97tRouM"
        youtube_url = pafy.new(video_url)
        stream_url = youtube_url.getbest(preftype="mp4").url
        self.video = cv2.VideoCapture(stream_url)
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

import pafy
import cv2


url = "https://www.youtube.com/watch?v=T9Sy2t0nY1s"
video = pafy.new(url)
stream_url = video.getbest(preftype="mp4").url



#start the video
cap = cv2.VideoCapture(stream_url)
while (True):
    ret,frame = cap.read()
    """
    your code here
    """
    cv2.imshow('frame',frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

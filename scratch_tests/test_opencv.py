import pafy
import cv2
import os

url = "https://www.youtube.com/watch?v=bU18kgpO_Tc"
video = pafy.new(url)
stream_url = video.getbest(preftype="mp4").url



#start the video
cap = cv2.VideoCapture(stream_url)

retval, frame = cap.read()
f_height, f_width, _ = frame.shape

file_path = os.path.join("../data/logs/",'test.avi')

output_video = cv2.VideoWriter(file_path,
                               cv2.VideoWriter_fourcc(*'MJPG'),
                               30,
                               (f_width, f_height))

while (True):
    ret,frame = cap.read()
    """
    your code here
    """
    cv2.imshow('frame',frame)

    output_video.write(frame)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

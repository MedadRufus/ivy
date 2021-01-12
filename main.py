'''
VCS entry point.
'''

# pylint: disable=wrong-import-position

import sys
import cv2
import pafy
import argparse
from flask import Flask, render_template, Response


args = None


class YoutubeCamera:

    def __init__(self,argfile):
        '''
        Initialize object counter class and run counting loop.
        '''

        video_url = settings.YOUTUBE_URL
        youtube_url = pafy.new(video_url)
        stream_url = youtube_url.getbest(preftype="mp4").url

        self.cap = cv2.VideoCapture(stream_url)

        if not self.cap.isOpened():
            logger.error('Invalid video source %s', video_url, extra={
                'meta': {'label': 'INVALID_VIDEO_SOURCE'},
            })
            sys.exit()
        retval, self.frame = self.cap.read()
        f_height, f_width, _ = self.frame.shape
        detection_interval = settings.DI
        mcdf = settings.MCDF
        mctf = settings.MCTF
        detector = settings.DETECTOR
        tracker = settings.TRACKER
        use_droi = settings.USE_DROI
        # create detection region of interest polygon
        droi = settings.DROI \
                if use_droi \
                else [(0, 0), (f_width, 0), (f_width, f_height), (0, f_height)]
        show_droi = settings.SHOW_DROI
        counting_lines = settings.COUNTING_LINES
        show_counts = settings.SHOW_COUNTS
        hud_color = settings.HUD_COLOR

        self.object_counter = ObjectCounter(self.frame, detector, tracker, droi, show_droi, mcdf, mctf,
                                       detection_interval, counting_lines, show_counts, hud_color)


        logger.info('Processing started.', extra={
            'meta': {
                'label': 'START_PROCESS',
                'counter_config': {
                    'di': detection_interval,
                    'mcdf': mcdf,
                    'mctf': mctf,
                    'detector': detector,
                    'tracker': tracker,
                    'use_droi': use_droi,
                    'droi': droi,
                    'counting_lines': counting_lines,
                    "argfile": argfile

                },
            },
        })

        self.is_paused = False
        self.output_frame = None
        self.frames_count = round(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.frames_processed = 0

    def get_frame(self):
        _timer = cv2.getTickCount() # set timer to calculate processing frame rate

        success,image = self.cap.read()
        self.object_counter.count(image)
        output_frame = self.object_counter.visualize()
        ret, jpeg = cv2.imencode('.jpg', output_frame)

        processing_frame_rate = round(cv2.getTickFrequency() / (cv2.getTickCount() - _timer), 2)
        self.frames_processed += 1
        logger.info('Frame processed.', extra={
            'meta': {
                'label': 'FRAME_PROCESS',
                'frames_processed': self.frames_processed,
                'frame_rate': processing_frame_rate,
                'frames_left': self.frames_count - self.frames_processed,
                'percentage_processed': round((self.frames_processed / self.frames_count) * 100, 2),
            },
        })

        return jpeg.tobytes()

    def __del__(self):
        self.cap.release()

if __name__ == '__main__':
    from dotenv import load_dotenv
    from util.mongo_data_logger import init_mongo_logger

    parser = argparse.ArgumentParser()
    parser.add_argument('--env_file', required=True)
    args = parser.parse_args()
    print(f'Using argfile: {args.env_file}')

    load_dotenv(args.env_file)

    init_mongo_logger(args.env_file)
    import settings

    from util.logger import init_logger
    from util.logger import get_logger
    from ObjectCounter import ObjectCounter

    init_logger()
    logger = get_logger()




    app = Flask(__name__)


    @app.route('/')
    def index():
        return render_template('index.html')


    def gen(camera):
        while True:
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


    @app.route('/video_feed')
    def video_feed():
        return Response(gen(YoutubeCamera(args.env_file)),
                        mimetype='multipart/x-mixed-replace; boundary=frame')


    app.run(host='0.0.0.0', debug=True)

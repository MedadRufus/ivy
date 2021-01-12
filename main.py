'''
VCS entry point.
'''

# pylint: disable=wrong-import-position

import sys
import time
import cv2
import pafy
import os
import argparse
from flask import Flask, render_template, Response
from camera import VideoCamera


args = None





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
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


class YoutubeCamera:

    def __init__(self,argfile):
        '''
        Initialize object counter class and run counting loop.
        '''

        video_url = settings.YOUTUBE_URL
        youtube_url = pafy.new(video_url)
        stream_url = youtube_url.getbest(preftype="mp4").url

        cap = cv2.VideoCapture(stream_url)

        if not cap.isOpened():
            logger.error('Invalid video source %s', video_url, extra={
                'meta': {'label': 'INVALID_VIDEO_SOURCE'},
            })
            sys.exit()
        retval, frame = cap.read()
        f_height, f_width, _ = frame.shape
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

        object_counter = ObjectCounter(frame, detector, tracker, droi, show_droi, mcdf, mctf,
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


        is_paused = False
        output_frame = None
        frames_count = round(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frames_processed = 0

    def do_in_main_loop(self):
        try:
            counter = 0
            # main loop

            _timer = cv2.getTickCount() # set timer to calculate processing frame rate

            object_counter.count(frame)
            output_frame = object_counter.visualize()


            processing_frame_rate = round(cv2.getTickFrequency() / (cv2.getTickCount() - _timer), 2)
            frames_processed += 1
            logger.info('Frame processed.', extra={
                'meta': {
                    'label': 'FRAME_PROCESS',
                    'frames_processed': frames_processed,
                    'frame_rate': processing_frame_rate,
                    'frames_left': frames_count - frames_processed,
                    'percentage_processed': round((frames_processed / frames_count) * 100, 2),
                },
            })

        finally:
            # end capture, close window, close log file and video object if any
            cap.release()
            logger.info('Processing ended.', extra={
                'meta': {
                    'label': 'END_PROCESS',
                    'counts': object_counter.get_counts(),
                    'completed': frames_count - frames_processed == 0,
                },
            })


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
    from util.image import take_screenshot
    from util.logger import get_logger
    from util.debugger import mouse_callback
    from util.job import get_recording_id
    from ObjectCounter import ObjectCounter

    init_logger()
    logger = get_logger()



    YoutubeCamera(args.env_file)

    app.run(host='0.0.0.0', debug=True)

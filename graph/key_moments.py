import cv2
import numpy as np

from gdown import download as GoogleDriveDownload
from yt_dlp import YoutubeDL

threshold = 30  # difference threshold for key moment detection


class KeyMoments:

    @staticmethod
    def get_youtube_stream(url:str="https://www.youtube.com/watch?v=7o_fRK-66bY"):
        stream_url = None
        with YoutubeDL(dict()) as ydl:
            info = ydl.extract_info(url, download=False)
            stream_url = info['url']  # direct stream url
        return stream_url

    @staticmethod
    def get_google_drive_stream(url: str):
        stream_url = 'my_video.mp4'
        GoogleDriveDownload(url=url, output=stream_url, fuzzy=True)
        return stream_url

    @staticmethod
    def detect_key_moments():
        stream_url = KeyMoments.get_youtube_stream()

        # Open video stream with OpenCV
        capture = cv2.VideoCapture(stream_url)
        if capture.isOpened():
            prev_frame = None
            end, frame = capture.read()
            while not end:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                if prev_frame:
                    difference = cv2.absdiff(frame, prev_frame)
                    mean_diff = np.mean(difference)
                    







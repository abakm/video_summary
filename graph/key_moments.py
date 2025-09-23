import os
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
        print("STREAM URL: ", stream_url)

        # Open video stream with OpenCV
        capture = cv2.VideoCapture(stream_url)
        if capture.isOpened():
            print("OPened")
            prev_frame = None
            success, frame = capture.read()
            print("END: ", success)
            while success:
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                if prev_frame is not None:
                    difference = cv2.absdiff(gray_frame, prev_frame)
                    mean_diff = np.mean(difference)
                    if mean_diff > threshold:
                        frame_num = int(capture.get(cv2.CAP_PROP_POS_FRAMES))
                        cv2.imwrite(f"frame_{frame_num}.jpg", gray_frame)  # Save key frame as image
                        print(f"Saved key frame: frame_{frame_num}.jpg")
                        cv2.imshow("Key Moment Frame", frame)
                        if cv2.waitKey(0) & 0xFF == ord('q'):
                            break

                prev_frame = gray_frame
                success, frame = capture.read()

        else:
            print("couldn't open")

        capture.release()
        cv2.destroyAllWindows()


KeyMoments.detect_key_moments()







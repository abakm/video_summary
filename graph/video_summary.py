import cv2
import numpy as np
from yt_dlp import YoutubeDL

from graph import Video
from common import video_db

threshold = 30  # difference threshold for key moment detection


class VideoSummary:

    @staticmethod
    def get_youtube_stream(video: Video):
        """ This functionality is used to find the stream youtube_url corresponds to the youtube URL
        params: youtube_url: str
        returns stream_url:stream_url
         """
        stream_url = None
        with YoutubeDL({'extractor_retries': 1, '_ies': ['Youtube'], 'skip_download': True, 'quiet': True}) as ydl:
            info = ydl.extract_info(video['youtube_url'], download=False)
            stream_url = info['url']
        return dict(stream_url=stream_url)

    @staticmethod
    def scene_change_detection(video: Video):
        capture = cv2.VideoCapture(video['stream_url'])
        video_db.update_one({"_id": video['video_id']}, {"$push": {"progress": "scene change detection in progress"}})
        if capture.isOpened():
            print("OPened")
            prev_frame = None
            success, frame = capture.read()
            print("END: ", success)
            while success:
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                print(f"prev_frame is not None :{prev_frame is not None}")
                if prev_frame is not None:
                    difference = cv2.absdiff(gray_frame, prev_frame)
                    mean_diff = np.mean(difference)
                    print(f"mean_diff > threshold: {mean_diff}")
                    if mean_diff > threshold:
                        frame_num = int(capture.get(cv2.CAP_PROP_POS_FRAMES))
                        cv2.imwrite(f"{video['video_id']}/frame_{frame_num}.jpg", gray_frame)  # Save key frame as image
                        print(f"Saved key frame: frame_{frame_num}.jpg")
                        # cv2.imshow("Key Moment Frame", frame)
                        if cv2.waitKey(0) & 0xFF == ord('q'):
                            break

                prev_frame = gray_frame
                success, frame = capture.read()
                print("END: ", success)

        else:
            print("couldn't open")

        video_db.update_one({"_id": video['video_id']}, {"$pull": {"progress": "scene change detection in progress"}})

    @staticmethod
    def audio_detection(video: Video):
        video_db.update_one({"_id": video['video_id']}, {"$push": {"progress": "detecting audio"}})
        with YoutubeDL(dict(format='bestaudio/best', quiet=True, outtmpl=f"{video['video_id']}/audio.mp3")) as ydl:
            ydl.download(video['youtube_url'])
        video_db.update_one({"_id": video['video_id']}, {"$pull": {"progress": "detecting audio"}})








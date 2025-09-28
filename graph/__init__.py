from typing import List
from typing_extensions import TypedDict

class Video(TypedDict):
    video_id: str
    youtube_url: str
    stream_url: str
    progress: List[str]
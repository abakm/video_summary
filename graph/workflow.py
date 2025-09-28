import os
from langgraph.graph import StateGraph, START, END

from common import video_db

from graph import Video
from graph.video_summary import VideoSummary



builder = StateGraph(Video)
builder.add_node("stream", VideoSummary.get_youtube_stream)
builder.add_node("scenes", VideoSummary.scene_change_detection)
builder.add_node("audio", VideoSummary.audio_detection)


builder.add_edge(START, "stream")
builder.add_edge(START, "audio")

builder.add_edge("stream", "scenes")


builder.add_edge("scenes", END)
builder.add_edge("audio", END)



graph = builder.compile()


def create_folder(directory_name: str):
    created = True
    try:
        os.mkdir(directory_name)
    except FileExistsError:
        os.rmdir(directory_name)
        create_folder(directory_name=directory_name)
    except PermissionError:
        created = False
    return created


def summary_extraction(video_id: int, youtube_url: str):
    if create_folder(directory_name=str(video_id)):
        for event in graph.stream(input=dict(video_id=video_id, youtube_url=youtube_url), stream_mode="updates"):
            print("\n\n\n", event)
    else:
        video_db.update_one({"_id": video_id}, {"$push": {"progress": "Unable to create folder"}})



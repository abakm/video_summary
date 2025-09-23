from pydantic import ValidationError
from flask import Flask, request, jsonify
from common import PayloadTemplate, video_db
app = Flask(__name__)


@app.post('/post')
def post():
    video = request.get_json()
    try:
        PayloadTemplate(**video)
    except ValidationError as e:
        return jsonify(message=str(e)), 400

    if request.form:
        video['source_url'] = request.files['file'].filename

    if not video.get("source_url", None):
        return jsonify(message="Source URL is missing"), 400
    video_ids = video_db.distinct("_id")
    video["_id"] = max(video_ids) + 1 if video_ids else 1
    video_db.insert_one(video)

    return jsonify(dict(video_id=video["_id"])), 200


@app.get('/get/<int:video_id>')
def get(video_id: int):
    video = video_db.find_one({"_id": video_id})
    if video:
        return jsonify(video), 200
    else:
        return jsonify(message="Not found"), 404





# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application
    # on the local development server.
    app.run(host='0.0.0.0', port=5000)
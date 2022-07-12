import json
from dataclasses import dataclass, field

from fastapi import FastAPI, HTTPException, Response

import uvicorn

app = FastAPI()

@dataclass
class Channel:
    id: str
    name: str
    tags: list[str] = field(default_factory=list)
    description: str = ""

channels: dict[str, Channel] = {}

# Channels information in json - normally, would use a database
with open("channels.json", encoding="utf-8") as file:
    channels_raw = json.load(file)

    for channel_raw in channels_raw:
        channel = Channel(**channel_raw)
        channels[channel.id] = channel

@app.get("/")
def read_root()-> Response:
    return Response("The server is running")

@app.get("/channels/{channel_id}", response_model=Channel)
def read_item(channel_id: str)-> Channel:
    if channel_id not in channels:
        raise HTTPException(status_code=404, details="Channel not found")
    
    return channels[channel_id]

# Equivalent of below, for local running
# uvicorn main:app --host 127.0.0.1 --port 8080 --reload
# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8080)

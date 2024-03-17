from collections import defaultdict
from typing import Dict, List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Vote(BaseModel):
    option: str
    votes: int = 0


class Poll(BaseModel):
    id: int
    name: str
    question: str
    votes: Dict[int, Vote] = defaultdict(int)


polls: Dict[int, Poll] = {}


@app.get("/poll", response_model=List[Poll])
async def show_polls():
    return list(polls.values())


@app.post("/poll", response_model=Poll)
async def create_poll(poll: Poll):
    if poll.id not in polls:
        polls[poll.id] = poll
        return poll
    else:
        raise HTTPException(status_code=404, detail="There is poll with that id: " + poll.id)


@app.delete("/poll/{poll_id}")
async def delete_poll(poll_id: int):
    if poll_id not in polls:
        raise HTTPException(status_code=404, detail="Poll not found.")
    else:
        del polls[poll_id]
        return True


@app.get("/poll/{poll_id}", response_model=Poll)
async def show_poll(poll_id: int):
    if poll_id not in polls:
        raise HTTPException(status_code=404, detail="Poll not found.")
    else:
        return polls[poll_id]


@app.put("/poll/{poll_id}")
async def put_poll(poll_id: int, poll: Poll):
    if poll_id not in polls:
        raise HTTPException(status_code=404, detail="Poll not found.")
    else:
        polls[poll_id] = poll
        return poll


@app.get("/poll/{poll_id}/vote")
async def show_votes(poll_id: int):
    if poll_id not in polls:
        raise HTTPException(status_code=404, detail="Poll not found.")
    else:
        return list(polls[poll_id].votes.values())


@app.post("/poll/{poll_id}/vote")
async def vote(poll_id: int, vote: Vote):
    if poll_id not in polls:
        raise HTTPException(status_code=404, detail="Poll not found.")

    for vote_option in polls[poll_id].votes.values():
        if vote_option.option == vote.option:
            vote_option.votes += 1
            return True
    else:
        polls[poll_id].votes[len(polls[poll_id].votes)] = vote


@app.get("/poll/{poll_id}/vote/{vote_id}", response_model=Vote)
async def show_vote(poll_id: int, vote_id: int):
    if poll_id not in polls:
        raise HTTPException(status_code=404, detail="Poll not found.")

    if polls[poll_id].votes[vote_id] is None:
        raise HTTPException(status_code=404, detail="Vote not found.")

    else:
        return polls[poll_id].votes[vote_id]


@app.put("/poll/{poll_id}/vote/{vote_id}")
async def put_vote(poll_id: int, vote_id: int):
    if poll_id not in polls:
        raise HTTPException(status_code=404, detail="Poll not found.")
    if polls[poll_id].votes[vote_id] is None:
        raise HTTPException(status_code=404, detail="Vote not found.")
    else:
        polls[poll_id].votes[vote_id].votes += 1
        return polls[poll_id].votes[vote_id]

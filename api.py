import sys
sys.path.append(".")

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from typing import List
from prospects import Prospect
from db_access import DbAccess

app = FastAPI(title="Prospects API")

class SaveNotesRequest(BaseModel):
    notes: str

# ----------------------------
# Set CORS Policy
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # OK for local/dev
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# Server the HTML
# ----------------------------
@app.get("/", response_class=HTMLResponse)
def serve_index():
    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.get("/sidney", response_class=HTMLResponse)
def serve_index():
    with open("sidney.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.get("/comox", response_class=HTMLResponse)
def serve_index():
    with open("comox.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

# ----------------------------
# All Prospects
# ----------------------------
@app.get("/prospects/comox", response_model=List[Prospect])
def get_prospects():
    db_access = DbAccess()
    db_access.start()
    prospects = db_access.query("Comox")
    db_access.close()

    prospects = sorted(prospects, key=lambda p: p.price)
    return prospects

@app.get("/prospects/sidney", response_model=List[Prospect])
def get_prospects():
    db_access = DbAccess()
    db_access.start()
    prospects = db_access.query("Sidney")
    db_access.close()

    # prospects = sorted(prospects, key=lambda p: p.price)
    # print(f"Prospects Liked: {prospects[-1].liked}")
    return prospects

# ----------------------------
# Mark a Prospect as Liked
# ----------------------------
@app.post("/markLiked/{listingId}/{region}")
def markLiked(listingId: str, region: str):
    print(f"Listing ID: {listingId}")
    db_access = DbAccess()
    db_access.start()
    prospects = db_access.markLiked(listingId, region)
    db_access.close()

    return {"status":"ok"}

# ----------------------------
# Mark a Prospect as Neutral
# ----------------------------
@app.post("/markNeutral/{listingId}/{region}")
def markLiked(listingId: str, region: str):
    db_access = DbAccess()
    db_access.start()
    prospects = db_access.markNeutral(listingId, region)
    db_access.close()

    return {"status":"ok"}

# ----------------------------
# Mark a Prospect as Disliked
# ----------------------------
@app.post("/markDisliked/{listingId}/{region}")
def markLiked(listingId: str, region: str):
    db_access = DbAccess()
    db_access.start()
    prospects = db_access.markDisliked(listingId, region)
    db_access.close()

    return {"status":"ok"}

# ----------------------------
# Mark a Prospect as Disliked
# ----------------------------
@app.post("/saveNotes/{listingId}/{region}")
def saveNotes(listingId: str, region: str, req: SaveNotesRequest):
    print("Received Save Notes Request")
    db_access = DbAccess()
    db_access.start()
    prospects = db_access.saveNotes(listingId, req.notes, region)
    db_access.close()

    return {"status":"ok"}

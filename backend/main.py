from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

# --- [PREVIOUS: Synchronous / Static JSON response] ---
# from simple_ai_assistant import get_ai_response

# --- [NEW: Generator for real-time token streaming] ---
from simple_ai_assistant import generate_chat_stream

app = FastAPI()

# Allow React (running on localhost:5173 or fallback ports) to call this backend
app.add_middleware(
    CORSMiddleware,
    # --- [PREVIOUS: Fixed list of origins] ---
    # allow_origins=[
    #     "http://localhost:5173",
    #     "http://localhost:5174",
    #     "http://127.0.0.1:5173",
    #     "http://127.0.0.1:5174",
    # ],
    # --- [NEW: Allow any local frontend origin so no port is ever blocked by CORS] ---
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessageRequest(BaseModel):
    message: str

# --- [PREVIOUS: Static JSON endpoint that returned all text in one shot] ---
# @app.post("/api/chat")
# def chat_endpoint(req: MessageRequest):
#     reply = get_ai_response(req.message)
#     return {"reply": reply}

# --- [NEW: StreamingResponse endpoint yielding live tokens to React] ---
@app.post("/api/chat")
def chat_endpoint(req: MessageRequest):
    return StreamingResponse(
        generate_chat_stream(req.message),
        media_type="text/plain"
    )
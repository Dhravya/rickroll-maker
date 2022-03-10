import io 
import random

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from .main import Rickroller

app = FastAPI()
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/", response_class=StreamingResponse)
@limiter.limit("1/5minute")
async def rickroll(url:str, request:Request):
    """Downloads and returns the URL"""
    n = random.randint(1, 3)
    rickroll = Rickroller()

    rickroll.make(url, output_path=f"rickrolls/rickroll_{n}.mp4")

    return StreamingResponse(io.open(f"rickrolls/rickroll_{n}.mp4", "rb"), media_type="video/mp4")


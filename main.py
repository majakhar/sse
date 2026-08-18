import asyncio
import json
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
import psutil

app = FastAPI()

# Enable CORS so any frontend can connect to your API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://sse.mjakhar.in"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Async generator function that streams live data
async def generate_server_metrics():
    while True:
        # Fetch real system stats using psutil
        memory = psutil.virtual_memory()
        cpu_usage = psutil.cpu_percent(interval=None)

        stats = {
            "timestamp": time.strftime("%H:%M:%S"),
            "memoryUsagePercent": round(memory.percent, 1),
            "usedMemMB": round((memory.total - memory.available) / (1024 * 1024)),
            "totalMemMB": round(memory.total / (1024 * 1024)),
            "cpuUsage": cpu_usage,
        }

        # 1. Standard default message
        yield f"data: {json.dumps(stats)}\n\n"

        # 2. Custom named event for High CPU Alert
        if cpu_usage > 75.0:
            alert = {
                "severity": "HIGH",
                "message": f"High CPU utilization: {cpu_usage}%",
                "timestamp": stats["timestamp"]
            }
            yield f"event: cpu-alert\ndata: {json.dumps(alert)}\n\n"

        # Stream update every 1 second
        await asyncio.sleep(5)

@app.get("/")
async def serve_dashboard():
    return FileResponse("index.html")

@app.get("/api/server-stats")
async def sse_endpoint():
    return StreamingResponse(
        generate_server_metrics(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            # Crucial header to tell reverse proxies (like Nginx) not to buffer the stream
            "X-Accel-Buffering": "no",
        }
    )

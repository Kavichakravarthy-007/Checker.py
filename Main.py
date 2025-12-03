# main.py
from fastapi import FastAPI, Request
import subprocess
import os
import sys
import uvicorn
from fastapi.responses import JSONResponse

app = FastAPI()

# Configure default pair/interval via env (optional)
DEFAULT_PAIR = os.getenv("DEFAULT_PAIR", "SOLUSDT")
DEFAULT_INTERVAL = os.getenv("DEFAULT_INTERVAL", "1m")

@app.post("/run")
async def run_checker(request: Request):
    body = await request.json() if request.headers.get("content-type","").startswith("application/json") else {}
    pair = body.get("pair", DEFAULT_PAIR)
    interval = body.get("interval", DEFAULT_INTERVAL)

    # Run the checker.py as a subprocess and capture stdout
    try:
        cmd = [sys.executable, "checker.py", pair, interval]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        stdout = proc.stdout
        stderr = proc.stderr
        return JSONResponse({"ok": True, "stdout": stdout, "stderr": stderr, "pair": pair, "interval": interval})
    except Exception as e:
        return JSONResponse({"ok": False, "error": str(e)}, status_code=500)

# health
@app.get("/health")
async def health():
    return {"status":"ok"}

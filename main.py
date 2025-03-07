import os
from typing import List, Optional
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import httpx
from pydantic import BaseModel
import json
from prompt_templates import VEHICLE_FEATURE_PROMPT

app = FastAPI(title="Vehicle Feature and Comparison Guide")

# Set up templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuration for open-webui API
WEBUI_ENABLED = True  # Set to use open-webui API
WEBUI_BASE_URL = "https://chat.ivislabs.in/api"
API_KEY = "sk-dfabda144e474e628a2ece95830c0697"  # Replace with your actual API key if needed
DEFAULT_MODEL = "gemma2:2b"

OLLAMA_ENABLED = True  # Fallback to local Ollama API if needed
OLLAMA_HOST = "localhost"
OLLAMA_PORT = "11434"
OLLAMA_API_URL = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}/api"

class ComparisonRequest(BaseModel):
    vehicle1: str
    vehicle2: str
    include_features: bool = True
    tone: Optional[str] = "informative"

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
   
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/compare")
async def compare_vehicles(
    vehicle1: str = Form(...),
    vehicle2: str = Form(...),
    include_features: bool = Form(True),
    tone: str = Form("informative"),
    model: str = Form(DEFAULT_MODEL)
):
    try:
        prompt = VEHICLE_FEATURE_PROMPT.format(
            vehicle1=vehicle1,
            vehicle2=vehicle2,
            include_features="including detailed features" if include_features else "without features",
            tone=tone
        )
        
        if WEBUI_ENABLED:
            try:
                messages = [{"role": "user", "content": prompt}]
                request_payload = {"model": model, "messages": messages}
                
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{WEBUI_BASE_URL}/chat/completions",
                        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
                        json=request_payload,
                        timeout=60.0
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        generated_text = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                        print(result)
                        return {"comparison_result": generated_text}
            except Exception as e:
                print(f"WebUI API failed: {str(e)}")
        
        if OLLAMA_ENABLED:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{OLLAMA_API_URL}/generate",
                    json={"model": model, "prompt": prompt, "stream": False},
                    timeout=60.0
                )
                if response.status_code == 200:
                    result = response.json()
                    return {"comparison_result": result.get("response", "")}
        
        raise HTTPException(status_code=500, detail="Failed to generate comparison.")
    except Exception as e:
        print(f"Error comparing vehicles: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error comparing vehicles: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)

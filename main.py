import os
from typing import Optional
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import google.generativeai as genai  # Corrected import
import markdown

from prompt_templates import VEHICLE_FEATURE_PROMPT

app = FastAPI(title="Vehicle Feature and Comparison Guide")

# Set up templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuration for Google's Gemini API
GEMINI_API_KEY = "Enter your Api key(Gemini)"  # Replace with your actual API key
genai.configure(api_key=GEMINI_API_KEY)
DEFAULT_MODEL = "gemini-2.0-flash"

@app.get("/", response_class=JSONResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/compare")
async def compare_vehicles(
    request: Request,
    vehicle1: str = Form(...),
    vehicle2: str = Form(...),
    include_features: bool = Form(True),
    tone: str = Form("informative"),
    model: str = Form(DEFAULT_MODEL)
):
    """Handles vehicle comparison requests using Google's Gemini API."""
    try:
        # Generate the AI prompt
        prompt = VEHICLE_FEATURE_PROMPT.format(
            vehicle1=vehicle1,
            vehicle2=vehicle2,
            include_features="including detailed features" if include_features else "without features",
            tone=tone
        )

        # Initialize Gemini API model
        client = genai.GenerativeModel(model)
        
        # Generate response
        response = client.generate_content(prompt)

        print("Gemini API Response:", response)

        # Extract generated content
        generated_text = response.text if response and hasattr(response, "text") else ""
        html_content = markdown.markdown(generated_text, extensions=["extra", "tables"])
        return JSONResponse(content={"success": True, "result": html_content})
    
    except Exception as e:
        print(f"Error comparing vehicles: {str(e)}")
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)

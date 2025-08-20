import os
from typing import Optional
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
import google.generativeai as genai
import markdown

from prompt_templates import VEHICLE_FEATURE_PROMPT  

# PDF libraries
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
import tempfile

app = FastAPI(title="Vehicle Feature and Comparison Guide")

# Set up templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuration for Google's Gemini API
GEMINI_API_KEY = "Your-API-KEY"  # replace with your actual key
genai.configure(api_key=GEMINI_API_KEY)
DEFAULT_MODEL = "gemini-2.0-flash"

@app.get("/", response_class=HTMLResponse)  # ✅ should return HTML
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/compare")
async def compare_vehicles(
    request: Request,
    vehicle1: str = Form(...),
    vehicle2: str = Form(...),
    include_features: bool = Form(True),
    analysis_style: str = Form("Professional Analysis"),
    comparison_focus: str = Form("Overall Comparison"),
    model: str = Form(DEFAULT_MODEL)
):
    """Handles vehicle comparison requests using Google's Gemini API."""
    try:
        # Generate the AI prompt
        prompt = VEHICLE_FEATURE_PROMPT.format(
            vehicle1=vehicle1,
            vehicle2=vehicle2,
            include_features="Include detailed features & specifications" if include_features else "Do not include detailed features",
            analysis_style=analysis_style,
            comparison_focus=comparison_focus
        )

        # Initialize Gemini API model
        client = genai.GenerativeModel(model)
        
        # Generate response (safer to wrap prompt in a list)
        response = client.generate_content([prompt])

        print("Gemini API Response:", response)

        # Extract generated content
        generated_text = response.text if response and hasattr(response, "text") else ""
        html_content = markdown.markdown(generated_text, extensions=["extra", "tables"])
        return JSONResponse(content={"success": True, "result": html_content})
    
    except Exception as e:
        print(f"Error comparing vehicles: {str(e)}")
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)

# ✅ New Export PDF Endpoint
@app.post("/export-pdf")
async def export_pdf(request: Request):
    """
    Takes the generated comparison content from frontend and returns a PDF.
    """
    try:
        data = await request.json()
        content = data.get("content", "")

        # Create temporary file
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        pdf_path = tmp_file.name
        tmp_file.close()

        # Build PDF
        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = [Paragraph(content, styles["Normal"])]
        doc.build(story)

        return FileResponse(pdf_path, filename="comparison.pdf", media_type="application/pdf")
    
    except Exception as e:
        print(f"Error exporting PDF: {str(e)}")
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)


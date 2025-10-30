from fastapi import APIRouter, UploadFile, File, Form
import shutil, os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from .services.morphometric import analyze_livestock_image

router = APIRouter()

@router.post("/analyze/")
async def analyze_livestock(
    file: UploadFile = File(...),
    reference_object_area: float = Form(None)
):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = analyze_livestock_image(temp_path, reference_object_area)
    os.remove(temp_path)
    return result

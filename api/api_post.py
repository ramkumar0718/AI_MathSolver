from fastapi import APIRouter, UploadFile, File, HTTPException
import base64
from io import BytesIO
from PIL import Image, ImageOps
import json
from evaluate import analyze_image

router = APIRouter()

@router.post("")
async def run(image: UploadFile = File(...)):
    try:
        # Converting image into data
        image_bytes = await image.read()
        image_stream = BytesIO(image_bytes)
        image = Image.open(image_stream).convert("RGB")
        
        # Checking wheather the drawing is empty
        grayscale = ImageOps.grayscale(image)
        if all(pixel == 0 for pixel in grayscale.getdata()):
            return {"message": "Canvas is empty!", "status": "error", "data": []}

        # Passing image data and getting output from gemini api
        responses = analyze_image(image)
        ans = str(responses[0]["expr"]) + " = " + str(responses[0]["result"]) if len(responses) >= 1 else " "

        return ans

    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
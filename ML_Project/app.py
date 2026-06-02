import io
import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

from model_loader import PestPredictor, TORCH_AVAILABLE
from pest_data import PEST_DATABASE

# Initialize FastAPI app
app = FastAPI(
    title="Crop Pest Detection API",
    description="Backend API for diagnosing crop pests using PyTorch and serving agricultural guidance.",
    version="1.0.0"
)

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instantiate the ML model predictor (looks for 'pest_model.pth' automatically)
predictor = PestPredictor(model_path="pest_model.pth")

# Static files mapping
# Ensure the static directory exists
os.makedirs("static", exist_ok=True)

@app.post("/api/predict")
async def predict_pest(file: UploadFile = File(...)):
    """
    Accepts an uploaded image file, runs inference (either ML or Simulated fallback),
    and returns predicted pest class, confidence score, and agricultural treatments.
    """
    # Verify file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image.")

    try:
        # Read image contents into memory
        contents = await file.read()
        image_stream = io.BytesIO(contents)
        
        # Run prediction
        predicted_class, confidence = predictor.predict(image_stream)
        
        # Get pest metadata
        pest_info = PEST_DATABASE.get(predicted_class, None)
        
        # Model status info to display on UI
        using_pytorch = predictor.is_ready and TORCH_AVAILABLE
        model_status = "PyTorch ML Inference" if using_pytorch else "Simulated/Fallback Inference"
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "pest_key": predicted_class,
                "confidence": confidence,
                "model_mode": model_status,
                "using_ml": using_pytorch,
                "pest_details": pest_info
            }
        )
    except Exception as e:
        print(f"[ERROR] Prediction API Error: {e}")
        raise HTTPException(status_code=500, detail=f"Diagnostic error: {str(e)}")

@app.get("/api/pests")
async def get_all_pests():
    """
    Returns the complete crop pest library with symptoms, prevention, and treatment protocols.
    """
    return JSONResponse(status_code=200, content=PEST_DATABASE)

@app.get("/api/health")
async def health_check():
    """
    Backend service health status.
    """
    return {
        "status": "healthy",
        "pytorch_loaded": TORCH_AVAILABLE,
        "model_file_exists": os.path.exists("pest_model.pth"),
        "active_predictor_mode": "PyTorch (ML)" if (predictor.is_ready and TORCH_AVAILABLE) else "Simulated/Fallback"
    }

# Serve Frontend static assets
# Mount static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve index.html on root url
@app.get("/")
async def serve_index():
    index_path = os.path.join("static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    else:
        return JSONResponse(
            status_code=404,
            content={"error": "Frontend files missing. Please run static setup."}
        )

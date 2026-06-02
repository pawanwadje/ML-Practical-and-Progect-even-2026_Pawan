import os
import random
from PIL import Image

# Global list of classes matching the training notebook
CLASSES = ['aphids', 'armyworm', 'beetle', 'locust', 'mites']

# Try to import torch and torchvision
TORCH_AVAILABLE = False
try:
    import torch
    import torch.nn as nn
    from torchvision import models, transforms
    TORCH_AVAILABLE = True
except ImportError:
    print("[Note] PyTorch or torchvision is not installed locally. The system will use Simulated Inference Mode.")

class PestPredictor:
    def __init__(self, model_path="pest_model.pth"):
        self.model_path = model_path
        self.model = None
        self.device = None
        self.is_ready = False
        
        if TORCH_AVAILABLE:
            self._initialize_pytorch()
        else:
            print("[INFO] Running in Simulated Mode (Reason: PyTorch libraries not installed).")

    def _initialize_pytorch(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Check if the weight file exists
        if not os.path.exists(self.model_path):
            print(f"[Warning] Model weights '{self.model_path}' not found.")
            print("[Info] To run real ML predictions, please train the model on Google Colab, download 'pest_model.pth', and place it in this folder.")
            print("[Info] Falling back to Simulated Inference Mode for testing.")
            return

        try:
            print(f"[Loading] Loading PyTorch model from '{self.model_path}' on {self.device}...")
            # Recreate MobileNetV2 structure matching the training script
            self.model = models.mobilenet_v2(pretrained=False)
            
            # Rebuild the customized classifier head
            num_features = self.model.classifier[1].in_features
            self.model.classifier[1] = nn.Sequential(
                nn.Linear(num_features, 256),
                nn.ReLU(),
                nn.Dropout(0.4),
                nn.Linear(256, len(CLASSES))
            )
            
            # Load state dictionary
            state_dict = torch.load(self.model_path, map_location=self.device)
            self.model.load_state_dict(state_dict)
            self.model.to(self.device)
            self.model.eval()
            
            # Define image transforms
            self.preprocess = transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225]
                )
            ])
            
            self.is_ready = True
            print("[Success] PyTorch Model loaded and ready for inference!")
        except Exception as e:
            print(f"[Error] Error loading model: {e}")
            print("[Warning] Falling back to Simulated Inference Mode.")
            self.is_ready = False

    def predict(self, image_bytes):
        """
        Accepts raw image bytes, runs inference, and returns (predicted_class, confidence).
        Runs real PyTorch inference if available, otherwise falls back to simulated inference.
        """
        try:
            # Load image using PIL
            image = Image.open(image_bytes).convert("RGB")
        except Exception as e:
            print(f"[Error] Failed to parse image file: {e}")
            return "unknown", 0.0

        if self.is_ready and TORCH_AVAILABLE:
            return self._predict_pytorch(image)
        else:
            return self._predict_simulated(image)

    def _predict_pytorch(self, image):
        """Runs PyTorch inference on the preprocessed image."""
        try:
            img_tensor = self.preprocess(image).unsqueeze(0).to(self.device)
            with torch.no_grad():
                outputs = self.model(img_tensor)
                probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
                confidence, preds = torch.max(probabilities, 0)
            
            predicted_class = CLASSES[preds.item()]
            return predicted_class, float(confidence.item())
        except Exception as e:
            print(f"[Error] PyTorch prediction error: {e}")
            return self._predict_simulated(image)

    def _predict_simulated(self, image):
        """
        Performs a simulated prediction based on basic image features.
        Helps test the backend and frontend without PyTorch dependencies.
        """
        # Get image width, height, and color channels
        width, height = image.size
        
        # Crop a small central part to analyze dominant colors
        box = (width // 4, height // 4, 3 * width // 4, 3 * height // 4)
        cropped = image.crop(box)
        
        # Calculate mean RGB values
        # Resize to 1x1 to get average color
        avg_color = cropped.resize((1, 1)).getpixel((0, 0))
        r, g, b = avg_color[0], avg_color[1], avg_color[2]
        
        # A simple heuristic mapping color bias to certain pests to make it feel responsive
        # Green plants with green/yellow highlights -> aphids
        # Reddish/Dark images -> beetles or mites
        # Earthy browns -> armyworm
        # Yellowish greens -> locusts
        # Otherwise random choice
        if g > 130 and r < 120 and b < 120:
            predicted_class = "aphids"
        elif r > 130 and g < 100 and b < 100:
            predicted_class = "beetle"
        elif r > 120 and g > 120 and b < 100:
            predicted_class = "locust"
        elif r > 100 and g > 90 and b > 90 and abs(r - g) < 20:
            predicted_class = "armyworm"
        elif r > 150 and g > 150 and b > 150:
            predicted_class = "mites"
        else:
            # Deterministic hash of image size to avoid completely random changes on same image
            predicted_class = CLASSES[(width + height) % len(CLASSES)]
            
        confidence = 0.75 + (random.randint(5, 23) / 100.0) # Random realistic confidence 80%-98%
        
        print(f"[SIMULATED INFERENCE] Predicted: {predicted_class} (Conf: {confidence * 100:.1f}%) | Avg RGB: ({r},{g},{b})")
        return predicted_class, confidence

# 🌾 BioShield AI: Crop Pest Detection & Monitoring System

BioShield AI is a state-of-the-art agricultural monitoring platform designed to diagnose crop leaf infections and pests in real-time. It integrates a lightweight **PyTorch MobileNetV2** deep learning classifier with a high-performance **FastAPI** Python backend and a premium, responsive **glassmorphic crop dashboard**.

The system is optimized for users without a local GPU, allowing model training to be performed entirely on **Google Colab (using free T4 GPUs)**, while running local predictions on standard laptop/desktop CPUs or falling back to local simulation mode.

---

## 🚀 Key Features

*   **Google Colab GPU Training**: A fully prepared Jupyter training notebook with data augmentation, transfer learning using `MobileNetV2`, performance plots, and automated model weight downloads.
*   **Dual Inference Modes**:
    *   *Real ML Inference*: Automatically loads PyTorch and fine-tuned weights (`pest_model.pth`) to run real neural network predictions.
    *   *Simulated Fallback Mode*: Instantly starts up without PyTorch dependency, performing simulated predictions based on average pixel values so you can showcase the frontend/backend interface immediately.
*   **Biotech Glassmorphism Dashboard**:
    *   **Drag-and-Drop** photo uploading area.
    *   **Live WebRTC Camera Scan** supporting device camera streams and snapshot capturing directly in-browser.
    *   **Circular gauge charts** indicating confidence match percentages.
    *   **Diagnostic History Log** storing past scans (with dates, thumbnails, and modes) locally in the browser's `localStorage`.
    *   **Interactive Pest Reference Library** storing detailed diagnostic profile sheets (symptoms, organic controls, chemical spray protocols, and cultural preventions) for 5 major agricultural pest classes:
        1. *Aphids (Plant Lice)*
        2. *Fall Armyworm*
        3. *Colorado Potato Beetle*
        4. *Desert Locust / Grasshopper*
        5. *Two-Spotted Spider Mites*

---

## 📁 Repository Structure

This project uses a clean, flat folder layout designed for immediate upload to **GitHub**:

```
ML_Project/
├── app.py                      # FastAPI core web application
├── model_loader.py             # Dual-mode predictor script (PyTorch / Simulated)
├── pest_data.py                # Agronomist pest database (symptoms, treatments)
├── requirements.txt            # Python dependencies
├── run.bat                     # One-click Windows runner script
├── pest_classifier_colab.ipynb # Google Colab Notebook for model training
├── README.md                   # Repository documentation (this file)
└── static/                     # Frontend static directory
    ├── index.html              # Dashboard structure
    ├── style.css               # Glassmorphic custom CSS styling
    └── app.js                  # Camera, upload, and charting JS logic
```

---

## ⚙️ Quick Start (Local Running)

### Option A: One-Click Startup (Windows)
1. Double-click the **`run.bat`** file in the root folder.
2. Select your desired execution mode in the terminal:
    *   `[1]` for *Lightweight Simulation Mode* (downloads in <30 seconds, runs mock diagnoses).
    *   `[2]` for *Full ML Mode* (downloads PyTorch CPU libraries for real model loading).
3. The script will configure a Python virtual environment, install the dependencies, launch the server, and automatically open `http://localhost:8000` in your default browser.

### Option B: Manual Startup (All OS)
Open your terminal in the project directory and execute the following:

```bash
# 1. Create virtual environment
python -m venv .venv

# 2. Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# 3. Install core dependencies
pip install -r requirements.txt

# 4. (Optional) Install PyTorch for local inference
pip install torch torchvision --extra-index-url https://download.pytorch.org/whl/cpu

# 5. Start the FastAPI server
uvicorn app:app --reload
```
Open [http://localhost:8000](http://localhost:8000) in your web browser.

---

## 🧠 Google Colab Training Workflow

Since training deep learning models requires a GPU, follow these steps to train your model for free on Google Colab:

### 1. Upload Notebook to Google Colab
1. Go to [Google Colab](https://colab.research.google.com/).
2. Click **File** -> **Upload notebook** and choose the `pest_classifier_colab.ipynb` file from this project.
3. Configure GPU: Go to **Runtime** -> **Change runtime type**, select **GPU** (T4 GPU is free), and click **Save**.

### 2. Configure Your Dataset
By default, the notebook creates a small synthetic dataset so you can run all cells immediately to test.
*   **For custom training**: Prepare your images in a ZIP file structured as follows:
    ```
    dataset.zip/
    ├── train/
    │   ├── aphids/
    │   ├── armyworm/
    │   ├── beetle/
    │   ├── locust/
    │   └── mites/
    └── val/
        ├── aphids/
        ├── armyworm/
        ├── beetle/
        ├── locust/
        └── mites/
    ```
*   Upload your ZIP file to Google Colab and uncomment the extraction cell to unpack your custom files.

### 3. Run and Download
1. Run all cells in the notebook.
2. Once training completes, the notebook will automatically export the model weights as **`pest_model.pth`** and trigger a browser download.
3. Move the downloaded `pest_model.pth` file into the root folder of this project.
4. Restart the FastAPI server. The system will automatically detect the file, load PyTorch, and switch from *Simulated* to *Real ML Inference* mode!

---

## 🛡️ License & Attributions

Designed for agricultural education, research, and remote sensing diagnostics.
*   Model Backbone: MobileNetV2 (ImageNet Pre-trained)
*   Styling: Custom CSS Glassmorphism
*   Icons: FontAwesome 6
*   Fonts: Google Fonts (Outfit & Inter)

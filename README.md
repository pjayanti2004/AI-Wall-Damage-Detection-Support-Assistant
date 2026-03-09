# AI Wall Damage Detection System

An AI-assisted computer vision application that analyzes wall images to detect cracks, paint peeling, and structural damage.

## Features
- Upload wall damage images
- Detect cracks using OpenCV
- Highlight damaged areas
- Calculate damage percentage
- Predict severity level
- Recommend technician
- Estimate repair cost

## Technologies Used
- Python
- OpenCV
- NumPy
- Streamlit
- PIL

## How It Works
1. User uploads a wall image
2. Image is processed using OpenCV
3. Edges and contours are detected
4. Damage areas are highlighted
5. Damage percentage is calculated
6. Severity and repair cost are predicted

## Run the Project
pip install -r requirements.txt
streamlit run app.py
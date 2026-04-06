import os
import numpy as np
from PIL import Image
try:
    import tensorflow as tf
    TF_AVAILABLE = True
except ImportError:
    tf = None
    TF_AVAILABLE = False

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    cv2 = None
    CV2_AVAILABLE = False
from fpdf import FPDF
from datetime import datetime

def medical_clahe_preprocessing(img_array):
    """Apply CLAHE to enhance lung detail for consistency with training."""
    if not CV2_AVAILABLE:
        return img_array
    
    # Input is expected to be [0, 1] scaled, 150x150x3
    img_uint8 = (img_array * 255).astype('uint8')
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    for i in range(3):
        img_uint8[:,:,i] = clahe.apply(img_uint8[:,:,i])
    return img_uint8.astype('float32') / 255.0

def generate_grad_cam(model, img_array, intensity=0.5, res=250):
    """Placeholder for Grad-CAM logic. In Demo, we mock the heatmap."""
    if not CV2_AVAILABLE:
        # Fallback to a blank heatmap if cv2 is not available
        return np.zeros((res, res, 3), dtype=np.uint8)
    
    heatmap = np.zeros((res, res), dtype=np.uint8)
    center = (int(res * 0.5), int(res * 0.6))
    axes = (int(res * 0.3), int(res * 0.2))
    cv2.ellipse(heatmap, center, axes, 0, 0, 360, 255, -1)
    heatmap = cv2.GaussianBlur(heatmap, (55, 55), 0)
    heatmap_color = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    return heatmap_color

def create_pdf_report(scan_data, pdf_path):
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="PneumoScan AI - Diagnostic Report", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
    pdf.ln(10)
    
    # Patient Info
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Patient Information", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.cell(100, 8, txt=f"Patient Name: {scan_data['patient_name']}", ln=True)
    pdf.cell(100, 8, txt=f"Age: {scan_data['patient_age']}", ln=True)
    pdf.cell(100, 8, txt=f"Diagnosis: {scan_data['prediction']} ({scan_data['disease_type']})", ln=True)
    pdf.cell(100, 8, txt=f"Confidence: {scan_data['confidence']}%", ln=True)
    pdf.ln(10)
    
    # Analysis & AI Suggestion
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="AI Clinical Assessment", ln=True)
    pdf.set_font("Arial", size=11)
    suggestion = get_ai_suggestions(scan_data['prediction'], scan_data['confidence'])
    pdf.multi_cell(180, 8, txt=suggestion)
    pdf.ln(10)
    
    # Footer
    pdf.set_font("Arial", 'I', 8)
    pdf.cell(200, 10, txt="* This report is AI-generated and should be reviewed by a certified radiologist.", ln=True, align='C')
    
    pdf.output(pdf_path)

def get_ai_suggestions(label, confidence):
    if label == 'PNEUMONIA':
        if confidence > 90:
            return "Recommendation: Immediate clinical review and possible hospitalization. Perform supplemental lung ultrasound and blood cultures."
        else:
            return "Recommendation: Broad-spectrum antibiotics and follow-up scan in 48 hours. Monitor blood oxygen levels."
    else:
        return "Recommendation: Normal findings. No immediate intervention required. Maintain routine follow-up if symptoms persist."

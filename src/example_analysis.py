import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import io, color, exposure

def load_and_preprocess(image_path):
    """Load and preprocess a medical image."""
    # Read the image
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")
    
    # Read as grayscale for medical images
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Enhance contrast using CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(image)
    
    return image, enhanced

def analyze_image(image):
    """Perform basic image analysis."""
    # Calculate basic statistics
    min_val = np.min(image)
    max_val = np.max(image)
    mean_val = np.mean(image)
    std_val = np.std(image)
    
    return {
        'min': min_val,
        'max': max_val,
        'mean': mean_val,
        'std': std_val
    }

def plot_images(original, processed, title1='Original', title2='Processed'):
    """Plot original and processed images side by side."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    
    axes[0].imshow(original, cmap='gray')
    axes[0].set_title(title1)
    axes[0].axis('off')
    
    axes[1].imshow(processed, cmap='gray')
    axes[1].set_title(title2)
    axes[1].axis('off')
    
    plt.tight_layout()
    
    # Create output directory if it doesn't exist
    os.makedirs('../output', exist_ok=True)
    
    # Save the figure
    output_path = '../output/processed_image.png'
    plt.savefig(output_path)
    plt.close()
    
    return output_path

def main():
    print("Python Medical Image Analysis")
    print("============================")
    
    # Example image path (you should replace this with your own image)
    image_path = '../data/example_xray.jpg'  # Replace with your image path
    
    try:
        # Load and preprocess the image
        original, processed = load_and_preprocess(image_path)
        
        # Analyze the image
        stats = analyze_image(processed)
        print("\nImage Analysis Results:")
        print(f"- Min intensity: {stats['min']:.2f}")
        print(f"- Max intensity: {stats['max']:.2f}")
        print(f"- Mean intensity: {stats['mean']:.2f}")
        print(f"- Standard deviation: {stats['std']:.2f}")
        
        # Plot and save results
        output_path = plot_images(original, processed, 
                                'Original X-ray', 'Enhanced X-ray')
        print(f"\nResults saved to: {os.path.abspath(output_path)}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Please make sure the image path is correct and the image is accessible.")

if __name__ == "__main__":
    main()

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def setup_directories():
    """Create necessary directories if they don't exist."""
    os.makedirs('../data/chest_xray', exist_ok=True)
    os.makedirs('../output', exist_ok=True)

def load_sample_image():
    """Load and display a sample medical image."""
    # Create a sample image (in a real scenario, you would load an actual X-ray)
    img = np.zeros((256, 256), dtype=np.uint8)
    cv2.putText(img, "Sample X-ray", (30, 128), 
               cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    # Save the sample image
    sample_path = '../output/sample_xray.png'
    cv2.imwrite(sample_path, img)
    
    # Display the image
    plt.figure(figsize=(8, 8))
    plt.imshow(img, cmap='gray')
    plt.title('Sample X-ray Image')
    plt.axis('off')
    plt.savefig('../output/sample_xray_plot.png')
    plt.close()
    
    return sample_path

def test_data_augmentation():
    """Test image augmentation pipeline."""
    # Create a sample image
    img = np.zeros((150, 150, 3), dtype=np.uint8)
    cv2.putText(img, "X", (50, 90), 
               cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 10)
    
    # Expand dimensions to (1, 150, 150, 3) for Keras
    img = np.expand_dims(img, axis=0)
    
    # Create data augmentation generator
    datagen = ImageDataGenerator(
        rotation_range=20,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    
    # Generate augmented images
    aug_iter = datagen.flow(img, batch_size=1)
    
    # Generate and save augmented images
    plt.figure(figsize=(10, 10))
    for i in range(9):
        plt.subplot(3, 3, i + 1)
        batch = next(aug_iter)  # Using next() function for compatibility
        image = batch[0].astype('uint8')
        plt.imshow(image)
        plt.axis('off')
    
    plt.tight_layout()
    plt.savefig('../output/augmented_samples.png')
    plt.close()

def main():
    print("Testing Medical Imaging Pipeline")
    print("===============================")
    
    # Setup directories
    setup_directories()
    
    # Test 1: Create and display a sample X-ray
    print("\n1. Creating sample X-ray image...")
    sample_path = load_sample_image()
    print(f"   - Sample X-ray saved to: {sample_path}")
    
    # Test 2: Test data augmentation
    print("\n2. Testing data augmentation...")
    test_data_augmentation()
    print("   - Augmented samples saved to: ../output/augmented_samples.png")
    
    print("\nPipeline test completed successfully!")
    print("Check the 'output' directory for generated images.")

if __name__ == "__main__":
    main()

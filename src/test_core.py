import sys
import numpy as np
import cv2
from PIL import Image

def test_environment():
    print("Core Python Environment Test")
    print("===========================")
    
    # Check Python version
    print(f"Python Version: {sys.version.split()[0]}")
    
    # Check package versions
    print("\nPackage Versions:")
    print(f"- NumPy: {np.__version__}")
    print(f"- OpenCV: {cv2.__version__}")
    print(f"- PIL (Pillow): {Image.__version__}")
    
    # Basic NumPy test
    print("\nNumPy Test:")
    arr = np.random.rand(3, 3)
    print("Random 3x3 matrix:")
    print(arr)
    
    # Basic OpenCV test
    print("\nOpenCV Test:")
    try:
        # Create a simple black image
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        cv2.putText(img, "OpenCV Works!", (10, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        # Save the test image
        test_img_path = '../output/test_opencv.png'
        cv2.imwrite(test_img_path, img)
        print(f"Test image saved to: {test_img_path}")
        print("OpenCV is working correctly!")
    except Exception as e:
        print(f"OpenCV test failed: {str(e)}")
    
    print("\n✅ Core Python environment is set up correctly!")

if __name__ == "__main__":
    test_environment()

import sys
import numpy as np
import cv2
import tensorflow as tf

def test_environment():
    print("Python Environment Test")
    print("======================")
    
    # Check Python version
    print(f"Python Version: {sys.version.split()[0]}")
    
    # Check package versions
    print("\nPackage Versions:")
    print(f"- NumPy: {np.__version__}")
    print(f"- OpenCV: {cv2.__version__}")
    print(f"- TensorFlow: {tf.__version__}")
    
    # Basic NumPy test
    print("\nNumPy Test:")
    arr = np.random.rand(3, 3)
    print("Random 3x3 matrix:")
    print(arr)
    
    # Basic OpenCV test
    print("\nOpenCV Test:")
    print("OpenCV can read/write images: Yes")
    
    # Basic TensorFlow test
    print("\nTensorFlow Test:")
    print(f"TensorFlow is built with CUDA: {'Yes' if tf.test.is_built_with_cuda() else 'No'}")
    print(f"GPU Available: {'Yes' if tf.config.list_physical_devices('GPU') else 'No'}")
    
    print("\n✅ Python environment is set up correctly!")

if __name__ == "__main__":
    test_environment()

import sys
import subprocess
import platform

def check_system():
    print("System Information")
    print("=================")
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Processor: {platform.processor()}")
    print(f"Python: {platform.python_version()}")
    print(f"Architecture: {'64-bit' if sys.maxsize > 2**32 else '32-bit'}")

def install_tensorflow():
    print("\nInstalling TensorFlow...")
    
    # Uninstall existing tensorflow if any
    subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", "tensorflow", "tensorflow-gpu"], 
                  check=False)
    
    # Install CPU-only version of TensorFlow compatible with Python 3.12
    subprocess.run([sys.executable, "-m", "pip", "install", "tensorflow-cpu==2.16.1"], 
                  check=True)
    
    print("\nTensorFlow installation completed!")

def verify_tensorflow():
    print("\nVerifying TensorFlow installation...")
    try:
        import tensorflow as tf
        print(f"TensorFlow Version: {tf.__version__}")
        print("Available Devices:")
        print(tf.config.list_physical_devices())
        print("\n✅ TensorFlow is working correctly!")
    except Exception as e:
        print(f"\n❌ TensorFlow verification failed: {str(e)}")
        print("\nTroubleshooting steps:")
        print("1. Make sure you have Visual C++ Redistributable 2019 installed")
        print("2. Try installing an older version: pip install tensorflow-cpu==2.10.0")
        print("3. Check TensorFlow's Windows setup guide: https://www.tensorflow.org/install/pip#windows")

if __name__ == "__main__":
    check_system()
    install_tensorflow()
    verify_tensorflow()

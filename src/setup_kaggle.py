import os
import json
from pathlib import Path

def setup_kaggle():
    """Set up Kaggle API credentials."""
    kaggle_dir = Path.home() / '.kaggle'
    kaggle_file = kaggle_dir / 'kaggle.json'
    
    # Create .kaggle directory if it doesn't exist
    kaggle_dir.mkdir(exist_ok=True)
    
    if not kaggle_file.exists():
        print("Kaggle API setup")
        print("================")
        print("1. Go to https://www.kaggle.com/")
        print("2. Click on your profile picture → Account")
        print("3. Scroll down to 'API' and click 'Create New API Token'")
        print("4. This will download 'kaggle.json'")
        print("5. Copy the contents of that file below (press Enter, then Ctrl+D when done):\n")
        
        # Get user input for kaggle.json
        contents = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            contents.append(line)
        
        # Save to kaggle.json
        if contents:
            kaggle_file.write_text('\n'.join(contents))
            kaggle_file.chmod(0o600)  # Set secure permissions
            print(f"\n✅ Kaggle API credentials saved to: {kaggle_file}")
        else:
            print("\n❌ No input received. Kaggle API setup incomplete.")
            return False
    else:
        print(f"✅ Kaggle API is already set up at: {kaggle_file}")
    
    return True

def download_dataset():
    """Download the Chest X-Ray Images (Pneumonia) dataset."""
    import kaggle
    
    dataset = 'paultimothymooney/chest-xray-pneumonia'
    data_dir = Path('../data/chest_xray')
    
    print(f"\nDownloading dataset: {dataset}")
    print("This may take a few minutes...")
    
    # Create data directory
    data_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Download the dataset
        kaggle.api.dataset_download_files(
            dataset,
            path=str(data_dir),
            unzip=True,
            quiet=False
        )
        
        print(f"\n✅ Dataset downloaded to: {data_dir}")
        return True
    except Exception as e:
        print(f"\n❌ Error downloading dataset: {str(e)}")
        return False

if __name__ == "__main__":
    # Install kaggle package if not already installed
    try:
        import kaggle
    except ImportError:
        print("Installing Kaggle API...")
        import sys
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "kaggle"])
        import kaggle
    
    if setup_kaggle():
        download_dataset()

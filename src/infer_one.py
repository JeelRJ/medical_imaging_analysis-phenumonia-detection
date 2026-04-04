import argparse
import os
import numpy as np
from PIL import Image
import tensorflow as tf


def load_and_preprocess(image_path: str, size=(150, 150)):
    img = Image.open(image_path).convert("RGB").resize(size)
    x = np.array(img, dtype="float32") / 255.0
    return x[None, ...]


def main():
    parser = argparse.ArgumentParser(description="Run single-image inference for pneumonia detection")
    parser.add_argument("image", help="Path to an X-ray image (jpg/png)")
    parser.add_argument("--model", default=os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "output", "models", "pneumonia_model.keras")), help="Path to saved Keras model")
    args = parser.parse_args()

    image_path = os.path.abspath(args.image)
    model_path = os.path.abspath(args.model)

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found: {model_path}")
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    model = tf.keras.models.load_model(model_path)
    x = load_and_preprocess(image_path)
    prob = float(model.predict(x, verbose=0)[0][0])
    label = "PNEUMONIA" if prob > 0.5 else "NORMAL"

    print(f"Image: {image_path}")
    print(f"Prediction: {label}")
    print(f"Score: {prob:.4f}")


if __name__ == "__main__":
    main()

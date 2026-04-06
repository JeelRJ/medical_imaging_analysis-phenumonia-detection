import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np

# Set paths
base_dir = r"e:\medical_image_classification\medical_imaging_analysis-phenumonia-detection"
model_path = os.path.join(base_dir, "output", "models", "pneumonia_model.keras")
test_dir = os.path.join(base_dir, "data", "chest_xray", "test")

def evaluate():
    if not os.path.exists(model_path):
        print(f"Model not found at {model_path}")
        return

    print(f"Loading model from {model_path}...")
    model = tf.keras.models.load_model(model_path)
    
    print("Setting up test data generator...")
    test_datagen = ImageDataGenerator(rescale=1./255)
    test_generator = test_datagen.flow_from_directory(
        test_dir,
        target_size=(150, 150),
        batch_size=32,
        class_mode='binary',
        shuffle=False
    )
    
    print("Evaluating model...")
    results = model.evaluate(test_generator)
    print(f"Test Loss: {results[0]:.4f}")
    print(f"Test Accuracy: {results[1]:.4f}")
    
    if len(results) > 2:
        print(f"Test AUC: {results[2]:.4f}")

    # Predictions for detailed report
    print("\nGenerating classification report...")
    y_pred = (model.predict(test_generator) > 0.5).astype("int32")
    y_true = test_generator.classes
    target_names = ['NORMAL', 'PNEUMONIA']
    print(classification_report(y_true, y_pred, target_names=target_names))

if __name__ == "__main__":
    evaluate()

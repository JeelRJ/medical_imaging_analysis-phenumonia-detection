import os
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import pandas as pd
import math

# Set random seed for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

class PneumoniaDetector:
    def __init__(self, data_dir='../data/chest_xray'):
        """Initialize the pneumonia detector with data directory."""
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        if not os.path.isabs(data_dir):
            data_dir = os.path.normpath(os.path.join(self.base_dir, data_dir))
        self.data_dir = data_dir
        self.train_dir = os.path.join(data_dir, 'train')
        self.val_dir = os.path.join(data_dir, 'val')
        self.test_dir = os.path.join(data_dir, 'test')
        self.classes = ['NORMAL', 'PNEUMONIA']
        self.img_size = (150, 150)
        self.batch_size = 32
        self.model = None
        self.history = None
        
    def setup_directories(self):
        """Create necessary directories if they don't exist."""
        os.makedirs(self.train_dir, exist_ok=True)
        os.makedirs(self.val_dir, exist_ok=True)
        os.makedirs(self.test_dir, exist_ok=True)
        out_models = os.path.normpath(os.path.join(self.base_dir, '..', 'output', 'models'))
        out_plots = os.path.normpath(os.path.join(self.base_dir, '..', 'output', 'plots'))
        os.makedirs(out_models, exist_ok=True)
        os.makedirs(out_plots, exist_ok=True)
    
    def create_data_generators(self):
        """Create data generators for training, validation, and testing."""
        # Data augmentation for training
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            fill_mode='nearest'
        )
        
        # Only rescaling for validation and test data
        test_datagen = ImageDataGenerator(rescale=1./255)
        
        # Create data generators
        self.train_generator = train_datagen.flow_from_directory(
            self.train_dir,
            target_size=self.img_size,
            batch_size=self.batch_size,
            class_mode='binary',
            classes=self.classes
        )
        
        self.validation_generator = test_datagen.flow_from_directory(
            self.val_dir,
            target_size=self.img_size,
            batch_size=self.batch_size,
            class_mode='binary',
            classes=self.classes,
            shuffle=False
        )
        
        self.test_generator = test_datagen.flow_from_directory(
            self.test_dir,
            target_size=self.img_size,
            batch_size=self.batch_size,
            class_mode='binary',
            classes=self.classes,
            shuffle=False
        )
    
    def build_model(self):
        """Build a CNN model for pneumonia detection."""
        model = models.Sequential([
            # First Convolutional Block
            layers.Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)),
            layers.MaxPooling2D((2, 2)),
            
            # Second Convolutional Block
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            
            # Third Convolutional Block
            layers.Conv2D(128, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            
            # Dense Layers
            layers.Flatten(),
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(1, activation='sigmoid')
        ])
        
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy', tf.keras.metrics.AUC(name='auc')]
        )
        
        self.model = model
        return model
    
    def train_model(self, epochs=10):
        """Train the model with early stopping."""
        if self.model is None:
            self.build_model()
        
        # Define callbacks
        callbacks = [
            tf.keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=3,
                restore_best_weights=True
            ),
            tf.keras.callbacks.ModelCheckpoint(
                filepath=os.path.normpath(os.path.join(self.base_dir, '..', 'output', 'models', 'pneumonia_model.keras')),
                save_best_only=True,
                monitor='val_accuracy',
                mode='max'
            )
        ]
        
        # Train the model
        self.history = self.model.fit(
            self.train_generator,
            steps_per_epoch=max(1, int(np.ceil(self.train_generator.samples / self.batch_size))),
            epochs=epochs,
            validation_data=self.validation_generator,
            validation_steps=max(1, int(np.ceil(self.validation_generator.samples / self.batch_size))),
            callbacks=callbacks
        )
        
        return self.history
    
    def evaluate_model(self):
        """Evaluate the model on the test set."""
        if self.model is None:
            raise ValueError("Model has not been trained yet.")
        
        # Evaluate on test set
        test_loss, test_acc, test_auc = self.model.evaluate(self.test_generator)
        print(f"\nTest Accuracy: {test_acc:.4f}")
        print(f"Test AUC: {test_auc:.4f}")
        
        # Generate predictions
        y_pred = (self.model.predict(self.test_generator) > 0.5).astype("int32")
        y_true = self.test_generator.classes
        
        # Classification report
        print("\nClassification Report:")
        print(classification_report(y_true, y_pred, target_names=self.classes))
        
        # Confusion matrix
        cm = confusion_matrix(y_true, y_pred)
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=self.classes, yticklabels=self.classes)
        plt.title('Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.tight_layout()
        plt.savefig(os.path.normpath(os.path.join(self.base_dir, '..', 'output', 'plots', 'confusion_matrix.png')))
        plt.close()
        
        return test_acc, test_auc
    
    def plot_training_history(self):
        """Plot training and validation accuracy/loss over epochs."""
        if self.history is None:
            raise ValueError("Model has not been trained yet.")
            
        history = self.history.history
        
        # Plot accuracy
        plt.figure(figsize=(12, 5))
        
        plt.subplot(1, 2, 1)
        plt.plot(history['accuracy'], label='Training Accuracy')
        plt.plot(history['val_accuracy'], label='Validation Accuracy')
        plt.title('Model Accuracy')
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.legend()
        
        # Plot loss
        plt.subplot(1, 2, 2)
        plt.plot(history['loss'], label='Training Loss')
        plt.plot(history['val_loss'], label='Validation Loss')
        plt.title('Model Loss')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.legend()
        
        plt.tight_layout()
        plt.savefig(os.path.normpath(os.path.join(self.base_dir, '..', 'output', 'plots', 'training_history.png')))
        plt.close()
    
    def visualize_predictions(self, num_images=5):
        """Visualize model predictions on sample test images."""
        # Get a batch of test data
        x_batch, y_batch = next(self.test_generator)
        
        # Make predictions
        preds = self.model.predict(x_batch)
        
        n = min(num_images, len(x_batch))
        cols = min(5, n)
        rows = int(math.ceil(n / cols))
        plt.figure(figsize=(cols * 3, rows * 3))
        
        for i in range(n):
            plt.subplot(rows, cols, i + 1)
            plt.imshow(x_batch[i])
            
            true_label = self.classes[int(y_batch[i])]
            pred_label = self.classes[int(preds[i] > 0.5)]
            prob = preds[i][0] if preds[i] > 0.5 else 1 - preds[i][0]
            
            title = f"True: {true_label}\nPred: {pred_label} ({prob:.2f})"
            color = 'green' if true_label == pred_label else 'red'
            
            plt.title(title, color=color)
            plt.axis('off')
        
        plt.tight_layout()
        plt.savefig(os.path.normpath(os.path.join(self.base_dir, '..', 'output', 'plots', 'sample_predictions.png')))
        plt.close()

def main():
    print("Pneumonia Detection from Chest X-Rays")
    print("====================================")
    
    # Initialize the detector
    detector = PneumoniaDetector()
    
    # Setup directories
    detector.setup_directories()
    
    # Create data generators
    print("\nSetting up data generators...")
    detector.create_data_generators()
    
    # Build the model
    print("\nBuilding the model...")
    detector.build_model()
    detector.model.summary()
    
    # Train the model
    print("\nTraining the model...")
    detector.train_model(epochs=10)
    
    # Evaluate the model
    print("\nEvaluating the model...")
    detector.evaluate_model()
    
    # Plot training history
    print("\nGenerating training plots...")
    detector.plot_training_history()
    
    # Visualize predictions
    print("\nGenerating prediction visualizations...")
    detector.visualize_predictions(num_images=12)
    
    print("\n✅ Pneumonia detection pipeline completed successfully!")
    print("Check the 'output' directory for results and visualizations.")

if __name__ == "__main__":
    main()

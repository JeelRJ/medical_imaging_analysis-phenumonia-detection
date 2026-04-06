import os
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models, optimizers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.utils.class_weight import compute_class_weight
import matplotlib.pyplot as plt
import cv2

# Set seeds for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

# Configuration
BASE_DIR = r"e:\medical_image_classification\medical_imaging_analysis-phenumonia-detection"
DATA_DIR = os.path.join(BASE_DIR, "data", "chest_xray")
MODEL_SAVE_PATH = os.path.join(BASE_DIR, "output", "models", "pneumonia_model_custom_v3.keras")
IMG_SIZE = (150, 150)
BATCH_SIZE = 32
EPOCHS = 50

def medical_clahe_preprocessing(img):
    """Apply CLAHE to enhance lung detail."""
    img_uint8 = img.astype('uint8')
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    for i in range(3):
        img_uint8[:,:,i] = clahe.apply(img_uint8[:,:,i])
    return img_uint8.astype('float32') / 255.0

def build_deep_custom_cnn(input_shape):
    """Builds a deep custom CNN architecture optimized for X-ray features."""
    model = models.Sequential([
        # Block 1
        layers.Conv2D(32, (3, 3), padding='same', input_shape=input_shape),
        layers.BatchNormalization(),
        layers.Activation('relu'),
        layers.MaxPooling2D((2, 2)),
        
        # Block 2
        layers.Conv2D(64, (3, 3), padding='same'),
        layers.BatchNormalization(),
        layers.Activation('relu'),
        layers.MaxPooling2D((2, 2)),
        
        # Block 3
        layers.Conv2D(128, (3, 3), padding='same'),
        layers.BatchNormalization(),
        layers.Activation('relu'),
        layers.MaxPooling2D((2, 2)),
        layers.SpatialDropout2D(0.2),
        
        # Block 4
        layers.Conv2D(256, (3, 3), padding='same'),
        layers.BatchNormalization(),
        layers.Activation('relu'),
        layers.MaxPooling2D((2, 2)),
        layers.SpatialDropout2D(0.3),
        
        # Block 5
        layers.Conv2D(512, (3, 3), padding='same'),
        layers.BatchNormalization(),
        layers.Activation('relu'),
        layers.MaxPooling2D((2, 2)),
        layers.SpatialDropout2D(0.4),

        # Block 6 (Deeper feature extraction)
        layers.Conv2D(512, (3, 3), padding='same'),
        layers.BatchNormalization(),
        layers.Activation('relu'),
        layers.GlobalAveragePooling2D(),
        
        # Dense Layers
        layers.Dense(512, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        layers.Dense(1, activation='sigmoid')
    ])
    
    # Phase 2: AdamW with Cosine Decay for peak accuracy
    lr_schedule = tf.keras.optimizers.schedules.CosineDecay(
        initial_learning_rate=2e-4,
        decay_steps=EPOCHS * (4173 // BATCH_SIZE)
    )
    
    model.compile(
        optimizer=optimizers.AdamW(learning_rate=lr_schedule, weight_decay=1e-4),
        loss='binary_crossentropy',
        metrics=['accuracy', tf.keras.metrics.Precision(name='precision'), tf.keras.metrics.Recall(name='recall')]
    )
    
    return model

def train():
    os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)
    
    # Phase 2 Augmented Training with CLAHE
    train_datagen = ImageDataGenerator(
        # Note: Rescaling is handled INSIDE our custom preprocessing function now
        preprocessing_function=medical_clahe_preprocessing,
        rotation_range=30,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.15,
        zoom_range=0.25,
        horizontal_flip=True,
        fill_mode='nearest',
        brightness_range=[0.8, 1.2],
        validation_split=0.2
    )
    
    # Rescaling for testing using the same CLAHE logic
    test_datagen = ImageDataGenerator(preprocessing_function=medical_clahe_preprocessing)
    
    # Generators
    print("Loading datasets with CLAHE Preprocessing and 20% validation split...")
    train_gen = train_datagen.flow_from_directory(
        os.path.join(DATA_DIR, 'train'),
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='binary',
        subset='training',
        shuffle=True
    )
    
    val_gen = train_datagen.flow_from_directory(
        os.path.join(DATA_DIR, 'train'),
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='binary',
        subset='validation',
        shuffle=False
    )
    
    test_gen = test_datagen.flow_from_directory(
        os.path.join(DATA_DIR, 'test'),
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='binary',
        shuffle=False
    )
    
    # Compute Class Weights to handle imbalance
    y_train = train_gen.classes
    class_weights = compute_class_weight(
        class_weight='balanced',
        classes=np.unique(y_train),
        y=y_train
    )
    weight_dict = dict(enumerate(class_weights))
    print(f"Calculated Class Weights: {weight_dict}")
    
    # Build Model
    print("Building Optimized Deep Custom CNN (Architecture Maintained)...")
    model = build_deep_custom_cnn(input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3))
    model.summary()
    
    # Phase 2 Callbacks
    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor='val_accuracy', 
            patience=15, 
            restore_best_weights=True,
            mode='max',
            verbose=1
        ),
        tf.keras.callbacks.ModelCheckpoint(
            MODEL_SAVE_PATH, 
            monitor='val_accuracy', 
            save_best_only=True, 
            mode='max',
            verbose=1
        )
    ]
    
    # Training Loop
    print(f"Starting Phase 2 Optimized Training (Goal: 96% Accuracy)...")
    history = model.fit(
        train_gen,
        epochs=EPOCHS,
        validation_data=val_gen,
        class_weight=weight_dict,
        callbacks=callbacks,
        verbose=1
    )
    
    # Final Evaluation on Test Set
    print("\nFinal Evaluation on Test Set (624 images):")
    results = model.evaluate(test_gen)
    print(f"Test Accuracy: {results[1]:.4f}")
    print(f"Test Precision: {results[2]:.4f}")
    print(f"Test Recall: {results[3]:.4f}")
    
    # Plotting History (New: Save plots automatically)
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='train')
    plt.plot(history.history['val_accuracy'], label='val')
    plt.title('Accuracy Optimization')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='train')
    plt.plot(history.history['val_loss'], label='val')
    plt.title('Loss Optimization')
    plt.legend()
    
    plot_path = os.path.join(BASE_DIR, "output", "plots", "custom_cnn_optimization_v3_clahe.png")
    os.makedirs(os.path.dirname(plot_path), exist_ok=True)
    plt.savefig(plot_path)
    print(f"Optimization plots saved to: {plot_path}")
    
    return history

if __name__ == "__main__":
    train()

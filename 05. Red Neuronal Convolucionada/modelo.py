from keras.src.models import Sequential
from tensorflow.keras import layers
from keras.src.legacy.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
import numpy as np

# Modelo de red neuronal convolucional
model = Sequential(
    [
        layers.Conv2D(32, (3, 3), input_shape=(64, 64, 3), activation='relu'),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Flatten(),
        layers.Dense(units=128, activation='relu'),
        layers.Dense(units=2, activation='softmax')
    ]
)

# Compilacion del modelo
model.compile(loss='categorical_crossentropy', metrics=['accuracy'])

# Entrenamiento del modelo
train_data = ImageDataGenerator(
    rescale=1./255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True).flow_from_directory(
    'cnn/dataset/train', target_size=(64, 64), batch_size=32, class_mode='categorical')
test_data = ImageDataGenerator(rescale=1./255).flow_from_directory(
    'cnn/dataset/test', target_size=(64, 64), batch_size=32, class_mode='categorical')

model.fit(train_data, epochs=40, steps_per_epoch=int(5000), validation_steps=int(1000),
          validation_data=test_data)

# Obtener la imagen a predecir
img = "cnn/dataset/test/yo/Alexandra1.jpg"
test_img = image.load_img(img, target_size=(64, 64))
test_img = image.img_to_array(test_img)
test_img = np.expand_dims(test_img, axis=0)

# Predicicon
prediction = model.predict(test_img)
print(f'Prediccion: {'Famoso' if prediction[0][0] >= 0.5 else 'Alexandra ❤️'}')

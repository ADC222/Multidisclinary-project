from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
import cv2
import time

#AI set up
camera= cv2.VideoCapture(0)

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("A:/MP/New folder/keras_Model.h5", compile=False)


# Load the labels
class_names = open("A:/MP/New folder/labels.txt", "r").readlines()

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

def image_detector():
    ret, image= camera.read()
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
    cv2.imshow("Webcam Image", image)
    image= np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
    image = (image/127.5) -1
    prediction=model.predict(image)
    index=np.argmax(prediction)
    class_name=class_names[index]
    confidence_score= prediction[0][index]
    print("class:", class_name[2:], end="")
    print("Confidence Score:", str(np.round(confidence_score * 100))[:-2],"%")


size = (224, 224)


# Predicts the model
prediction = model.predict(data)
index = np.argmax(prediction)
class_name = class_names[index]
confidence_score = prediction[0][index]

while True:
    image_detector()
    time.sleep(5)
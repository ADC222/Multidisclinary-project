from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
import cv2 
import time

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("A:\MP\Project\MP/keras_model.h5", compile=False)

# Load the labels
class_names = open("A:\MP\Project\MP/labels.txt", "r").readlines()

camera= cv2.VideoCapture(0)



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
    
# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

# Replace this with the path to your image
#image = Image.open("A:\MP/test.jpeg").convert("RGB")

# resizing the image to be at least 224x224 and then cropping from the center
size = (224, 224)
#image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

# turn the image into a numpy array
#image_array = np.asarray(image)

# Normalize the image
#normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

# Load the image into the array
#data[0] = normalized_image_array

# Predicts the model
prediction = model.predict(data)
index = np.argmax(prediction)
class_name = class_names[index]
confidence_score = prediction[0][index]

# Print prediction and confidence score
#print("Class:", class_name[2:], end="")
#print("Confidence Score:", confidence_score)

while True:
    image_detector()
    time.sleep(5)
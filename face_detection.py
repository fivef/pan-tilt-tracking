from PIL import Image
import numpy as np
import face_recognition
import time
import requests
from io import BytesIO

while True:


	response = requests.get("http://octopi.local:8080/?action=snapshot")
	img = Image.open(BytesIO(response.content))

	start_time = time.time()

	# Load the jpg file into a numpy array
	#image = face_recognition.load_image_file("test.jpg")

	image = np.array(img)

	# Find all the faces in the image using the default HOG-based model.
	# This method is fairly accurate, but not as accurate as the CNN model and not GPU accelerated.
	# See also: find_faces_in_picture_cnn.py
	# number_of_times_to_upsample allows detection smaller faces, default is 1 (takes 5s per vga image)
	# 0 takes only 1.3s per vga image
	face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0)


	time_passed = time.time() - start_time

	print("Time passed {}s".format(time_passed))

	print("I found {} face(s) in this photograph.".format(len(face_locations)))

	for face_location in face_locations:

	    # Print the location of each face in this image
	    top, right, bottom, left = face_location
	    print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))

	    # You can access the actual face itself like this:
	    face_image = image[top:bottom, left:right]
	    pil_image = Image.fromarray(face_image)
	    pil_image.show()



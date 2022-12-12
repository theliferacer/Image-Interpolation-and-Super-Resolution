import matplotlib.pyplot as plt
from PIL import Image
from math import floor, ceil
import numpy as np
import os
import tensorflow as tf
import numpy as np
import random
import albumentations as aug
from math import ceil, floor
import cv2
import io

def nearest_neighbour(img, scale=4):
    img_np = np.array(img)
    (h, w, c) = img_np.shape
    new_img = np.zeros([int(h*scale), int(w*scale), 3])
    for i in range(int(h*scale)):
        for j in range(int(w*scale)):
            new_img[i, j]= img_np[int(i / scale),int(j / scale)]
    new_pil = Image.fromarray(np.uint8(new_img))
    return new_pil

def bilinear(img, scale=4):
    img_np = np.array(img)
    (h, w, c) = img_np.shape
    new_img = np.zeros([int(h*scale), int(w*scale), 3])
    
    for i in range (int(h * scale)):
        x1 = int(floor(i/scale))
        x2 = int(ceil(i/scale))
        if x1 == 0:
            x1 = 1
        if x2 == h:
            x2 -= 1
        x = i/scale % 1

        for j in range(int(w * scale)):
            y1 = int(floor(j/scale))
            y2 = int(ceil(j/scale))
            if y1 == 0:
                y1 = 1
            if y2 == w:
                y2 -= 1
            y = j/scale % 1

            a = img_np[x1, y1, :]
            b = img_np[x2, y1, :]
            c = img_np[x1, y2, :]
            d = img_np[x2, y2, :]

            left = (c*y) + (a*(1-y))
            right = (d*y) + (b*(1-y))
            new_img[i, j, :] = (right*x)+(left*(1-x))
    
    new_pil = Image.fromarray(np.uint8(new_img))
    
    return new_pil

model = tf.keras.models.load_model("./model.h5")

def fsrcnn_infer(img):
    img_np = np.array(img)
    w,h,c = img_np.shape
    new_img_np = np.zeros((ceil(w/162)*162, ceil(h/162)*162, c))
    new_img_np[:w,:h,:] = img_np
    new_img_np = np.expand_dims(new_img_np,0)
    new_pred = np.zeros((1, ceil(w/162)*648, ceil(h/162)*648, c))
    for i in range((ceil(w/162))):
        for j in range((ceil(h/162))):
            new_pred[:, i*648:(i+1)*648, j*648:(j+1)*648, :] = model.predict(new_img_np[:,i*162:(i+1)*162, j*162:(j+1)*162, :])
    pred = new_pred[0]
    pred = pred[:int((w*648)/162), :int((h*648)/162), :]
    pred_pil=Image.fromarray(np.uint8(np.clip(pred,0,255)))
    return pred_pil

#Resizing an image
def Resize(image):
	np_img = np.array(image)
	#Resizing the image by maintaining the aspect ratio r
	r = 600/np_img.shape[0]
	M = int(np_img.shape[1]*r)
	if M >= 1200:
		M = 1200
	else:
		M = M
	dim = (M,600)
	stretch_near = cv2.resize(np_img, dim,interpolation = cv2.INTER_AREA)
	pil_img = Image.fromarray(stretch_near)
	
	return pil_img

def compare(image):
	plt.subplot(2, 2, 1)
	nn = nearest_neighbour(image, scale = 4)
	plt.imshow(nn)
	plt.axis("off")
	plt.title("Nearest Neighbour")

	plt.subplot(2, 2, 2)
	bil = bilinear(image, scale = 4)
	plt.imshow(bil)
	plt.axis("off")
	plt.title("Bilinear")

	plt.subplot(2, 2, 3)
	fsr = fsrcnn_infer(image)
	plt.imshow(fsr)
	plt.axis("off")
	plt.title("FSRCNN")

	plt.subplot(2, 2, 4)
	hires = image
	plt.imshow(hires)
	plt.axis("off")
	plt.title("Original High Res")

	img_buf = io.BytesIO()
	plt.savefig(img_buf, format='png')

	pil_img = Image.open(img_buf)

	return pil_img
import cv2
import numpy as np
import sys
import math
import matplotlib.pyplot as plt
import argparse
import os
import glob
from skimage import img_as_float
from scipy.ndimage import gaussian_filter
from skimage.morphology import reconstruction
from scipy import ndimage as ndi
from skimage.feature import canny
import pylab
import mahotas as mh
from math import sqrt
from skimage.feature import blob_dog, blob_log, blob_doh

parse = argparse.ArgumentParser()
# imgName is the name of the image to be analyzed or the file name containing the images to be analyzed
# if the user wants to provide the composite and single color channel images, then imgName must be one image, not a file name
# otherwise if the user wants the pipeline to separate the image channels for them, they can provide either one image or a file name
parse.add_argument("-imgName",help="Put (path to) image name here or folder name of images here for multiple images")

# if inputting separate color channels, must put in color1, color2, color3 in order of the respective channels
parse.add_argument("-color1",help="enter channel color",default='green')
parse.add_argument("-color2",help="enter channel color",default='red')
parse.add_argument("-color3",help="enter channel color",default='blue')

parse.add_argument("-outputFolderName",help="Name of output file",default='results') 
# add in arguments to adjust parameters

args = parse.parse_args()

path = args.imgName

if os.path.isfile(path):
	imgNames = [args.imgName]

else:
	assert(os.path.isdir(path))
	pathToImages = ("%s/*.jpg" %path)
	imgNames = glob.glob(pathToImages)

def img_processing(img1):
	grayImage = img1
	grayImage_c = grayImage.copy()
		
	seed = np.copy(grayImage)
	seed[1:-1, 1:-1] = grayImage.min()
	mask = grayImage

	dilated = reconstruction(seed, mask, method='dilation')
	recons1 = (grayImage - dilated).astype('uint8')

	dnaf1 = mh.gaussian_filter(recons1, 1).astype('uint8')
	T1 = mh.thresholding.otsu(dnaf1)
	green_img = dnaf1>=T1

	# fig, (ax0, ax1) = plt.subplots(nrows=1, ncols=2, figsize=(8, 2.5), sharex=True, sharey=True)
	# ax0.imshow(grayImage, cmap='gray')
	# ax0.set_title('gray')
	# ax0.axis('off')

	# ax1.imshow(green_img, cmap='gray')
	# ax1.set_title('reconstructed')
	# ax1.axis('off')

	# fig.tight_layout()
	# plt.show()

	return green_img


if __name__ == "__main__":

	print('Starting')
	outputFolder = args.outputFolderName
	
	color1 = args.color1
	color2 = args.color2
	color3 = args.color3

	# go through each image, analyze each image, put results in Excel spreadsheet

	for i in range(0,len(imgNames)):

		compImageName = imgNames[i]

		compositeImage = cv2.imread(imgNames[i])

		blueImage,greenImage,redImage = cv2.split(compositeImage)
		# print(blueImage.shape)

		colorImgDict = {'red':redImage,
						'green':greenImage,
						'blue':blueImage}
	
		listOfColors = ['red','green','blue']
		j = 0
		imgShape = (compositeImage.shape)
		reconstructed = np.zeros((imgShape),'uint8')
		# print(reconstructed.shape)
		for color in listOfColors:
			imageToGetKPs = colorImgDict[color]
			reconstructed[:,:,j] = img_processing(imageToGetKPs)
			j += 1

		output_path = outputFolder+compImageName
		fig, (ax0) = plt.subplots(nrows=1, ncols=1, figsize=(8, 2.5), sharex=True, sharey=True)
		ax0.imshow(reconstructed, cmap='gray')
		ax0.set_title('gray')
		ax0.axis('off')	
		fig.tight_layout()
		plt.show()
		# print(output_path)
		# cv2.imwrite(output_path, reconstructed)





	
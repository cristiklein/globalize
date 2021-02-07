import cv2
import numpy as np
from PIL import Image, ImageDraw

# Input image to get rectangle (region of interest, roi) from
image = Image.open('/home/cklein/Downloads/20201206_181230.jpg')
roi = ((100, 30), (300, 200))

# Dummy output image with some quad to paste to
output = Image.new('RGB', (600, 800), (255, 255, 255))
draw = ImageDraw.Draw(output)
draw.polygon(((100, 20), (40, 740), (540, 350), (430, 70)), outline=(0, 0, 0))

# Convert images to NumPy arrays for processing in OpenCV
image_cv2 = np.array(image)
output_cv2 = np.array(output)

# Source points, i.e. roi in input image
tl = (roi[0][0], roi[0][1])
tr = (roi[1][0], roi[0][1])
br = (roi[1][0], roi[1][1])
bl = (roi[0][0], roi[1][1])
pts = np.array([bl, br, tr, tl])

# Find (or know) target points in output image w.r.t. the quad
# Attention: The order must be the same as defined by the roi points!
tl_dst = (100, 20)
tr_dst = (430, 70)
br_dst = (540, 350)
bl_dst = (40, 740)
dst_pts = np.array([bl_dst, br_dst, tr_dst, tl_dst])

# Get transformation matrix, and warp image
pts = np.float32(pts.tolist())
dst_pts = np.float32(dst_pts.tolist())
M = cv2.getPerspectiveTransform(pts, dst_pts)
image_size = (output_cv2.shape[1], output_cv2.shape[0])
warped = cv2.warpPerspective(image_cv2, M, dsize=image_size)

# Get mask from quad in output image, and copy content from warped image
gray = cv2.cvtColor(output_cv2, cv2.COLOR_BGR2GRAY)
gray = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)[1]
cnts = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
mask = np.zeros_like(output_cv2)
mask = cv2.drawContours(mask, cnts, 0, (255, 255, 255), cv2.FILLED)
mask = mask.all(axis=2)
output_cv2[mask, :] = warped[mask, :]

# Transform back to PIL images
output_new = Image.fromarray(output_cv2)
output_new.save('final_output.jpg')

# Just for visualization
import matplotlib.pyplot as plt
draw = ImageDraw.Draw(image)
draw.rectangle(roi, outline=(255, 0, 0), width=3)
plt.figure(0, figsize=(18, 9))
plt.subplot(1, 3, 1), plt.imshow(image), plt.title('Input with ROI')
plt.subplot(1, 3, 2), plt.imshow(output), plt.title('Output with quad')
plt.subplot(1, 3, 3), plt.imshow(output_new), plt.title('Final output')
plt.tight_layout(), plt.show()

import cv2
import numpy as np
from PIL import Image, ImageDraw

def transform_roi_to_quad(simg, dimg, src, dst):
    '''
    Transforms a source rectangle image into a destination quad.

    Parameters
    ----------
    simg : PIL.Image
        Source image
    dimg : PIL.Image
        Destination image
    src : tuple of Point
        Region of interest in the source image
    dst : tuple of Point
        Quad in the destination image

    `src` is given as `(tl, br)`. E.g., `((0, 0), (100, 100))` takes the
    rectangle from x=0, y=0 to x=100, y=100.

    `dst` is given as `(tl, tr, br, bl)`, where each point is `(x, y)`.
    '''
    # Convert images to NumPy arrays for processing in OpenCV
    simg_cv2 = np.array(simg)
    dimg_cv2 = np.array(dimg)

    # Source points, i.e. roi in input image
    roi = src
    tl = (roi[0][0], roi[0][1])
    tr = (roi[1][0], roi[0][1])
    br = (roi[1][0], roi[1][1])
    bl = (roi[0][0], roi[1][1])
    pts = np.array([tl, tr, br, bl])

    # Find (or know) target points in output image w.r.t. the quad
    # Attention: The order must be the same as defined by the roi points!
    dst_pts = np.array(dst)

    # Get transformation matrix, and warp image
    pts = np.float32(pts.tolist())
    dst_pts = np.float32(dst_pts.tolist())
    M = cv2.getPerspectiveTransform(pts, dst_pts)
    image_size = (dimg_cv2.shape[1], dimg_cv2.shape[0])
    warped = cv2.warpPerspective(simg_cv2, M, dsize=image_size)

    # Get mask from quad in output image, and copy content from warped image
    mask = np.zeros_like(dimg_cv2)
    mask = cv2.fillConvexPoly(mask, np.int32(dst_pts), (255, 255, 255))
    mask = mask.all(axis=2)
    dimg_cv2[mask, :] = warped[mask, :]

    # Just for visualization
    import matplotlib.pyplot as plt

    simg_with_roi = Image.fromarray(simg_cv2)
    draw = ImageDraw.Draw(simg_with_roi)
    draw.rectangle(roi, outline=(255, 0, 0), width=5)
    
    warped_with_dst = Image.fromarray(warped)
    draw = ImageDraw.Draw(warped_with_dst)
    draw.polygon((dst), outline=(255, 0, 0))

    plt.figure(0, figsize=(18, 9))
    plt.subplot(1, 5, 1), plt.imshow(simg_with_roi), plt.title('Source Image with ROI')
    plt.subplot(1, 5, 2), plt.imshow(warped_with_dst), plt.title('Warped with dst')
    plt.subplot(1, 5, 4), plt.imshow(mask), plt.title('Mask')
    plt.subplot(1, 5, 5), plt.imshow(dimg_cv2), plt.title('Dimg')
    plt.tight_layout(), plt.show()

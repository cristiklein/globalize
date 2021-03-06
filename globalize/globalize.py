import os
import sys

import numpy as np
from PIL import Image, ImageDraw

from .transform import transform_roi_to_quad

def globalize(
        inputFilename,
        outputFilename,
        tropicsToEquatorRatio = 0.9,
        polesToEquatorRatio = 0.6,
    ):
    simg = Image.open(inputFilename)
    (w, h) = simg.size

    # Back the image with numpy arrays
    simg_np = np.asarray(simg)
    dimg_np = np.full_like(simg_np, (255, 255, 255))

    rt = tropicsToEquatorRatio
    rp = polesToEquatorRatio

    for xsection in range(8):
        for ysection in range(5):
            x0 = (w // 8) * (xsection)
            x1 = (w // 8) * (xsection + 1) - 1
            y0 = (h // 5) * (ysection)
            y1 = (h // 5) * (ysection + 1) - 1

            if ysection in [ 0, 4 ]:
                # North/South Pole
                xlt = int(x0*(rp) + x1*(1-rp))
                xrt = int(x1*(rp) + x0*(1-rp))

                xlb = int(x0*(rt) + x1*(1-rt))
                xrb = int(x1*(rt) + x0*(1-rt))

            elif ysection in [ 1, 3 ]:
                # North/South of equator
                xlt = int(x0*rt + x1*(1-rt))
                xrt = int(x1*rt + x0*(1-rt))

                xlb = x0
                xrb = x1

            else:
                # Equator
                xlt, xrt, xrb, xlb = x0, x1, x1, x0

            if ysection >= 3:
                # South
                xlt, xlb = xlb, xlt
                xrt, xrb = xrb, xrt

            p1 = (xlt, y0)
            p2 = (xrt, y0)
            p3 = (xrb, y1)
            p4 = (xlb, y1)

            transform_roi_to_quad(simg_np, dimg_np,
                src = ((x0, y0), (x1, y1)),
                dst = (p1, p2, p3, p4)
            )
    dimg = Image.fromarray(dimg_np)
    dimg.save(outputFilename)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} input.jpg")
        raise SystemExit()

    inputFilename = sys.argv[1]
    basePath, baseExt = os.path.splitext(inputFilename)
    outputFilename = basePath + '-globalized' + baseExt

    print(f"Globalizing {inputFilename} to {outputFilename}")
    globalize(inputFilename, outputFilename)

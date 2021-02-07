import os
import sys

from PIL import Image, ImageDraw

from .transform import transform_roi_to_quad

def globalize(inputFilename, outputFilename, tropicsToEquatorRatio = 0.8):
    simg = Image.open(inputFilename)
    (w, h) = simg.size
    dimg = Image.new('RGB', simg.size, 'white')

    r = tropicsToEquatorRatio

    draw = ImageDraw.Draw(dimg)
    for xsection in range(8):
        for ysection in range(4):
            x0 = (w // 8) * (xsection)
            x1 = (w // 8) * (xsection + 1) - 1
            y0 = (h // 4) * (ysection)
            y1 = (h // 4) * (ysection + 1) - 1

            if ysection in [ 0, 3 ]:
                # North/South Pole
                xlt = (x0+x1)//2
                xrt = (x0+x1)//2

                xlb = int(x0*r+x1*(1-r))
                xrb = int(x1*r+x0*(1-r))

            else:
                # North/South of equator
                xlt = int(x0*r + x1*(1-r))
                xrt = int(x1*r + x0*(1-r))

                xlb = x0
                xrb = x1

            if ysection >= 2:
                # South
                xlt, xlb = xlb, xlt
                xrt, xrb = xrb, xrt

            p1 = (xlt, y0)
            p2 = (xrt, y0)
            p3 = (xrb, y1)
            p4 = (xlb, y1)

            draw.line([p1, p2, p3, p4, p1], fill = 'black', width = 10)

            if xsection == 0 and ysection == 0:
                transform_roi_to_quad(simg, dimg,
                    src = ((x0, y0), (x1, y1)),
                    dst = (p1, p2, p3, p4)
                )
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

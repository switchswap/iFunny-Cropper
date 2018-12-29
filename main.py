import os
import math
from PIL import Image

THRESHOLD = 8
INPUT_DIRECTORY = "./iFunny"
OUTPUT_DIRECTORY = "./output/"


# Get color difference
def color_difference(pixel1, pixel2):
    difference = math.sqrt(
        abs(pixel2[0] - pixel1[0]) ** 2 + abs(pixel2[1] - pixel1[1]) ** 2 + abs(pixel2[2] - pixel1[2]) ** 2)
    return difference


# Assumes image has watermark and attempts to crop
def crop():
    for file in os.listdir(INPUT_DIRECTORY):  # For each file in directory
        filename = os.fsdecode(file)  # Get filename
        if filename.endswith(".jpg"):
            img = Image.open(INPUT_DIRECTORY + "/" + filename)
            pix = img.load()
            width, length = img.size
            curr_y = length - 1

            # While color difference is less than threshold, move up and decrease Y height
            while color_difference(pix[0, curr_y], pix[0, length - 1]) < THRESHOLD:
                curr_y = curr_y - 1
            watermark_size = length - curr_y

            # For possible bad crops since the average watermark size is 21 pixels or less
            cropped = img.crop((0, 0, width, length - watermark_size))
            if watermark_size > 21:
                print("[Skipped]:", filename, watermark_size)
                # img.show()
                # cropped.show()
            else:  # Save image
                cropped.save(OUTPUT_DIRECTORY + filename, format='JPEG', subsampling=0, quality=100)


# Just check image for iFunny watermark
def has_watermark():
    pass


def menu():
    print("Cropping images...")
    crop()
    print("Done")


if __name__ == "__main__":
    menu()

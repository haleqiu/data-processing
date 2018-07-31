import os, cv2
import argparse

from utils_tool import utils_tool

"""
image2video
Author: Hale Qiu

Convert image to video
Argument:
--video is the output video file, take care of directory
--image is the image directory
--fps is the output frame per seconds

Notice: the count is %03d%  for the sake of Hale's data (0=_=0)
"""

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('--video', type=str, default = "./Video/out.avi")
parser.add_argument('--image', type=str, default= "./Image")
parser.add_argument('--fps', type=int, default= 1)
parser.add_argument('--size', type=tuple, default= (701,701))
args = parser.parse_args()


def main(args):
    Video_Path = args.video
    Image_Path = args.image

    fps = args.fps
    fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
    img_size=(701,701)
    videowrite(Video_Path,Image_Path,fourcc,fps,img_size)


def videowrite(video_path, image_path, fourcc, fps, img_size):
    videoWriter = cv2.VideoWriter(video_path, fourcc, fps, img_size)
    #file_dir="RAD_206482414212530_"
    file_dir=[]
    utils_tool.ldir(image_path,file_dir)
    file_name_prefix = file_dir[0][0:-7]
    for i in range(0,len(file_dir)):
        index = "%03d" %i
        img = cv2.imread(file_name_prefix+str(index)+".png")
        print(file_name_prefix+str(index)+".png")

        videoWriter.write(img)
    videoWriter.release()


if __name__ == "__main__":
   main(args)

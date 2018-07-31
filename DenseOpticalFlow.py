import cv2, argparse, sys
import numpy as np

from utils_tool import visual

'''
image2video
Author: Hale Qiu

In this optical flow script, processing the video and output the generate result
in image.
The goal is to visualize, thus hsv and vetor are provided for visualization
'''

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('--video', type=str, default = "/Users/qiuyuheng/env2/data-processing/doc/raw-data-gray.avi")
parser.add_argument('--image', type=str, default= "./Image")
parser.add_argument('--type', type=str, default= "video")
parser.add_argument('--mode', type=str, default= "vector")
args = parser.parse_args()


def main():
    cap = cv2.VideoCapture(args.video)
    ret, frame1 = cap.read()
    prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
    hsv = np.zeros_like(frame1)
    hsv[...,1] = 255
    count=0
    while(ret):
        ret, frame2 = cap.read()
        if not ret:
            #break when no frame in video
            break
        next = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(prvs,next, None, 0.5, 3, 15, 3, 5, 1.2, 0)

        index = "%03d" %count
        count+=1
        if args.mode == "vector":
            flow_visual=visual.draw_flow(prvs, flow)
            cv2.imwrite("./Output/"+str(index)+".png",flow_visual)
            cv2.imshow("vector",flow_visual)

        elif args.mode == "hsv":
            flow_visual=visual.hsv_visual(prvs, flow)
            cv2.imwrite("./Output/"+str(index)+".png",flow_visual)
            cv2.imshow("hsv",flow_visual)

        print("./Output/"+str(index)+".png")
        #cv2.imwrite("./Output/hsv/"+str(index)+".png",hsv)
        #cv2.imwrite("./Output/bgr/"+str(index)+".png",bgr)
        prvs = next

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()

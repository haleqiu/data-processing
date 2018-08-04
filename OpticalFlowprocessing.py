import cv2,time
import os
import numpy as np
import argparse
from utils_tool import utils_tool, visual

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('--output', type=str, default = "./Output")
parser.add_argument('--image', type=str, default= "./Image")
parser.add_argument('--mode', type=str, default= "single")
parser.add_argument('--size', type=tuple, default= (501,501))
args = parser.parse_args()


def batch_processing(image_folder,output_folder):
    input_folder_list = os.listdir(image_folder)
    folder_num = len(input_folder_list)
    print("total-folder: " + str(folder_num))
    for i in range(len(input_folder_list)):
        if os.path.isfile(image_folder+"/"+input_folder_list[i]):
            single_processing((image_folder+"/"+input_folder_list[i]),\
                              (output_folder+"/"+input_folder_list[i]))
        else:
            print("not directory")
            folder_num-=1
    print("done"+ str(len(input_folder_list)))


def single_processing(image_path, output_path, mod="image"):
    start = time.clock()
    file_dir=[]
    utils_tool.ldir(image_path,file_dir)
    file_name_prefix=file_dir[0][0:-7]
    #print(file_name_prefix)
    for i in range(0,len(file_dir)-1):
        index1 = "%03d" %i
        index2 = "%03d" %(i+1)
        #print(file_name_prefix+str(index)+".png")
        raw_image1=cv2.imread(file_name_prefix+str(index1)+".png")
        raw_image2=cv2.imread(file_name_prefix+str(index2)+".png")
        prvs = raw_image1[:,:,1]
        next = raw_image2[:,:,1]
        flow = cv2.calcOpticalFlowFarneback(prvs,next, \
        None, 0.5, 3, 15, 3, 5, 1.2, 0)

        isExists=os.path.exists(output_path)
        if not isExists:
            os.makedirs(output_path)

        if mod == "image":
            hsv_image = hsv_visual(flow)
            cv2.imwrite(output_path+ "/hsv_image_" + index1 + ".png",hsv_image)
        elif mod == "matrix":
            pass
    elapsed = (time.clock() - start)
    print("time: "+str(elapsed))


def batch_optical_flow(rawdata):

    flow_list = list()
    for i in range(0,len(rawdata)-1):
        prvs = rawdata[i]
        now = rawdata[i+1]
        if prvs.ndim == 3:
            prvs = cv2.cvtColor(prvs,cv2.COLOR_BGR2GRAY)
            now = cv2.cvtColor(now,cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(prvs,now, \
        None, 0.5, 3, 15, 3, 5, 1.2, 0)
        flow_list.append(flow)
    return flow_list


def matrix_processing(image_path,output_path):
    flow_list = batch_optical_flow(raw_list)



def smooth_processing(image_folder,output_folder, scal = 3):
    smooth_flow_list = list()
    input_folder_list = os.listdir(image_folder)
    folder_num = len(input_folder_list)
    print("total-folder: " + str(folder_num))
    for i in range(len(input_folder_list)):
        output_path = (output_folder+"/"+input_folder_list[i])
        isExists=os.path.exists(output_path)
        if not isExists:
            os.makedirs(output_path)

        raw_list = list()
        #print(image_folder+"/"+input_folder_list[i])
        if os.path.isdir(image_folder+"/"+input_folder_list[i]):
            start = time.clock()
            file_dir=[]
            image_path = image_folder+"/"+input_folder_list[i]
            utils_tool.ldir(image_path,file_dir)
            file_name_prefix=file_dir[0][0:-7]
            raw_list = list()

            for i in range(0,len(file_dir)-1):
                index = "%03d" %i
                raw_image = cv2.imread(file_name_prefix+str(index)+".png")
                raw_list.append(raw_image)
            flow_list = batch_optical_flow(raw_list)

            for i in range(0,len(flow_list)):
                index = "%03d" %i
                now = flow_list[i]
                if i ==0:
                    prvs = flow_list[i]
                else:
                    prvs = flow_list[i-1]
                if i == len(flow_list)-1:
                    next = flow_list[i]
                else:
                    next = flow_list[i+1]

                smpoth_flow = (prvs + now + next)/3
                smooth_flow_list.append(smpoth_flow)
                hsv_image = visual.hsv_visual(smpoth_flow)
                cv2.imwrite(output_path+ "/hsv_image_" + index + ".png",hsv_image)

        else:
            print("not directory")
            folder_num-=1
    flow_list = batch_optical_flow(raw_list)
    print("done"+ str(len(input_folder_list)))
    return smooth_flow_list

def main():
    print("using mode"+str(args.mode))
    if args.mode == "single":
        single_processing(args.image,args.output)
    elif args.mode == "batch":
        batch_processing(args.image, args.output)
    elif args.mode == "matrix":
        # notice the image x and y [y,x] in opencv
        matrix_processing(args.image, args.output)
    elif args.mode == "smooth_batch":
        smpoth_flow_list = smooth_processing(args.image, args.output)

if __name__ == '__main__':
    main()

import cv2,os,time
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('--output', type=str, default = "./Output")
parser.add_argument('--image', type=str, default= "./Image")
parser.add_argument('--mode', type=str, default= "single")
parser.add_argument('--size', type=tuple, default= (501,501))
args = parser.parse_args()

def hsv_visual(frame,flow):
    hsv = np.zeros_like(frame)
    hsv[...,1] = 255
    mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
    hsv[...,0] = ang*180/np.pi/2
    hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
    bgr = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
    #print(hsv[320][475])
    #print(bgr[320][475])
    return bgr

def batch_processing(image_folder,output_folder):
    input_folder_list = os.listdir(image_folder)
    print("total-folder: " + str(len(input_folder_list)))
    for i in range(len(input_folder_list)):
        single_processing((image_folder+"/"+input_folder_list[i]),\
                          (output_folder+"/"+input_folder_list[i]))

def ldir(path, list_name, re = False):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path) and re:
            ldir(file_path, list_name)
        elif os.path.splitext(file_path)[1]=='.png':
            list_name.append(file_path)

def single_processing(image_path, output_path):
    start = time.clock()
    file_dir=[]
    ldir(image_path,file_dir)
    file_name_prefix=file_dir[0][0:-7]
    print(file_name_prefix)
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
        hsv_image = hsv_visual(raw_image1,flow)

        isExists=os.path.exists(output_path)
        if not isExists:
            os.makedirs(output_path)
        #print(output_path+ "/hsv_image_" + index1)
        cv2.imwrite(output_path+ "/hsv_image_" + index1 + ".png",hsv_image)
    elapsed = (time.clock() - start)
    print("time: "+str(elapsed))


def main():
    if args.mode == "single":
        single_processing(args.image,args.output)
    else:
        print(args.image + args.output)
        batch_processing(args.image, args.output)

if __name__ == '__main__':
    main()

import sys, os, cv2


Video_Path="./Video"
Image_Path="./Image"

def main(argv):
    if len(argv) > 1:
        Video_Path = argv[1]
        Image_Path = argv[2]

    vc=cv2.VideoCapture(Video_Path)

    if not vc.isOpened():
        print("error happened on vc")
    else:
        count = 1
        while vc.isOpened():
            rval,frame=vc.read()
            cv2.imwrite(Image_Path+'/Image'+str(count)+'.jpg',frame)
            count+=1
            cv2.waitKey(1)

    vc.release()


if __name__ == "__main__":
   main(sys.argv)

import os, cv2
import argparse
from matplotlib import pyplot as plt

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('--output', type=str, default = "./Output/")
parser.add_argument('--image', type=str, default= "./Image")
parser.add_argument('--name', type=str, default= "Image")
parser.add_argument('--mode', type=str, default= "gray")
parser.add_argument('--frame', type=int, default= 1)
args = parser.parse_args()


def main(args):
    Output_Path = args.output
    Image_Path = args.image
    #view_all = matrix

    file_dir=[]
    ldir(Image_Path,file_dir)
    file_name_prefix=file_dir[0][0:-7]
    print(file_name_prefix)
    for i in range(0,len(file_dir)):
        index = "%03d" %i
        print(file_name_prefix+str(index)+".png")
        raw_image=cv2.imread(file_name_prefix+str(index)+".png")
        image = raw_image[:,:,1]
        scal(image)
        if args.mode == "gray":
            cv2.imwrite(Output_Path+str(index)+".png",image)
        elif args.mode == "color":
            plt.matshow(image, cmap=plt.cm.jet)
            plt.axis('off')

            fig = plt.gcf()
            fig.set_size_inches(5.01/3,5.01/3)
            plt.gca().xaxis.set_major_locator(plt.NullLocator())
            plt.gca().yaxis.set_major_locator(plt.NullLocator())
            plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
            plt.margins(0,0)
            fig.savefig(Output_Path+str(index)+".png", format='png', transparent=True, dpi=300, pad_inches = 0)


def ldir(path, list_name, re = False):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path) and re:
            ldir(file_path, list_name)
        elif os.path.splitext(file_path)[1]=='.png':
            list_name.append(file_path)

def scal(image):
    for i in range(len(image)):
        for j in range(len(image[i])):
            if image[i][j]==255:
                image[i][j]= 0
                image[i][j]=int(image[i][j]*80/256)

if __name__ == "__main__":
   main(args)

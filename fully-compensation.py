import cv2, copy
import numpy as np
import argparse
import matplotlib.pyplot as plt



def main():
    cap = cv2.VideoCapture("/Users/qiuyuheng/env2/data-processing/doc/raw-data-gray.avi")
    ret, frame = cap.read()
    count = 0
    rawdata = list()
    while ret:
        rawdata.append(frame)
        ret, frame = cap.read()
        count+=1

    sum_vpx,sum_vpy,orf = push_forward(count,rawdata)
    sum_vbx,sum_vby,orb = push_backward(count,rawdata)
    fully_compense(sum_vpx,sum_vpy,sum_vbx,sum_vby,orf,orb,count,rawdata)


def matrix_compensa(matrix,length):
    height = matrix.shape[1]
    width = matrix.shape[0]

    hor = np.zeros((width,length))
    vec = np.zeros((length,height + length * 2))

    #print(matrix.shape)
    result = np.hstack((matrix,hor))
    result = np.hstack((hor,result))
    result = np.vstack((vec,result))
    result = np.vstack((result,vec))

    #for i in range(length,length+width):

     #   result[501+length][i] = 1
      #  result[length][i] = 1
       # result[i][501+length] = 1
        #result[i][length] = 1
    return result


def blackalize(frame):
    height = frame.shape[1]
    width = frame.shape[0]
    result = np.zeros((height,width))
    for i in range(width):
        for j in range(height):
            zero = (frame[i][j]==0).all()
            if not zero:
                result[i][j] =255;
    return result

def hsv_visual(frame,flow):
    hsv = np.zeros_like(frame1)
    hsv[...,1] = 255
    mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
    hsv[...,0] = ang*180/np.pi/2
    hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
    bgr = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
    #print(hsv[320][475])
    #print(bgr[320][475])
    return bgr

def push_forward(count,rawdata):
    points_x=list()
    points_y=list()
    oringinal_points=list()
    vpx = list()
    vpy = list()
    orp=list()
    for cou in range(count-1):
        print(str(cou))

        frame1 = rawdata[cou]
        frame2 = rawdata[cou+1]

        prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
        now = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(prvs,now, None, 0.5, 3, 15, 3, 5, 1.2, 0)

        fx = flow[...,0]
        fy = flow[...,1]
        y, x = np.mgrid[0:501, 0:501]
        x2=x+fx.astype(int)
        y2=y+fy.astype(int)

        for i in vpx:
            i[1]=i[1]+i[0]
        for j in vpy:
            j[1]=j[1]+j[0]

        for i in range(10,491):
            for j in range(10,491):
                if y2[i][j] >= 491 or \
                x2[i][j] >= 491 or \
                y2[i][j] < 10 or \
                x2[i][j] < 10:
                    vpx.append([fx[i][j],x2[i][j]])
                    vpy.append([fy[i][j],y2[i][j]])
                    orp.append(prvs[i][j])

                    #newcframe[x2[i][j],y2[i][j]]=prvs[x[i][j],y[i][j]]
                    #print([i,j])
        temp1=copy.deepcopy(vpx)
        temp2=copy.deepcopy(vpy)
        temp3=copy.deepcopy(orp)
        points_x.append(temp1)
        points_y.append(temp2)
        oringinal_points.append(temp3)
        #print(len(oringinal_points[cou]))
        #for i in range(len(vpx)):
            #cv2.circle(vis, (int(vpx[i][1]+100), int(vpy[i][1]+100)), 1, (255, 0, 0), -1)
        #cv2.imwrite("./Image/im"+ str(index) +".png",vis)

    return points_x, points_y, oringinal_points



def push_backward(count,rawdata):
    points_x=list()
    points_y=list()
    oringinal_points=list()

    vbx = list()
    vby = list()
    orp=list()
    for index in range(1,count):
        print(str(index))
        ind = "%03d" %(index-1)
        frame1 = rawdata[count-index]
        frame2 = rawdata[count-(index+1)]

        prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
        now = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(prvs,now, None, 0.5, 3, 15, 3, 5, 1.2, 0)


        fx = flow[...,0]
        fy = flow[...,1]
        y, x = np.mgrid[0:501, 0:501]
        x2=x + fx.astype(int)
        y2=y + fy.astype(int)

        #newcframe = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
        #newcframe = matrix_compensa(newcframe,100)
        vis = cv2.cvtColor(newcframe.astype(np.uint8), cv2.COLOR_GRAY2BGR)

        for i in vbx:
            i[1]=i[1]+i[0]
        for j in vby:
            j[1]=j[1]+j[0]

        for i in range(10,491):
            for j in range(10,491):
                if y2[i][j] >= 491 or \
                x2[i][j] >= 491 or \
                y2[i][j] < 10 or \
                x2[i][j] < 10:
                    vbx.append([fx[i][j],x2[i][j]])
                    vby.append([fy[i][j],y2[i][j]])
                    orp.append(prvs[i][j])

                    #newcframe[x2[i][j],y2[i][j]]=prvs[x[i][j],y[i][j]]
                    #print([i,j])
        #for i in range(len(vbx)):
        #    cv2.circle(vis, (int(vbx[i][1]+100), int(vby[i][1]+100)), 1, (255, 0, 0), -1)
        #cv2.imwrite("./Output/im"+ str(ind) +".png",vis)
        temp1=copy.deepcopy(vbx)
        temp2=copy.deepcopy(vby)
        temp3=copy.deepcopy(orp)
        points_x.append(temp1)
        points_y.append(temp2)
        oringinal_points.append(temp3)

    return points_x,points_y,oringinal_points


def fully_compense(sum_vpx,sum_vpy,sum_vbx,sum_vby,orf,orb,count,rawdata):

    for i in range(count):
        index = "%03d" %i
        print(i)
        newcframe = cv2.cvtColor(rawdata[i],cv2.COLOR_BGR2GRAY)
        newcframe = matrix_compensa(newcframe,100)
        vis = cv2.cvtColor(newcframe.astype(np.uint8), cv2.COLOR_GRAY2BGR)
        if i >0:
            for j in range(len(sum_vpx[i-1])):
                value = int(orf[i-1][j])
                cv2.circle(vis, (int(sum_vpx[i-1][j][1]+100), int(sum_vpy[i-1][j][1]+100)), 1, (0,value, 0), -1)
        if i <60:
            for k in range(len(sum_vbx[count-2-i])):
                value = int(orb[count-2-i][k])
                cv2.circle(vis, (int(sum_vbx[count-2-i][k][1]+100), int(sum_vby[count-2-i][k][1]+100)), 1, (0,value, 0), -1)
        cv2.imwrite("./Output/im"+ str(index) +".png",vis)


if __main__ = "main":
    main()

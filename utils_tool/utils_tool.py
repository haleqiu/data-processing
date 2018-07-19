# This is the util_tool
import cv2,time,os
import numpy as np

def warp_flow(img, flow):
    h, w = flow.shape[:2]
    flow = -flow
    flow[:,:,0] += np.arange(w)
    flow[:,:,1] += np.arange(h)[:,np.newaxis]
    res = cv.remap(img, flow, None, cv.INTER_LINEAR)
    return res


def ldir(path, list_name, re=False):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path) and re:
            ldir(file_path, list_name)
        elif os.path.splitext(file_path)[1]=='.png':
            list_name.append(file_path)


def matrix_compensa(matrix,length):
    height = matrix.shape[1]
    width = matrix.shape[0]

    if matrix.ndim == 2:
        hor = np.zeros((width,length))
        vec = np.zeros((length,height + length * 2))
    elif matrix.ndim == 3:
        depth = matrix.shape[2]
        hor = np.zeros((width,length,depth))
        vec = np.zeros((length,height + length * 2,depth))

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

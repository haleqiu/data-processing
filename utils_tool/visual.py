def create_gif(gif_name, path, duration = 0.3):
    '''
    生成gif文件，原始图片仅支持png格式
    gif_name ： 字符串，所生成的 gif 文件名，带 .gif 后缀
    path :      需要合成为 gif 的图片所在路径
    duration :  gif 图像时间间隔
    '''

    frames = []
    pngFiles = os.listdir(path)
    image_list = [os.path.join(path, f) for f in pngFiles]
    for image_name in image_list:
        # 读取 png 图像文件
        frames.append(imageio.imread(image_name))
    # 保存为 gif
    imageio.mimsave(gif_name, frames, 'GIF', duration = duration)


def hsv_visual(flow):
    hsv = np.zeros((flow.shape[0],flow.shape[1],3)).astype(np.uint8)
    hsv[...,1] = 255
    mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])

    hsv[...,0] = ang*180/np.pi/2
    hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)

    bgr = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)

    return bgr


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


def boundary(frame,length,ind =0 ):
    if frame.ndim == 2:
        frame = cv2.cvtColor(frame.astype(np.uint8),cv2.COLOR_GRAY2BGR)

    height = frame.shape[1]
    width = frame.shape[0]

    for i in range(length,width-length):
        frame[i][length][2]=255
        frame[i][height-length][2]=255
    for j in range(length,height-length):
        frame[length][j][2]=255
        frame[width-length][j][2]=255

    return frame

import cv2
import numpy as np
from sklearn.decomposition import PCA

def RGB2Gray(image):
    image = image[...,::-1].copy() # chuyển đổi BGR thành RGB
    # tách 3 kênh màu của ảnh
    red, green, blue = image[:,:,0], image[:,:,1], image[:,:,2]
    gray = 0.2989*red + 0.5870*green + 0.1140*blue
    return gray.astype(np.uint8) # chuyển đổi định dạng của ảnh về kiểu dữ liệu uint8 (giá trị pixel 0-255)

def Brightness(image, C):
    result = image + C
    # giá trị trong ma trận cộng với C mà > 255 thì sẽ được gán thành 255
    # còn < 0 thì sẽ được gán là 0
    result = np.clip(result, 0, 255)
    return result.astype(np.uint8)
    
def Contrast(image, C):
    result = image * C
    # giá trị trong ma trận cộng với C mà > 255 thì sẽ được gán thành 255
    # còn < 0 thì sẽ được gán là 0
    result = np.clip(result, 0, 255)
    return result.astype(np.uint8)
    
def CircleCrop(image):
    mask = mask = np.zeros(image.shape[:2], np.uint8)

    # Define the circle parameters: center (x, y) and radius
    center = (image.shape[1]//2, image.shape[0]//2)
    radius = min(center)

    # Draw a white circle on the mask
    cv2.circle(mask, center, radius, (255, 255, 255), thickness=-1)

    # Bitwise-and for Region of Interest
    result = cv2.bitwise_and(image, image, mask=mask)
    result = result[center[1]-radius:center[1]+radius+1, center[0]-radius:center[0]+radius+1]
    return result.astype(np.uint8)

def RGB2Sep(image):
    img = image.copy()
    # Tạo ma trận Sepia
    sepia_matrix = np.array([[0.393, 0.769, 0.189],
                             [0.349, 0.686, 0.168],
                             [0.272, 0.534, 0.131]])
    # Vì ảnh được stack theo cột nên ta cần chuyển vị ma trận sepia để phù hợp cho phép nhân ma trận
    img = img.dot(sepia_matrix.T)
    # gán các ma trận vượt ngưỡng = 255
    img[img > 255] = 255
    return img.astype(np.uint8)

def flipVertical(image):
    img = image.copy()
    h = img.shape[1]
    
    for i in range(h // 2):
        col = img[:, i, :].copy()
        img[:, i, :] = img[:, h - i - 1, :]
        img[:, h - i - 1, :] = col

    return img.astype(np.uint8)

def flipHorizontal(image):
    img = image.copy()
    w = img.shape[0]
    
    for i in range(w // 2):
        row = img[i, :, :].copy()
        img[i, :, :] = img[w - i - 1, :, :]
        img[w - i - 1, :, :] = row

    return img.astype(np.uint8)
    
def BlurImg(image):
    def gaussian_filter(k=5): # return gaussian mask matrix
        sigma = 1.5
        center = k // 2
        x, y = np.mgrid[0:k, 0:k] # tạo mảng 2D có giá trị mỗi ô 0->(k-1)
        g = (1/(2*np.pi*(sigma**2)))*np.exp(-((x - center)**2 + (y - center)**2) / (2 * sigma**2))
        return g / g.sum()
    
    kernel = gaussian_filter()
    blurred = cv2.filter2D(image, -1, kernel)
    return blurred.astype(np.uint8)

def CropCenter(image):
    image_height, image_width, _ = image.shape

    # trung tâm
    c_height = (image_height - 1) // 2
    c_width = (image_width - 1) // 2
    dist_row = c_height // 2
    dist_col = c_width // 2

    # xén hình
    result = image[dist_row:c_height+dist_row+1, dist_col:c_width+dist_col+1,:]

    return result.astype(np.uint8)

def EdgeDetection(image, low, high):
    img = RGB2Gray(image)
    blurred = cv2.GaussianBlur(src=img, ksize=(3, 5), sigmaX=0.5) 
    result = cv2.Canny(blurred,threshold1=low, threshold2=high)
    return result

def pca_compressor(image, k):
    red = image[:,:,0]
    green = image[:,:,1]
    blue = image[:,:,2]

    pca = PCA(k)
    #Applying to red channel and then applying inverse transform to transformed array.
    red_transformed = pca.fit_transform(red)
    red_inverted = pca.inverse_transform(red_transformed)
    
    #Applying to Green channel and then applying inverse transform to transformed array.
    green_transformed = pca.fit_transform(green)
    green_inverted = pca.inverse_transform(green_transformed)
    
    #Applying to Blue channel and then applying inverse transform to transformed array.
    blue_transformed = pca.fit_transform(blue)
    blue_inverted = pca.inverse_transform(blue_transformed)

    img_reduced = (np.dstack((red_inverted, green_inverted, blue_inverted))).astype(np.uint8)
    return img_reduced
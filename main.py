import cv2
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import os
import mediapipe as mp

#TODO: idea... add functionality for user uploading files and handling segmentation approvals 
#               from a web interface or mobile app then sexify

# Parent Directory path
parent_dir = "/Users/bigdaddy/Desktop/Code projects/bg-remover-for-images/"

# Create output folder if doesn't exist
try:
    # Target directory name
    directory = "segmented_images"
    
    path = os.path.join(parent_dir, directory)
    os.mkdir(path)
    print("Directory '% s' created" % directory)
except:
    print('segmented_images folder already exists, continuing process')
    pass

# Create used images folder if doesn't exist
try:
    # Target directory name
    directory = "used_images"
    
    used_path = os.path.join(parent_dir, directory)
    os.mkdir(used_path)
    print("Directory '% s' created" % directory)
except:
    print('used_images folder already exists, continuing process')
    pass

# Read in images folder as a list
list_img = os.listdir("images")
print(list_img)
# Store the list of images in a list
img_list = []
for img_path in list_img:
    img = cv2.imread(f'images/{img_path}')
    img_list.append(img)
print(len(img_list))

# Create SelfiSegmentation object
segmentor = SelfiSegmentation()

img_index = 0
for image in img_list:
    print("Attempting image ", img_index)
    try:
        # Resize the image
        img = cv2.resize(image, (640, 640))

        # Run the segmentor
        img_out = segmentor.removeBG(img, (255, 255, 255), threshold=0.62)

        # Show the image and check user input for segmentation approval
        cv2.imshow('Segmented Image', img_out)
        print('Do you want to save this segmentation? (y) or (n)')

        if cv2.waitKey(0) == ord('y'):
            # Save the segmented image
            save_path = os.path.join(path, "img_" + str(img_index) + ".png")
            print(save_path)
            cv2.imwrite(save_path, img_out)

            # Add orignal image to the used_images folder
            cv2.imwrite(os.path.join(used_path, list_img[img_index]), image)

            # Remove original image from images folder
            orig_img_path = os.path.join(parent_dir, "images", list_img[img_index])
            os.remove(orig_img_path)
        if cv2.waitKey(0) == ord('n'):
            print('Segmentation of (', list_img[img_index], ') failed continuing...')
            break
        print('Segmentation of (', list_img[img_index], ') successful! continuing...')
    except:
        print('Segmentation of (', list_img[img_index], ') failed, continuing...')
        pass 

    img_index += 1

print("Image segmentation process completed!")

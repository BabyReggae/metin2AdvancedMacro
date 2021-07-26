import cv2

CONFIG = {
    "width" : 800,
    "height" : 600
}

def getImgPosInImg( large_img_path , small_img_path , method = cv2.TM_SQDIFF_NORMED, debug = False ):
    # Read the images from the file
    large_image = cv2.imread(large_img_path)
    small_image = cv2.imread(small_img_path)
    result = cv2.matchTemplate(small_image, large_image, method)
    # We want the minimum squared difference
    mn,_,mnLoc,_ = cv2.minMaxLoc(result)
    # Draw the rectangle:
    # Extract the coordinates of our best match
    MPx,MPy = mnLoc
    # print( MPx,MPy )
    if debug :
        # - - - DEBUG  Step 2: Get the size of the template. This is the same size as the match.
        trows,tcols = small_image.shape[:2]
        # Step 3: Draw the rectangle on large_image
        cv2.rectangle(large_image, (MPx,MPy),(MPx+tcols,MPy+trows),(0,0,255),2)
        # Display the original image with the rectangle around the match.
        cv2.imshow('output',large_image)
        # The image is only displayed if we call this
        cv2.waitKey(0)

    return [MPx,MPy]

# def getMetinWindowPosInUserScreen():
#     print('coucou')


# def getInventoryPosition( userClickedZoneImg_path = "/ancor/user_suggest.png" , dragonSlotImg_path = '/ancor/dragonStone.png',  ):
#     ancorX, ancorY = getImgPosInImg( userClickedZoneImg_path , dragonSlotImg_path )

# def getShopPosition():
#     # detect shop position and retrieved topLeft coordonate
#     print('TODO')
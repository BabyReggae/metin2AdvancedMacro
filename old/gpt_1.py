import cv2
import pyautogui
import numpy as np

# Function to find local image within a screenshot
def find_image_in_screenshot(screenshot, local_image_path):
    # Load the local image
    local_img = cv2.imread(local_image_path)
    local_height, local_width, _ = local_img.shape

    # Match the local image within the screenshot
    result = cv2.matchTemplate(screenshot, local_img, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    threshold = 0.8  # Adjust this threshold according to your needs
    if max_val >= threshold:
        return max_loc, (max_loc[0] + local_width, max_loc[1] + local_height)
    else:
        return None, None

# Function to capture a screenshot around the mouse position
def capture_screenshot_around_mouse(box_size):
    mouse_x, mouse_y = pyautogui.position()
    screenshot = pyautogui.screenshot(region=(mouse_x - box_size//2, mouse_y - box_size//2, box_size, box_size))
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    return screenshot

def main():
    box_size = 100
    local_image_path = "ancor/favicon.png"

    while True:
        input("Press Enter to capture a screenshot around the mouse position...")
        screenshot = capture_screenshot_around_mouse(box_size)
        match_start, match_end = find_image_in_screenshot(screenshot, local_image_path)
        
        if match_start is not None:
            cv2.rectangle(screenshot, match_start, match_end, (0, 255, 0), 2)
            cv2.imshow("Screenshot", screenshot)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            print("Local image found within the screenshot!")
        else:
            print("Local image not found within the screenshot.")

if __name__ == "__main__":
    main()
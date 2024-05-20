import cv2
import pyautogui
import numpy as np
import time
from classes.actions.create_shop_doom import CreateShopDoom
import lib.utils as u
# import lib.config as coord
import keyboard
from classes.game_instance import GameInstance
from classes.actions.scan_market_place import ScanMarketPlace


# Function to find local image within a screenshot
def find_image_in_screenshot(screenshot, local_image_path):
    # Load the local image
    local_img = cv2.imread(local_image_path)
    local_height, local_width, _ = local_img.shape

    # Match the local image within the screenshot
    result = cv2.matchTemplate(screenshot, local_img, cv2.TM_CCOEFF_NORMED)

    # cv2.imshow("result", result)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    threshold = 0.8  # Adjust this threshold according to your needs
    if max_val >= threshold:
        return max_loc, (max_loc[0] + local_width, max_loc[1] + local_height)
    else:
        return None, None

# Function to capture a screenshot around the mouse position
def capture_screenshot_around_mouse(box_size):
    mouse_x, mouse_y = pyautogui.position()
    screenshot = pyautogui.screenshot(region=(mouse_x - box_size/2, mouse_y - box_size/2, box_size, box_size))
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    return screenshot

def find_favicon_position():
    print("En attente d'un click sur le coin haut-gauche d'un Metin")
    box_size = 50
    click_pos = u.getNextClickPos()
    screenshot = capture_screenshot_around_mouse(box_size)

    # cv2.imshow("Screenshot", screenshot)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    match_start, _ = find_image_in_screenshot(screenshot, "ancor/favicon.png")
    if match_start == None:
        print("ECHEC - vérifier que l'icon apparait en entier dans le screenShot")
        cv2.imshow("Screenshot", screenshot)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        exit(0)
    ancor = u.get_img_dimensions("ancor/favicon.png")
    # Adjust the matched position with mouse position
    match_start_adjusted = ((match_start[0]+ancor[0]) + click_pos[0]-(box_size//2), (match_start[1]+ancor[1]) + click_pos[1]-(box_size//2) )

    return match_start_adjusted

def initGameInstance(num_instances=1):
    instances = []
    for _ in range(num_instances):
        match_start = find_favicon_position()

        if match_start is not None:
            instance = GameInstance(match_start,'init')
            instances.append(instance)
            print("Metin enregistré en position :", match_start)
        else:
            print("Une erreur c'est produite")
            exit(0)

    return instances

############ DELEGUATE TO FOLDER ACTION

def perform_global_action(instances):
    # print("Health intance check")
    # if len(instances) < 2:
    #     print("At least 3 game instances are required.")
    #     return
    wait_user_action(instances)

def wait_user_action(instances):
    print("En attende d'une action utilisateur...")
    while True:
        if keyboard.is_pressed('m'):
            for i in instances:
                # u.moveThenClick("left", pos)
                i.focus
                time.sleep(1)
            break
        if keyboard.is_pressed('c'):
            print("New Coord creation - waiting for user click")
            d = instances[0].getRelativeDistanceFromClick()
            print(d)
            u.add_new_coordinate(d)
            break
        if keyboard.is_pressed('t'):
            for instance in instances:
                action = CreateShopDoom(instance,"MIAM MIAM",5000000)
                action.execute()
                # co = Connect( self.instance )
                # co.execute()

            # scanShop = ScanShop(  )
            # scanShop.execute()
            break
        time.sleep(0.1)
    
    wait_user_action(instances)
    print("Action started.")

if __name__ == "__main__":
    intances = initGameInstance(1)
    perform_global_action( intances )

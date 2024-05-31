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

# Global variable for action queue
ACTION_QUEUE = []
LAST_SHOP_INFO = None

# Function to find local image within a screenshot
def find_image_in_screenshot(screenshot, local_image_path):
    local_img = cv2.imread(local_image_path)
    local_height, local_width, _ = local_img.shape
    result = cv2.matchTemplate(screenshot, local_img, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    threshold = 0.8
    if max_val >= threshold:
        return max_loc, (max_loc[0] + local_width, max_loc[1] + local_height)
    else:
        return None, None

# Function to capture a screenshot around the mouse position
def capture_screenshot_around_mouse(box_size):
    mouse_x, mouse_y = pyautogui.position()
    screenshot = pyautogui.screenshot(region=(mouse_x - box_size / 2, mouse_y - box_size / 2, box_size, box_size))
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    return screenshot

def find_favicon_position():
    print("En attente d'un click sur le coin haut-gauche d'un Metin")
    box_size = 50
    click_pos = u.getNextClickPos()
    screenshot = capture_screenshot_around_mouse(box_size)
    match_start, _ = find_image_in_screenshot(screenshot, "ancor/favicon.png")
    if match_start is None:
        print("ECHEC - vérifier que l'icon apparait en entier dans le screenShot")
        # cv2.imshow("Screenshot", screenshot)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # exit(0)
        return None
    ancor = u.get_img_dimensions("ancor/favicon.png")
    match_start_adjusted = ((match_start[0] + ancor[0]) + click_pos[0] - (box_size // 2), (match_start[1] + ancor[1]) + click_pos[1] - (box_size // 2))
    return match_start_adjusted

def initGameInstance():
    match_start = find_favicon_position()
    if match_start is not None:
        instance = GameInstance(match_start, 'init')
        print("Metin enregistré en position :", match_start)
        return instance
    else:
        print("Une erreur s'est produite")
        exit(0)

def askUserQuestion(question: str, answer_type: type):
    while True:
        user_input = input(question + ' ')
        if answer_type == int:
            try:
                return int(user_input)
            except ValueError:
                print("Please enter a valid integer.")
        elif answer_type == str:
            return user_input
        else:
            raise ValueError("Unsupported answer type. Supported types are 'str' and 'int'.")
    

def wait_user_action(instances):
    global LAST_SHOP_INFO
    
    print("TOUT LANCER ou AJOUTER DES ACTIONS DANS LA FILE D'ATTENTE\r\n \r\n'e' => Sa lance toute les actions que ta creer dans la file d'attente \r\n'n' => Nouveau SHOP\r\n'b' => Répéter le SHOP(genre t'as dautre shop le même prix que celui qye tu viens de creer )" )
    nbaction = len(ACTION_QUEUE)
    print(f"POUR LINSTANT {nbaction} DANS LA FILE D'ATTENTE")
    while True:
        if keyboard.is_pressed('t'):
            instances.append(initGameInstance())
            action = ScanMarketPlace(instances[0])
            ACTION_QUEUE.append(action)
            break
        
        if keyboard.is_pressed('r'):
            action = ScanMarketPlace(instances[0])
            ACTION_QUEUE.append(action)
            break
        
        if keyboard.is_pressed('n'):
            new_instance = initGameInstance()
            shop_name = askUserQuestion("\r\n \r\nENTRER LE NOM DU SHOP (chiffre,lettre simple, majuscule ) : ", str)
            price = askUserQuestion("\r\n \r\nENTRER LE PRIX DU SHOP : ", int)
            action = CreateShopDoom(new_instance, shop_name, price)
            ACTION_QUEUE.append(action)
            LAST_SHOP_INFO = (shop_name, price)
            print(f"'{shop_name}' AVEC LE PRIX '{price}' A ETE AJOUTER A LA FILE DATTENTE")
            break

        if keyboard.is_pressed('b'):
            if LAST_SHOP_INFO:
                shop_name, price = LAST_SHOP_INFO
                new_instance = initGameInstance()
                action = CreateShopDoom(new_instance, shop_name, price)
                ACTION_QUEUE.append(action)
                print(f"'{shop_name}' AVEC LE PRIX '{price}' A ETE AJOUTER A LA FILE DATTENTE")
            else:
                print("AUCUN SHOP DEJA DANS LA FILE D'ATTENTE, CREE EN UN DABORD !")
            break

        if keyboard.is_pressed('e'):
            for action in ACTION_QUEUE:
                action.execute()
            print("Bimbamboum - finito les trucs a faire- Metin un jeu de dog quand même ")
            ACTION_QUEUE.clear()
            break

    time.sleep(1)
    wait_user_action(instances)

if __name__ == "__main__":
    wait_user_action([])

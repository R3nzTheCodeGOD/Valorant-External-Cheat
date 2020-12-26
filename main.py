import keyboard
import pyautogui
import time
import ctypes
import PIL.ImageGrab
import PIL.Image
import winsound 
import os
import mss
from colorama import Fore, Style, init
S_HEIGHT, S_WIDTH = (PIL.ImageGrab.grab().size)
PURPLE_R, PURPLE_G, PURPLE_B = (250, 100, 250)
TOLERANCE = 31
GRABZONE = 10
TRIGGER_KEY = "ctrl + alt"
SWITCH_KEY = "ctrl + tab"
GRABZONE_KEY_UP = "ctrl + up"
BUNNY_KEY = "ctrl + space"
GRABZONE_KEY_DOWN = "ctrl + down"
mods = ["OPERATOR/MARSHAL", "GUARDIAN", "VANDAL/PHANTOM/SHOTGUNS"]
pyautogui.FAILSAFE = False
 
class FoundEnemy(Exception):
    pass
 
class triggerBot():
    def __init__(self) -> None:
        self.toggled = False
        self._bunny = False
        self.mode = 1
        self.last_reac = 0
 
    def toggle(self) -> None: self.toggled = not self.toggled
    def bunnyy(self) -> None: self._bunny = not self._bunny
 
    def switch(self):
        if self.mode != 2: self.mode += 1
        else: self.mode = 0
        if self.mode == 0: winsound.Beep(200, 200)
        if self.mode == 1: winsound.Beep(200, 200), winsound.Beep(200, 200)
        if self.mode == 2: winsound.Beep(200, 200), winsound.Beep(200, 200), winsound.Beep(200, 200)

    def click(self) -> None:
        ctypes.windll.user32.mouse_event(2, 0, 0, 0,0) # sol bas
        ctypes.windll.user32.mouse_event(4, 0, 0, 0,0) # sol bırak
        
    def approx(self, r, g ,b) -> bool: return PURPLE_R - TOLERANCE < r < PURPLE_R + TOLERANCE and PURPLE_G - TOLERANCE < g < PURPLE_G + TOLERANCE and PURPLE_B - TOLERANCE < b < PURPLE_B + TOLERANCE
 
    def grab(self) -> None:
        with mss.mss() as sct:
            bbox=(int(S_HEIGHT/2-GRABZONE), int(S_WIDTH/2-GRABZONE), int(S_HEIGHT/2+GRABZONE), int(S_WIDTH/2+GRABZONE))
            sct_img = sct.grab(bbox)
            return PIL.Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
    
    def scan(self) -> None:
        start_time = time.time()
        pmap = self.grab()
        
        try:
            for x in range(0, GRABZONE*2):
                for y in range(0, GRABZONE*2):
                    r, g, b = pmap.getpixel((x,y))
                    if self.approx(r, g, b): raise FoundEnemy
        except FoundEnemy:
            self.last_reac = int((time.time() - start_time)*1000)
            self.click()
            if self.mode == 0: time.sleep(0.5)
            if self.mode == 1: time.sleep(0.25)
            if self.mode == 2: time.sleep(0.2)
            print_banner(self)

    def bunny(self) -> None:
        while True:
            if keyboard.is_pressed("space"): pyautogui.press("space")
            else: break
def print_banner(bot: triggerBot) -> None:
    os.system("cls")
    print(Style.BRIGHT + Fore.CYAN + "R3nzTheCodeGOD Valorant Trigger Bot v1.0.0" + Style.RESET_ALL)
    print("===== Kontroller =====")
    print("Aktifleştirme Tuşu   :", Fore.YELLOW + TRIGGER_KEY + Style.RESET_ALL)
    print("Mod Değiştirme Tuşu  :", Fore.YELLOW + SWITCH_KEY + Style.RESET_ALL)
    print("Yakalama Alanı Ayar  :", Fore.YELLOW + GRABZONE_KEY_UP + "/" + GRABZONE_KEY_DOWN + Style.RESET_ALL)
    print("==== Bilgilendirme ===")
    print("Mod                  :", Fore.CYAN + mods[bot.mode] + Style.RESET_ALL)
    print("Yakalama Alanı       :", Fore.CYAN + str(GRABZONE) + "x" + str(GRABZONE) + Style.RESET_ALL)
    print("Trigger Durumu       :", (Fore.GREEN if bot.toggled else Fore.RED) + ("Açık" if bot.toggled else "Kapalı") + Style.RESET_ALL)
    print("Bunny Durumu         :", (Fore.GREEN if bot._bunny else Fore.RED) + ("Açık" if bot._bunny else "Kapalı") + Style.RESET_ALL)
    print("Son Reaksiyon Süresi :", Fore.CYAN + str(bot.last_reac) + Style.RESET_ALL + " ms ("+str((bot.last_reac)/(GRABZONE*GRABZONE))+"ms/pix)")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
if __name__ == "__main__":
    bot = triggerBot()
    print_banner(bot)
    while True:
        if keyboard.is_pressed(SWITCH_KEY):
            bot.switch()
            print_banner(bot)
            while keyboard.is_pressed(SWITCH_KEY): pass
        if keyboard.is_pressed(GRABZONE_KEY_UP):
            GRABZONE += 5
            print_banner(bot)
            winsound.Beep(400, 200)
            while keyboard.is_pressed(GRABZONE_KEY_UP): pass
        if keyboard.is_pressed(GRABZONE_KEY_DOWN):
            GRABZONE -= 5
            print_banner(bot)
            winsound.Beep(300, 200)
            while keyboard.is_pressed(GRABZONE_KEY_DOWN): pass
        if keyboard.is_pressed(TRIGGER_KEY):
            bot.toggle()
            print_banner(bot)
            if bot.toggled: winsound.Beep(440, 75), winsound.Beep(700, 100)
            else: winsound.Beep(440, 75), winsound.Beep(200, 100)
            while keyboard.is_pressed(TRIGGER_KEY): pass
        if keyboard.is_pressed(BUNNY_KEY): 
            bot.bunnyy()
            print_banner(bot)
            if bot._bunny: winsound.Beep(440, 75), winsound.Beep(700, 100)
            else: winsound.Beep(440, 75), winsound.Beep(200, 100)
            while keyboard.is_pressed(BUNNY_KEY): pass

        if bot.toggled: bot.scan()
        if bot._bunny:
            if keyboard.is_pressed("space"): bot.bunny()
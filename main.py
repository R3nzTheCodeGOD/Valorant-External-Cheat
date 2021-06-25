"""
MIT License

Copyright (c) 2020-2021 Erdem Yılmaz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from winsound import Beep
from colorama import Fore, Style, init
from mss import base, mss
from PIL import ImageGrab, Image
from ctypes import windll
from time import perf_counter, sleep
from os import system
from keyboard import is_pressed
from hashlib import sha256
from random import random
from json import load, dump


__author__   = 'R3nzTheCodeGOD'
__version__  = 'v2.0.3'


S_HEIGHT, S_WIDTH  = ImageGrab.grab().size
GRABZONE           = 5
IS_HOLDKEY         = True
IS_RUNING          = True
HOLDKEY            = 'shift'
TOGGLEKEY          = 'F6'
SWITCH_KEY         = 'ctrl + tab'
GRABZONE_KEY_UP    = 'ctrl + up'
GRABZONE_KEY_DOWN  = 'ctrl + down'
MODS               = ('0.3s Delay', '0.25s Delay', '0.2s Delay', '0.15s Delay', '0.1s Delay', 'No Delay Full-Auto')


class FoundEnemy(Exception):
    pass


class Config:

    base = {
        'Grabzone'  : 5,
        'IsHoldKey' : False,
        'HoldKey'   : 'shift',
        'ToggleKey' : 'F6'
    }

    def __init__(self, configName: str = 'config.json') -> None:
        self.configName = configName
        self.config     = None


    def createBaseConfig(self) -> None:
        with open(self.configName, 'w', encoding='utf-8') as f:
            self.config = self.base
            dump(self.config, f, ensure_ascii=False)


    def cfgLoad(self) -> dict:
        try:
            with open(self.configName, 'r', encoding='utf-8') as f:
                self.config = load(f)
                return self.config
        
        except FileNotFoundError:
            self.createBaseConfig()
            self.config = self.cfgLoad()
            return self.config



    def cfgDump(self) -> None:
        with open(self.configName, 'w', encoding='utf-8') as f:
            dump({
                'Grabzone'  : GRABZONE,
                'IsHoldKey' : IS_HOLDKEY,
                'HoldKey'   : HOLDKEY,
                'ToggleKey' : TOGGLEKEY
            }, f, ensure_ascii=False)


class TriggerBot:

    def __init__(self) -> None:
        self._mode       = 1
        self._last_reac  = 0


    def switch(self) -> None:
        Beep(200, 100)
        if self._mode != 5: self._mode += 1
        else: self._mode = 0


    def color_check(self, red: int, green: int, blue: int) -> bool:
        if green >= 0xAA: return False
        if green >= 0x78: return abs(red - blue) <= 0x8 and red - green >= 0x32 and blue - green >= 0x32 and red >= 0x69 and blue >= 0x69
        
        return abs(red - blue) <= 0xD and red - green >= 0x3C and blue - green >= 0x3C and red >= 0x6E and blue >= 0x64


    def grab(self) -> Image:
        with mss() as sct:
            bbox     = (int(S_HEIGHT / 2 - GRABZONE), int(S_WIDTH / 2 - GRABZONE), int(S_HEIGHT / 2 + GRABZONE), int(S_WIDTH / 2 + GRABZONE))
            sct_img  = sct.grab(bbox)
            return Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')


    def scan(self) -> None:
        start_time  = perf_counter()
        pmap        = self.grab()

        try:
            for x in range(0, GRABZONE * 2):
                for y in range(0, GRABZONE * 2):
                    r, g, b = pmap.getpixel((x, y))
                    if self.color_check(r, g, b): raise FoundEnemy
        
        except FoundEnemy:
            self._last_reac = int((perf_counter() - start_time) * 1000)
            windll.user32.mouse_event(0x2, 0x0, 0x0, 0x0, 0x0), windll.user32.mouse_event(0x4, 0x0, 0x0, 0x0, 0x0)

            if self._mode == 0: sleep(0.3)
            elif self._mode == 1: sleep(0.25)
            elif self._mode == 2: sleep(0.2)
            elif self._mode == 3: sleep(0.15)
            elif self._mode == 4: sleep(0.1)
            elif self._mode == 5: pass


def print_banner(bot: TriggerBot) -> None:
    system('cls')
    print(Style.BRIGHT + Fore.CYAN + f'{__author__} Valorant External Cheat {__version__}' + Style.RESET_ALL)
    print('====== Controls ======')
    print('Trigger Key          :', Fore.YELLOW + f'{f"HoldKey [{HOLDKEY}]" if IS_HOLDKEY else f"ToggleKey [{TOGGLEKEY}]"}' + Style.RESET_ALL)
    print('Mode Change Key      :', Fore.YELLOW + SWITCH_KEY + Style.RESET_ALL)
    print('Grab Zone Change Key :', Fore.YELLOW + GRABZONE_KEY_UP + '/' + GRABZONE_KEY_DOWN + Style.RESET_ALL)
    print('===== Information ====')
    print('Mode                 :', Fore.CYAN  + MODS[bot._mode] + Style.RESET_ALL)
    print('Grab Zone            :', Fore.CYAN  + str(GRABZONE) + 'x' + str(GRABZONE) + Style.RESET_ALL)
    print('Trigger Status       :', Fore.GREEN + f'{f"Hold down the [{HOLDKEY}] key" if IS_HOLDKEY else "Active" if IS_RUNING else Fore.RED + "Passive"}' + Style.RESET_ALL)
    print('Last React Time      :', Fore.CYAN  + str(bot._last_reac) + Style.RESET_ALL + ' ms (' + str((bot._last_reac) / (GRABZONE * GRABZONE)) + 'ms/pix)')


if __name__ == "__main__":
    _hash = sha256(f'{random()}'.encode('utf-8')).hexdigest()
    print(_hash), system(f'title {_hash}'), sleep(0.5), init(), system('@echo off'), system('cls')

    # Config Load
    cfg        = Config().cfgLoad()
    GRABZONE   = cfg['Grabzone']
    IS_HOLDKEY = cfg['IsHoldKey']
    HOLDKEY    = cfg['HoldKey']
    TOGGLEKEY  = cfg['ToggleKey']
    bot        = TriggerBot()

    print_banner(bot)

    while True:
        if is_pressed(SWITCH_KEY):
            bot.switch()
            print_banner(bot)
            continue

        if is_pressed(GRABZONE_KEY_UP):
            GRABZONE += 1
            print_banner(bot), Beep(400, 100) 
            continue  

        if is_pressed(GRABZONE_KEY_DOWN):
            if GRABZONE != 1: GRABZONE -= 1
            print_banner(bot), Beep(300, 100)
            continue

        if IS_HOLDKEY:
            if is_pressed(HOLDKEY):
                bot.scan(), print_banner(bot)
                continue
        
        else:
            if is_pressed(TOGGLEKEY):
                IS_RUNING = not IS_RUNING
                print_banner(bot), Beep(400, 100)

            if IS_RUNING:
                bot.scan(), print_banner(bot)
                continue

        sleep(0.0025)

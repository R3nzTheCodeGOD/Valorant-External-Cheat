"""
MIT License

Copyright (c) 2020 Erdem Yılmaz

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
from mss import mss
from PIL import ImageGrab, Image
from ctypes import windll
from time import perf_counter, sleep
from os import system
from keyboard import is_pressed
from hashlib import sha256
from random import random


__author__   = 'R3nzTheCodeGOD'
__version__  = 'v2.0.2'


S_HEIGHT, S_WIDTH  = ImageGrab.grab().size
GRABZONE           = 0x5
TRIGGER_KEY        = 'shift'
SWITCH_KEY         = 'ctrl + tab'
GRABZONE_KEY_UP    = 'ctrl + up'
GRABZONE_KEY_DOWN  = 'ctrl + down'
MODS               = ('0.3s Delay', '0.25s Delay', '0.2s Delay', '0.15s Delay', '0.1s Delay', 'No Delay Full-Auto')


class FoundEnemy(Exception):
    pass


class TriggerBot:

    def __init__(self) -> None:
        self._mode       = 0x1
        self._last_reac  = 0x0


    def switch(self) -> None:
        Beep(0xC8, 0x64)
        if self._mode != 0x5: self._mode += 0x1
        else: self._mode = 0x0


    def color_check(self, red: int, green: int, blue: int) -> bool:
        if green >= 0xAA: return False
        if green >= 0x78: return abs(red - blue) <= 0x8 and red - green >= 0x32 and blue - green >= 0x32 and red >= 0x69 and blue >= 0x69
        
        return abs(red - blue) <= 0xD and red - green >= 0x3C and blue - green >= 0x3C and red >= 0x6E and blue >= 0x64


    def grab(self) -> Image:
        with mss() as sct:
            bbox     = (int(S_HEIGHT / 0x2 - GRABZONE), int(S_WIDTH / 0x2 - GRABZONE), int(S_HEIGHT / 0x2 + GRABZONE), int(S_WIDTH / 0x2 + GRABZONE))
            sct_img  = sct.grab(bbox)
            return Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')


    def scan(self) -> None:
        start_time  = perf_counter()
        pmap        = self.grab()

        try:
            for x in range(0x0, GRABZONE * 0x2):
                for y in range(0x0, GRABZONE * 0x2):
                    r, g, b = pmap.getpixel((x, y))
                    if self.color_check(r, g, b): raise FoundEnemy
        
        except FoundEnemy:
            self._last_reac = int((perf_counter() - start_time) * 0x3E8)
            windll.user32.mouse_event(0x2, 0x0, 0x0, 0x0, 0x0), windll.user32.mouse_event(0x4, 0x0, 0x0, 0x0, 0x0)

            if self._mode == 0x0: sleep(0.3)
            elif self._mode == 0x1: sleep(0.25)
            elif self._mode == 0x2: sleep(0.2)
            elif self._mode == 0x3: sleep(0.15)
            elif self._mode == 0x4: sleep(0.1)
            elif self._mode == 0x5: pass


def print_banner(bot: TriggerBot) -> None:
    system('cls')
    print(Style.BRIGHT + Fore.CYAN + f'{__author__} Valorant External Cheat {__version__}' + Style.RESET_ALL)
    print('====== Controls ======')
    print('Trigger Key          :', Fore.YELLOW + TRIGGER_KEY + Style.RESET_ALL)
    print('Mode Change Key      :', Fore.YELLOW + SWITCH_KEY + Style.RESET_ALL)
    print('Grab Zone Change Key :', Fore.YELLOW + GRABZONE_KEY_UP + '/' + GRABZONE_KEY_DOWN + Style.RESET_ALL)
    print('===== Information ====')
    print('Mode                 :', Fore.CYAN  + MODS[bot._mode] + Style.RESET_ALL)
    print('Grab Zone            :', Fore.CYAN  + str(GRABZONE) + 'x' + str(GRABZONE) + Style.RESET_ALL)
    print('Trigger Status       :', Fore.GREEN + f'Hold down the "{TRIGGER_KEY}" key' + Style.RESET_ALL)
    print('Last React Time      :', Fore.CYAN  + str(bot._last_reac) + Style.RESET_ALL + ' ms (' + str((bot._last_reac) / (GRABZONE * GRABZONE)) + 'ms/pix)')


if __name__ == "__main__":
    _hash = sha256(f'{random()}'.encode('utf-8')).hexdigest()
    print(_hash), system(f'title {_hash}'), sleep(0.5), init(), system('@echo off'), system('cls')
    bot = TriggerBot()
    print_banner(bot)

    while 0x1:
        if is_pressed(SWITCH_KEY):
            bot.switch()
            print_banner(bot)
            continue

        if is_pressed(GRABZONE_KEY_UP):
            GRABZONE += 0x1
            print_banner(bot), Beep(0x190, 0x64) 
            continue  

        if is_pressed(GRABZONE_KEY_DOWN):
            if GRABZONE != 0x1: GRABZONE -= 0x1
            print_banner(bot), Beep(0x12C, 0x64)
            continue

        if is_pressed(TRIGGER_KEY):
            bot.scan(), print_banner(bot)
            continue

        sleep(0.001)
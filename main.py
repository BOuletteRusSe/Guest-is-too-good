from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import random
import pyautogui
import keyboard
from tkinter import Tk, Label, Entry
from tkinter import ttk
from pynput.mouse import Listener
import os
import json

# Variables
used_words = list()
focused_letters = str()

# Json
with open(r"assets\settings.json", "r") as j: 
    settings = json.load(j)
    
# Functions
def join_room():
    roomcode = url_entry.get()
    driver.get(f"https://jklm.fun/{roomcode}")

    ok_button = driver.find_element(By.XPATH, '//button[text()="OK"]')
    ok_button.click()

    driver.maximize_window()
        
def find_maximum(lst,start=0,max_word=''):
    if start == len(lst):
        return max_word
    if len(lst[start]) > len(max_word):
        max_word = lst[start]
    return find_maximum(lst, start + 1, max_word)

# A Optimiser #

def update_json(settings):
    with open(r"assets\settings.json", "w") as j: 
        json.dump(settings, j, indent=4)

def detect_click_bomb():

    def on_click(x, y, button, pressed):
        print(x, y)
        for k in settings.keys():
            if k == "bomb_position":
                settings[k] = [x, y]
                update_json(settings)
        return False
        
    with Listener(on_click=on_click) as listener:
        listener.join()
            
def detect_click_input():
    
    def on_click(x, y, button, pressed):
        print(x, y)
        for k in settings.keys():
            if k == "input_position":
                settings[k] = [x, y]
                update_json(settings)
        return False
        
    with Listener(on_click=on_click) as listener:
        listener.join()
###

def process():
    
    global used_words
    
    for k, v in settings.items():
        if k == "bomb_position":
            pyautogui.moveTo(v[0], v[1])
    pyautogui.click(clicks=2)
    pyautogui.hotkey('ctrl', 'c')

    syll = root.clipboard_get()

    syll_label.config(text=f"Syllabe : {syll}")

    correct_words = []
    with open(r'assets\words_list.txt', 'r', encoding="utf-8") as f:
        for line in f:
            if syll.lower() in line:
                correct_words += line.split(' ')

    # Find the best word by number of different letters

    words_match = {}
    max_letters = [None, 0]
    
    for w in correct_words:
        total_letters = 0
        all_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

        for s in w:
            if s in all_letters:
                total_letters += 1
                all_letters.remove(s)

        if total_letters > max_letters[1]:
            max_letters = [w, total_letters]
    

    if max_letters[0]:
        print(max_letters[0])
        for k, v in settings.items():
            if k == "input_position":
                pyautogui.click(v[0], v[1])
        for i in max_letters[0]:
            sleep(random.uniform(0.02, 0.12))
            keyboard.write(i)
        used_words.append(max_letters[0])
    else:
        print("Aucun mot trouvé pour les lettres spécifiées.")
        
def reset_used_words():
    global used_words
    used_words = []
    
def update_focused_letters(*args):
    global focused_letters
    focused_letters = letters_entry.get()

# Updater avec keybind
keyboard.on_press_key('0', process)

# Selenium
driver = webdriver.Chrome(executable_path=r'assets\chromedriver.exe')

# Tkinter
root = Tk()
root.title("Guest is too good - Bomb Party")
root.geometry("400x175")
root.resizable(False, False)
root.iconbitmap(r"assets\bomb.ico")

code_label = Label(root, text="Code de partie : ")
code_label.place(x=0, y=18)

url_entry = Entry(root)
url_entry.place(x=120, y=20)

join_button = ttk.Button(root, text="Rejoindre", command=join_room)
join_button.place(x=287, y=18)

get_syll_button = ttk.Button(root, text="Tricher", command=process)
get_syll_button.place(x=100, y=45)

reset_button = ttk.Button(root, text="Réinitialiser", command=reset_used_words)
reset_button.place(x=200, y=45)

syll_label = Label(root, text="Syllabe : ")
syll_label.place(x=167, y=75)

letters_label = Label(root, text="Lettres prioritaires :")
letters_label.place(x=0, y=98)

letters_entry = Entry(root)
letters_entry.place(x=147, y=100)

bomb_config = ttk.Button(root, text="Bomb Config", command=detect_click_bomb)
bomb_config.place(x=87, y=125)

code_label = Label(root, text="")
code_label.place(x=0, y=18)

input_config = ttk.Button(root, text="Answer Input Config", command=detect_click_input)
input_config.place(x=200, y=125)

letters_entry.bind("<KeyRelease>", update_focused_letters)

root.attributes('-topmost', 1)


def main():

    # Start code
    root.mainloop()

    # End
    driver.quit()
    os.system("quit")

# Start code
if __name__ == "__main__":
    main()

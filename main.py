from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import random
import pyautogui
import keyboard
from tkinter import Tk, Label, Entry, StringVar
from tkinter import ttk
from pynput.mouse import Listener
import os
import json

# Json
with open(r"assets\settings.json", "r") as j: 
    settings = json.load(j)

# Variables
used_words = list()
focused_letters = str()
keys_rate = str()
root = Tk()
langue_list = ("French", "English", "Spanish")
langue = StringVar(root)
language = "assets/languages_words_list/french_words_list.txt"
for k, v in settings.items():
    if k == "language":
        default_language = langue_list[v]
    
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

def update_json(settings):
    with open(r"assets\settings.json", "w") as j: 
        json.dump(settings, j, indent=4)

def change_langue(*args):
    global language
    print(langue.get())
    language = "assets/languages_words_list/%s_words_list.txt" % (langue.get().lower())
    for k in settings.keys():
        if k == "language":
            settings[k] = langue_list.index(langue.get())
    update_json(settings)

# A Optimiser #

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
    
    global used_words, keys_rate, language
    
    for k, v in settings.items():
        if k == "bomb_position":
            pyautogui.moveTo(v[0], v[1])
    pyautogui.click(clicks=2)
    pyautogui.hotkey('ctrl', 'c')

    syll = root.clipboard_get()

    syll_label.config(text=f"Syllabe : {syll}")

    correct_words = []
    with open(language, 'r', encoding="utf-8") as f:
        for line in f:
            if syll.lower() in line:
                correct_words += line.split(' ')

    # Find the best word by number of different letters

    max_letters = [None, 0]
    temp = False

    while True:
    
        for w in correct_words:
            total_letters = 0
            all_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

            for s in w:
                if s in all_letters:
                    total_letters += 1
                    all_letters.remove(s)

            if total_letters > max_letters[1]:
                if w not in used_words:
                    if (focused_letters in w) or temp:
                        max_letters = [w, total_letters]

        if (max_letters == [None, 0]) and (not temp):
            temp = True
        else:
            break

    # Write word
    if max_letters[0]:
        print(max_letters[0])
        for k, v in settings.items():
            if k == "input_position":
                pyautogui.click(v[0], v[1])
        for i in max_letters[0]:
            try:
                k = float(keys_rate)
                _a_ = k + k / 2
                _b_ = k / 2
                sleep(random.uniform(_a_, _b_))
            except:
                _a_ = 0.1
                _b_ = 0.05
                sleep(random.uniform(_a_, _b_))
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
    
def update_keys_rate(*args):
    global keys_rate
    keys_rate = keys_entry.get()

# Updater avec keybind
keyboard.on_press_key('0', process)

# Selenium
driver = webdriver.Chrome(executable_path=r'assets\chromedriver.exe')

# Tkinter
root.title("Guest is too good - Bomb Party")
root['background']='#35323F'
root.geometry("400x225")
root.resizable(False, False)
root.iconbitmap(r"assets\bomb.ico")

code_label = Label(root, text="Code de partie : ", bg="#35323F", fg="white")
code_label.place(x=25, y=18)

url_entry = Entry(root)
url_entry.place(x=125, y=20)

join_button = ttk.Button(root, text="Rejoindre", command=join_room)
join_button.place(x=150, y=45)

get_syll_button = ttk.Button(root, text="Tricher", command=process)
get_syll_button.place(x=50, y=45)

reset_button = ttk.Button(root, text="Réinitialiser", command=reset_used_words)
reset_button.place(x=250, y=45)

syll_label = Label(root, text="Syllabe : Aucune", bg="#35323F", fg="white")
syll_label.place(x=150, y=75)

letters_label = Label(root, text="Lettres prioritaires :", bg="#35323F", fg="white")
letters_label.place(x=15, y=98)

letters_entry = Entry(root)
letters_entry.place(x=125, y=100)

keys_label = Label(root, text="Vitesse de \nfrappe (secondes) :", bg="#35323F", fg="white")
keys_label.place(x=15, y=135)

keys_entry = Entry(root)
keys_entry.place(x=125, y=143)

bomb_config = ttk.Button(root, text="Config bombe", command=detect_click_bomb)
bomb_config.place(x=285, y=98)

input_config = ttk.Button(root, text="Config entrée texte", command=detect_click_input)
input_config.place(x=275, y=140)

langue_label = Label(root, text="Langage :", bg="#35323F", fg="white")
langue_label.place(x=75, y=185)

langue_menu = ttk.OptionMenu(root, langue, default_language, *langue_list, command=change_langue)
langue_menu.place(x=150, y=185)

keys_entry.bind("<KeyRelease>", update_keys_rate)
letters_entry.bind("<KeyRelease>", update_focused_letters)

root.attributes('-topmost', 1)

# File start
def main():

    # Start code
    root.mainloop()

    # End
    driver.quit()
    os.system("quit")

# Start code
if __name__ == "__main__":
    main()

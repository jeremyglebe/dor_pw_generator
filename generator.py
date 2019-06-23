#!/usr/bin/env python

# The resource file used by this program (containing all the passwords from the
# game) was created through the incredible hard work of a youtuber named
# "GenericMadScientist". I take no credit for his work.

# IMPORTS
from tkinter import *
import os
from urllib.request import urlopen
from PIL import ImageTk, Image
from io import BytesIO
from random import choice, random
from beautifulscraper import BeautifulScraper
from time import sleep
import urllib
from urllib.request import Request, urlopen
import json
from pprint import pprint as Print

# Get our directory
dir_path = os.path.dirname(os.path.realpath(__file__))
print("Found path: " + dir_path)


def show_image(canvas, images, card_name):

    search = 'yugioh+' + card_name.replace(' ', '+')

    scraper = BeautifulScraper()
    scraper.add_header(
        'User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36')
    url = 'https://www.google.co.in/search?q='+search+'&source=lnms&tbm=isch'
    page = scraper.go(url)

    image_url = json.loads(page.find_all(
        'div', {'class': 'rg_meta'})[0].text)['ou']
    print(image_url)
    image_bytes = urlopen(image_url).read()
    pil_image = Image.open(BytesIO(image_bytes))
    w, h = pil_image.size
    ratio = 300 / h
    pil_image = pil_image.resize((int(w * ratio), int(h * ratio)),Image.ANTIALIAS)
    images[0] = ImageTk.PhotoImage(pil_image)
    # create_image(xpos, ypos, image, anchor)
    canvas.create_image(150, 150, image=images[0], anchor='center')
    canvas.pack(expand='yes', side='top')


def handler_generate(root, canvas, images):
    # Open the resource file
    print("Opening file: " + dir_path + "\\passwords.csv")
    passwords_csv = open(dir_path + "\\passwords.csv", 'r')

    # Read the lines from the file
    print("Reading lines...")
    passwords = passwords_csv.readlines()

    # Close the file
    passwords_csv.close()

    # Process each line
    print("Processing passwords...")
    for i in range(len(passwords)):
        # Split each line by commas
        passwords[i] = passwords[i].split(',')
        # Remove the trailing newline character
        passwords[i][2] = passwords[i][2].replace('\n', '')

    # Select a random one
    print("Generating...")
    item = choice(passwords)
    # Make sure the chosen line actually has a password in it
    while item[2] == '':
        item = choice(passwords)

    # Print the results
    Label(root, text="Card #" + item[0]).pack()
    Label(root, text=item[1]).pack()
    Label(root, text="Unlock Code: " + item[2]).pack()

    show_image(canvas, images, item[1])


# User Interface
master = Tk()

# List to hold image references
images = [None]

# Create the image canvas
canvas = Canvas(master, bg='white', width=300, height=300)

# Create the generate button
btn_generate = Button(master, text="Generate",
                      command=lambda: handler_generate(master, canvas, images))

# Pack all gui elements
btn_generate.pack()
canvas.pack(expand='yes', side='top')

# Open the window
mainloop()

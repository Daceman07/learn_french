BACKGROUND_COLOR = "#B1DDC6"
import pandas
from tkinter import *
import random

TO_LEARN = {}
try:
    DATA = pandas.read_csv("data/french_words.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    TO_LEARN = original_data.to_dict(orient="records")
else:
    TO_LEARN = DATA.to_dict(orient="records")

current_card = {}


# ---------------------------- words ------------------------------- #

def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(TO_LEARN)

    canvas.itemconfig(flash_card_title, text="French", fill="Black")
    canvas.itemconfig(flash_card_word, text=current_card["French"], fill="Black")
    canvas.itemconfig(card_background, image=flash_card_front)
    flip_timer = window.after(3000, func=flip_card)


# ---------------------------- card_back ------------------------------- #
def flip_card():
    canvas.itemconfig(flash_card_title, text="English", fill="White")
    canvas.itemconfig(flash_card_word, text=current_card["English"], fill="White")
    canvas.itemconfig(card_background, image=flash_card_back)


# ---------------------------- is_known ------------------------------- #

def is_known():
    TO_LEARN.remove(current_card)
    data = pandas.DataFrame(TO_LEARN)
    data.to_csv("data/Words_to_learn.csv", index=False)
    next_card()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flashy")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
X_MARK = PhotoImage(file="images/wrong.png")
CHECK_MARK = PhotoImage(file="images/right.png")
flip_timer = window.after(3000, func=flip_card)

# Canvas
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
flash_card_front = PhotoImage(file="images/card_front.png")
flash_card_back = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=flash_card_front)

flash_card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))

flash_card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))

canvas.grid(row=0, column=0, columnspan=2)

next_card()

# buttons

wrong_button = Button(image=X_MARK, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=0)

correct_button = Button(image=CHECK_MARK, highlightthickness=0, command=is_known)
correct_button.grid(row=1, column=1)

window.mainloop()

from tkinter import *
import pandas
import random

# Constant variables
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

# Read the CSV file and create a dictionary of French and English words to learn
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


# Function to display the next card
def next_card():
    global current_card, flip_timer
    # Cancel the current timer
    window.after_cancel(flip_timer)
    # Select a random card from the list
    current_card = random.choice(to_learn)
    # Update the card's text and image to the front
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    # Set a timer to flip the card after 3 seconds
    flip_timer = window.after(3000, func=flip_card)


# Function to flip the card
def flip_card():
    # Update the card's text and image to the back
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)


# Function to remove the current card from the list and display the next card
def is_known():
    # Remove the current card from the list
    to_learn.remove(current_card)
    # Print the number of cards left to learn
    print(len(to_learn))
    # Convert the list of cards to a DataFrame and save it to the CSV file
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    # Display the next card
    next_card()


# Create the window
window = Tk()
window.title("Tolly")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# Set a timer to flip the card after 3 seconds
flip_timer = window.after(3000, func=flip_card)

# Create the canvas to display the card
canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font="Arial 40 italic")
card_word = canvas.create_text(400, 263, text="", font="Arial 60 bold")
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

# Create the buttons to move to the next card or remove the current card
cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

# Display the first card
next_card()

# Run the window
window.mainloop()

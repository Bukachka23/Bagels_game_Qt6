import random
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QMessageBox, QVBoxLayout
from PyQt6.QtCore import QTimer, QUrl
from PyQt6.QtMultimedia import QSoundEffect


# Global variables
num_digits = 3
max_guesses = 90
secretNum = ""


# This function generates a secret number
class Bagels(QWidget):
    # Constructor
    def __init__(self):
        # Call the constructor of the parent class
        super().__init__()
        # Initialize the UI
        self.initUI()
        # Load the sound effects
        self.correct_sound = QSoundEffect()
        self.correct_sound.setSource(
            QUrl.fromLocalFile("path"))
        print("Correct sound effect loaded:", self.correct_sound.isLoaded())
        self.incorrect_sound = QSoundEffect()
        self.incorrect_sound.setSource(
            QUrl.fromLocalFile("path"))
        print("Incorrect sound effect loaded:", self.incorrect_sound.isLoaded())
        # Initialize the number of attempts
        self.numAttempts = 0

    # Initialize the UI
    def initUI(self):
        # Create widgets
        self.label_intro = QLabel("Bagels, a deductive logic game.\n\nI am thinking of a {}-digit number with no repeated digits. Try to guess what it is. You have {} guesses to get it.\n\n".format(num_digits, max_guesses))
        # The first widget is a label
        self.label_guess = QLabel("Guess #1: ")
        # The number of guesses is 1 at the beginning
        self.text_guess = QLineEdit()
        # The second widget is a text field
        self.button_guess = QPushButton("Guess")
        # Connect the clicked signal of the button to the guessClicked() method
        self.button_guess.clicked.connect(self.guessClicked)
        self.button_new_game = QPushButton("New Game")
        self.button_new_game.clicked.connect(self.newGame)


        # Create layout and add widgets
        vbox = QVBoxLayout()
        # Add the widgets to the layout
        vbox.addWidget(self.label_intro)
        # Add the widgets to the layout
        vbox.addWidget(self.label_guess)
        # The second widget will be below the first one
        vbox.addWidget(self.text_guess)
        # The third widget will be below the second one
        vbox.addWidget(self.button_guess)
        vbox.addWidget(self.button_new_game)


        # Set main layout
        self.setLayout(vbox)

        # Set window properties
        # Set the position and size of the window
        self.setGeometry(300, 300, 300, 200)
        # Set the title of the window
        self.setWindowTitle('Bagels')
        # Show the window
        self.show()

        # Initialize the game
        self.newGame()
        self.button_guess.setEnabled(True)

    def newGame(self):
        # Declare secretNum as a global variable
        global secretNum
        # Generate a new secret number
        secretNum = getSecretNum()
        # Reset the number of guesses
        self.numGuesses = 1
        # Display the intro message
        self.label_intro.setText("I have thought up a number. You have {} seconds to get it.\n\n".format(max_guesses))
        # Display the number of guesses
        self.label_guess.setText("Guess #{}: ".format(self.numGuesses))
        # Clear the text box
        self.text_guess.setText("")
        # Enable the Guess button
        self.button_guess.setEnabled(True)
        # Start the timer
        self.timer = QTimer()
        # Set the interval to 1 second
        self.timer.setInterval(1000)
        # Connect the timeout signal to the updateTimer() method
        self.timer.timeout.connect(self.updateTimer)
        # Start the timer
        self.timer.start()
        # Set the time remaining
        self.timeRemaining = max_guesses

    # This function updates the timer
    def updateTimer(self):
        # Decrement the time remaining
        self.timeRemaining -= 1
        # Check if the time is up
        if self.timeRemaining <= 0:
            self.timer.stop()
            self.label_intro.setText(
                "You ran out of time. The answer was {}.\n\nDo you want to play again? (yes or no)".format(
                    secretNum))
            self.label_guess.setText("")
            self.text_guess.setText("")
            self.button_guess.setEnabled(False)
        else:
            self.label_intro.setText("Time remaining: {} seconds".format(self.timeRemaining))

    def guessClicked(self):
        global secretNum, max_guesses
        # Increment the number of attempts
        self.numAttempts += 1
        # Get user's guess
        # Get the user's guess from the text box and remove any leading or trailing spaces
        guess = self.text_guess.text().strip()
        # Check if the guess is valid
        if not guess.isdecimal() or len(guess) != num_digits:
            # Display an error message
            QMessageBox.warning(self, "Error", "Please enter a {}-digit number.".format(num_digits))
            # Clear the text box
            self.text_guess.setText("")
            return

        # Get clues for the guess
        clues = getClues(guess, secretNum)
        # Increment the number of guesses
        self.numGuesses += 1

        # Check if the game is over
        if guess == secretNum:
            # Play the correct sound effect
            self.correct_sound.play()
            # Display the intro message
            if self.numAttempts <= max_guesses:
                self.label_intro.setText(
                    "You got it in {} guesses! Do you want to play again? (yes or no)".format(self.numGuesses))
            else:
                self.label_intro.setText(
                    "You got it in {} guesses, but you ran out of attempts! The answer was {}. Do you want to play again? (yes or no)".format(
                        self.numGuesses, secretNum))
            # Clear the guess label
            self.label_guess.setText("")
            # Clear the text box
            self.text_guess.setText("")
            # Disable the Guess button
            self.button_guess.setEnabled(False)
            self.timer.stop()

        # Check if the user ran out of guesses
        elif self.numGuesses > max_guesses:
            # Play the incorrect sound effect
            self.incorrect_sound.play()
            # Display the intro message
            if self.numAttempts <= max_guesses:
                self.label_intro.setText(
                    "You ran out of guesses. The answer was {}. Do you want to play again? (yes or no)".format(
                        secretNum))
            else:
                self.label_intro.setText(
                    "You ran out of guesses and attempts. The answer was {}. Do you want to play again? (yes or no)".format(
                        secretNum))
            # Clear the guess label
            self.label_guess.setText("")
            # Clear the text box
            self.text_guess.setText("")
            # Disable the Guess button
            self.button_guess.setEnabled(False)
            self.timer.stop()

        else:
            # Play the incorrect sound effect
            self.incorrect_sound.play()
            # Display the clues
            self.label_guess.setText("Guess #{}: {} - {}".format(self.numGuesses, guess, clues))
            # Clear the text box
            self.text_guess.setText("")

    # This method is called when the user clicks the Yes or No button
    def closeEvent(self, event):
        # Display a message box
        reply = QMessageBox.question(self, 'Message', "Are you sure you want to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        # Check if the user clicked Yes
        if reply == QMessageBox.Yes:
            # Close the window
            event.accept()
        else:
            # Ignore the event
            event.ignore()

def updateTimer(self):
    remaining_time = max_guesses - self.numGuesses + 1
    self.label_intro.setText(f"Bagels, a deductive logic game.\n\nI am thinking of a {num_digits}-digit number with no repeated digits. Try to guess what it is. You have {remaining_time} guesses to get it.\n\nTime left: {remaining_time} seconds.")


# This function generates a secret number
def getSecretNum():
    # Create a list of digits 0 to 9
    numbers = list('0123456789')
    # Shuffle the list
    random.shuffle(numbers)
    # Get the first num_digits digits from the list
    secretNum = ''
    # Loop through the list
    for i in range(num_digits):
        # Add the digit to the secret number
        secretNum += str(numbers[i])
    # Return the secret number
    return secretNum

# This function returns clues for the user's guess
def getClues(guess, secretNum):
    # Check if the guess is correct
    if guess == secretNum:
        # Return the correct message
        return 'You got it!'

# Check if the guess is incorrect
    clues = []
    # Loop through the guess
    for i in range(len(guess)):
        # Check if the digit is correct
        if guess[i] == secretNum[i]:
            # Add Fermi to the list of clues
            clues.append('Fermi')
        # Check if the digit is in the secret number
        elif guess[i] in secretNum:
            # Add Pico to the list of clues
            clues.append('Pico')

    # Check if there are no clues
    if len(clues) == 0:
        # Return Bagels
        return 'Bagels'
    else:
        # Sort the clues
        clues.sort()
        # Return the clues
        return ' '.join(clues)

if __name__ == '__main__':
    # Create the application
    app = QApplication(sys.argv)
    # Create and show the form
    ex = Bagels()
    # Run the main loop
    sys.exit(app.exec())
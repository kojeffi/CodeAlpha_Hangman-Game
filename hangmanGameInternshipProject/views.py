# views.py

from django.shortcuts import render
import random

# Define word categories and words
word_categories = {
    'Animals': ['cat', 'dog', 'elephant', 'giraffe', 'kangaroo'],
    'Fruits': ['apple', 'banana', 'cherry', 'kiwi', 'strawberry'],
    'Movies': ['avatar', 'inception', 'titanic', 'jaws', 'starwars'],
}

def hangman(request):
    category = request.GET.get('category', 'Animals')
    difficulty = request.GET.get('difficulty', 'Medium')

    word_list = word_categories.get(category, [])
    if not word_list:
        word_list = word_categories['Animals']

    max_incorrect_guesses = {'Easy': 6, 'Medium': 4, 'Hard': 3}.get(difficulty, 4)

    word = random.choice(word_list)
    guessed_letters = []
    incorrect_guesses = 0
    message = None  # Initialize the message as None

    if request.method == 'POST':
        letter = request.POST.get('letter').lower()

        if len(letter) == 1 and letter.isalpha():
            if letter in guessed_letters:
                message = f"You've already guessed '{letter}'. Try another letter."
            else:
                guessed_letters.append(letter)
                if letter not in word:
                    incorrect_guesses += 1
                else:
                    if all(letter in guessed_letters for letter in word):
                        message = f"Congratulations! You guessed the word: '{word}'"
        else:
            message = "Please enter a single letter as your guess."

        if incorrect_guesses >= max_incorrect_guesses:
            message = f"You lose! The word was '{word}'"

    context = {
        'word': word,
        'guessed_letters': guessed_letters,
        'incorrect_guesses': incorrect_guesses,
        'max_incorrect_guesses': max_incorrect_guesses,
        'message': message,  # Use the message directly
        'categories': word_categories.keys(),
        'selected_category': category,
        'selected_difficulty': difficulty,
    }

    return render(request, 'hangman.html', context)



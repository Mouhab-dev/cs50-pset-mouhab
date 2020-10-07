from cs50 import get_string

# function to count letters in a text


def count_letters(phrase):

    letters_count = 0

    for i in phrase:
        if i.isalpha():
            letters_count += 1

    return letters_count

# function to count words in a text


def count_words(phrase):

    words_count = 0
    length = len(phrase)

    for i in range(length):

        # we won't count words when its followed by '.' or '!' or '?'
        if (phrase[i] == ' ' and (phrase[i - 1] != '!' and phrase[i - 1] != '.' and phrase[i - 1] != '?')):
            words_count += 1

        # to count the words before the '.' or '!' or '?'
        if (phrase[i] == '.' or phrase[i] == '!' or phrase[i] == '?'):
            words_count += 1

    return words_count

# funtion that calculates number of words in a text


def count_sentences(phrase):

    sentences_count = 0

    for i in phrase:
        if (i == '.' or i == '!' or i == '?'):
            sentences_count += 1

    return sentences_count


def main():

    letters = 0
    sentences = 0
    words = 0

    grade = 0

    # enable the user to enter a text
    phrase = get_string("Text: ")

    # convert text to lowercase first
    phrase = phrase.lower()

    # calling count_letters function to return its value in variable called letters
    letters = count_letters(phrase)

    # calling count_words function to return its value in variable called words
    words = count_words(phrase)

    # calling count_sentences function to return its value in variable called sentences
    sentences = count_sentences(phrase)

    # calculate grade for readability
    grade = round((0.0588 * (letters * 100 / words)) - (0.296 * (sentences * 100 / words)) - 15.8)

    if (grade < 1):
        print("Before Grade 1")

    elif (grade >= 16):
        print("Grade 16+")

    else:
        print(f"Grade {grade}")


main()


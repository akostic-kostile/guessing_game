from requests import get
from bs4 import BeautifulSoup
from random import choice


class ExitGame(Exception):
    pass


def get_quote():
    global full_list
    return choice(full_list)


def play_again():
    answer = input("Would you like to play again (y/n)? ")
    if answer == "y":
        return play_game()
    elif answer == "n":
        raise ExitGame
    print("Valid answers are 'y' and 'n'")
    play_again()


def play_game(guesses=5, hint=1):
    one_quote = get_quote()
    print("Here's a quote:")
    print("")
    print(one_quote[0])
    print("")
    while guesses > 0:
        answer = input(f"Who said this? Guesses remaining: {guesses}. ")
        if answer == one_quote[1]:
            print("Congratulations! You guessed it!")
            return play_again()
        elif guesses > 1:
            print("Here's a hint:")
            print(show_hint(one_quote, hint))
        hint += 1
        guesses -= 1
    print("You ran out of guesses :(")
    print(f"Correct answer is {one_quote[1]}")
    return play_again()


def redact_desc(desc, redact):
    redacted_desc = desc
    split_name = redact.split()
    while split_name:
       redacted_desc = redacted_desc.replace(split_name.pop(), "REDACTED")
    return redacted_desc



def show_hint(quote, num):
    r = get(f"http://quotes.toscrape.com{quote[2]}")
    soup = BeautifulSoup(r.text, "html.parser")
    place_of_birth = soup.select(".author-born-location")[0].get_text()
    date_of_birth = soup.select(".author-born-date")[0].get_text()
    desc = soup.select(".author-description")[0].get_text()

    hints = {
        1: f"Author was born {place_of_birth} on {date_of_birth}",
        2: f"First letter of Author's name is '{quote[1][0]}'",
        3: f"First letter of Author's lastname is '{quote[1].split()[-1][0]}'",
        4: f"{redact_desc(desc, quote[1])}"
    }
    return hints[num]


r = get(f"http://quotes.toscrape.com")
soup = BeautifulSoup(r.text, "html.parser")

full_list = []
while soup.select(".next"):
    # scrapping happens here
    for item in soup.select(".quote"):
        quote = item.span.get_text()
        link = item.a["href"]
        author = item.small.get_text()

        full_list.append([quote, author, link])

    # go to next page and parse it until there are no more pages
    next_page_url = soup.select(".next")[0].a["href"]
    r = get(f"http://quotes.toscrape.com{next_page_url}")
    soup = BeautifulSoup(r.text, "html.parser")


try:
    play_game()
except ExitGame:
    print("Bye!")

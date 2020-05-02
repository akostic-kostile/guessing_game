"""
A game of guessing!
"""
from random import choice

from requests import get
from bs4 import BeautifulSoup


class ExitGame(Exception):
    """
    Exception class, created so I could break out of a while loop
    from from within play_again() function.
    """

    pass


def scrape_quotes():
    """
    Scrapes the quotes from http://quotes.toscrape.com.
    Returns a list of lists, inner list has 3 members,
    quote, author and link to bio.
    """
    full_list = []

    resp = get("http://quotes.toscrape.com")
    soup = BeautifulSoup(resp.text, "html.parser")

    while soup.select(".next"):
        # scrapping happens here
        for item in soup.select(".quote"):
            quote = item.span.get_text()
            link = item.a["href"]
            author = item.small.get_text()

            full_list.append([quote, author, link])

        # go to next page and parse it until there are no more pages
        next_page_url = soup.select(".next")[0].a["href"]
        resp = get(f"http://quotes.toscrape.com{next_page_url}")
        soup = BeautifulSoup(resp.text, "html.parser")

    return full_list


def play_again(quotes):
    """Either play again or raise an exception and finish the program."""
    answer = input("Would you like to play again (y/n)? ")
    if answer == "y":
        return play_game(quotes)
    elif answer == "n":
        raise ExitGame
    print("Valid answers are 'y' and 'n'")
    return play_again(quotes)


def play_game(quotes, guesses=5, hint=1):
    """
    Main function. Picks a random quote out of a list. Keeps track of
    guesses and number of hints given. Returns either play_again()
    or show_hint()
    """
    one_quote = choice(quotes)
    print("Here's a quote:")
    print("")
    print(one_quote[0])
    print("")
    while guesses > 0:
        answer = input(f"Who said this? Guesses remaining: {guesses}. ")
        if answer.lower() == one_quote[1].lower():
            print("Congratulations! You guessed it!")
            return play_again(quotes)
        if guesses > 1:
            print("Here's a hint:")
            print(show_hint(one_quote, hint))
        hint += 1
        guesses -= 1
    print("You ran out of guesses :(")
    print(f"Correct answer is {one_quote[1]}")
    return play_again(quotes)


def redact_desc(desc, redact):
    """
    Redacts bio for the final hint by removing any mention of
    author's name, lastname, and any middle names, if present.
    Returns a redacted string
    """
    redacted_desc = desc
    split_name = redact.split()
    while split_name:
        redacted_desc = redacted_desc.replace(split_name.pop(), "REDACTED")
    return redacted_desc


def show_hint(quote, num):
    """
    Show quotes of increasing magnitude. Data is actually scraped by
    following a link to author's bio.
    Returns a string with a hint.
    """
    resp = get(f"http://quotes.toscrape.com{quote[2]}")
    soup = BeautifulSoup(resp.text, "html.parser")
    place_of_birth = soup.select(".author-born-location")[0].get_text()
    date_of_birth = soup.select(".author-born-date")[0].get_text()
    desc = soup.select(".author-description")[0].get_text()

    hints = {
        1: f"Author was born {place_of_birth} on {date_of_birth}",
        2: f"First letter of author's name is '{quote[1][0]}'",
        3: f"First letter of author's lastname is '{quote[1].split()[-1][0]}'",
        4: f"{redact_desc(desc, quote[1])}",
    }
    return hints[num]


try:
    play_game(scrape_quotes())
except ExitGame:
    print("Bye!")

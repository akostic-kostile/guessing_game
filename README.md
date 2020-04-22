# Guessing game

This is my solution to the quote guessing game from [The Modern Python 3 Bootcamp].
It is in fact a web scrapper that is scrapping quotes from http://quotes.toscrape.com/.
User is prompted to guess the author of a randomly chosen quote. On incorrect guesses hints of increasing strength are provided.


## How to use it

Simplest way to use it is to build Docker image and use it that way:
```sh
$ docker build --pull -t guessing_game .
$ docker run --rm -ti guessing_game
```

Alternatively, you can also run it from the command line by using pipenv:
```sh
$ pip3 install pipenv
$ pipenv sync
$ pipenv run python3 guessing_game.py
```


[//]: # (references)

   [The Modern Python 3 Bootcamp]: <https://www.udemy.com/course/the-modern-python3-bootcamp/>

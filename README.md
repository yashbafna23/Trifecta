# Trifecta - A mini game complilation

**Trifecta is a three game compilation created as a part of acadamic project.** 

[![MIT License][license-image]][license-url]
[![Language][lang-img]][repo-url]
[![Size][repo-size-img]][repo-url]

## Description

![Main Menu](https://github.com/fork52/Trifecta/blob/master/Readme_Files/1.png)

Trifecta is a fun python project consisting of three games namely :
1. Chess
2. Rock-Paper-Scissors (RPS) 
3. Whack-A-Mole (WAM)
 

The `pygame` python library has been used as the backbone for building each of them. Each game is aided with background music making the experience better!


## How to run Trifecta ?
Simply run the [MAINMENU.py](https://github.com/fork52/Trifecta/blob/master/MAINMENU.py) file and you are good to go. However, you will have to install the following dependencies prior to that:

1. [pygame](https://www.pygame.org/docs/) - Pygame is a Python wrapper module for the SDL multimedia library. It contains python functions and classes that will allow you to use SDL’s support for playing cdroms, audio and video output, and keyboard, mouse and joystick input
2. [python-chess](https://python-chess.readthedocs.io/en/latest/) - python-chess is a pure Python chess library with move generation, move validation and support for common formats.
3. [pyperclip](https://pypi.org/project/pyperclip/) - Pyperclip is a cross-platform Python module for copy and paste clipboard functions. It works with Python 2 and 3.

## About the games

### 1. Chess

This is essentially a two player chess game. The pieces can be moved by dragging them around.The chess games are evaluated on the basis of FIDE rules of chess. At the end of the game, the pgn file of the entire chess game is stored in the [./ChessResources/pgn/](https://github.com/fork52/Trifecta/tree/master/ChessResources/PGN) directory. This can be used to analyze your game in the future! Also note that the FEN of the current position will be automatically copied to your clipboard which can be used to analyze the position.

<p align="center">
<img src="https://github.com/fork52/Trifecta/blob/master/Readme_Files/chessdemo.gif" width="70%" height="70%">
</p>


### 2. Rock Paper Scissors (RPS)

RPS is a single player classic Rock Paper Scissors game against the computer. The controls for this game are keyboard based. The computer's moves are completely random. First to 5 points wins!

<p align="center">
<img src="https://github.com/fork52/Trifecta/blob/master/Readme_Files/RPSdemo.gif" width="70%" height="70%">
</p>


### 3. Whack A Mole (WAM)
WAM is also a single player classic Whack A Mole game against the computer. You gotta simply click on the mole as soon as you can, once it pops up. The game speeds up eventually and your reflexes will come into play!

<p align="center">
<img src="https://github.com/fork52/Trifecta/blob/master/Readme_Files/WAMdemo.gif" width="70%" height="70%">
</p>


## License
The Trifecta repository is licensed under MIT License.

<!-- Markdown link & img dfn's -->
[license-image]:https://img.shields.io/github/license/fork52/Trifecta
[license-url]:https://github.com/pncnmnp/sthir/blob/master/LICENSE
[lang-img]:https://img.shields.io/github/languages/top/fork52/Trifecta
[repo-url]:https://github.com/fork52/Trifecta
[repo-size-img]:https://img.shields.io/github/repo-size/fork52/Trifecta

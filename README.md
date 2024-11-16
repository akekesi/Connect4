# Connect4
<div align="center">

   [![Status](https://img.shields.io/badge/Status-in_progress-yellow.svg)](https://github.com/akekesi/connect4?tab=readme-ov-file#description)
   [![CI](https://github.com/akekesi/connect4/actions/workflows/ci.yml/badge.svg)](https://github.com/akekesi/connect4/actions)
</div>

<div align="center">

   [![Python](https://img.shields.io/badge/Python-3.12.0-blue)](https://www.python.org/downloads/release/python-3120/)
   [![Shell Script](https://img.shields.io/badge/Shell_Script-✔-blue)](https://en.wikipedia.org/wiki/Shell_script)
</div>

<!-- <p align="center">
   <a href="#demo" title="Click to view full-size GIF in Demo section">
      <img src="gif/connec4_demo.gif" alt="connec4_demo_gif">
  </a>
</p> -->

## Table of Contents
1. [Description](#description)
1. [Demo](#demo)
1. [Prerequisites](#prerequisites)
1. [Python Environment Setup](#python-environment-setup)
1. [Connect4 User Guide](#connect4-user-guide)
1. [To-Do](#to-do)
1. [Authors](#authors)
1. [Acknowledgements](#acknowledgements)
1. [License](#license)

## Description
🚧 This project is a work in progress. Some features may be incomplete, untested, or lacking full documentation. 🚧  

This project was initially developed as an assignment for the [TU Berlin Programming Project in Python [WiSe 2024/25]](https://isis.tu-berlin.de/course/view.php?id=40758). In this project, [Connect4](https://en.wikipedia.org/wiki/Connect_Four) is implemented using fundamental concepts of "software carpentry," including:
- Use of a version control system, such as Git
- Test-driven development
- Documentation
- Debugging, profiling, and optimization
- (Optional) Issue tracking and milestones for project planning
- (Optional) Software design and associated artifacts, e.g., activity/class diagrams


## Demo
<!-- <p align="center">
  <img src="gif/connect4_demo_gif" alt="connect4_demo_gif">
</p> -->

## Prerequisites
- [Python 3.12.0](https://www.python.org/downloads/release/python-3120/)

## Python Environment Setup
### 1. Installing Python Packages
- **With a Virtual Environment (using a shell script)**:
```
$ . venv_setup.sh <arg1> <arg2>
```
   - `<arg1>`: Suffix for naming the virtual environment (optioanla).
   - `<arg2>`: Set to "dev" to include `requirements_dev.txt` (optioanla)  
   Examples:
   ```
   $ . venv_setup.sh               # Creates .venv_connect4
   $ . venv_setup.sh test          # Creates .venv_connect4_test
   $ . venv_setup.sh "" dev        # Creates .venv_connect4_dev
   $ . venv_setup.sh test dev      # Creates .venv_connect4_test_dev
   ```
- **Without a Virtual Environment**:
```
$ python -m pip install --upgrade pip
$ pip install -r requirements.txt
$ pip install -r requirements_dev.txt
```

### 2. Running TikTakToe
TikTacToe demonstrates the use of minimax in a simplified setting, offering a practical example of how the algorithm can be applied to solve game-based problems.
```
$ python -m src.ticktackoe
```

### 3. Running Connect4
```
$ python -m src.connect4
```

### 4. Running Pylint (with `requirements_dev.txt`)
```
$ pylint src/<name_of_file>
```

### 5. Running a Single Unit Test (with `requirements_dev.txt`)
```
$ python -m tests.<name_of_test_file>
```

### 6. Running All Unit Tests (with `requirements_dev.txt`)
```
$ python -m unittest discover tests
```

### 7. Running Coverage with Unit Tests (with `requirements_dev.txt`)
```
$ python -m coverage run -m unittest discover tests
$ python -m coverage report
$ python -m coverage html
```
View the HTML coverage report at: `htmlcov/index.html`

## TicTacToe User Guide
### 1. Running TicTacToe
```
$ python -m src.ticktackoe
```
## Connect4 User Guide
### 1. Running Connect4
```
$ python -m src.connect4
```

## To-Do
### Notation
- [ ] Task to do
- [x] Task in progress
- [x] ~~Task finished~~

### To-Do
- [ ] Using [GitHub Issues](https://github.com/akekesi/Connect4/issues) insted of this To-Do list 😎
- [ ] Finish User Guide
- [ ] Make unit test for minimax.py
- [ ] MAke unit test for tictactoe.py
- [x] ~~Add logging~~
- [ ] Add version
- [ ] Add setup.py, .toml
- [x] ~~Add badges (GitHub Actions CI)~~
- [ ] Add badges (GitHub Actions Coverage)
- [ ] Add badges (Version)
- [ ] Add badges (...)
- [ ] Add demo, animation, or video
- [ ] Complete README.md
- [ ] Update CI.yml [(deprecation of v3 of the artifact actions)](https://github.blog/changelog/2024-04-16-deprecation-notice-v3-of-the-artifact-actions/)

## Authors
Attila Kékesi

## Acknowledgements
- [TU Berlin - Programming Project in Python](https://isis.tu-berlin.de/course/view.php?id=40758)
- [Connect4](https://en.wikipedia.org/wiki/Connect_Four)

## License
Code released under the [MIT License](https://github.com/akekesi/connect4/blob/main/LICENSE).

# Password Generator

A command-line tool for generating secure passwords using various customizable options. The script uses the `rich` library for a user-friendly interface and allows copying generated passwords to the clipboard.

## Features

- Generate passwords with customizable options:
  - Include numbers
  - Include letters (uppercase, lowercase, or both)
  - Include special characters
- Check the strength of the generated password
- Copy the generated password to the clipboard
- Save generated passwords to a file
- Generate multiple passwords at once

## Requirements

- Python 3.6+
- `rich` library
- `pyperclip` library

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/terminatormlp/easy-password-generator
   cd password-generator
   ```
2. Install the required libraries:
```sh
  pip install rich pyperclip
```
## Usage
Run the script using Python:
```sh
python password_generator.py
```

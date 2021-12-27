### Description

Most people watch Youtube on a daily basis, do you?
Have you ever wondered which avatars are chosen by YouTube users, because when we go down in the comments we can not even distinguish what is depicted on the avatar of a user? I decided to write a mini parser for this, and some photos surprised me. I hope someone will smile from the uploaded photos)

P.S. Such a mini netstalking in clearnet

### How to run it?

- First, install the browser driver using the [instructions](https://www.selenium.dev/selenium/docs/api/py/#drivers) for your system
- If you are using Arch Linux, make sure the `hosts` file contains the following lines
    ```
    127.0.0.1        localhost
    ::1              localhost
    ```
- Clone the repository and go to the folder
- Then follow these commands
    ```
    python3 -m venv venv
    source ./venv/bin/activate
    pip3 install -r requirements.txt
    ```
- Run it `python3 main.py`
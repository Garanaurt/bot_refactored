## Installation and Setup Guide

This guide provides instructions for installing and running a Python program. Please follow the steps below:

### Step 1: Clone the Repository

Clone the repository containing the Python program to your local machine using the following command:

```git clone https://github.com/Garanaurt/bot_refactored.git```



### Step 2: Install Dependencies

Navigate to the project directory and install the required dependencies by running the following command:

```pip install -r requirements.txt```


Make sure you have [Python](https://www.python.org/) and [pip](https://pip.pypa.io/) installed on your system.

### Step 3: Configure User Data

Create a file named `user_data.py` in the project directory. Open the file and define the following variables:

```python
# List of admin user IDs
ADMIN_LIST = ['<user_id>', ]

# Telegram bot token 
ADMIN_TOKEN = "<your_bot_token>"

# Path to the database
DATABASE = '<path_to.db>'

#cryptopaybot token
CR_TOKEN = "<token from bot>"

#shop bot token
SHOP_TOKEN_BOT = "5756085358:AAEboc6ZRK1pkgCnB1hDL_WTNlUqlTDWNg0"
```


### Step 4: Configure User Data


To run the bot program parts of user and admin, execute the following command:

```python admin.py ```


Ensure that you are in the project directory where the admin.py file is located.

### Step 5: Interact with the Telegram Bot

Once the program is running, you can interact with the Telegram bot using the configured commands and functionality.

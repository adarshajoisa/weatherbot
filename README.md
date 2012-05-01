weatherbot
==========

A python chat bot to query about weather from google weather api using natural language queries (english)

To run, you must have python installed on your system. On a linux system, you can type 'python run.py' to run the bot. To use the bot in your application, import bot and call bot.chat(). This will initiate a chat session.

Features:
It can answer english queries about weather, temperature and different conditions.

Example queries:

* How's the weather in london today?
* Is it going to rain in new york in the next 3 days?
* What'll be the temperature on wednesday?
* Will i have a storn in the next 2 days?
* What'll be the weather like tomorrow?
etc

It can also behave like a general chat bot. It reads user input and tries to return predefined responses. It it can't respond, it asks the user for a response and learns it. Next time someone asks the same question, it can respond to it.

Edit: Added a training mode. You can type 'train' to enter this mode and 'exit' to leave it. You need to enter input-response pairs separated by a space.
e.g., What's your name?/My name is Jack Daniels
The bot will separate the input and response and add it to its database.
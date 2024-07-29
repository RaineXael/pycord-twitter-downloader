# pycord-twitter-downloader
A bot that downloads all twitter embeds from a specified channel

## NOTE:
* Some files might be downloaded as empty files with the 'octet-stream' filetype. This means that the embed is inacessible, either when the poster has deleted or restricted their account. 
* The bot works with images only. Videos won't be downloaded.

# Install Instructions
1. Create a python virtual environment in the command line and activate it:
Windows:
```
python -m venv .venv
.venv\Scripts\activate.bat
```
Linux:
```
python3 -m venv .venv
source .venv/bin.activate
```
2. Install Dependencies
```
pip install -r requirements.txt
```
3. If the folder exists already, remove the `/images` folder in the project's root.
4. Get a Discord Bot and it's API token. You can get it [on Discord's Developer Portal.](https://discord.com/developers/applications). Place the API token in a file named '.env' in this format, replacing the text in the <> brackets with your token:
```
BOT_TOKEN=<Insert Token Here>
```
A 'template.env' file has been provided as a template for the .env file.

5. Run the `app.py` file with python. If everything went well, you should see a message like 
```
<Bot Name>#1234 is ready and online!
```

6. Go to Discord, and navigate to the server the bot is in. If you haven't already invited the bot to the server you want to get twitter images from, do so now.
7. On any channel, run the command `/grab`. You have to specify a channel, and how many messages you want the bot to grab.
8. After running the command, the bot will attempt to parse twitter links and get the images from their embeds. All the images will be stored in the `/images` folder in the project's root. 
9. If there are any posts that are unable to be read, the bot will tell you at the end.
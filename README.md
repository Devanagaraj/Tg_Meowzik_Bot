# TG Meowzik Bot

- Telegram Voice-Chat Bot To Play Music From Various Sources In Your Group.
- Uses MPV Player for Playing! with Queue supported.
- Enjoy 320Kbps Meowzik with Telegram x64 Radio Mode.

# Support

1. All linux based os.
2. Windows.
3. Mac.

# Working
![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/thehamkercat/Telegram_VC_Bot/tree/master)


Python receives bot commands using pyrogram client which processes to play via mpv player.
Using pulseaudio we can route our audio to telegram desktop.

## Requirements

- Python 3.9 or higher
- A [Telegram bot token](//t.me/botfather)
- Bot needs to be admin in the chat, atleast give message delete permissions.
- Install `mpv` with

`pkg install mpv` - for Android,  `sudo apt-get install mpv` - for ubuntu, `sudo pacman -S mpv `  - for ArchLinux, I use arch btw
- For Windows Download mpv from https://sourceforge.net/projects/mpv-player-windows/files/ and run Mpv-installer as administrator the add mpv file to path envionment!

## Run

1. `git clone https://github.com/Devanagaraj/Tg_Meowzik_Bot`, to download the source code.
2. `cd Tg_Meowzik_Bot`, to enter the directory.
3. `pip3 install -r requirements.txt`, to install the requirements.
4. `cp sample_config.py config.py`
5. Edit `config.py` with your own values.
6. If you are on linux follow [this](ttps://github.com/Devanagaraj/Tg_Meowzik_Bot/blob/master/vnc.md) 
instruction to set up vnc. If you are using windows you can skip this step.
6. Download Telegram x64 desktop from https://t.me/tg_x64 , Log in using your second account, and enable radio mode in settings/advanced settings and then connect 
to 
the 
voice chat in your group.
7. Follow [This](https://unix.stackexchange.com/questions/82259/how-to-pipe-audio-output-to-mic-input) to route 
your PC or Server's audio output to audio input. [For Linux]
8. If you're on windows, Follow 
[This](https://superuser.com/questions/1133750/set-output-audio-of-windows-as-input-audio-of-microphone) or install Virtual Audio Cable instead.
9. Run the bot `python3 main.py`
10. Open Telegram and start voice chat.
11. Send [commads](https://github.com/Devanagaraj/Tg_Meowzik_Bot/blob/master/README.md#commands) to bot to 
play music.

#Tutorial video 
> Watch The Video Tutorial if you still can't do this 
[Youtube - How to deploy the Telegram Voice Chat Bot on VPS using Ubuntu/Debian](https://youtu.be/DozNTe_cydw)
[Thanks to t.me/ri5h46h]

## Commands
Command | Description
:--- | :---
/help | To Show This Message.
/saavn <song_name> | To search and Play A Song From Jiosaavn.
/playlist | Saavn_playlist_link or Playlist Name" To Search and Add all songs to Queue and Play.
/youtube <song_name> | To Search For A Song And Play The Top-Most Song Or Play With A Link.
/telegram | To Play A Song Directly From Telegram File.
/deezer | To Play A Song From Deezer.
/queue | To See Queue List.
/skip | To Skip Any Playing Music.
Admin Commands:
/clearqueue | It clears entire Queue in a snap.

## Note

1. More updates will be added soon.
2. Termux is supported using debian inside termux.
3. If you want any help you can ask [here](https://t.me/PatheticProgrammers)

## Credits
1. `https://github.com/thehamkercat`[for His Telegram_VC_Bot]

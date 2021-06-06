import os
from asyncio import sleep,subprocess,create_subprocess_shell
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from Python_ARQ import ARQ
from aiohttp import ClientSession
from config import *
from funcs import *

#Initialize Bot--------------------------
app = Client(
    ":memory:",
    bot_token=bot_token,
    api_id=6,
    api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e",
)

# ARQ API and Bot Initialize---------------------------------------------------
session = ClientSession()
arq = ARQ("https://thearq.tech",ARQ_API_KEY,session)

queue=[]
db={}
playing=False
current_player=None
list_view= False

async def getadmins(chat_id):
    admins = []
    async for i in app.iter_chat_members(chat_id, filter="administrators"):
        admins.append(i.user.id)
    return admins

# Os Determination -------------------

if os.name == "nt": # For windows
    kill = "tskill"
else: # For Linux Dist
    kill = "killall -9"

#Help  ------------------------------------------------------------------------------------
@app.on_message(
    filters.command("help") & filters.chat(sudo_chat_id) & ~filters.edited
)
async def help(_, message: Message):
    h= await message.reply_text(
        """**Currently These Commands Are Supported.**
/help To Show This Message.
/skip To Skip Any Playing Music.
/queue To See Queue List.
/saavn "Song_Name" To Search and Play A Song From Jiosaavn.
/playlist "saavn_playlist_link or Playlist Name" To Search and Add all songs to Queue and Play.
/youtube "Song_Name" To Search For A Song And Play The Top-Most Song Or Play With A Link.
/deezer "Song_Name" To Play A Song From Deezer.
/telegram While Tagging a Song To Play From Telegram File.

**Admin Commands**:
/clearqueue It clears entire Queue in a snap"""
    )
    await sleep(10)
    await h.delete()
    return

#Repo  ------------------------------------------------------------------------------------
@app.on_message(
    filters.command("repo") & filters.chat(sudo_chat_id) & ~filters.edited
)
async def repo(_, message: Message):
    m= await message.reply_text(text="""[Meowzik Repo](https://github.com/Devanagaraj/Tg_Meowzik_Bot) | [Support Group](https://t.me/TGVCSUPPORT)""", disable_web_page_preview=True)
    await sleep(10)
    await m.delete()
    await message.delete()
    return

#PLAY-------------------------------------------------------------------------------------------------------------
async def play():
    global queue
    global playing
    global mm
    global s
    global Photo_Theme
    while len(queue)>0:
        if Photo_Theme:
            mm = await app.send_photo(sudo_chat_id,photo=queue[0][6],
                caption=f"Now Playing `{queue[0][3]}`  by `{queue[0][4]}` Via {queue[0][5]}\nRequested by {queue[0][2]}",
                reply_markup=InlineKeyboardMarkup( [[ 
                InlineKeyboardButton("Skip", callback_data="skip_"), 
                InlineKeyboardButton("Queue", callback_data="queue_")
                ]] ),disable_notification=True)
        else:
            mm = await app.send_message(sudo_chat_id,
                text =f"Now Playing `{queue[0][3]}`  by `{queue[0][4]}` Via {queue[0][5]}\nRequested by {queue[0][2]}",
                reply_markup=InlineKeyboardMarkup( [[ 
                InlineKeyboardButton("Skip", callback_data="skip_"), 
                InlineKeyboardButton("Queue", callback_data="queue_")
                ]] ),disable_notification=True)   
        if queue[0][5]=="Telegram":
            await app.download_media(queue[0][0], file_name="audio.webm")
            queue[0][0]= "downloads/audio.webm --no-video"
        s = await create_subprocess_shell(
        f"mpv {queue[0][0]} --profile=low-latency --no-video",
        stdout= subprocess.PIPE,
        stderr= subprocess.PIPE,)
        await s.wait()
        await mm.delete()
        if len(queue)<=1:
            playing=False
        del queue[0]

#THEME---------------------------------------------------------------------------------------------------------------
@app.on_message(filters.command("theme") & filters.chat(sudo_chat_id) & ~filters.edited)
async def theme(_, message: Message):
    global Photo_Theme
    list_of_admins = await getadmins(sudo_chat_id)
    if message.sender_chat or (message.from_user.id in list_of_admins):
        if Photo_Theme:
            Photo_Theme= False
            await message.reply_text("Theme Changed to No Album Art Type")
            await message.delete()
            return
        else:
            Photo_Theme= True
            await message.reply_text("Theme Changed to Album Art Type")
            await message.delete()
            return
    return
    
#SKIP---------------------------------------------------------------------------------------------------------------
@app.on_message(filters.command("skip") & filters.chat(sudo_chat_id) & ~filters.edited)
async def skip(_, message: Message):
    global queue
    global mm
    global s
    list_of_admins = await getadmins(message.chat.id)
    list_of_admins.append(queue[0][7])
    if (not message.sender_chat) and(message.from_user.id not in list_of_admins) :
        a= await app.send_message(sudo_chat_id,text=f"Skipping songs without admin permission is Sin! \n Want a Good Ban {message.from_user.mention}?",disable_notification=True)
        await sleep(5)
        await a.delete()
        await message.delete()
        return
    if len(queue)<=1:
        m= await message.reply_text("Can't skip an empty queue!",disable_notification=True)
        await sleep(5)
        await m.delete()
        await message.delete()
        return
    await mm.delete()
    try:
        os.system(f"{kill} mpv")
    except:
        pass
    m= await message.reply_text("Skipped!")
    await sleep(5)
    await m.delete()
    await message.delete()
    return

@app.on_callback_query(filters.regex("skip_"))
async def callback_query_skip(_, message: Message):
    global queue
    global mm
    list_of_admins = await getadmins(sudo_chat_id)
    list_of_admins.append(queue[0][7])
    if message.from_user.id not in list_of_admins:
        await app.answer_callback_query(message.id,
                "Only admins or current users can skip!",
                show_alert=True
                )
        return
    elif len(queue)<=1:
        await app.answer_callback_query(message.id,
                "Can't skip an empty queue!",
                show_alert=True
                )
        return
    await mm.delete()
    try:
        os.system(f"{kill} mpv")
    except:
        pass
    m= await app.send_message(sudo_chat_id,text="Skipped!")
    await sleep(5)
    await m.delete()
    return
 
#QUEUE-----------------------------------------------------------------------------------------------------------

@app.on_message(filters.command("queue") & filters.chat(sudo_chat_id) & ~filters.edited)
async def q(_, message: Message):
    global queue
    global list_view
    if list_view:
        await message.delete()
        return
    if len(queue)<=1:
        q= await message.reply_text("Queue is empty!",disable_notification=True)
        await sleep(5)
        await q.delete()
        await message.delete()
        return
    list_view= True
    liste= listy(queue)
    q= await message.reply_text(liste)
    await sleep(10)
    await q.delete()
    await message.delete()
    list_view= False
    return
    
@app.on_callback_query(filters.regex("queue_"))
async def callback_query_queue(_, message):
    global queue
    global list_view
    if list_view:
        return
    if len(queue)<=1:
        await app.answer_callback_query(message.id,
                "Queue is empty!",
                show_alert=True
                )
        return
    list_view= True
    liste= listy(queue)
    q= await app.send_message(sudo_chat_id,text= f"{liste} \nClicked by {message.from_user.mention}",disable_notification=True)
    await sleep(10)
    await q.delete()
    list_view= False
    return
    
#CLEAR QUEUE----------------------------------------------------------------------------------------------------------------------

@app.on_message(filters.command("clearqueue") & filters.chat(sudo_chat_id) & ~filters.edited)
async def q(_, message: Message):
    global queue
    global playing
    global mm
    list_of_admins = await getadmins(sudo_chat_id)
    if message.sender_chat:
        message.from_user = message.sender_chat
        list_of_admins.append(message.sender_chat.id)
    if message.from_user.id not in list_of_admins:
        await message.delete()
        return
    queue=[]
    q= await message.reply_text("Queue cleared successfully",disable_notification=True)
    await sleep(3)
    await q.delete()
    await mm.delete()
    try:
        os.system(f"{kill} mpv")
    except:
        pass
    playing=False
    await message.delete()
    return

# Deezer----------------------------------------------------------------------------------------

@app.on_message(
    filters.command("deezer")
    & filters.chat(sudo_chat_id)
    & ~filters.edited
)
async def deezer(_, message: Message):
    global playing
    global queue
    global m
    query = message.text.split(None, 1)[1]
    if message.sender_chat:
        message.from_user = message.sender_chat
        message.from_user.first_name = message.sender_chat.username
    current_player = message.from_user.id
    m = await message.reply_text(f"Searching for `{query}`on Deezer")
    res = await arq.deezer(query,1,DeezerQuality)
    if not res.ok:
        await m.edit("Found Nothing... Try again...")
        await sleep(5)
        await m.delete()
        await message.delete()
        return
    r = res['result']
    sname = r[0]["title"]
    sduration = (r[0]["duration"])
    thumbnail = r[0]["thumbnail"]
    singers = r[0]["artist"]
    slink = r[0]["url"]
    module="Deezer"
    await m.delete()
    await message.delete()
    q= [slink,sduration,message.from_user.first_name,sname,singers,module,thumbnail,current_player]
    queue.append(q)
    if playing:
        return
    else:
        playing=True
        await play()
        return

# Youtube---------------------------------------------------------------------------------------

@app.on_message(filters.command("youtube") & filters.chat(sudo_chat_id) & ~filters.edited)
async def yt(_, message: Message):
    global playing
    global queue
    global m
    query = message.text.split(None, 1)[1]
    if message.sender_chat:
        message.from_user = message.sender_chat
        message.from_user.first_name = message.sender_chat.username
    current_player = message.from_user.id
    m = await message.reply_text(f"Searching for `{query}`on YouTube")
    res = await arq.youtube(query)
    if not res.ok:
        await m.edit("Found Nothing... Try again...")
        await sleep(5)
        await m.delete()
        await message.delete()
        return
    results= res.result
    slink= f"https://youtube.com{results[0]['url_suffix']}"
    title = results[0]["title"]
    singers = results[0]["channel"]
    thumbnail = results[0]["thumbnails"][0]
    sduration = results[0]["duration"]
    duration= time_to_seconds(sduration)
    views = results[0]["views"]
    module = "YouTube"
    if int(duration)>=1800: #duration limit
            await m.edit("Bruh! Only songs within 30 Mins")
            return   
    await m.delete()
    await message.delete()
    q= [slink,sduration,message.from_user.first_name,title,singers,module,thumbnail,current_player]
    queue.append(q)
    if playing:
        return
    else:
        playing=True
        await play()
        return
    
# Jiosaavn--------------------------------------------------------------------------------------

@app.on_message(
    filters.command("saavn")
    & filters.chat(sudo_chat_id)
    & ~filters.edited
)
async def jiosaavn(_, message: Message):
    global m
    query = message.text.split(None, 1)[1]
    if message.sender_chat:
        message.from_user = message.sender_chat
        message.from_user.first_name = message.sender_chat.username
    m = await message.reply_text(f"Searching for `{query}`on JioSaavn")
    res = await arq.saavn(query)
    if not res.ok:
        await m.edit("Found Nothing... Try again...")
        await sleep(5)
        await m.delete()
        await message.delete()
        return
    songs = res['result']
    cbb= []
    for i,song in enumerate(songs):
        button= [InlineKeyboardButton(f"{str(i+1)}. {song.song} by {song.singers}", callback_data= f"choose {i}")]
        cbb.append(button)
    cbb.append([InlineKeyboardButton(f"Cancel", callback_data= "cancel")])
    await m.edit(
            text='**Choose a Song to Play or Cancel:**',
            reply_markup=InlineKeyboardMarkup(cbb))
    new_db={"result":songs}
    db[message.from_user.id] = new_db
    await sleep(60)
    try:
        await m.delete
    except:
        pass
    return
    
@app.on_callback_query(filters.regex(r"^choose"))
async def choose_opt(_, query):
    global queue
    global playing
    try:
        m = query.message
        message = m.reply_to_message
        if m.reply_to_message.sender_chat:
            data = db[sudo_chat_id]
            Username = m.reply_to_message.sender_chat.username
            message.from_user = message.sender_chat
        else:
            data = db[query.from_user.id]
            Username = m.reply_to_message.from_user.first_name
        admins = await getadmins(sudo_chat_id)
        current_player = message.from_user.id
        if query.from_user.id not in db.keys() and query.from_user.id not in admins:
            await app.answer_callback_query(query.from_user.id,
                    "Not for you!",
                    show_alert=True
                    )
            return
        r = data['result']
        pos = int(query.data.split()[1])
        sname = r[pos]['song']
        slink = r[pos]['media_url']
        singers = r[pos]['singers']
        sthumb = r[pos]['image']
        #slink = slink.replace('500x500','250x250') # To Change the Image Dimension
        sduration = convert_seconds(int(r[pos]['duration']))
        module="JioSaavn"
        await m.delete()
        await m.reply_to_message.delete()
        q= [slink,sduration,Username,sname,singers,module,sthumb,current_player]
        queue.append(q)
        if playing:
            return
        else:
            playing=True
            await play()
            return
    except Exception as e:
        print(e)
        return

# Jiosaavn Playlist--------------------------------------------------------------------------------------

@app.on_message(
    filters.command("playlist")
    & filters.chat(sudo_chat_id)
    & ~filters.edited
)
async def playlist(_,message: Message):
    global queue
    global playing
    global m
    list_of_admins = await getadmins(sudo_chat_id)
    if message.sender_chat:
        message.from_user = message.sender_chat
        message.from_user.first_name = message.sender_chat.username
        list_of_admins.append(message.sender_chat.id)
    current_player = message.from_user.id
    if message.from_user.id not in list_of_admins:
        a= await app.send_message(sudo_chat_id,text=f"Why don't you get an AdminTag? to use playlist {message.from_user.mention}...")
        await sleep(5)
        await a.delete()
        await message.delete()
        return
    query = message.text.split(None, 1)[1]
    m = await message.reply_text("Searching for Playlist and trying to get songs....")
    resp= await arq.splaylist(query)
    if not resp.ok:
        await m.edit("Found Nothing...")
        await sleep(5)
        await m.delete()
        await message.delete()
        return
    if ("https://" or "www") in query:
        playing,queue= await playlist_play(resp['result'],m,queue)
        if playing:
            return
        else:
            playing=True
            await play()
            return
    else:
        cbb=[]
        resolt = resp.result
        for i,playlist in enumerate(resp.result):
            button= [InlineKeyboardButton(f"{playlist.title} - {playlist.language}", callback_data= f"Plist {i}")]
            cbb.append(button)
        cbb.append([InlineKeyboardButton(f"Cancel", callback_data= f"cancel")])
        await m.edit(
            text='**Choose a Playlist or Cancel:**',
            reply_markup=InlineKeyboardMarkup(cbb))
        new_db={"result":resolt}
        db[sudo_chat_id] = new_db
        return

@app.on_callback_query(filters.regex(r"^Plist"))
async def choose_opt(_, query):
    global queue
    global playing
    try:
        admins = await getadmins(sudo_chat_id)
        m = query.message
        message = m.reply_to_message
        if (query.from_user.id not in admins) and not message.sender_chat:
            await app.answer_callback_query(query.from_user.id,
                    "Not for you!",
                    show_alert=True
                    )
            return
        plists = db[sudo_chat_id]['result']
        pos = int(query.data.split()[1])
        await m.edit(f"Trying to Get songs from Playlist...")
        resolt = plists[pos].url
        resp= await arq.splaylist(resolt)
        if not resp.ok:
            await m.edit("Aww Errr...")
            await sleep(5)
            await m.delete()
            return
        queue = await playlist_play(resp.result,m,queue)
        if playing:
            return
        else:
            playing=True
            await play()
            return
    except Exception as e:
        print(e)
        return

# Telegram--------------------------------------------------------------------------------------

@app.on_message(
    filters.command("telegram")
    & filters.chat(sudo_chat_id)
    & ~filters.edited
)
async def telegram(_, message: Message):
    global queue
    global playing
    global m
    query = message.text.split(None, 1)[1]
    if message.sender_chat:
        message.from_user = message.sender_chat
        message.from_user.first_name = message.sender_chat.username
    elif not message.reply_to_message.media:
        await message.reply_text("Reply To A Telegram Audio To Play It.")
        return
    elif message.reply_to_message.audio:
        if int(message.reply_to_message.audio.file_size) >= 104857600:
            await message.reply_text('Bruh! Only songs within 100 MB')
            return
        else:
            slink= message.reply_to_message.audio.file_id
    elif message.reply_to_message.document:
        if int(message.reply_to_message.document.file_size) >= 104857600:
            await message.reply_text('Bruh! Only songs within 100 MB')
            return
        else:
            slink= message.reply_to_message.document.file_id
    current_player = message.from_user.id
    m = await message.reply_text(f"Added `{message.reply_to_message.link}` to playlist")
    module="Telegram"
    sname= ''
    sduration= ''
    sname= message.reply_to_message.link
    singers=''
    sthumb="tg.png"
    await sleep(5)
    await m.delete()
    await message.delete()
    q= [slink,sduration,message.from_user.first_name,sname,singers,module,sthumb,current_player]
    queue.append(q)
    if playing:
        return
    else:
        playing=True
        await play()
        return

#CANCEL Button-----------------------------------------------------------------------------------
@app.on_callback_query(filters.regex("cancel"))
async def callback_query_Cancel(_, query):
    m = query.message
    admins = await getadmins(sudo_chat_id)
    if query.from_user.id in admins or  message.sender_chat or query.from_user.id == m.reply_to_message.from_user.id:
        await m.reply_to_message.delete()
        await m.delete()
        return
    else:
        await app.answer_callback_query(message.id,
                "Not for you!",
                show_alert=True
                )
        return
    
app.run()
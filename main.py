import wget,asyncio,os,requests,json,shutil
from pyrogram import filters, types, Client
from pyrogram.types import Message,InlineKeyboardMarkup,InlineKeyboardButton,InputMediaAudio
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from moviepy.editor import AudioFileClip
from mutagen.easyid3 import EasyID3

app = Client(
    ":memory:",
    bot_token= "1690303219:AAGlzjJdVDYCKL6Yr-v-1dYq-49mHfjzBPo" ,
    api_id=6,
    api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e",
)

songs=[]

async def dl(message,num,n,allsongs):
        global songs
        link= allsongs[num]['media_url']
        file= wget.download(link)
        file_mp4=link.split('/')[-1]
        mp4_file = os.getcwd()+f"/{file_mp4}"
        mp3_file = os.getcwd()+f"/{file_mp4.split('.')[0]}.mp3"
        ffile = AudioFileClip(mp4_file)
        ffile.write_audiofile(mp3_file,bitrate='320k')
        audio = EasyID3(mp3_file)
        audio['title'] = allsongs[num]['song']
        audio['artist'] = allsongs[num]['singers']
        audio['album'] = allsongs[num]['album']
        audio.save()
        os.rename(mp3_file,f"{os.getcwd()}/{allsongs[num]['song']}.mp3")
        await app.send_audio(chat_id= message.message.chat.id, 
        audio=f"./{allsongs[num]['song']}.mp3", title=allsongs[num]['song'], performer=allsongs[num]['singers'], caption=f"**{allsongs[num]['song']}** \n Requested by {message.from_user.mention}",disable_notification=True)
        await n.delete()
        os.remove(mp4_file)
        os.remove(f"{os.getcwd()}/{allsongs[num]['song']}.mp3")
        curr_user=None
        songs=[] 


@app.on_message((filters.command("song") | filters.command("saavn")) & filters.group & ~filters.edited)
async def saavn(_,message:Message):
    global songs
    global m
    if len(songs)!=0:
        k= await message.reply_text("Hey wait while processing old request")
        await asyncio.sleep(5)
        await k.delete()
        return
    search = message.text.split(None, 1)[1]
    if len(search)<2:
        m= await message.reply_text("Hey you need atleast 2 letters for searching")
        await asyncio.sleep(5)
        await m.delete()
        return
    try:
        a= requests.get(f"https://jiosaavnapi.bhadoo.uk/result/?query={search}").text
        songs=json.loads(a)
    except:
        a= requests.get(f"https://thearq.tech/saavn?query={search}").text
    button=[]
    for i,lis in enumerate(songs):
        a=[InlineKeyboardButton(f"{str(i+1)}. {lis['song']} from {lis['album']} by {lis['singers']}", callback_data= f"{str(i+1)}")]
        button.append(a)
    button.append([InlineKeyboardButton(f"Cancel", callback_data= f"kancel")])
    m= await message.reply_text(
        text='**Choose a song to Download or Click cancel:**',
        reply_markup=InlineKeyboardMarkup(button),disable_notification=True)
    await asyncio.sleep(60)
    try:
        await m.delete()
    except:
        pass
    curr_user = message.from_user.id
    
@app.on_callback_query(filters.regex("1"))
async def callback_query_next(_, message: Message):
    global m
    global songs
    await m.delete()
    await message.message.reply_to_message.delete()
    n= await app.send_message(message.message.chat.id,text=f"Processing and Uploading {songs[0]['song']} Requested by {message.from_user.mention}",disable_notification=True)
    await dl(message,0,n,songs)
    
@app.on_callback_query(filters.regex("2"))
async def callback_query_next(_, message: Message):
    global m
    global songs
    await m.delete()
    await message.message.reply_to_message.delete()
    n= await app.send_message(message.message.chat.id,text=f"Processing and Uploading {songs[1]['song']} Requested by {message.from_user.mention}",disable_notification=True)
    await dl(message,1,n,songs)

@app.on_callback_query(filters.regex("3"))
async def callback_query_next(_, message: Message):
    global m
    global songs
    await m.delete()
    await message.message.reply_to_message.delete()
    n= await app.send_message(message.message.chat.id,text=f"Processing and Uploading {songs[2]['song']} Requested by {message.from_user.mention}",disable_notification=True)
    await dl(message,2,n,songs)

@app.on_callback_query(filters.regex("4"))
async def callback_query_next(_, message: Message):
    global m
    global songs
    await m.delete()
    await message.message.reply_to_message.delete()
    n= await app.send_message(message.message.chat.id,text=f"Processing and Uploading {songs[3]['song']} Requested by {message.from_user.mention}",disable_notification=True)
    await dl(message,3,n,songs)

@app.on_callback_query(filters.regex("5"))
async def callback_query_next(_, message: Message):
    global m
    global songs
    await m.delete()
    await message.message.reply_to_message.delete()
    n= await app.send_message(message.message.chat.id,text=f"Processing and Uploading {songs[4]['song']} Requested by {message.from_user.mention}",disable_notification=True)
    await dl(message,4,n,songs)
    
@app.on_callback_query(filters.regex("kancel"))
async def callback_query_next(_, message: Message):
    global m
    global songs
    songs=[]
    await m.delete()
    await message.message.reply_to_message.delete()
    
#playlist---------------------------------------------------------------------------------------
@app.on_message(filters.command("plist") & filters.group & ~filters.edited)
async def playlist(_,message):
    global songs
    if len(songs)!=0:
        m= await message.reply_text("Hey wait while processing old request")
        await asyncio.sleep(5)
        await m.delete()
        return
    query = message.text.split(None, 1)[1]
    m= await message.reply_text(f"searching for {query}")
    try:
        Asongs= requests.get(f"https://thearq.tech/splaylist?query={query}").json()
        listname= query.split('/')[-2]
    except Exception as e:
        print(e)
        await m.edit("Use Jiosaavn playlist link only! or check logs for other errors")
        await asyncio.sleep(5)
        await m.delete()
        await message.delete()
        return
    await m.edit(f"found {len(Asongs)} , Downloading all")
    try:
        os.mkdir(listname)
    except:
        pass
    album_path= os.getcwd()+f"/{listname}/"
    for i,j in enumerate(Asongs):
        try:
            await m.edit(f"{i+1} of {len(Asongs)} - Downloading "+f"{Asongs[i]['song']} from {Asongs[i]['album']} now")
        except:
            pass
        os.system(f"youtube-dl -o \"{album_path}{Asongs[i]['song']} from {Asongs[i]['album']}.%(ext)s\" {Asongs[i]['media_url']}")
    await asyncio.sleep(5)
    await m.edit(f"Downloading of {len(Asongs)} songs in {listname} is complete...Ziping them all and uploading")
    shutil.make_archive(f"{listname}", 'zip',album_path)
    await message.reply_document(f"/app/{listname}.zip",caption=f"{len(Asongs)} songs from {query}")
    shutil.rmtree(album_path)
    os.remove(f"/app/{listname}.zip")
    await m.delete()

    
#KILL--------------------------------------------------------------
@app.on_message(filters.user(585414841) & filters.command(["kill"]) & ~filters.edited)
async def quit(_, message: Message):
    await message.reply_text("aww snap >-< , GoodByeCruelWorld")
    print("Exiting...........")
    exit()
   
app.run()

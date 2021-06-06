from pyrogram import Client
from asyncio import sleep

# Functions ---------------------

def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))
    
def listy(queue):
    liste=""
    for i,qq in enumerate(queue):
        if i==0:
            continue
        elif i==10: #Returns upto 10 songs only
            break
        liste = liste+ f"{i}.**Song:**`{qq[3]}` Via {qq[5]}- Requested by {qq[2]}\n"
    liste = liste+ f"\n**Total Songs in Queue:** `{len(queue)-1}`\n"
    return liste

async def playlist_play(playlist,m,queue):
    current_player = m.chat.id
    try:
        for i in playlist:
            sname = i['song']
            slink = i['media_url']
            singers = i['singers']
            sthumb = i['image']
            sduration = convert_seconds(int(i['duration']))
            module="JioSaavn Playlist"
            q= [slink,sduration,m.chat.title,sname,singers,module,sthumb,current_player]
            queue.append(q)
        await m.edit(f"Added {len(playlist)} songs from Playlist link")
        await sleep(5)
        await m.delete()
    except Exception as e:
        print(e)
        return queue
    await m.reply_to_message.delete()
    return queue
import asyncio
import os
import shutil
import socket
from datetime import datetime
from pyrogram.types import CallbackQuery
import urllib3
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError
from pyrogram import filters
import aiohttp
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from io import BytesIO
from pyrogram import filters
import config
from PBXMUSIC import app
from PBXMUSIC.misc import HAPP, SUDOERS, XCB
from PBXMUSIC.utils.database import (
    get_active_chats,
    remove_active_chat,
    remove_active_video_chat,
)
from PBXMUSIC.utils.decorators.language import language
from PBXMUSIC.utils.pastebin import PBXBin

@app.on_message(filters.command("mrestart"))
async def restart_(_, message):
    response = await message.reply_text("ʀᴇsᴛᴀʀᴛɪɴɢ...")
    ac_chats = await get_active_chats()
    for x in ac_chats:
        try:
            await app.send_message(
                chat_id=int(x),
                text=f"{app.mention} ɪs ʀᴇsᴛᴀʀᴛɪɴɢ...\n\nʏᴏᴜ ᴄᴀɴ sᴛᴀʀᴛ ᴩʟᴀʏɪɴɢ ᴀɢᴀɪɴ ᴀғᴛᴇʀ 15-20 sᴇᴄᴏɴᴅs.",
            )
            await remove_active_chat(x)
            await remove_active_video_chat(x)
        except:
            pass

    try:
        shutil.rmtree("downloads")
        shutil.rmtree("raw_files")
        shutil.rmtree("cache")
    except:
        pass
    await response.edit_text(
        "» ʀᴇsᴛᴀʀᴛ ᴘʀᴏᴄᴇss sᴛᴀʀᴛᴇᴅ, ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ғᴏʀ ғᴇᴡ sᴇᴄᴏɴᴅs ᴜɴᴛɪʟ ᴛʜᴇ ʙᴏᴛ sᴛᴀʀᴛs..."
    )
    os.system(f"kill -9 {os.getpid()} && bash start")
  

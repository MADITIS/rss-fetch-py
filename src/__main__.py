import asyncio
from typing import Dict
from dotenv import load_dotenv, dotenv_values
from pydantic import ValidationError
from pyrogram.client import Client
from src import app
from pyrogram.types import Message

from src.scrape import scrape
from src.models import Post
from src import config
from pyrogram import enums
from pyrogram import filters


async def send_message(item: Post, isPhoto=False):
    await app.send_photo(
        int(config.group_id),
        photo=item.thumbnail,
        caption=(
            f"""
            <u>Title</u>: <b>{item.title}</b> | <b>{item.date}</b>\n
<u>Description</u>: <code>{item.description}</code>\n
<b>Dates</b>
    • <u>Start Date</u>: <b>{item.start_date}</b>
    • <u>End Date</u>: <b>{item.end_date}</b>\n
<u>Links</u>: <a href="https://announcements.bybit.com{item.url}">Source</a>
            """
        ),
        parse_mode=enums.ParseMode.HTML,
    )


async def send_reply(messageOBJ: Message, post: list[Post], multi=False):
    if multi:
        message = f"<b>Latest {len(post)} Posts</b>: \n"
        for article in post:
            message += f"""
Title: <b>{article.title}</b> | <a href="https://announcements.bybit.com{article.url}">Source</a> | <b>{article.date}</b>\n
<b>Dates</b>
    • Start Date: <b>{article.start_date}</b>
    • End Date: <b>{article.end_date}</b>
-----------------------------------------------------------------------------------
"""
        return await messageOBJ.reply_text(
            # photo=post[0].thumbnail,
            text=message,
            parse_mode=enums.ParseMode.HTML,
        )
    return await messageOBJ.reply_photo(
        photo=post[0].thumbnail,
        caption=(
            f"""
            <u>Title</u>: <b>{post[0].title}</b> | <b>{post[0].date}</b>\n
<u>Description</u>: <code>{post[0].description}</code>\n
<b>Dates</b>
    • <u>Start Date</u>: <b>{post[0].start_date}</b>
    • <u>End Date</u>: <b>{post[0].end_date}</b>\n
<u>Links</u>: <a href="https://announcements.bybit.com{post[0].url}">Source</a>
            """
        ),
        parse_mode=enums.ParseMode.HTML,
    )


global_posts = []


async def main():
    global global_posts
    posts = await scrape()
    await app.start()
    if posts and posts != []:
        prev_post = posts[0].title
        await send_message(posts[0])
        global_posts = posts

    while True:
        await asyncio.sleep(300)
        new_posts = await scrape()

        if new_posts and new_posts != [] and prev_post != new_posts[0].title:
            global_posts = new_posts
            await send_message(new_posts[0])


@app.on_message(filters.command(["last"], prefixes="/"))
async def start(_, message: Message):

    if not global_posts and global_posts == []:
        await message.reply_text(text="Server is busy! please try again later")

    chat_member = await app.get_chat_member(
        chat_id=message.chat.id, user_id=message.from_user.id
    )

    if chat_member.status in (
        "ChatMemberStatus.OWNER",
        "ChatMemberStatus.ADMINISTRATOR",
    ):
        args = message.text.split()[1:]
        if args:
            try:
                list_number = int(args[0])
                if list_number > 8:
                    return await message.reply_text(
                        text="Invalid Argument! Please provide valid arg between 1 & 8"
                    )
            except ValueError:
                return await message.reply_text(
                    text="Invalid Argument! Please provide valid arg between 1 & 8"
                )

            await send_reply(
                messageOBJ=message, post=global_posts[:list_number], multi=True
            )
        else:
            await send_reply(messageOBJ=message, post=global_posts[:1])
    else:
        await message.reply_text(text="You are not authorized to use this command.")


if __name__ == "__main__":
    app.run(main())

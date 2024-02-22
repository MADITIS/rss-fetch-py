import asyncio
from typing import Dict
from dotenv import load_dotenv, dotenv_values
from pydantic import ValidationError
from pyrogram.client import Client
from src import app
from pyrogram.types import Message

from src.scrape import posts, scrape
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
-------------------------------------------------------------------------------------------------
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


async def main():
    await scrape()
    await app.start()
    prev_post = posts[0].title

    await send_message(posts[0])

    while True:
        await scrape()
        await asyncio.sleep(5)

        if prev_post != posts[0].title:
            await send_message(posts[0])


@app.on_message(filters.command(["last"], prefixes="/"))
async def start(_, message: Message):
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

        await send_reply(messageOBJ=message, post=posts[:list_number], multi=True)
    else:
        await send_reply(messageOBJ=message, post=posts[:1])


if __name__ == "__main__":
    app.run(main())

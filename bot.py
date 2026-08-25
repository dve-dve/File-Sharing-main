import os
import asyncio

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# =========================================================
# CONFIG
# =========================================================

API_HASH = os.environ.get(
    'API_HASH',
    'a41d007169ca0f05f8cb99cd1b3273ec'
)

APP_ID = int(os.environ.get(
    'APP_ID',
    '34552415'
))

BOT_TOKEN = os.environ.get(
    'BOT_TOKEN',
    '8556089916:AAEzxu5vFSsMs_qjTdltCZY7HqwJ2LN0p40'
)

TRACK_CHANNEL = int(os.environ.get(
    'TRACK_CHANNEL',
   ' -1003814449485'
))

OWNER_ID = os.environ.get(
    'OWNER_ID',
    '8546199829'
)


# =========================================================
# BUTTONS
# =========================================================

START_BUTTONS = [
    [
        InlineKeyboardButton(
            'Source',
            url='https://github.com/X-Gorn/File-Sharing'
        ),
        InlineKeyboardButton(
            'Project Channel',
            url='https://t.me/xTeamBots'
        ),
    ],
    [
        InlineKeyboardButton(
            'Author',
            url='https://t.me/xgorn'
        )
    ],
]


# =========================================================
# BOT CLIENT
# =========================================================

xbot = Client(
    'File-Sharing',
    api_id=APP_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


# =========================================================
# BOT USERNAME
# =========================================================

xbot_username = ""


# =========================================================
# START & GET FILE
# =========================================================

@xbot.on_message(
    filters.command('start') & filters.private
)
async def _startfile(bot, update):

    if update.text == '/start':

        await update.reply_text(
            "I'm File-Sharing!\n"
            "You can share any telegram files and get "
            "the sharing link using this bot!\n\n"
            "/help for more details...",
            True,
            reply_markup=InlineKeyboardMarkup(
                START_BUTTONS
            )
        )

        return

    if len(update.command) != 2:
        return

    code = update.command[1]

    if '-' in code:

        msg_id = code.split('-')[-1]

        unique_id = '-'.join(
            code.split('-')[0:-1]
        )

        if not msg_id.isdigit():
            return

        try:

            check_media_group = await bot.get_media_group(
                TRACK_CHANNEL,
                int(msg_id)
            )

            check = check_media_group[0]

        except Exception:

            check = await bot.get_messages(
                TRACK_CHANNEL,
                int(msg_id)
            )

        if check.empty:

            await update.reply_text(
                'Error: [Message does not exist]\n'
                '/help for more details...'
            )

            return

        unique_idx = None

        if check.video:
            unique_idx = check.video.file_unique_id

        elif check.photo:
            unique_idx = check.photo.file_unique_id

        elif check.audio:
            unique_idx = check.audio.file_unique_id

        elif check.document:
            unique_idx = check.document.file_unique_id

        elif check.sticker:
            unique_idx = check.sticker.file_unique_id

        elif check.animation:
            unique_idx = check.animation.file_unique_id

        elif check.voice:
            unique_idx = check.voice.file_unique_id

        elif check.video_note:
            unique_idx = check.video_note.file_unique_id

        if unique_idx is None:
            return

        if unique_id != unique_idx.lower():
            return

        try:

            await bot.copy_media_group(
                update.from_user.id,
                TRACK_CHANNEL,
                int(msg_id)
            )

        except Exception:

            await check.copy(
                update.from_user.id
            )

    else:
        return


# =========================================================
# HELP
# =========================================================

@xbot.on_message(
    filters.command('help') & filters.private
)
async def _help(bot, update):

    await update.reply_text(
        "Supported file types:\n\n"
        "- Video\n"
        "- Audio\n"
        "- Photo\n"
        "- Document\n"
        "- Sticker\n"
        "- GIF\n"
        "- Voice note\n"
        "- Video note\n\n"
        "If bot didn't respond, contact @xgorn",
        True
    )


# =========================================================
# CREATE SHARING LINK
# =========================================================

async def __reply(update, copied):

    msg_id = copied.message_id

    unique_idx = None

    if copied.video:
        unique_idx = copied.video.file_unique_id

    elif copied.photo:
        unique_idx = copied.photo.file_unique_id

    elif copied.audio:
        unique_idx = copied.audio.file_unique_id

    elif copied.document:
        unique_idx = copied.document.file_unique_id

    elif copied.sticker:
        unique_idx = copied.sticker.file_unique_id

    elif copied.animation:
        unique_idx = copied.animation.file_unique_id

    elif copied.voice:
        unique_idx = copied.voice.file_unique_id

    elif copied.video_note:
        unique_idx = copied.video_note.file_unique_id

    else:

        await copied.delete()

        return

    await update.reply_text(
        'Here is Your Sharing Link:',
        True,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    'Sharing Link',
                    url=(
                        f'https://t.me/{xbot_username}'
                        f'?start={unique_idx.lower()}-{str(msg_id)}'
                    )
                )
            ]
        ])
    )

    await asyncio.sleep(0.5)


# =========================================================
# MEDIA GROUP
# =========================================================

media_group_id = 0


@xbot.on_message(
    filters.media &
    filters.private &
    filters.media_group
)
async def _main_grop(bot, update):

    global media_group_id

    if OWNER_ID == 'all':

        pass

    elif int(OWNER_ID) == update.from_user.id:

        pass

    else:

        return

    if int(media_group_id) != int(
        update.media_group_id
    ):

        media_group_id = update.media_group_id

        copied = (
            await bot.copy_media_group(
                TRACK_CHANNEL,
                update.from_user.id,
                update.message_id
            )
        )[0]

        await __reply(
            update,
            copied
        )

    else:

        return


# =========================================================
# SINGLE FILE
# =========================================================

@xbot.on_message(
    filters.media &
    filters.private &
    ~filters.media_group
)
async def _main(bot, update):

    if OWNER_ID == 'all':

        pass

    elif int(OWNER_ID) == update.from_user.id:

        pass

    else:

        return

    copied = await update.copy(
        TRACK_CHANNEL
    )

    await __reply(
        update,
        copied
    )


# =========================================================
# START BOT
# =========================================================

def main():

    global xbot_username

    print("Starting File-Sharing Bot...")

    with xbot:

        me = xbot.get_me()

        xbot_username = me.username

        print(
            f"Bot username: @{xbot_username}"
        )

        print("Bot started!")

        if OWNER_ID != 'all':

            try:

                xbot.send_message(
                    int(OWNER_ID),
                    "Bot started!"
                )

            except Exception as e:

                print(
                    f"Startup notification error: {e}"
                )

    xbot.run()


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    main()
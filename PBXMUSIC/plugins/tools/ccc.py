import logging
import random
import string
import re
from pyrogram import filters
from PBXMUSIC import app

# Configure logging
logging.basicConfig(level=logging.INFO)

# Random DATA
letters = string.ascii_lowercase
First = "".join(random.choice(letters) for _ in range(6))
Last = "".join(random.choice(letters) for _ in range(6))
PWD = "".join(random.choice(letters) for _ in range(10))
Name = f"{First}+{Last}"
Email = f"{First}.{Last}@gmail.com"


def gen(first_6: int, mm: int = None, yy: int = None, cvv: int = None):
    BIN = 15 - len(str(first_6))
    card_no = [int(i) for i in str(first_6)]
    card_num = [int(i) for i in str(first_6)]
    seventh_15 = random.sample(range(10), BIN)
    for i in seventh_15:
        card_no.append(i)
        card_num.append(i)
    for t in range(0, 15, 2):
        card_no[t] = card_no[t] * 2
    for i in range(len(card_no)):
        if card_no[i] > 9:
            card_no[i] -= 9
    s = sum(card_no)
    mod = s % 10
    check_sum = 0 if mod == 0 else (10 - mod)
    card_num.append(check_sum)
    card_num = [str(i) for i in card_num]
    cc = "".join(card_num)
    if mm is None:
        mm = random.randint(1, 12)
    mm = f"0{mm}" if len(str(mm)) < 2 else mm
    yy = random.randint(2023, 2028) if yy is None else yy
    if cvv is None:
        cvv = random.randint(0, 999)
    cvv = f"{cvv:03}"
    return f"{cc}|{mm}|{yy}|{cvv}"


@app.on_message(filters.command(["gen"]))
async def generate_card(client, message):
    try:
        text = message.text.split()[1:]  # Extract arguments after the command
        if not text:
            await message.reply_text("<b>Format:\n /gen 549184</b>")
            return

        x = re.findall(r"\d+", " ".join(text))
        if len(x) == 0:
            await message.reply_text("<b>Format:\n /gen 549184</b>")
            return

        ccn = int(x[0])
        mm = int(x[1]) if len(x) > 1 else None
        yy = int(x[2]) if len(x) > 2 else None
        cvv = int(x[3]) if len(x) > 3 else None

        # Generate 10 cards
        cards = []
        for _ in range(10):
            card = gen(first_6=ccn, mm=mm, yy=yy, cvv=cvv)
            cards.append(card)

        # Send the generated cards with user information only once at the end
        user_info = f'BY: <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>'
        await message.reply_text(
            "\n".join(f"<code>{card}</code>" for card in cards) + "\n" + user_info
        )
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")

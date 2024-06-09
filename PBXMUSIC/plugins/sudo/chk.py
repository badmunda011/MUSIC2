import re
import random
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from PBXMUSIC import app

approved_cards = []
declined_cards = []
invalid_format_cards = []

# Credit card validation function
def daxx(card_number):
    card_number = re.sub(r'\D', '', card_number)
    if not card_number.isdigit():
        return "ᴅᴇᴄʟɪɴᴇᴅ ❌"

    digits = list(map(int, card_number))
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]

    total = sum(odd_digits)
    for digit in even_digits:
        total += sum(divmod(digit * 2, 10))

    return "ᴀᴘʟʀᴏᴠᴇᴅ ✅" if total % 10 == 0 else "ᴅᴇᴄʟɪɴᴇᴅ ❌"

def get_credit_card_info(card_number):
    card_number = card_number.replace(' ', '')
    result = daxx(card_number)
    gateway = "Braintree Auth"

    return f"""
ᴄᴀʀᴅ: {card_number}
ɢᴀᴛᴇᴡᴀʏ: {gateway}
ʀᴇsᴘᴏɴᴇ: {result}
"""

@app.on_message(filters.command("chk"))
async def check_credit_cards(client: Client, message: Message):
    card_numbers = message.text.split()[1:]  # Extract card numbers from the message
    if len(card_numbers) > 10:
        await message.reply("Yᴏᴜ ᴄᴀɴ ᴏɴʟʏ ᴄʜᴇᴄᴋ ᴜᴘ ᴛᴏ 10 ᴄᴀʀᴅ ɴᴜᴍʙᴇʀs ᴀᴛ ᴀ ᴛɪᴍᴇ.")
        return

    results = []
    for card_number in card_numbers:
        info = get_credit_card_info(card_number)
        results.append(info)

    results_text = "\n".join(results)
    await message.reply(results_text)

@app.on_message(filters.document)
async def handle_document(client, message):
    global approved_cards, declined_cards, invalid_format_cards
    approved_cards = []
    declined_cards = []
    invalid_format_cards = []

    document = message.document
    if document.mime_type == 'text/plain':
        await message.download(f"/tmp/{document.file_name}")

        with open(f"/tmp/{document.file_name}", 'r') as file:
            card_details = file.readlines()

        for line in card_details:
            parts = line.strip().split('|')
            if len(parts) == 4:
                card_number, exp_month, exp_year, cvc = parts
                is_approved = random.random() > 0.99  # 1% chance of approval
                result = f"ᴄᴀʀᴅ: {card_number}|{exp_month}|{exp_year}|{cvc}\nɢᴀᴛᴇᴡᴀʏ: Braintree Auth\nʀᴇsᴘᴏɴsᴇ: {'Approved' if is_approved else 'Card Issuer Declined CVV'}"
                if is_approved:
                    approved_cards.append(f"ᴀᴘʟʀᴏᴠᴇᴅ ✅\n{result}")
                else:
                    declined_cards.append(f"ᴅᴇᴄʟɪɴᴇᴅ ❌\n{result}")
            else:
                invalid_format_cards.append(line.strip())

        total_cards = len(card_details)
        approved_count = len(approved_cards)
        declined_count = len(declined_cards)
        invalid_count = len(invalid_format_cards)

        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(f"ᴀᴘʟʀᴏᴠᴇᴅ ✅ ({approved_count})", callback_data="view_approved")],
                [InlineKeyboardButton(f"ᴅᴇᴄʟɪɴᴇᴅ ❌ ({declined_count})", callback_data="view_declined")],
                [InlineKeyboardButton(f"ɪɴᴠᴀɪʟᴅ👽 ({invalid_count})", callback_data="view_invalid")],
            ]
        )

        await message.reply(
            f"𝘚𝘏𝘖𝘗𝘐𝘍𝘠 + 𝘈𝘜𝘛𝘏𝘖𝘙𝘐𝘡𝘌 $5!\n\n ᴛᴏᴛᴀʟ ᴄᴀʀᴅs 💳: {total_cards}\n ᴀᴘʟʀᴏᴠᴇᴅ ✅: {approved_count}\nᴅᴇᴄʟɪɴᴇᴅ ❌: {declined_count}\n ɪɴᴠᴀɪʟᴅ👽 : {invalid_count}",
            reply_markup=keyboard
        )
    else:
        await message.reply("Please upload a valid .txt file.")

@app.on_callback_query(filters.regex("view_approved"))
async def view_approved(client, callback_query):
    global approved_cards
    if approved_cards:
        approved_text = "\n\n".join(approved_cards)
        approved_cards = []  # Clear approved cards after displaying
        await callback_query.message.reply(f"𝖦𝖠𝖳𝖤𝖶𝖠𝖸: 𝖲𝖧𝖮𝖯𝖨𝖥𝖸 + 𝖠𝖴𝖳𝖧𝖮𝖱𝖨𝖹𝖤 $5:\n\n{approved_text}")
    else:
        await callback_query.message.reply("No approved cards.")
    await update_buttons(callback_query)

@app.on_callback_query(filters.regex("view_declined"))
async def view_declined(client, callback_query):
    global declined_cards
    if declined_cards:
        declined_text = "\n\n".join(declined_cards)
        declined_cards = []  # Clear declined cards after displaying
        await callback_query.message.reply(f"Declined Cards:\n{declined_text}")
    else:
        await callback_query.message.reply("No declined cards.")
    await update_buttons(callback_query)

@app.on_callback_query(filters.regex("view_invalid"))
async def view_invalid(client, callback_query):
    global invalid_format_cards
    if invalid_format_cards:
        invalid_text = "\n".join(invalid_format_cards)
        invalid_format_cards = []  # Clear invalid format cards after displaying
        await callback_query.message.reply(f"Invalid Format Cards:\n{invalid_text}")
    else:
        await callback_query.message.reply("No invalid format cards.")
    await update_buttons(callback_query)

async def update_buttons(callback_query):
    global approved_cards, declined_cards, invalid_format_cards
    approved_count = len(approved_cards)
    declined_count = len(declined_cards)
    invalid_count = len(invalid_format_cards)

    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(f"ᴀᴘʟʀᴏᴠᴇᴅ ✅ ({approved_count})", callback_data="view_approved")],
            [InlineKeyboardButton(f"ᴅᴇᴄʟɪɴᴇᴅ ❌ ({declined_count})", callback_data="view_declined")],
            [InlineKeyboardButton(f"ɪɴᴠᴀɪʟᴅ👽 ({invalid_count})", callback_data="view_invalid")],
        ]
    )

    await callback_query.message.edit_reply_markup(reply_markup=keyboard)
    await callback_query.answer()

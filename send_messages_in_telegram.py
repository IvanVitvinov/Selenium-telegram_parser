import time
import random
from pyrogram import Client
from pyrogram import enums
import asyncio


async def main():

    message = "your_message"

    # Authenticate and initialize the Pyrogram client
    async with Client("my_account1", api_id='your_id', api_hash='your_hash') as app:
        # Send message to contact list
        contacts = await app.get_contacts()
        subscribers = [contact.username for contact in contacts if contact.username is not None]

        # Send message loop with big pause every 10 messages
        i = 1
        for username in subscribers:
            # Pause condition
            if i % 10 == 0:
                time.sleep(random.randint(700, 900))
                i = 0
            i += 1

            time.sleep(random.randint(60, 90))

            # Sending a message
            await app.send_photo(
                chat_id=f"{username}",
                photo="photo/123.png",
                caption=message,
                parse_mode=enums.ParseMode.MARKDOWN
            )
            print(f"User {username}, received a message!")


asyncio.run(main())

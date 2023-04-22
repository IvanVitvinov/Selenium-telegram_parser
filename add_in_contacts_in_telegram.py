import time
import random
from pyrogram import Client
import asyncio


async def main():
    # List of subscriber nicknames
    with open("Results_ready_for_use/results1000.txt", "r") as file:
        lines = file.readlines()

    subscribers = [line.strip() for line in lines]

    # Authenticate and initialize the Pyrogram client
    async with Client("my_account1", api_id='your_id', api_hash='your_hash') as app:
        # Cycle of adding usernames to contacts
        for username in subscribers:
            time.sleep(random.randint(7, 15))
            try:
                user = await app.get_users(username)
                first_name = user.first_name if user.first_name is not None else ""
                last_name = user.last_name if user.last_name is not None else ""
                await app.add_contact(user.id, first_name=first_name, last_name=last_name)
                print(f"User {username} added to contacts successfully!")

            except Exception as e:
                print(f"Error adding user {username}: {e}")


asyncio.run(main())

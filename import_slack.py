from src.config import slack_client, db
from src.fastapi import get_slack_users


thread = db.threads


async def import_messages():
    users = await get_slack_users()
    user_ids = [x["id"] for x in users["members"]]
    messages = await slack_client.conversations_history(channel="C05PGS91WNS")

    for message in messages.data["messages"]:
        event = message
        if event.get("subtype") == "channel_join":
            continue

        user_id = event["user"]
        user_name = next(x["name"] for x in users["members"] if x["id"] == user_id)
        text = event["text"]

        # Change user ids in text to names
        for _id in user_ids:
            if _id in text:
                name = next(x["name"] for x in users["members"] if x["id"] == _id)
                text = text.replace(f"<@{_id}>", f"{name}")

        if event.get("thread_ts") is None or event["thread_ts"] == event["ts"]:
            await thread.insert_one(
                {
                    "slack_thread_id": event["ts"],
                    "user_ids": [user_id],
                    "channel": "C05PGS91WNS",
                    "messages": [
                        {
                            "text": text,
                            "user_id": user_id,
                            "name": user_name,
                        }
                    ],
                }
            )
        else:
            rec = await thread.find_one({"slack_thread_id": event["thread_ts"]})
            filter_push = {
                "messages": {
                    "text": text,
                    "user_id": user_id,
                    "name": user_name,
                },
            }
            update = {"$push": filter_push}
            if user_id not in rec["user_ids"]:
                filter_push["user_ids"] = user_id
            await thread.update_one(
                {"slack_thread_id": event["thread_ts"]},
                update,
            )


if __name__ == "__main__":
    import asyncio

    asyncio.run(import_messages())

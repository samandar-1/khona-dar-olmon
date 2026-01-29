async def telegram_message_exists(bot, chat_id, message_id):
    try:
        await bot.copy_message(
            chat_id=chat_id,
            from_chat_id=chat_id,
            message_id=message_id
        )
        return True
    except Exception:
        return False

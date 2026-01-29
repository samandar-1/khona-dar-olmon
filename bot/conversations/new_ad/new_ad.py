# from enum import Enum, auto
#
# from sqlalchemy import select
# from sqlalchemy import select
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.exc import IntegrityError
# from db.models import User  # your User model
# from telegram import Update
# from telegram.ext import ContextTypes
# from .states import NewAdState
#
# # class NewAdState(Enum):
# #     TITLE = auto()
# #     TYPE = auto()       # kommt in Schritt 2
# #     PRICE = auto()      # später
# #     CONFIRM = auto()    # später
#
#
#
# async def new_ad_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     context.user_data.clear()  # sauberen Start erzwingen
#
#     await update.message.reply_text(
#         "📝 Neue Anzeige erstellen\n\n"
#         "Bitte gib den *Titel* deiner Anzeige ein:",
#         parse_mode="Markdown"
#     )
#
#     return NewAdState.TITLE
#
# async def new_ad_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     title = update.message.text.strip()
#
#     if len(title) < 5:
#         await update.message.reply_text(
#             "❌ Der Titel ist zu kurz.\n"
#             "Bitte gib mindestens 5 Zeichen ein:"
#         )
#         return NewAdState.TITLE
#
#     context.user_data["title"] = title
#
#     await update.message.reply_text(
#         f"✅ Titel gespeichert:\n*{title}*\n\n"
#         "➡️ Nächster Schritt kommt gleich.",
#         parse_mode="Markdown"
#     )
#
#     return NewAdState.TYPE  # noch leer, kommt als nächstes
#
#
#
#
# async def save_or_update_user(session: AsyncSession, telegram_user):
#     """
#     Save a new user or update existing user data.
#
#     Parameters:
#         session (AsyncSession): async db session
#         telegram_user (telegram.User): object from update.effective_user
#
#     Returns:
#         User: the User instance
#     """
#     # Try to find existing user
#     stmt = select(User).where(User.telegram_id == telegram_user.id)
#     result = await session.execute(stmt)
#     user = result.scalars().first()
#
#     if user:
#         # Update fields if user exists
#         user.username = telegram_user.username
#         user.first_name = telegram_user.first_name
#         user.last_name = telegram_user.last_name
#     else:
#         # Create new user
#         user = User(
#             telegram_id=telegram_user.id,
#             username=telegram_user.username,
#             first_name=telegram_user.first_name,
#             last_name=telegram_user.last_name
#         )
#         session.add(user)
#
#     try:
#         await session.commit()
#     except IntegrityError:
#         await session.rollback()
#         # rare race condition, fetch again
#         stmt = select(User).where(User.telegram_id == telegram_user.id)
#         result = await session.execute(stmt)
#         user = result.scalars().first()
#
#     return user

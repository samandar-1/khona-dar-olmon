# 🏠 Community Housing Bots for Germany

This project contains **two Telegram bots** for housing advertisements in Germany, created specifically for Central Asian communities:

* 🇺🇿 Uzbek community:
     * Bot: https://t.me/uybor_de_bot
     * Channel: https://t.me/uybor_de
* 🇹🇯 Tajik community: 
     * Bot: https://t.me/khona_dar_olmon_bot
     * Channel: https://t.me/khona_dar_olmon

Each bot has its own Telegram channel where approved apartment and room advertisements are published.

The platform allows users to:

* Search for apartments or rooms
* Publish housing advertisements
* Manage their own advertisements directly in the bot
* Contact landlords directly through Telegram

All submitted advertisements are reviewed by admins before being published.

---

# ✨ Features

* Two separate Telegram bots:

  * Uzbek housing bot
  * Tajik housing bot
* Separate public channels for each community
* Apartment and room advertisement publishing
* User advertisement management
* Admin moderation system
* Approval/rejection workflow
* Photo support
* Structured listing format
* Easy-to-use Telegram interface

---

# 🛠️ How It Works

## 1. User submits an advertisement

Users send:

* City
* Rent price
* Apartment/room details
* Photos
* Contact information

through the Telegram bot.

---

## 2. Advertisement goes to moderation

The bot forwards the listing to the admin moderation channel.

---

## 3. Admin reviews the advertisement

Admins can:

* ✅ Approve
* ❌ Reject

---

## 4. Approved advertisement is published

After approval, the bot automatically publishes the advertisement to the corresponding community channel.

* Uzbek ads → Uzbek channel
* Tajik ads → Tajik channel

---

# 👤 User Advertisement Management

Users can manage their own advertisements directly inside the bot.

Available actions:

* View active advertisements
* Delete advertisements
* Check advertisement status

---

# ⚙️ Technologies

* Telegram Bot API
* Python 
* SQLite
* Telegram Channels

---

# 👥 Target Audience

* Uzbek community in Germany
* Tajik community in Germany
* Students
* Workers
* Newcomers looking for housing

---

# 🔐 Admin Features

* Review pending advertisements
* Approve or reject posts
* Prevent spam and fake listings
* Manage housing channels

---

# 🚀 Future Improvements

* Search filters
* Automatic deletion of outdated ads
* User reputation system
* Web dashboard for admins
* Notification subscription feature

---

# 📄 License

MIT License


## Installation
1. Clone Repo
```bash
git clone https://github.com/samandar-1/khona-dar-olmon.git
cd khona-dar-olmon
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Sie können mit hilfe von diesem bot Ihre Anzeigen im Hauptkanal posten.

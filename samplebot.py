import os
import sys
import asyncio
from typing import Final
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from video_generator.video_maker import create_travel_video

TOKEN: Final = '8142158412:AAEVhy1H_X2ZxT2wEqun_OxqD7SKWqnFqPo'
BOT_USERNAME: Final = 'wanderwbot'

# Directories
IMAGE_DIR = "media/images"
VIDEO_DIR = "media/videos"
MUSIC_DIR = "media/music"
os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)
os.makedirs(MUSIC_DIR, exist_ok=True)

# User Data Storage
user_images = {}
user_effects = {}  # Store user-selected effects
user_music = {}  # Store user-selected music

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! I am WanderWBot, your personal travel assistant. How can I help you today?')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('I am here to help you with your travel needs. Just type /start to begin.')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom command.')

async def set_effect(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sets a custom transition effect for the user."""
    user_id = update.message.from_user.id
    effects = ["fade", "slide", "zoom"]
    
    if not context.args:
        await update.message.reply_text(f"Available Effects: {', '.join(effects)}\nUsage: /set_effect <effect>")
        return
    
    effect = context.args[0].lower()
    
    if effect not in effects:
        await update.message.reply_text(f"Invalid effect! Choose from: {', '.join(effects)}")
        return

    user_effects[user_id] = effect
    await update.message.reply_text(f"✅ Effect set to: {effect}")

async def set_music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sets a custom music track for the user."""
    user_id = update.message.from_user.id
    music_choices = ["adventure", "chill", "cinematic"]
    
    if not context.args:
        await update.message.reply_text(f"Available Music: {', '.join(music_choices)}\nUsage: /set_music <music>")
        return
    
    music = context.args[0].lower()
    
    if music not in music_choices:
        await update.message.reply_text(f"Invalid music choice! Choose from: {', '.join(music_choices)}")
        return

    user_music[user_id] = music
    await update.message.reply_text(f"✅ Music set to: {music}")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles image uploads."""
    user_id = update.message.from_user.id
    photo = update.message.photo[-1]  # Get the highest resolution image
    file = await context.bot.get_file(photo.file_id)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(IMAGE_DIR, f"{user_id}_{timestamp}.jpg")

    await file.download_to_drive(file_path)

    if user_id not in user_images:
        user_images[user_id] = []
    user_images[user_id].append(file_path)

    await update.message.reply_text("📸 Image received! Upload more or type /generate_video to create your travel video.")

async def generate_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generates a travel video based on user-uploaded images."""
    user_id = update.message.from_user.id
    if user_id not in user_images or not user_images[user_id]:
        await update.message.reply_text("⚠️ You haven't uploaded any images! Please send some first.")
        return

    sorted_images = sorted(user_images[user_id])
    selected_effect = user_effects.get(user_id, "fade")  # Default to "fade"
    selected_music = user_music.get(user_id, "adventure")  # Default to "adventure"

    video_path = os.path.join(VIDEO_DIR, f"travel_{user_id}.mp4")

    try:
        # Generate the video
        await update.message.reply_text("🎥 Generating your travel video. Please wait...")
        final_video_path = create_travel_video(sorted_images, video_path, effect=selected_effect, music=selected_music)

        with open(final_video_path, "rb") as video:
            await context.bot.send_video(
                chat_id=update.message.chat_id,
                video=video,
                caption="🎬 Here is your travel video!"
            )

        # Clear user data after sending the video
        user_images[user_id] = []
        await update.message.reply_text("✅ Your travel video has been created and sent!")
    except Exception as e:
        await update.message.reply_text(f"❌ An error occurred while generating the video: {e}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /help command."""
    await update.message.reply_text(
        "📌 Commands:\n"
        "/start - Start the bot\n"
        "/set_effect <effect> - Set transition effect (fade, slide, zoom)\n"
        "/set_music <music> - Set background music (adventure, chill, cinematic)\n"
        "/generate_video - Create a travel video from your uploaded images"
    )

# Responses to messages
def handle_response(text: str) -> str:
    processed: str = text.lower()
    
    if 'hello' in processed:
        return 'Hey There!'
    if 'how are you' in processed:
        return 'Great'
    
    if 'karo kuch' in processed:
        return 'hum karte hai kuch'
    
    return 'Clear bol Clear!'

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    
    print(f'User: {update.message.chat.id} Message Type: {message_type}')
    
    if message_type == 'PRIVATE':  # Changed from 'private' to 'PRIVATE'
        response: str = handle_response(text)
        await update.message.reply_text(response)
    elif message_type == 'GROUP':  # Changed from 'group' to 'GROUP' and changed if to elif
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '')
            response: str = handle_response(new_text)
            await update.message.reply_text(response)  # Added this line
    else: 
        response: str = handle_response(text)
        await update.message.reply_text(response)
    
    print(f'Bot: {response}')
    
async def error_handler(update, context):  # Removed type hints to make it more flexible
    print(f'Update {update} Error: {context.error}')
    
if __name__ == '__main__':
    print("Bot is starting")
    app = Application.builder().token(TOKEN).build()
    
    # commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    # app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("generate_video", generate_video))
    app.add_handler(CommandHandler("set_effect", set_effect))
    app.add_handler(CommandHandler("set_music", set_music))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    # Use TEXT filter instead of Text
    app.add_handler(MessageHandler(filters.TEXT, message_handler))
    
    app.add_error_handler(error_handler)
    print("Bot is running")
    app.run_polling(poll_interval=3)

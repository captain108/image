from pyrogram import Client, filters
import requests
from config import API_ID, API_HASH, BOT_TOKEN  # ✅ Import from config

app = Client("ai_image_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

STYLES = {
    "photorealistic": "ultra realistic, 8k resolution, photorealistic",
    "anime": "anime style, manga illustration, colorful",
    "digital": "digital painting, concept art",
    "painting": "oil painting, canvas texture",
    "cinematic": "cinematic lighting, epic scene",
    "abstract": "abstract art, creative shapes"
}

def get_image_url(prompt, style, seed):
    enhancement = STYLES.get(style, STYLES["photorealistic"])
    full_prompt = f"{prompt}, {enhancement}"
    encoded = requests.utils.quote(full_prompt)
    return f"https://image.pollinations.ai/prompt/{encoded}?seed={seed}&width=1024&height=1024&nologo=true"

user_styles = {}

@app.on_message(filters.command("start"))
async def start(_, msg):
    await msg.reply(
        "**👋 Welcome to AI Image Generator Bot!**\n\n"
        "Send a prompt to generate an image.\nUse /style to change style."
    )

@app.on_message(filters.command("style"))
async def style(_, msg):
    await msg.reply(
        "**🎨 Choose a style:**\n"
        "`photorealistic`, `anime`, `digital`, `painting`, `cinematic`, `abstract`\n"
        "Send your preferred style."
    )

@app.on_message(filters.text)
async def generate(_, msg):
    user_id = msg.from_user.id
    text = msg.text.lower()

    if text in STYLES:
        user_styles[user_id] = text
        await msg.reply(f"✅ Style set to `{text}`.", parse_mode="markdown")
        return

    prompt = msg.text
    style = user_styles.get(user_id, "photorealistic")
    seed = msg.id

    await msg.reply("🎨 Generating image...")
    try:
        image_url = get_image_url(prompt, style, seed)
        await msg.reply_photo(image_url, caption=f"🖼 Prompt: `{prompt}`\n🎨 Style: `{style}`", parse_mode="markdown")
    except Exception as e:
        await msg.reply("❌ Failed to generate image.")

app.run()

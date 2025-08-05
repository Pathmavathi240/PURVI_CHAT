import re

if len(message.command) < 2:
    buttons = botplaylist_markup(_)
    return await mystic.edit_text(
        _["play_18"],
        reply_markup=InlineKeyboardMarkup(buttons),
    )

slider = True
query = message.text.split(None, 1)[1]
url = None  # ✅ INITIALIZE FIRST

# If it's not a URL, convert search text to YouTube URL
if not re.search(r"(https?://)", query):
    try:
        url = await text_to_youtube_url(query)
    except Exception as e:
        print(f"Search Error: {e}")
        return await message.reply_text("😣 தேடலில் பிழை ஏற்பட்டது. பிறகு முயற்சிக்கவும்.")
    if not url:
        return await message.reply_text("❌ பாடல் கிடைக்கவில்லை. வேறு பெயர் முயற்சிக்கவும்.")
else:
    url = query  # ✅ Directly assign URL

# Now url is guaranteed to be a YouTube URL (either from text search or directly)
if await YouTube.exists(url):
    if "playlist" in url:
        try:
            details = await YouTube.playlist(
                url,
                config.PLAYLIST_FETCH_LIMIT,
                message.from_user.id,
            )
        except:
            return await mystic.edit_text(_["play_3"])
        streamtype = "playlist"
        plist_type = "yt"
        if "&" in url:
            plist_id = (url.split("=")[1]).split("&")[0]
        else:
            plist_id = url.split("=")[1]
        img = config.PLAYLIST_IMG_URL
        cap = _["play_9"]

    elif "https://youtu.be" in url:
        videoid = url.split("/")[-1].split("?")[0]
        details, track_id = await YouTube.track(
            f"https://www.youtube.com/watch?v={videoid}"
        )
        streamtype = "youtube"
        img = details["thumb"]
        cap = _["play_10"].format(
            details["title"],
            details["duration_min"],
        )

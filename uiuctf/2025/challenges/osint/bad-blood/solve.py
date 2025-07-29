from atproto import Client, models
from atproto.exceptions import AtProtocolError
import re

# 🔐 Credentials
USERNAME = "me@landon.pw"
APP_PASSWORD = "5*bBSw^k%4LAu^p$"

# 📌 Target post
POST_URI = "at://mrbluesky1989.bsky.social/app.bsky.feed.post/3lspmsdtlvs2k"

# 🌐 Initialize client
client = Client()
client.login(USERNAME, APP_PASSWORD)

# ✅ Storage
found_flags = []

def check_user_for_flag(handle: str):
    try:
        profile = client.app.bsky.actor.get_profile({'actor': handle})
        # Access profile attributes properly
        description = getattr(profile, 'description', '') or ''
        display_name = getattr(profile, 'display_name', '') or ''
        
        bio_fields = [description, display_name, handle]
        for field in bio_fields:
            if "uiuctf" in field.lower():
                print(f"[🎯 FLAG] Found in profile of @{handle} → {field}")
                found_flags.append((handle, field))
        
        # Check their last 10 posts
        posts = client.app.bsky.feed.get_author_feed({'actor': handle, 'limit': 10})
        for post in posts.feed:
            text = getattr(post.post.record, 'text', '') or ''
            if "uiuctf" in text.lower():
                print(f"[🎯 FLAG] Found in post by @{handle} → {text}")
                found_flags.append((handle, text))
    except AtProtocolError as e:
        print(f"[⚠️] Failed to fetch or parse @{handle}: {e}")
    except Exception as e:
        print(f"[⚠️] Error checking @{handle}: {e}")

# 🧵 Step 1: Get Post Thread
post_thread = client.app.bsky.feed.get_post_thread({'uri': POST_URI})

def extract_commenters(thread_node):
    if not thread_node:
        return
    
    # Access post attribute directly, not with .get()
    if hasattr(thread_node, 'post') and thread_node.post:
        post = thread_node.post
        if hasattr(post, 'author') and post.author:
            handle = post.author.handle
            check_user_for_flag(handle)
    
    # Recurse into replies
    if hasattr(thread_node, 'replies') and thread_node.replies:
        for reply in thread_node.replies:
            extract_commenters(reply)

extract_commenters(post_thread.thread)

# 🧡 Step 2: Get Likes
try:
    likes = client.app.bsky.feed.get_likes({'uri': POST_URI})
    for like in likes.likes:
        handle = like.actor.handle
        check_user_for_flag(handle)
except Exception as e:
    print(f"[⚠️] Error getting likes: {e}")

# 🔁 Step 3: Get Reposts
try:
    reposts = client.app.bsky.feed.get_reposted_by({'uri': POST_URI})
    for repost in reposts.reposted_by:
        handle = repost.handle
        check_user_for_flag(handle)
except Exception as e:
    print(f"[⚠️] Error getting reposts: {e}")

# 💬 Step 4: Search for Quotes
try:
    quote_search = client.app.bsky.feed.search_posts({'q': POST_URI})
    for post in quote_search.posts:
        handle = post.author.handle
        text = getattr(post.record, 'text', '') or ''
        if POST_URI in text:
            check_user_for_flag(handle)
except Exception as e:
    print(f"[⚠️] Error searching for quotes: {e}")

# ✅ Done
print(f"\n🎉 Total Flags Found: {len(found_flags)}")
for handle, flag_text in found_flags:
    print(f"- @{handle}: {flag_text}")

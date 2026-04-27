---
project: Media Dashboard
description: technical instructions for using YouTube's API for extracting channel IDs using various methods
subproject:
  - YouTube Channel ID Fetcher
---
# Extracting YouTube Channel IDs via the YouTube API

You can extract a YouTube channel ID using the YouTube Data API v3 through several different methods depending on the information you already have.

## 1. Extract by Channel Handle (e.g., @Google)

The most common modern method is using the `forHandle` parameter with the `channels.list` endpoint.

**Endpoint:** `https://www.googleapis.com/youtube/v3/channels`

**Parameters:**
- `part=id`
- `forHandle=@handleName`
- `key=YOUR_API_KEY`

**Note:** This works for newer YouTube handles and most custom URLs.

---

## 2. Extract from a Video ID

If you have a video from that channel, you can retrieve the channel ID from the video's metadata.

**Endpoint:** `https://www.googleapis.com/youtube/v3/videos`

**Parameters:**
- `part=snippet`
- `id=VIDEO_ID`
- `key=YOUR_API_KEY`

**Result:** The channel ID is found in the `snippet.channelId` field.

---

## 3. Extract by Search (Channel Name/Title)

If you only have a channel's display name, you can use the search endpoint to find matching channels.

**Endpoint:** `https://www.googleapis.com/youtube/v3/search`

**Parameters:**
- `part=snippet`
- `type=channel`
- `q=CHANNEL_NAME`
- `key=YOUR_API_KEY`

**Note:** This may return multiple results; the ID is located at `items[i].id.channelId`.

---

## 4. Extract for Your Own Channel

To find the ID of the channel you are currently authenticated as, use the `mine` parameter.

**Endpoint:** `https://www.googleapis.com/youtube/v3/channels`

**Parameters:**
- `part=id`
- `mine=true`

**Requirement:** Requires OAuth 2.0 authorization.

---

## 5. Extract by Legacy Username

For very old channels that still have a legacy username (not a handle), you can use the `forUsername` parameter.

**Endpoint:** `https://www.googleapis.com/youtube/v3/channels`

**Parameters:**
- `part=id`
- `forUsername=USERNAME`
- `key=YOUR_API_KEY`

---

## Pro Tip

If you just need a single ID quickly and don't want to write code, many channels have their ID directly in the source code of their page. You can find it by searching for `externalId` or `channelId` in the browser's View Page Source (`Ctrl+U`).

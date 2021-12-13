# mpd-streamer-bot

I play MPD HTTP Streams on a Discord voice channel.

*It's your music; play it.*

## Installation

Currently, requires a `.env` file with the following variables:

* `DISCORD_TOKEN`: A unique token for connecting to Discord
* `MPD_HOST`: The URL or IP address to the MPD server
* `MPD_PORT`: The port number for the MPD connection
* `MPD_STREAM_PORT`: The port number for the MPD HTTP stream
* `MPD_PASSWORD`: (Optional) The password for the MPD instance, if applicable

## Usage

These are the current commands that can be sent to the bot in a Discord chat.
Either prefix the command with a `$`, or **mention** the bot.

* `join`: Connects to a voice channel. Currently requires specifying the channel ID
* `stop`: Disconnects from the voice channel
* `currentsong`: Gets the current song name and other data
* `next`: Skips to the next song in the playlist
* `previous` Goes back to the previous song in the playlist

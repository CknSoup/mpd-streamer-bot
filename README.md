# mpd-streamer-bot

I play MPD HTTP Streams on a Discord voice channel.

*It's your music; play it.*

### Usage

Currently, requires a `.env` file with the following variables:

* `DISCORD_TOKEN`: A unique token for connecting to Discord
* `MPD_HOST`: The URL or IP address to the MPD server
* `MPD_PORT`: The port number for the MPD connection
* `MPD_STREAM_PORT`: The port number for the MPD HTTP stream
* `MPD_PASSWORD`: (Optional) The password for the MPD instance, if applicable

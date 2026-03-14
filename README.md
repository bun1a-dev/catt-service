# Cast All The Things! Service

Cast All The Things! for Home Assistant

---

> [!NOTE]
> This is a fork of the original [miumida/catt](https://github.com/miumida/catt) project. Thank you **[@miumida](https://github.com/miumida)** for the original work! ❤️

---

## Installation
This can be installed through HACS:

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=bun1a-dev&repository=catt-service&category=integration)

or manually.

## Services
#### scan
  Scan the local network and show all Chromecasts and their IP's.
#### help
  Shows CATT help.
#### command
 | commands | Desc.        |
 | ------------- | --------- |
 | cast         | Send a video to a Chromecast for playing. |
 | cast_site    | Cast any website to a Chromecast.         |
 | play         | Resume a video after it has been paused.  |
 | play_toggle  | Toggle between playing and paused state.  |
 | pause        | Pause a video.                            |
 | clear        | Clear the queue (YouTube only).           |
 | add          | Add a video to the queue (YouTube only).  |
 | remove       | Remove a video from the queue (YouTube only). |
 | seek         | Seek the video to TIME position. |
 | ffwd         | Fastforward a video by TIME duration. |
 | rewind       | Rewind a video by TIME duration. |
 | volume       | Set the volume to LVL [0-100]. |
 | volumedown   | Turn down volume by a DELTA increment. |
 | volumemute   | Enable or disable mute on supported devices.|
 | volumeup     | Turn up volume by a DELTA increment. |
#### stop
  Stops playing on device.
  
## Thanks:
- [skorokithakis/catt](https://github.com/skorokithakis/catt) - Library
- [miumida/catt](https://github.com/miumida/catt) - Original Project

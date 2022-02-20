# JQBX Bot

A chatbot for [JQBX](https://jqbx.fm/) rooms.

## Requirements

* [Python 3.8.6](https://www.python.org/downloads/release/python-386/)
* [pipenv](https://pypi.org/project/pipenv/)
<!-- * A Spotify premium account that is already connected to JQBX -->
<!-- * An AWS account to deploy to -->

## Running Locally

See the `Makefile` for available `make` actions

## Configuration file

data/config.json
| Key | Type | Description |
| --- | --- | --- |
| log_level | int | set 20 by default |
| username | str | Bot username |
| room_id | str | Room id to connect |
| thumbsUpImage | str | optional |
| thumbsDownImage | str | optional |
| djImage | str | optional |
| welcome_message | str | optional |
| welcome_enabled | bool | optional |
| welcome_whisper | str | optional |
| auto-first_enabled | bool | optional |
| spotify_refresh_token | str | optional |
| spotify_client_id | str | optional |
| spotify_client_secret | str | optional |
| spotify_playlist_playback | str | optional |

### Example

```json
{
    "log_level": 20,
    "username": "username",
    "room_id": "XXXX"
}
```

<!-- ## Github Actions

This repository is currently setup to run tests and deploy on each push to `master`

In order for the AWS deployment to succeed, the repository should be configured with the following secrets: -->

## TODO

* [ ] link to last.fm for stats
* [ ] tune of the month (statistics)

* [ ] /best (Rooms analyse? API?)

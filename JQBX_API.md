# JQBX API

## Users
### User
> `GET https://jqbx.fm/user/spotify:user:{USER_ID}`

Response
```JSON
{
  "_id": "YYYYYYYYYYYYYYYYYYYYYY",
  "uri": "spotify:user:XXXXXXXXXXXXXXXXXXXXXXXX",
  "country": "US",
  "display_name": "",
  "device": "desktop | mobile | bot",
  "external_urls": {
    "spotify": "https://open.spotify.com/user/XXXXXXXXXXXXXXXXXXXXXXXX"
  },
  "href": "https://api.spotify.com/v1/users/XXXXXXXXXXXXXXXXXXXXXXXX",
  "id": "XXXXXXXXXXXXXXXXXXXXXXXX",
  "firstTime": false,
  "status": "inactive | active",
  "username": "",
  "image": "",
  "djImage": "",
  "thumbsUpImage": "",
  "thumbsUp": 2093,
  "stars": 955,
  "acceptsMarketing": false,
  "website": "",
  "instagram": "",
  "lastfm": "",
  "following": [
    "spotify:user:",
    "spotify:user:"
  ],
  "followers": [
    "spotify:user:",
    "spotify:user:"
  ],
  "userWhitelist": [
    "HHHHHHHHHHHHHHHHHHHHHHHH",
    "HHHHHHHHHHHHHHHHHHHHHHHH"
  ],
  "lastDjNotification": 1622314575946,
  "canNotify": true,
  "canBroadcast": true,
  "keepAfterPlay": true,
  "openLinksWithSpotify": true,
  "twitter": "",
  "showPushNotifications": false,
  "alwaysInactive": true,
  "distractionFreeMode": false,
  "thumbsDownImage": "",
  "hideStatsUri": true,
  "hideSpotifyUri": false,
  "hideUserImages": false,
  "showNotificationIcon": true,
  "disableConfetti": true
}
```

## Rooms
### All Rooms
> `GET https://jqbx.fm/all-rooms/{PAGE}`

Response
```JSON
{
  "rooms": [
    {
      "_id": "",
      "users": [
        {
          "id": "",
          "_id": "",
          "uri": "spotify:user:",
          "device": "desktop",
          "status": "inactive",
          "country": "MY",
          "socketId": "",
          "statusChangedAt": 1622384041312
        }
      ],
      "djs": [
        {
          "username": "",
          "id": "",
          "_id": "",
          "uri": "spotify:user:",
          "image": "https://jqbx.s3.amazonaws.com/",
          "device": "desktop",
          "status": "active",
          "country": "MY",
          "socketId": "",
          "statusChangedAt": 1622390591028,
          "playCount": 0,
          "votes": []
        }
      ],
      "banned": [],
      "title": "",
      "visibility": "private",
      "genre": null,
      "flexibility": null,
      "maxDjs": null,
      "maxTurns": null,
      "modDjsOnly": false,
      "highlightMods": false,
      "messageTracks": false,
      "hideModFlair": false,
      "admin": [
        "spotify:user:",
        "spotify:user:",
        "spotify:user:"
      ],
      "mods": [],
      "usersCount": 41,
      "djsCount": 1,
      "lastTouched": "2021-05-30T21:03:10.489Z",
      "sentWarningEmail": false,
      "savedCount": 108,
      "infoLink": "",
      "promoImageUrl": "",
      "promoImageHref": "",
      "welcomeMessage": "",
      "modsCanBan": null,
      "tracks": [
        {
          "_id": "",
          "id": "",
          "album": {
            "images": [
              {
                "height": 640,
                "url": "https://i.scdn.co/image/ab67616d0000b2738e49866860c25afffe2f1a02",
                "width": 640
              },
              {
                "height": 300,
                "url": "https://i.scdn.co/image/ab67616d00001e028e49866860c25afffe2f1a02",
                "width": 300
              },
              {
                "height": 64,
                "url": "https://i.scdn.co/image/ab67616d000048518e49866860c25afffe2f1a02",
                "width": 64
              }
            ],
            "name": "...Baby One More Time (Digital Deluxe Version)",
            "uri": "spotify:album:3WNxdumkSMGMJRhEgK80qx"
          },
          "artists": [
            {
              "external_urls": {
                "spotify": "https://open.spotify.com/artist/26dSoYclwsYLMAKD3tpOr4"
              },
              "href": "https://api.spotify.com/v1/artists/26dSoYclwsYLMAKD3tpOr4",
              "id": "26dSoYclwsYLMAKD3tpOr4",
              "name": "Britney Spears",
              "type": "artist",
              "uri": "spotify:artist:26dSoYclwsYLMAKD3tpOr4"
            }
          ],
          "duration_ms": 211066,
          "href": "https://api.spotify.com/v1/tracks/3MjUtNVVq3C8Fn0MP3zhXa",
          "name": "...Baby One More Time",
          "popularity": 79,
          "uri": "spotify:track:3MjUtNVVq3C8Fn0MP3zhXa",
          "userUri": "spotify:user:",
          "username": "",
          "socketId": "",
          "startedAt": "2021-05-30T21:03:10.489Z",
          "thumbsDown": 0,
          "thumbsUp": 1,
          "thumbsUpUris": [
            "spotify:user:"
          ],
          "room": ""
        }
      ]
    }
  ],
  "pages": 334,
  "total": 9360,
  "page": "0"
}
```

### Room
> `GET https://jqbx.fm/room/{ROOM_ID}`

Response
```JSON
{
  "_id": "",
  "users": [
    {
      "username": "Sous-chef de Cuisine",
      "id": "",
      "uri": "spotify:user:",
      "device": "bot",
      "status": "active",
      "country": "US",
      "image": "https://i.imgur.com/7BUns2g.jpg",
      "socketId": "",
      "statusChangedAt": 1622325966907
    }
  ],
  "djs": [],
  "banned": [],
  "title": "",
  "visibility": "public",
  "password": "",
  "genre": "",
  "flexibility": null,
  "maxDjs": 10,
  "maxTurns": null,
  "modDjsOnly": null,
  "highlightMods": null,
  "messageTracks": null,
  "hideModFlair": null,
  "admin": [
    "spotify:user:"
  ],
  "mods": [
    "spotify:user:"
  ],
  "usersCount": 1,
  "djsCount": 0,
  "lastTouched": "2021-05-30T18:47:39.371Z",
  "sentWarningEmail": false,
  "savedCount": 36,
  "infoLink": "",
  "promoImageUrl": "",
  "promoImageHref": "",
  "welcomeMessage": "",
  "modsCanBan": null
}
```

### Active Rooms
> `GET https://jqbx.fm/active-rooms/{PAGE}`

Response
```JSON
{
  "rooms": [
    {
      "_id": "",
      "users": [
        {
          "id": "",
          "_id": "",
          "uri": "spotify:user:",
          "device": "desktop",
          "status": "active",
          "country": "TW",
          "socketId": "",
          "statusChangedAt": 1622401178153
        },
        {
          "username": "",
          "id": "",
          "_id": "",
          "uri": "spotify:user:",
          "image": "",
          "thumbsUpImage": "",
          "thumbsDownImage": "",
          "djImage": "",
          "device": "mobile",
          "status": "inactive",
          "country": "US",
          "socketId": "",
          "statusChangedAt": 1622404991121
        }
      ],
      "djs": [
        {
          "username": "",
          "id": "",
          "_id": "",
          "uri": "spotify:user:",
          "image": "",
          "thumbsUpImage": "",
          "thumbsDownImage": "",
          "djImage": "",
          "device": "desktop",
          "status": "active",
          "country": "",
          "socketId": "",
          "statusChangedAt": 1622383475212,
          "playCount": 0,
          "votes": []
        }
      ],
      "banned": [],
      "title": "",
      "visibility": "public",
      "genre": "",
      "flexibility": null,
      "maxDjs": 50,
      "maxTurns": 99,
      "modDjsOnly": null,
      "highlightMods": true,
      "messageTracks": null,
      "hideModFlair": null,
      "admin": [
        "spotify:user:"
      ],
      "mods": [],
      "usersCount": 20,
      "djsCount": 9,
      "lastTouched": "2021-05-30T20:56:24.083Z",
      "sentWarningEmail": false,
      "infoLink": "",
      "promoImageUrl": "",
      "promoImageHref": "",
      "welcomeMessage": "",
      "modsCanBan": true,
      "savedCount": 150,
      "tracks": [
        {
          "_id": "",
          "id": "",
          "album": {
            "images": [
              {
                "height": 640,
                "url": "https://i.scdn.co/image/ab67616d0000b27303d57a14692f0dcadd75d4d3",
                "width": 640
              },
              {
                "height": 300,
                "url": "https://i.scdn.co/image/ab67616d00001e0203d57a14692f0dcadd75d4d3",
                "width": 300
              },
              {
                "height": 64,
                "url": "https://i.scdn.co/image/ab67616d0000485103d57a14692f0dcadd75d4d3",
                "width": 64
              }
            ],
            "name": "沒路",
            "uri": "spotify:album:03ctDjJ4MZy4qZaPkt7JIl"
          },
          "artists": [
            {
              "external_urls": {
                "spotify": "https://open.spotify.com/artist/1bSuXaZRDQeCLEgtFb6a1U"
              },
              "href": "https://api.spotify.com/v1/artists/1bSuXaZRDQeCLEgtFb6a1U",
              "id": "1bSuXaZRDQeCLEgtFb6a1U",
              "name": "非人物種",
              "type": "artist",
              "uri": "spotify:artist:1bSuXaZRDQeCLEgtFb6a1U"
            }
          ],
          "duration_ms": 247880,
          "href": "https://api.spotify.com/v1/tracks/1scivLbVNcXhSW3e0Oa2CS",
          "name": "",
          "popularity": 29,
          "uri": "spotify:track:1scivLbVNcXhSW3e0Oa2CS",
          "userUri": "spotify:user:",
          "username": "",
          "socketId": "",
          "startedAt": "2021-05-30T20:56:24.083Z",
          "thumbsDown": 0,
          "thumbsUp": 1,
          "thumbsUpUris": [
            "spotify:user:"
          ],
          "room": ""
        }
      ]
    }
  ],
  "pages": 1,
  "total": 39,
  "page": "0"
}
```

### Saved Rooms
> `GET https://jqbx.fm/saved-rooms/0/spotify:user:{USER_ID}` [AUTH REQUIRED]

### Savad Users List
> `GET https://jqbx.fm/user/spotify:user:{USER_ID}/savedUsersList/{ROOM_ID}` [AUTH REQUIRED]


## Tracks
### First
> `GET https://jqbx.fm/tracks/first/spotify:track:{TRACK_ID}`

Response
```JSON
{
  "track": {
    "_id": "",
    "id": "",
    "album": {
      "images": [
        {
          "height": 640,
          "url": "https://i.scdn.co/image/e41f098d91fb1c96d133d5e8a825e84d1e01c9d5",
          "width": 640
        },
        {
          "height": 300,
          "url": "https://i.scdn.co/image/573ed158b70957bf7dabe7301bffab5e6c19dd84",
          "width": 300
        },
        {
          "height": 64,
          "url": "https://i.scdn.co/image/4dc907d5d7193fa4f8bb3706532721e2e53f391c",
          "width": 64
        }
      ],
      "name": "Glad To Be Sad",
      "uri": "spotify:album:3FequuV4vTOYFOFhRqCKCm"
    },
    "artists": [
      {
        "external_urls": {
          "spotify": "https://open.spotify.com/artist/4W1v5X4x0ObMOJVJreZX3k"
        },
        "href": "https://api.spotify.com/v1/artists/4W1v5X4x0ObMOJVJreZX3k",
        "id": "4W1v5X4x0ObMOJVJreZX3k",
        "name": "DMX Krew",
        "type": "artist",
        "uri": "spotify:artist:4W1v5X4x0ObMOJVJreZX3k"
      }
    ],
    "duration_ms": 123983,
    "href": "https://api.spotify.com/v1/tracks/4HpKLgvBpFlLgW5RhXGGc7",
    "name": "Shell Game - Original Mix",
    "popularity": 0,
    "uri": "spotify:track:",
    "userUri": "spotify:user:",
    "username": "",
    "socketId": "",
    "startedAt": "2019-03-01T18:16:44.008Z",
    "thumbsDown": 0,
    "thumbsUp": 1,
    "thumbsUpUris": [
      "spotify:user:"
    ],
    "room": ""
  },
  "user": {
    "_id": "",
    "uri": "spotify:user:",
    "country": "US",
    "status": "inactive",
    "thumbsUp": 34319,
    "stars": 13012,
    "username": "",
    "image": "",
    "thumbsDown": 742
  },
  "room": {
    "_id": "",
    "title": "",
    "visibility": "public",
    "genre": "",
    "maxDjs": null,
    "maxTurns": null,
    "modDjsOnly": false,
    "highlightMods": false,
    "hideModFlair": false,
    "usersCount": 0,
    "djsCount": 0,
    "handle": "",
    "infoLink": "",
    "promoImageUrl": "",
    "promoImageHref": ""
  }
}
```

## Promotions
> `GET https://jqbx.fm/promotions`

Response
```JSON
{
  "promo": null
}
```

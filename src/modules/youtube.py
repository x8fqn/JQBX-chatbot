from typing import Any, List
from youtube_search import YoutubeSearch

class Youtube:
    def searchTune(name: str, artist: List[str], lenght: int, maxResults: int = 10):
        query = name + ' '
        for item in artist:
            query += item + ' '
        request = YoutubeSearch(query, max_results = maxResults).to_dict()

        for video in request:
            durationYouTube = Youtube.durationToTimestamp(video['duration'])
            durationSpotify = lenght
            if -2 <= (durationYouTube - durationSpotify) <= 2:
                result = {'title': video['title'], 'url': 'https://youtu.be/%s' % video['id'], 
                    'duration': video['duration']}
                break
        if 'result' in locals():
            return result
        else:
            return False

    def durationToTimestamp(duration: str) -> int:
        duration = duration.split(':')[::-1]
        timestamp = int(duration[0])
        for i in range(1, len(duration)):
            timestamp += int(duration[i]) * (pow(60, i))
        return timestamp

    def search(query: str):
        pass

from unittest import TestCase
from src.track_history import AbstractTrackHistory, TrackHistory
from src.test_utils.test_helpers import create_random_track_object

class TrackHistoryTest(TestCase):
    def setUp(self) -> None:
        self.track_history: AbstractTrackHistory = TrackHistory()
        self.track_history.connect('trackHistoryTest')
        self.track = create_random_track_object()

    def test_add(self):
        self.track_history.add_track(self.track['name'], self.track['artists'], 
            self.track['uri'], self.track['startedAt'], self.track['userUri'])
        
    def test_add_and_update(self):
        self.track_history.add_track(self.track['name'], self.track['artists'], 
            self.track['uri'], self.track['startedAt'], self.track['userUri'])
        self.track_history.update_track_votes(self.track['startedAt'], 3, 4, 5, 8)

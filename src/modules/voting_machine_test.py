from typing import List
from unittest import TestCase

from src.test_utils.fake_bot_controller import FakeBotController
from src.test_utils.test_helpers import create_random_id_object, create_random_string
from src.room_state import RoomState
from src.modules.voting_machine import VotingMachine
from src.modules.starring_machine import StarringMachine


class VotingMachineTest(TestCase):
    def setUp(self) -> None:
        self.__bot_controller = FakeBotController()
        self.__room_state = RoomState.get_instance(self.__bot_controller)
        self.__voting_machine = VotingMachine('row', self.__bot_controller, self.__room_state)
        self.__starring_machine = StarringMachine('star', self.__bot_controller, self.__room_state)
        self.__room_state.set_current_track(create_random_id_object())
        self.__room_state.set_djs([create_random_id_object() for _ in range(1, 10)])
        self.__mo = create_random_string()
        self.__curly = create_random_string()
        self.__joe = create_random_string()

    def test_ro_star_twice_same_user(self) -> None:
        self.assertIsNone(self.__do_vote(self.__mo))
        self.assertFalse(self.__do_vote(self.__mo))
        self.assertIsNone(self.__do_star(self.__mo))
        self.assertFalse(self.__do_star(self.__mo))
        self.assertFalse(self.__bot_controller.doped)
        self.assertFalse(self.__bot_controller.starred)
        self.__dequeue_and_print_chats(self.__bot_controller.dequeue_chats())
    
    def test_ro_star_by_dj(self) -> None:
        self.__room_state.set_djs([{"id": self.__mo}])
        self.assertFalse(self.__do_vote(self.__mo))
        self.assertFalse(self.__do_star(self.__mo))
        self.__dequeue_and_print_chats(self.__bot_controller.dequeue_chats())

    def test_ro_two_different_songs(self) -> None:
        self.__do_vote(self.__mo)
        self.__room_state.set_current_track(create_random_id_object())
        self.__do_vote(self.__mo)
        self.assertFalse(self.__bot_controller.doped)
        self.__dequeue_and_print_chats(self.__bot_controller.dequeue_chats())
    
    def test_star_by_two_people(self) -> None:
        self.__do_star(self.__mo)
        self.__do_star(self.__curly)
        self.assertFalse(self.__bot_controller.starred)
        self.__dequeue_and_print_chats(self.__bot_controller.dequeue_chats())

    def test_ro(self) -> None:
        self.__do_vote(self.__mo)
        self.assertFalse(self.__bot_controller.doped)
        self.__do_vote(self.__curly)
        self.assertFalse(self.__bot_controller.doped)
        self.__do_vote(self.__joe)
        self.assertTrue(self.__bot_controller.doped)
        self.__dequeue_and_print_chats(self.__bot_controller.dequeue_chats())

    def test_star(self) -> None:
        self.__do_star(self.__mo)
        self.assertFalse(self.__bot_controller.starred)
        self.__do_star(self.__curly)
        self.assertFalse(self.__bot_controller.starred)
        self.__do_star(self.__joe)
        self.assertFalse(self.__bot_controller.starred)
        self.__dequeue_and_print_chats(self.__bot_controller.dequeue_chats())

    def test_already_bopping(self) -> None:
        self.__bot_controller.dope()
        self.__do_vote(self.__mo)
        self.__dequeue_and_assert_chats([
            'I\'m already bopping to this'
        ])
        self.__dequeue_and_print_chats(self.__bot_controller.dequeue_chats())

    def test_already_hating(self) -> None:
        self.__bot_controller.nope()
        self.__do_vote(self.__mo)
        self.__dequeue_and_assert_chats([
            'I\'m already hating this'
        ])
        self.__dequeue_and_print_chats(self.__bot_controller.dequeue_chats())

    def __do_vote(self, user_id: str) -> None:
        return self.__voting_machine.vote(user_id, lambda x: x.dope())

    def __do_star(self, user_id: str):
        return self.__starring_machine.vote(user_id, lambda x: x.dope())

    def __dequeue_and_assert_chats(self, expected_chats: List[str]) -> None:
        chats = self.__bot_controller.dequeue_chats()
        self.assertEqual(expected_chats, chats)

    def __dequeue_and_print_chats(self, chats: List[str]):
        if len(chats) <= 0:
            return
        chats.insert(0,'\n' + ' CHATS '.center(15, '-'))
        chats.append('-' * 15)
        print('\n'.join(chats) + '\n')
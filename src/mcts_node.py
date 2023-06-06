from abc import abstractmethod, ABC
from typing import Set


class MCTSNode(ABC):
    @abstractmethod
    def find_children(self) -> Set['MCTSNode']:
        return set()

    @abstractmethod
    def make_random_move(self) -> 'MCTSNode':
        pass

    @property
    @abstractmethod
    def terminal(self) -> bool:
        pass

    @abstractmethod
    def reward(self) -> int:
        return 0

    @abstractmethod
    def __hash__(self)->int:
        return 123456789

    @abstractmethod
    def __eq__(self, other)->bool:
        return True

import __main__
from typing import Union

from .State import State


class Machine:
    """
    State machine.
    """

    def __init__(self, state: list, initial: str, tabular=""):
        """
        States must be a dictionary, initial must be the first state.

        @type state: list[State]
        @param state: list of states.

        @type initial: str
        @param initial: initial state, expressed as a string.
        """

        self.state = self.initialize(state)
        self.current = self.state[initial]
        self.tabular = tabular

    def get_state(self) -> State:
        """
        Returns the current state.

        @rtype: State
        @returns: current state.
        """

        return self.current

    def set_state(self, this_state: str):
        """
        Sets the current state.
        """

        self.current = self.state[this_state]

    def get_next_state(self) -> State:
        """
        Returns the next state.
        """

        next_state = self.current.next_state

        if next_state:
            if next_state in self.state:
                return self.state[self.current.next_state]
            else:
                print(
                    f"{self.tabular}[{__main__.__file__}]: next state: "
                    + f"{next_state}, does not exist!!!"
                )

                return None

        return None

    def to_next_state(self):
        """
        Sets the current state to the next state.
        """

        self.current = self.get_next_state()

    @staticmethod
    def initialize(state: Union[list, dict]) -> dict:
        """
        It receives a list of States and converts it to a dictionary
        with the name and instantiated object of the class.

        @type state: list[State] or dict
        @param state: list or data dictionary.

        @rtype: dict
        @returns: dictionary with the name and instantiated
        object of the class.
        """

        if isinstance(state, dict):
            return state

        if isinstance(state, list):
            proper_states = {}

            for i, sta in enumerate(state):
                sta.number = i
                proper_states[sta.name] = sta

            return proper_states

        insiders = dict()

        for sta in state:
            name = sta.name
            insiders[name] = sta

        return insiders

    def execute(self, **kwargs: dict) -> dict:
        """
        Executes the current state and goes to the next one.

        @type kwargs: dict
        @param kwargs: dictionary with the data to be processed.

        @rtype: dict
        @returns: dictionary with the processed data.
        """

        return self.current(**kwargs)

    def cicle(self, **kwargs: dict) -> dict:
        """
        It loops through each of the states, executes them,
        until the next one is None.

        @type kwargs: dict
        @param kwargs: dictionary with the data to be processed.

        @rtype: dict
        @returns: dictionary with the processed data.
        """

        while self.current is not None:
            try:
                kwargs = self.execute(**kwargs)
            except Exception as e:
                kwargs["error"] = e
                print(f"{self.tabular}[{__main__.__file__}]: Error: {e}")
                break

            self.to_next_state()

        return kwargs

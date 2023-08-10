class State:
    """
    default state class.
    """

    number = None
    next_state = None

    def __init__(self, name: str = None, number: int = None,
                 next_state: str = None, tabular: str = ""):
        """
        State class initialization.

        @type name: str
        @param name: String containing the name of this state.

        @type number: int
        @param number: Integer content or number of this state.

        @type next_state: str
        @param next_state: String naming the next state.

        @type tabular: str
        @param tabular: String containing the tabular of this state,
        used only for print in verbose mode.
        """

        if name:
            self.name = name
        else:
            self.name = self.__class__.__name__

        if number:
            self.number = number

        if next_state:
            self.next_state = next_state

        self.tabular = tabular

    def __str__(self):
        """
        String representation of this state.
        """

        return self.name

    def __call__(self, **kwargs: dict) -> dict:
        """
        execute the current state according to passed parameters
        and return the next one.

        @type kwargs: dict
        @param kwargs: dictionary of parameters.

        @rtype: dict
        @returns: dictionary with data for the next state.
        """

        if kwargs.get("verbose"):
            print(f'{self.tabular} running state: {self.name} {self.tabular}')

        return self.execute(**kwargs)

    def execute(self, **kwargs: dict) -> dict:
        """
        execute the current state according to passed parameters
        and return the next one.

        @type kwargs: dict
        @param kwargs: dictionary of parameters.

        @rtype: dict
        @returns: dictionary with data for the next state.
        """

        """
        This method must be implemented in the child class with the logic of
        the state is called by the __call__ method.
        is important to return the dictionary with the data for the next state.
        """

        return kwargs

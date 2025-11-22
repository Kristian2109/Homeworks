class State:
    def __init__(self, empty_space_index: int,
                 left_frogs_after_empty_space: int,
                 frogs_count_per_side: int):
        self.empty_space_index: int = empty_space_index
        self.left_frogs_after_empty_space: int = left_frogs_after_empty_space
        self.frogs_count_per_side: int = frogs_count_per_side

    def is_target(self) -> bool:
        return self.empty_space_index == self.frogs_count_per_side and\
               self.left_frogs_after_empty_space == self.frogs_count_per_side


class FrogsJumping:
    def __init__(self, frogs_count: int):
        self.isCompleted = False
        self.winningPath = []
        self.state_string = []

        for _ in range(frogs_count):
            self.state_string.append('>')

        self.state_string.append('_')

        for _ in range(frogs_count):
            self.state_string.append('<')

        self.initialState: State = State(frogs_count, 0, frogs_count)

    def execute(self):
        self.walk_frogs(self.initialState)
    
    def walk_frogs(self, state: State):
        if self.isCompleted:
            return
    
        if state.is_target():
            self.isCompleted = True
    
        if state.empty_space_index >= 2 and self.state_string[state.empty_space_index - 2] == '>':
            self.state_string[state.empty_space_index - 2] = '_'
            self.state_string[state.empty_space_index] = '>'
            left_frogs_after_empty_space = state.left_frogs_after_empty_space + 1
            if self.state_string[state.empty_space_index - 1] == '>':
                left_frogs_after_empty_space += 1
    
            self.walk_frogs(State(state.empty_space_index - 2, left_frogs_after_empty_space, state.frogs_count_per_side))
            self.state_string[state.empty_space_index - 2] = '>'
            self.state_string[state.empty_space_index] = '_'
    
        if state.empty_space_index >= 1 and self.state_string[state.empty_space_index - 1] == '>':
            self.state_string[state.empty_space_index - 1] = '_'
            self.state_string[state.empty_space_index] = '>'
            left_frogs_after_empty_space = state.left_frogs_after_empty_space + 1
    
            self.walk_frogs(State(state.empty_space_index - 1, left_frogs_after_empty_space, state.frogs_count_per_side))
            self.state_string[state.empty_space_index - 1] = '>'
            self.state_string[state.empty_space_index] = '_'
    
        if state.empty_space_index <= state.frogs_count_per_side * 2 - 2 and \
                self.state_string[state.empty_space_index + 2] == '<':
    
            self.state_string[state.empty_space_index + 2] = '_'
            self.state_string[state.empty_space_index] = '<'
            left_frogs_after_empty_space = state.left_frogs_after_empty_space
            if self.state_string[state.empty_space_index + 1] == '>':
                left_frogs_after_empty_space -= 1
    
            self.walk_frogs(State(state.empty_space_index + 2, left_frogs_after_empty_space, state.frogs_count_per_side))
            self.state_string[state.empty_space_index + 2] = '<'
            self.state_string[state.empty_space_index] = '_'
    
        if state.empty_space_index <= state.frogs_count_per_side * 2 - 1 and \
                self.state_string[state.empty_space_index + 1] == '<':
    
            self.state_string[state.empty_space_index + 1] = '_'
            self.state_string[state.empty_space_index] = '<'
            left_frogs_after_empty_space = state.left_frogs_after_empty_space
    
            self.walk_frogs(State(state.empty_space_index + 1, left_frogs_after_empty_space, state.frogs_count_per_side))
            self.state_string[state.empty_space_index + 1] = '<'
            self.state_string[state.empty_space_index] = '_'
    
        if self.isCompleted:
            self.winningPath.append(''.join(self.state_string))


def start_frogs():
    frogs_count = int(input())
    frogs_jumping = FrogsJumping(frogs_count)
    frogs_jumping.execute()

    for s in reversed(frogs_jumping.winningPath):
        print(s)


if __name__ == '__main__':
    start_frogs()
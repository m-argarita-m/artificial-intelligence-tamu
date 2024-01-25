class State:
    def __init__(self, stacks):
        self.stacks = stacks

    def __eq__(self, other):
        return self.stacks == other.stacks

    def __hash__(self):
        return hash(tuple(tuple(stack) for stack in self.stacks))

    def __str__(self):
        stack_strings = [''.join(stack) for stack in self.stacks]
        return '\n'.join(stack_strings)

    def move(self, source_stack_index, dest_stack_index):
        if not self.is_valid_move(source_stack_index, dest_stack_index):
            raise ValueError('Invalid move')

        block = self.stacks[source_stack_index].pop()
        self.stacks[dest_stack_index].append(block)

    def is_valid_move(self, source_stack_index, dest_stack_index):
        if source_stack_index < 0 or source_stack_index >= len(self.stacks):
            return False
        if dest_stack_index < 0 or dest_stack_index >= len(self.stacks):
            return False
        if len(self.stacks[source_stack_index]) == 0:
            return False
        if source_stack_index == dest_stack_index:
            return False
        return True

    def is_goal(self, goal_state):
        return self == goal_state

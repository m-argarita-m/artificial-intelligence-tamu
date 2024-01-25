from state import State

class Node:
    def __init__(self, state, parent=None, action=None, depth=0, path_cost=0, heuristic_value=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = depth
        self.path_cost = path_cost

    def __hash__(self):
        return hash(self.state)

    def __str__(self):
        parent_str = str(self.parent.state) if self.parent else 'None'
        node_str = f'State:\n{str(self.state)}\nParent Stack:\n{parent_str}\nAction: Moved block from stack {self.action[0]} to stack {self.action[1]}\n\nDepth: {self.depth}\nPath Cost: {self.path_cost}\n'
        return node_str

    def successors(self):
        successor_nodes = []
        current_stacks = self.state.stacks

        for source_stack in range(len(current_stacks)):
            for dest_stack in range(len(current_stacks)):
                if source_stack != dest_stack and self.state.is_valid_move(source_stack, dest_stack):
                    new_stacks = [stack[:] for stack in current_stacks]
                    new_state = State(new_stacks)

                    new_state.move(source_stack, dest_stack)
                    successor_node = Node(new_state, parent=self, action=(source_stack, dest_stack),
                                          depth=self.depth + 1, path_cost=self.path_cost + 1)

                    successor_nodes.append(successor_node)

        return successor_nodes

from state import State
from node import Node
import heapq

def parse_bwp_file(file_path):
    data = {}

    with open(file_path, 'r') as file:
        lines = file.readlines()

        num_stacks, num_blocks, num_moves = map(int, lines.pop(0).strip().split())

        lines.pop(0)

        initial_stacks = [[elem for elem in line] for line in lines[:num_stacks]]
        for stack in initial_stacks:
            stack.pop()

        lines = lines[num_stacks + 1:]

        final_stacks = [[elem for elem in line] for line in lines[:num_stacks]]
        for stack in final_stacks:
            stack.pop()

        data['numStacks'] = num_stacks
        data['numBlocks'] = num_blocks
        data['numMovesUsedToGenerate'] = num_moves
        data['initialStacks'] = initial_stacks
        data['finalStacks'] = final_stacks

        initialState = State(initial_stacks)
        goalState = State(final_stacks)

        data['initialState'] = initialState
        data['goalState'] = goalState

    return data

def state_stack_to_letter_position_dict(state):
    letter_to_position_dict = {}

    for row_index, each_stack in enumerate(state.stacks):
        if len(each_stack) == 0:
            continue

        for index, block in enumerate(each_stack):
            x_coord = row_index
            y_coord = index
            position = (x_coord, y_coord)
            letter_to_position_dict[block] = position

    return letter_to_position_dict

def heuristic(current_state, current_state_positions_dict, goal_state_positions_dict, which_heuristic):
    if which_heuristic == 'H0':
        return 0
    elif which_heuristic == 'H1':
        return h1(current_state_positions_dict, goal_state_positions_dict)
    elif which_heuristic == 'H2':
        return h2(current_state, current_state_positions_dict, goal_state_positions_dict)
    elif which_heuristic == 'H3':
        return h3(current_state_positions_dict, goal_state_positions_dict)
    elif which_heuristic == 'H4':
        return h4(current_state_positions_dict, goal_state_positions_dict)
    elif which_heuristic == 'H5':
        return h5(current_state, current_state_positions_dict, goal_state_positions_dict)
    else:
        return h6(current_state, current_state_positions_dict, goal_state_positions_dict)

def h1(current_state_positions_dict, goal_state_positions_dict):
    h_score = 0
    for key in current_state_positions_dict.keys():
        true_position = current_state_positions_dict[key]
        goal_position = goal_state_positions_dict[key]
        if true_position != goal_position:
            h_score += 1

    return h_score

def h2(current_state, current_state_positions_dict, goal_state_positions_dict):
    h_score = 0
    x = 1
    y = 2
    z = 3

    for stack_index, current_stack in enumerate(current_state.stacks):
        for height, block in enumerate(current_stack):
            true_position = current_state_positions_dict[block]
            goal_position = goal_state_positions_dict[block]

            if true_position != goal_position:
                if true_position[0] != goal_position[0]:
                    a = 1
                elif true_position[0]+1 == len(current_state.stacks[true_position[0]]):
                    a = 2
                else:
                    a = 3
                m_blocks_blocking_movement = height + 1
                d_blocks_blocking_destination = abs(len(current_state.stacks[goal_position[0]]) - goal_position[1])
                h_score += ((a * x) + (m_blocks_blocking_movement * y) + (d_blocks_blocking_destination * z))

    return h_score


def h3(current_state_positions_dict, goal_state_positions_dict):
    h_score = 0

    for block, current_position in current_state_positions_dict.items():
        goal_position = goal_state_positions_dict[block]
        distance = abs(current_position[0] - goal_position[0]) + abs(current_position[1] - goal_position[1])
        h_score += distance

    return h_score

def h4(current_state_positions_dict, goal_state_positions_dict):
    h_score = 0

    for block, (current_stack, current_height) in current_state_positions_dict.items():
        if block in goal_state_positions_dict:
            goal_stack, goal_height = goal_state_positions_dict[block]

            if current_stack != goal_stack or current_height != goal_height:
                must_be_moved_once = False
                must_be_moved_twice = False

                for other_block, (other_stack, other_height) in current_state_positions_dict.items():
                    if other_stack == current_stack and other_height < current_height:
                        if (other_block not in goal_state_positions_dict) or (goal_state_positions_dict[other_block] != (goal_stack, other_height)):
                            must_be_moved_once = True
                            break

                for other_block, (other_stack, other_height) in current_state_positions_dict.items():
                    if (other_stack == current_stack) and (other_height < current_height):
                        if (other_block in goal_state_positions_dict) and (goal_state_positions_dict[other_block] == (goal_stack, other_height)):
                            must_be_moved_twice = True
                            break

                if must_be_moved_once:
                    h_score += 1
                elif must_be_moved_twice:
                    h_score += 4

    return h_score

def h5(current_state, current_state_positions_dict, goal_state_positions_dict):
    h_score = 0
    x = 1
    y = 2
    z = 3

    for block, current_position in current_state_positions_dict.items():
        goal_position = goal_state_positions_dict[block]

        if current_position != goal_position:
            a = 1
            m_blocks_blocking_movement = count_blocks_blocking_movement(current_state, block, current_state_positions_dict)
            d_blocks_blocking_destination = count_blocks_blocking_destination(current_state, block, goal_state_positions_dict)
            w_blocks_under_in_wrong_position = count_blocks_under_in_wrong_position(current_state, block, current_state_positions_dict, goal_state_positions_dict)

            h_score += ((a * x) + (m_blocks_blocking_movement * y) + (d_blocks_blocking_destination * z) + (w_blocks_under_in_wrong_position // 2))
        else:
            w_blocks_under_in_wrong_position = count_blocks_under_in_wrong_position(current_state, block, current_state_positions_dict, goal_state_positions_dict)
            h_score += (w_blocks_under_in_wrong_position // 2)

    return h_score

def count_blocks_under_in_wrong_position(current_state, block, current_state_positions_dict, goal_state_positions_dict):
    w_blocks_under_in_wrong_position = 0
    current_position = current_state_positions_dict[block]
    block_curr_stack_index = current_position[0]
    block_curr_height = current_position[1]
    blocks_to_check = current_state.stacks[block_curr_stack_index][:block_curr_height]
    for under_block in blocks_to_check:
        if current_state_positions_dict[under_block] != goal_state_positions_dict[under_block]:
            w_blocks_under_in_wrong_position += 1

    return w_blocks_under_in_wrong_position

def count_blocks_blocking_movement(current_state, block, current_state_positions_dict):
    block_curr_stack_index = current_state_positions_dict[block][0]
    size_of_curr_block_stack = len(current_state.stacks[block_curr_stack_index])
    block_curr_height = current_state_positions_dict[block][1]
    m_blocks_blocking_movement = (size_of_curr_block_stack - 1) - block_curr_height

    return m_blocks_blocking_movement

def count_blocks_blocking_destination(current_state, block, goal_state_positions_dict):
    goal_position = goal_state_positions_dict[block]
    block_goal_stack_index = goal_position[0]
    block_goal_height = goal_position[1]

    needed_height_for_dest_stack = block_goal_height - 1
    actual_height_for_dest_stack = len(current_state.stacks[block_goal_stack_index]) - 1

    d_blocks_blocking_destination = abs(needed_height_for_dest_stack - actual_height_for_dest_stack)

    return d_blocks_blocking_destination

def h6(current_state, current_state_positions_dict, goal_state_positions_dict):
    h_score = 0

    for block, true_position in current_state_positions_dict.items():
        goal_position = goal_state_positions_dict[block]
        if true_position != goal_position:
            block_curr_stack_index = true_position[0]
            block_curr_height = true_position[1]
            block_curr_stack_height = len(current_state.stacks[block_curr_stack_index])
            h_score += max(1, block_curr_stack_height - block_curr_height)

    return h_score

def a_star_search(initial_state, goal_state, which_heuristic, max_iters=1000000):
    open_set = []
    closed_set = set()

    goal_state_positions_dict = state_stack_to_letter_position_dict(goal_state)

    initial_node = Node(initial_state)
    heapq.heappush(open_set, (0, id(initial_node), initial_node))

    iterations = 0
    max_queue_size = 0
    while open_set and iterations < max_iters:
        _, _, current_node = heapq.heappop(open_set)
        iterations += 1
        current_state_positions_dict = state_stack_to_letter_position_dict(current_node.state)

        depth = current_node.depth
        path_cost = depth
        heuristic_value = heuristic(current_node.state, current_state_positions_dict, goal_state_positions_dict, which_heuristic)
        score = path_cost + heuristic_value
        num_children = len(current_node.successors())
        queue_size = len(open_set)
        print(f'Iteration {iterations}: depth = {depth}, pathcost = {path_cost}, score = {score}, heuristic = {heuristic_value}, children = {num_children}, q_size = {queue_size}')
        max_queue_size = max(max_queue_size, queue_size)
        if current_node.state.is_goal(goal_state):
            solution_node = current_node
            moves = []

            while solution_node.parent:
                moves.append(solution_node.action)
                solution_node = solution_node.parent

            moves.reverse()

            current_state = initial_state  # Initialize the current state with the initial state
            print(f'\n---goal state---\n{goal_state}\n>>>>>>>>>>>>>>>>>>>>')
            print(f'---initial state---\n{initial_state}\n>>>>>>>>>>>>>>>>>>>>')
            num_steps = 0
            for move_num, (source_stack, dest_stack) in enumerate(moves):
                moved_block_name = current_state.stacks[source_stack][-1]
                current_state.move(source_stack, dest_stack)
                num_steps += 1
                current_state_positions_dict = state_stack_to_letter_position_dict(current_state)
                h_cost = heuristic(current_state, current_state_positions_dict, goal_state_positions_dict,
                                   which_heuristic)
                print(
                    f'Move {move_num + 1}:\npath_cost = {num_steps}, heuristic = {h_cost}, f(n) =  g(n) + h(n) = {num_steps + h_cost}\nMoved block {moved_block_name} from stack {source_stack + 1} to stack {dest_stack + 1}, resulting in...')

                print(current_state)
                print('>>>>>>>>>>>>>>>>>>>>')

            print(f'\nSuccess! Using {which_heuristic}, found solution with cost = {current_node.path_cost} on iteration {iterations}. Max queue size was {max_queue_size}.')
            return current_node

        closed_set.add(str(current_node.state))

        for successor_node in current_node.successors():
            successor_state_str = str(successor_node.state)

            if successor_state_str in closed_set:
                continue

            current_cost = current_node.depth + 1
            hueristic_cost_estimation = heuristic(successor_node.state, current_state_positions_dict, goal_state_positions_dict, which_heuristic)
            predicted_cost = current_cost + hueristic_cost_estimation
            heapq.heappush(open_set, (predicted_cost, id(successor_node), successor_node))

    print(f'No Solution: max queue size reached was {max_queue_size}')
    return None
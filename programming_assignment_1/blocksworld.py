import sys
from helper_functions import parse_bwp_file, a_star_search

which_heuristic = 'H6'
max_iters = 1000000

script_name = sys.argv[0]

if len(sys.argv) > 1:
    filename = sys.argv[1]
    file_path = f'./probs/{filename}.bwp'
    parsed_data = parse_bwp_file(file_path)
    initial_state = parsed_data['initialState']
    goal_state = parsed_data['goalState']
else:
    print('You must provide a filename.')
    sys.exit(1)

arguments = sys.argv[2:]
i = 0
while i < len(arguments):
    arg = arguments[i]

    if arg == '-h' and i + 1 < len(arguments):
        which_heuristic = arguments[i + 1]
        i += 2
    elif arg == '-m' and i + 1 < len(arguments):
        max_iters = int(arguments[i + 1])
        i += 2
    else:
        print(f'Invalid argument: {arg}')
        sys.exit(1)

print(f'Script Name: {script_name}')
print(f'Test Case: {filename}')
print(f'Selected heuristic was: {which_heuristic}')
print(f'max_iters will be: {max_iters}')
print(f'file_path is: {file_path}')
print(f'\n---initial state---\n{initial_state}')
print(f'---goal state---\n{goal_state}')
print('**'*100)

solution_node = a_star_search(initial_state, goal_state, which_heuristic, max_iters)

if solution_node:
    print(f'Solution found for test case: {filename}')
else:
    print(f'Could not find solution for test case: {filename} within {max_iters} iterations.')
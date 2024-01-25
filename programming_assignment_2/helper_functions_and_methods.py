import sys
sys.setrecursionlimit(100000)
counter = 0

def create_model_and_clauses(file_name, given_statements):
    model = get_vars_for_model_from_kb(file_name)
    print(f'model is initially:\n{model}\n')

    model = add_given_statements_to_model(model, given_statements)
    print(f'after considering given statements, model is:\n{model}\n')

    clauses = get_clauses_from_kb(file_name)
    return model, clauses

def print_given_arguments(cmd_line_args, script_name, file_name, transcript_file_path, use_unit_clause_heuristic, given_statements):
    cmd_line_args.insert(0, 'python3')
    print(f'Command:                           {" ".join(cmd_line_args)}')
    print(f'Script Name:                       {script_name}')
    print(f'CNF File Name:                     {file_name}')
    print(f'Transcript File Path:              {transcript_file_path}')
    print(f'We will use Unit Clause Heuristic? {use_unit_clause_heuristic}')
    print('Given Statements for KB:\n')
    print('.' * 125)
    if len(given_statements) == 0:
        print('No Given Statements')
    else:
        for index, statement in enumerate(given_statements):
            print(f'{index + 1}.\t{statement}')
    print('.' * 125)
    print()

    print('*' * 250)

def gather_user_input():
    script_name = sys.argv[0]

    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        print('\nExpected usage: python3 DPLL.py <filename> <literal>* [+UCH] -t <transcript_path>')
        sys.exit(1)

    remaining_arguments = sys.argv[2:]

    use_unit_clause_heuristic = True if '+UCH' in remaining_arguments else False
    create_transcript = True if '-t' in remaining_arguments else False
    if create_transcript:
        transcript_path = remaining_arguments[-1]
        remaining_arguments.remove('-t')
        remaining_arguments.remove(transcript_path)
    else:
        transcript_path = None
    given_statements = remaining_arguments[:len(remaining_arguments)-1] if use_unit_clause_heuristic else remaining_arguments

    return (use_unit_clause_heuristic, given_statements, file_name, transcript_path, script_name, sys.argv)

def add_given_statements_to_model(model, given_statements):
    for statement in given_statements:
        if statement[0] == '-':
            variable = statement[1:]
            model[variable] = -1
        else:
            model[statement] = 1

    return model

def get_vars_for_model_from_kb(filename):
    model = {}

    with open(filename, 'r') as file:
        for line in file:
            if not line.startswith('#') and '#' not in line:
                words = line.split()
                for word in words:
                    word = word.lstrip('-')
                    model[word] = 0

    return model

def get_clauses_from_kb(file_name):
    clauses_list = []

    with open(file_name, 'r') as file:
        lines = file.readlines()

        for line in lines:
            line = line.strip()

            if line and not line.startswith('#'):
                clauses_list.append(line)

    return clauses_list

def DPLL(clauses, model, use_unit_clause_heuristic=False):
    if use_unit_clause_heuristic:
        is_satisfiable, final_model = DPLL_with_UCH(clauses, model)
        print(f'\nIs satisfiable: {is_satisfiable}\n')
        if final_model is not None:
            print(f'\nFinal model:\n{final_model}')
    else:
        is_satisfiable, final_model = DPLL_without_UCH(clauses, model)
        print(f'\nIs satisfiable: {is_satisfiable}\n')
        if final_model is not None:
            print(f'\nFinal model:\n{final_model}')

    print(f'\nTotal DPLL Calls: {counter}')
    print(f'Used UCH? {use_unit_clause_heuristic}')
    if is_satisfiable:
        print('\n  -  Just the SATISFIED / TRUE Propositions  -  \n')
    else:
        print('\n  -  MODEL WAS UNSATISFIABLE  -  \n')
    if final_model is not None:
        for variable, truth_value in final_model.items():
            if truth_value == 1:
                print(f'{variable}', end=' ')
    print('\n' + '_'*80)

# Looks good
def all_clauses_satisfied(clauses, model):
    for clause in clauses:
        clause_satisfied = False
        clause_list = clause.split(' ')
        for literal in clause_list:
            if (literal[0] == '-' and model[literal[1:]] == -1) or (literal[0] != '-' and model[literal] == 1):
                clause_satisfied = True
                break
        if not clause_satisfied:
            print('All Clauses Satisfied returned False for this model - Found Unsatisfied Clause :(')
            return False
    print('All Clauses Satisfied returned True for this model - All Clauses Satisfied :)')
    return True

def any_clause_unsatisfiable(clauses, model):
    for clause in clauses:
        clause_unsatisfiable = True

        clause_list = clause.split(' ')
        for literal in clause_list:
            if (literal[0] == '-' and model[literal[1:]] != 1) or (literal[0] != '-' and model[literal] != -1):
                clause_unsatisfiable = False
                break

        if clause_unsatisfiable:
            print('Any Clause Unsatisfiable returned True for this model - Found Unsatisfiable Clause :(')
            return True

    print('Any Clause Unsatisfiable returned False for this model - Did NOT find Unsatisfiable Clause :)')
    return False

def DPLL_without_UCH(clauses, model):
    global counter
    counter += 1
    print(f'\t-\tAttempt {counter}\t-\t')

    if all_clauses_satisfied(clauses, model):
        return True, model
    if any_clause_unsatisfiable(clauses, model):
        return False, None

    variable_to_assign = choose_variable(model)
    if variable_to_assign == 0:
        if all_clauses_satisfied(clauses, model):
            return True, model
        else:
            return False, None

    print(f'\nTrying {variable_to_assign} = True')
    model_copy = model.copy()
    model_copy[variable_to_assign] = 1
    print(f'\nModel now looks like:\n{model_copy}\n')
    is_satisfiable, final_model = DPLL_without_UCH(clauses, model_copy)
    if is_satisfiable:
        return True, final_model

    print(f'\nBacktracking from {variable_to_assign} = True')
    print(f'\nTrying {variable_to_assign} = False')
    model_copy = model.copy()
    model_copy[variable_to_assign] = -1
    print(f'\nModel now looks like:\n{model_copy}\n')
    is_satisfiable, final_model = DPLL_without_UCH(clauses, model_copy)
    return is_satisfiable, final_model

def DPLL_with_UCH(clauses, model):
    global counter
    counter += 1
    print(f'\t-\tAttempt {counter}\t-\t')

    if all_clauses_satisfied(clauses, model):
        return True, model
    if any_clause_unsatisfiable(clauses, model):
        return False, None

    unit_clause = find_unit_clause(clauses, model)
    if unit_clause:
        print(f'Unit Clause Found: {unit_clause}')
        variable_to_assign, value = unit_clause
        model_copy = model.copy()
        model_copy[variable_to_assign] = value
        print(f'Assigning {variable_to_assign} = {value}')
        print(f'Model now looks like:\n{model_copy}\n')
        return DPLL_with_UCH(clauses, model_copy)

    variable_to_assign = choose_variable(model)
    if variable_to_assign == 0:
        if all_clauses_satisfied(clauses, model):
            return True, model
        else:
            return False, None

    print(f'Trying {variable_to_assign} = True')
    model_copy = model.copy()
    model_copy[variable_to_assign] = 1
    print(f'Model now looks like:\n{model_copy}\n')
    is_satisfiable, final_model = DPLL_with_UCH(clauses, model_copy)
    if is_satisfiable:
        return True, final_model

    print(f'Backtracking from {variable_to_assign} = True')
    print(f'Trying {variable_to_assign} = False')
    model_copy = model.copy()
    model_copy[variable_to_assign] = -1
    print(f'Model now looks like:\n{model_copy}\n')
    is_satisfiable, final_model = DPLL_with_UCH(clauses, model_copy)
    return is_satisfiable, final_model


def clause_is_satisfied(clause, model):
    clause_list = clause.split(' ')
    for literal in clause_list:
        if (literal[0] == '-' and model[literal[1:]] == -1) or (literal[0] != '-' and model[literal] == 1):
            return True

    return False

def is_unit_clause(clause, model):
    num_literals_unknown = 0
    clause_list = clause.split(' ')
    for literal in clause_list:
        if (literal[0] == '-' and model[literal[1:]] == 0) or (literal[0] != '-' and model[literal] == 0):
            num_literals_unknown += 1

    if num_literals_unknown == 1:
        return True
    return False

def find_unit_clause(clauses, model):
    for clause in clauses:
        if not clause_is_satisfied(clause, model):
            if is_unit_clause(clause, model):
                unknown_variable = ''
                value_to_assign = 0
                clause_list = clause.split(' ')
                for literal in clause_list:
                    if literal[0] == '-' and model[literal[1:]] == 0:
                        unknown_variable = literal[1:]
                        value_to_assign = -1
                        break
                    elif literal[0] != '-' and model[literal] == 0:
                        unknown_variable = literal
                        value_to_assign = 1
                        break
                return unknown_variable, value_to_assign
    return None

def choose_variable(model):
    for variable, value in model.items():
        if value == 0:
            return variable

    return 0
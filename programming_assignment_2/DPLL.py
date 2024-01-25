from helper_functions_and_methods import DPLL, get_vars_for_model_from_kb, gather_user_input, \
    add_given_statements_to_model, get_clauses_from_kb, print_given_arguments, create_model_and_clauses

import sys
import os

if __name__ == '__main__':
    use_unit_clause_heuristic, given_statements, file_name, transcript_file_path, script_name, cmd_line_args = gather_user_input()

    if transcript_file_path:
        transcripts_folder = transcript_file_path.split('/')[0]
        os.makedirs(transcripts_folder, exist_ok=True)
        transcript_file_name = transcript_file_path.split('/')[1]

        with open(transcript_file_path, 'w') as transcript_file:
            sys.stdout = transcript_file

            print_given_arguments(cmd_line_args, script_name, file_name, transcript_file_path, use_unit_clause_heuristic, given_statements)

            model, clauses = create_model_and_clauses(file_name, given_statements)
            DPLL(clauses, model, use_unit_clause_heuristic)

            sys.stdout = sys.__stdout__
            print(f'Transcript saved to: {transcript_file_path}')
    else:
        print_given_arguments(cmd_line_args, script_name, file_name, transcript_file_path, use_unit_clause_heuristic, given_statements)

        model, clauses = create_model_and_clauses(file_name, given_statements)
        DPLL(clauses, model, use_unit_clause_heuristic)
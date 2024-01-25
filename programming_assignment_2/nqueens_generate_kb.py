n = int(input('Enter N (number of queens): '))
print()


props = []
for i in range(1, n+1):
    for j in range(1, n+1):
        prop = f'Q{i}{j}'
        props.append(prop)

columns = []
for i in range(n):
    col = [f'Q{i+1}{j}' for j in range(1, n+1)]
    columns.append(col)

rows = []
for j in range(n):
    row = [f'Q{i+1}{j+1}' for i in range(n)]
    rows.append(row)

diagonals_list = []
for i in range(1, n+1):
    for j in range(1, n+1):
        diagonal = [f'Q{i}{j}']

        for r in range(1, n+1):
            for c in range(1, n+1):
                if f'Q{r}{c}' != f'Q{i}{j}' and (((r - i) == (c - j)) or ((r - i) == (j - c)) or ((i - r) == (j - c)) or ((i - r) == (c - j))):
                    diagonal.append(f'Q{r}{c}')

        diagonals_list.append(diagonal)

print(f'\nprops: {props}\n')
print(f'rows: {rows}\n')
print(f'columns: {columns}\n')
print(f'diagonals: {diagonals_list}')

print()
for i in range(5):
    print('#' * 300)
print()

# exactly 1 queen in each column
def generate_clauses_for_1_queen_in_each_column(columns):
    result = []
    for column in columns:
        for literal in column:
            s = f'(implies {literal} (and'
            for j in range(len(column)):
                if column[j] != literal:
                    s += f' (not {column[j]})'
            s += '))'
            result.append(s)
    return result

clauses_for_1_queen_in_each_column = generate_clauses_for_1_queen_in_each_column(columns)
print('\n~    ~    NO MORE THAN 1 QUEEN IN EACH COLUMN    ~    ~')
for index, clause in enumerate(clauses_for_1_queen_in_each_column):
    print(f'{clause}')

# exactly 1 queen in each row
# (implies Q11 (and (not Q21) (not Q31) (not Q41) (not Q51) (not Q61)))
def generate_clauses_for_1_queen_in_each_row(rows):
    result = []
    for row in rows:
        for literal in row:
            s = f'(implies {literal} (and'
            for j in range(len(row)):
                if row[j] != literal:
                    s += f' (not {row[j]})'
            s += '))'
            result.append(s)
    return result

clauses_for_1_queen_in_each_row = generate_clauses_for_1_queen_in_each_row(rows)
print('\n\n~    ~    NO MORE THAN 1 QUEEN IN EACH ROW    ~    ~')
for index, clause in enumerate(clauses_for_1_queen_in_each_row):
    print(f'{clause}')


# no queens in same diagonal
def generate_clauses_for_no_queens_in_same_diagonal(n, diagonals):
    result = []
    for diag_list in diagonals:
        statement = f'(implies {diag_list[0]} (and'
        for i in range(1, len(diag_list)):
            not_clause = f' (not {diag_list[i]})'
            statement += not_clause
        statement += '))'
        result.append(statement)
    return result

clauses_for_no_queens_in_same_diagonal = generate_clauses_for_no_queens_in_same_diagonal(n, diagonals_list)
print('\n\n~    ~    NO QUEENS IN SAME DIAGONAL    ~    ~')
for index, clause in enumerate(clauses_for_no_queens_in_same_diagonal):
    print(f'{clause}')

# AT LEAST 1 QUEEN IN EACH COLUMN
def generate_clauses_for_at_least_1_queen_in_each_column(n):
    result = []
    for i in range(1, n+1):
        s = '(or'
        for j in range(1, n+1):
            s += f' Q{i}{j}'
        s += ')'
        result.append(s)
    return result

print('\n\n~    ~    AT LEAST 1 QUEEN IN EACH COLUMN    ~    ~')
clauses_for_at_least_1_queen_in_each_column = generate_clauses_for_at_least_1_queen_in_each_column(n)
for index, clause in enumerate(clauses_for_at_least_1_queen_in_each_column):
    print(f'{clause}')

# AT LEAST 1 QUEEN IN EACH ROW
# (or Q11 Q21 Q31 Q41 Q51 Q61)
# (or Q12 Q22 Q32 Q42 Q52 Q62)
# ...
def generate_clauses_for_at_least_1_queen_in_each_row(n):
    result = []
    for i in range(1, n+1):
        s = '(or'
        for j in range(1, n+1):
            s += f' Q{j}{i}'
        s += ')'
        result.append(s)
    return result

print('\n\n~    ~    AT LEAST 1 QUEEN IN EACH ROW    ~    ~')
clauses_for_at_least_1_queen_in_each_row = generate_clauses_for_at_least_1_queen_in_each_row(n)
for index, clause in enumerate(clauses_for_at_least_1_queen_in_each_row):
    print(f'{clause}')
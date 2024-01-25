# Instructions and requirements for running this program:

# Expected Usage:
`python3 DPLL.py <filename>.cnf <literal>* [+UCH] [-t <path_to_transcript>.txt]`

# Example Usage:
- `python3 DPLL.py mapcolor.cnf`
- `python3 DPLL.py mapcolor.cnf -Q_Green`
- `python3 DPLL.py mapcolor.cnf Q_Green V_Blue`
- `python3 DPLL.py mapcolor.cnf Q_Green V_Blue +UCH`
- `python3 DPLL.py mapcolor.cnf Q_Green V_Blue +UCH -t transcripts/results_mapcolor3.UCH.txt`
- `python3 DPLL.py mapcolor.cnf Q_Green V_Blue -t transcripts/results_mapcolor3.txt`
- `python3 DPLL.py mapcolor.cnf -t transcripts/results_mapcolor3.txt`
# Required Arguments:
- filename - a .cnf file in DIMACS format representing the knowledge base 
- the .cnf files must be in the root directory

# Optional Arguments:
- literals: either `<varName>` or `-<varName>` to force a variable in the problem to have a True or False value, respectively (make sure the varName matches one from the KB)
- UCH: use the `+UCH` flag to force the DPLL algorithm to utilize the Unit Clause Heuristic while solving the problem (defaults to not using the UCH)
- -t <path_to_transcript>.txt: use the -t flag in combination with a path to a transcript.txt file to generate a transcript for your run. The transcript file path must be of the form `transcripts/results_mapcolor.txt`, that is you MUST specify a folder in which you are going to dump the transcript (see the example usages at the top)


# Problems
## Australia Map Coloring
Use DPLL to solve the problem of coloring a map using 3 colors such that no two bordering states share the same color. Variables are
Q_Blue, Q_Green, Q_Red, V_Blue, V_Green, V_Red, T_Blue, T_Green, T_Red, SA_Blue, SA_Green, SA_Red, WA_Blue, WA_Green, WA_Red, NT_Blue, NT_Green, NT_Red, NSW_Blue, NSW_Green, and NSW_Red.

## Sammy's Sport Shop
Use DPLL to solve the Sammy's Sport Shop problem. We have 3 boxes. Each box contains either Yellow Balls, White Balls, or Yellow and White (Both) Balls - there is exactly 1 box of each type. Each box has a single label displaying Yellow, White, or Both. All labels on the boxes are incorrect. We draw 1 ball from each box and observe its color, then use the facts we know to determine the true contents of the boxes. The variables are O1Y, O1W, O2Y, O2W, O3Y, O3W, L1Y, L1W, L1B, L2Y, L2W, L2B, L3Y, L3W, L3B, C1Y, C1W, C1B, C2Y, C2W, C2B, C3Y, C3W, and C3B where O means Observed, L means Labelled, and C means Contains.

## N-Queens
Use DPLL to solve the n-queens problem, where we must place n queens on an nxn chessboard such that no queen can attack each other. The variables are Q11 through Qnn, representing a Queen's position on the board being True (1), False (-1), or Unknown (0).

# UCH: Unit Clause Heuristic
In the context of DPLL (Davis-Putnam-Logemann-Loveland) algorithm, UCH (Unit Clause Heuristic) is a strategy that prioritizes unit clauses, which contain only one unassigned literal. The algorithm assigns truth values to these clauses first, simplifying the formula. UCH accelerates the search for a satisfying assignment by exploiting readily determined truth values, enhancing the efficiency of the overall SAT-solving process.




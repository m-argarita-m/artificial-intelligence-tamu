# Instructions and requirements for running this program:

# Example Usage:
`python3 blocksworld.py probB20 -h H3 -m 1000000`

# Required Arguments:
- filename (3rd argument)
- must be one of the .bwp files in the `probs` directory

# Optional Arguments:
- heuristic: indicated by `-h` flag: any out of `H0`, `H1`, `H2`, `H3`, `H4`, `H5`, `H6`
  - heuristic will default to `H6`, the heuristic that performed best on the given test cases.
- max_iters: indicated by `-m` flag: an integer of your choice
  - max_iters will default to 1,000,000

# Heuristics
In the section below I describe the approach behind a number of heuristic functions that I developed for this problem, as well as the effectiveness of each heuristic.
## ---H0---
### Overview:
This is the most basic heuristic that returns 0 for any state, resulting in the A* search functioning the same as BFS.
### Effectiveness:
This heuristic resulted in failures for the following test cases:
- B11
- B12
- B13
- B14
- B15
- B16
- B17
- B18
- B19
- B20
## ---H1---
### Overview:
This is the second most basic heuristic which simply counts the number of blocks that are in the wrong position for a given state.
### Effectiveness:
This heuristic resulted in failures for the following test cases:
- B14
- B15
- B16
- B17
- B19
- B20
## ---H2---
### Overview:
This is the first heuristic I wrote. I wanted to increase the calculated cost for a state depending on 3 conditions. 
1. If a block was in the wrong position, it would result a higher cost. 
2. If a block was in the wrong position AND it had blocks above it that needed to be moved first, it would result in a higher cost.
3. If a block was in the wrong position AND there were blocks covering its destination (or additional blocks needed to be placed in the destination stack before this block could be moved in), this would result in a higher cost.

I think this was not a bad approach, but I did not have time to mess around with my 'hyperparameters' that impacted the cost for each of the three conditions. In the end, this heuristic performed worse than some established heuristics that have been created for this problem.
### Effectiveness:
This heuristic resulted in failures for the following test cases:
- B13
- B14
- B17
- B19
## ---H3---
### Overview:
This heuristic calculates the Manhattan distance for each block between the current state and the goal state. The Manhattan distance is defined as the absolute value of the difference between x-coordinates from the current state to the goal state plus the absolute value of the difference between the y-coordinates from the current state to the goal state, where the x-coordinates for this problem are the stack indices and the y-coordinates are the heights of blocks.
### Effectiveness:
This heuristic resulted in failures for the following test cases:
- B16
- B19
## ---H4---
### Overview:
This heuristic calculates a score for a given state by determining if a block must be moved once, or if it must be moved at least twice.
### Effectiveness:
This heuristic resulted in failures for the following test cases:
- B13
- B14
- B15
- B16
- B17
- B18
- B19
- B20
## ---H5---
### Overview:
This heuristic is an extension (improvement?) of H2. There is an additional cost imposed for each block underneath the current block that is in the wrong position. 
### Effectiveness:
This heuristic resulted in failures for the following test cases:
- B13
- B14
- B15
- B16
- B17
- B18
- B19
- B20
## ---H6---
### Overview:
This heuristic calculates a score for every block and sums them together for the final heuristic score. For each block that is in the wrong position, we add max(1, stack_height - block_height) to the h_score. Blocks in the wrong position with many blocks above them end up with large scores, while blocks in the wrong position with no blocks above them receive scores of 1.
### Effectiveness:
This heuristic resulted in all the test cases passing.
# CSC-520-Assignment-2
Instructions to run code:

Run the command python3 og.py

Interesting little things I have learned from this program:

1. I had a problem where the program wouldn't stop runnning after generating the first move and returning its optimal move. This is because the algorithms are exploring evert possible move on a 4x4 board which 16 squares for teh first move, 15 for the next, 14 for the next, and so on so forth, which would take 16! positions. To fix this I added a depth and max_depth parameter to stop recursion after a certain number of moves, using max_depth as a cutoff.

2. The minimax and alpha beta pruning algorithm are somewhat similar, but the difference is that with alpha beta pruning, I had to think about pruning if the alpha value is greater than or equal to beta value. That's why there were less nodes explored in the alpha beta algorithm than the minmax algorithm. 

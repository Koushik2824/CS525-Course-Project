def generate_full_board_cnf(n):
    clauses = []
    var_count = 0

    # Define which cells have domino placements
    var_map = {}
    # Generate variables for horizontal and vertical dominoes
    for i in range(n):
        for j in range(n):
        	
        	var_map[(i, j, 'h')] = var_count
        	var_count += 1
        	var_map[(i, j, 'v')] = var_count
        	var_count += 1
    
    for i in var_map:
    	print(i)
	
    # Constraints: Each square must be covered by exactly one domino
    for i in range(n):
        for j in range(n):
        	if (i == 0 and j == 0) or (i == n-1 and j == n-1):
        		continue
        	# List of possible dominoes covering the current square (i, j)
        	covering_literals = []
        	# Horizontal domino covers (i, j) and (i, j+1)
        	covering_literals.append(var_map[(i, j, 'h')])
        	# Horizontal domino covering (i, j-1) and (i, j)
        	if j > 0: # and (i!=0 or j!=1):
        		covering_literals.append(var_map[(i, j - 1, 'h')])
        	# Vertical domino covers (i, j) and (i+1, j)
        	covering_literals.append(var_map[(i, j, 'v')])
        	# Vertical domino covering (i-1, j) and (i, j)
        	if i > 0: # and (i!=1 or j!=0):
        		covering_literals.append(var_map[(i - 1, j, 'v')])
        		
        	clauses.append(" ".join(map(str, covering_literals)) + " 0")
        	
        	# Pairwise exclusion to ensure it's covered by at most one domino
        	for a in range(len(covering_literals)):
        		for b in range(a + 1, len(covering_literals)):
        			clauses.append(f"-{covering_literals[a]} -{covering_literals[b]} 0")
    for a in range(n):
        clauses.append(f"-{var_map[(9,a,'v')]}")
        clauses.append(f"-{var_map[(a,9,'h')]}")
    clauses.append(f"-{var_map[(0,0,'v')]}")
    clauses.append(f"-{var_map[(0,0,'h')]}")
    # DIMACS CNF format header: p cnf <num_variables> <num_clauses>
    cnf = f"p cnf {var_count} {len(clauses)}\n"
    cnf += "\n".join(clauses)

    return cnf

# Generate CNF for a complete 10x10 board
n = 10
cnf_output = generate_full_board_cnf(n)

# Save the CNF to a file
with open("full_board_1.cnf", "w") as f:
    f.write(cnf_output)

print("CNF file 'full_board_1.cnf' generated successfully.")

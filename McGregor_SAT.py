'''
            .
            .
            .
    6       7       8
        2       3
...         1           ...
        4       5
    9       10      11
            .
            .
            .

    Variable ordering in Graph (above)
    Extend by:
    Extending to include color variables by changing vertex number vertex_num to 
    (vertex_num-1) * num_colors + 1 and color k by (vertex_num-1) * num_colors + k

    Sinz's constraints: 
    Count constraint r to be put on color 1.

    Tree type constraints: (Bailleaux and Boufkhad)
    Count constraint r to be put on color 1.
'''
from random import randint,sample

def generate_McGregor_graph_aux(order: int) -> list:
    '''
        Auxiliary method which generates the recursive base of the graph\n
        Returns outer vertices (vertices at the boundary) and all edges built 
    '''
    if order == 1:
        return [[1],[]]
    G = generate_McGregor_graph_aux(order-1)
    current_outer_vertices = G[0]
    len_current_outer_vertices = len(G[0])
    current_edge_set = G[1]
    current_largest_outer_vertex = max(current_outer_vertices)
    new_outer_vertices = [(current_largest_outer_vertex + i) for i in range(1,2*order+1)]
    len_new_outer_vertex = len(new_outer_vertices)
    iter_var = 0
    executed = False
    for j in range(len_current_outer_vertices//2):
        current_edge_set.append([current_outer_vertices[j],new_outer_vertices[iter_var]])
        current_edge_set.append([current_outer_vertices[j],new_outer_vertices[iter_var+1]])
        iter_var = iter_var + 1
        executed = True
    if executed:
        iter_var = iter_var + 1 
    for j in range(len_current_outer_vertices//2,len_current_outer_vertices):
        current_edge_set.append([current_outer_vertices[j],new_outer_vertices[iter_var]])
        current_edge_set.append([current_outer_vertices[j],new_outer_vertices[iter_var+1]])
        iter_var = iter_var + 1
    for i in range(len_new_outer_vertex//2-1):
        current_edge_set.append([new_outer_vertices[i],new_outer_vertices[i+1]])
        current_edge_set.append([new_outer_vertices[i+(len_new_outer_vertex//2)],new_outer_vertices[i+(len_new_outer_vertex//2)+1]])
    current_edge_set.append([new_outer_vertices[0],new_outer_vertices[(len_new_outer_vertex//2)]])
    current_edge_set.append([new_outer_vertices[-1],new_outer_vertices[(len_new_outer_vertex//2)-1]])
    current_edge_set.append([new_outer_vertices[(len_new_outer_vertex//2)], current_outer_vertices[0]])
    current_edge_set.append([new_outer_vertices[-1], current_outer_vertices[len_current_outer_vertices//2 -1]])
    return [new_outer_vertices,current_edge_set]

def generate_McGregor_graph(order: int) -> list:
    '''
        Method which generates the recursive base of the graph
        and adds the final closing edges\n
        Returns outer vertices (vertices at the boundary) and all edges built 
    '''
    G = generate_McGregor_graph_aux(order)
    outer_vertices = G[0]
    len_outer_vertices = len(outer_vertices)
    edge_set = G[1]
    min_outer_vertex = min(outer_vertices)
    max_outer_vertex = max(outer_vertices)
    last_vertex = max_outer_vertex + 1
    for i in range(len_outer_vertices//2-1):
        edge_set.append([max_outer_vertex,outer_vertices[i]])
    for i in range(1,len_outer_vertices//4+1):
        edge_set.append([min_outer_vertex,outer_vertices[i+len_outer_vertices//2]])
    for i in range(len_outer_vertices//4):
        edge_set.append([last_vertex,outer_vertices[-i-1]])
    edge_set.append([last_vertex,min_outer_vertex])
    outer_vertices.append(last_vertex)
    return [outer_vertices,edge_set]

def generate_McGregor_SAT_aux(order: int, colors: int) -> list:
    '''
        Auxiliary method to generate the graph and extend the variables for colors
    '''
    G = generate_McGregor_graph(order)
    # print(G)
    last_outer_vertex = max(G[0])
    edge_set = G[1]
    clauses = []
    number_of_variables = colors*last_outer_vertex
    for vertex in range(1,last_outer_vertex+1):
        start = (vertex-1)*colors
        clause = []
        for vertex_color_var in range(1,colors+1):
            clause.append(f"{start+vertex_color_var}")
        clause.append("0")
        clauses.append(' '.join(clause))
    for edge in edge_set:
        for color in range(1,colors+1):
            clauses.append(f"-{(edge[0]-1)*colors + color} -{(edge[1]-1)*colors + color} 0")
    return [number_of_variables,clauses]

def generate_McGregor_SAT(order:int = 10,colors:int = 4) -> None:
    '''
        Method to output the SAT encoding of McGregor's graph of order (default 10) and colors 
        (default 4) in a file.
    '''
    number_of_variables, clauses = generate_McGregor_SAT_aux(order,colors)
    number_of_clauses = len(clauses)
    cnf = f"p cnf {number_of_variables} {number_of_clauses}\n"
    cnf += "\n".join(clauses)
    filename = f"Naive_Encoding_McGregor_{order}.cnf"
    with open(filename,"w") as file:
        file.write(cnf)

# ''' @todo later '''
# def generate_Naive_SAT(reqMcGregor:bool = True,reqInf:list = [10,4]) -> None:
#     if reqMcGregor:
#         generate_McGregor_SAT(reqInf[0],reqInf[1])

def generate_McGregor_SAT_Sinz(order: int = 10, colors: int = 4, constraint: int = 7) -> None:
    ''' Sinz's constraint to limit the number of one color to @constraint on 
        coloring McGregor's graph of order @order with @colors colors '''
    number_of_var, clauses = generate_McGregor_SAT_aux(order,colors)
    base_count = number_of_var
    vertex_count = number_of_var//colors
    for j in range(1,vertex_count-constraint+1):
        if j != vertex_count-constraint:
            for k in range(1,constraint+1):
                subexp = base_count + (j-1)*constraint + k
                clauses.append(f"-{subexp} {subexp+constraint} 0")
        for k in range(constraint+1):
            subexp = base_count + (j-1)*constraint + k
            if k == 0:
                clauses.append(f"-{(j+k-1)*colors + 1} {subexp+1} 0")
            elif k == constraint:
                clauses.append(f"-{(j+k-1)*colors + 1} -{subexp} 0")
            else:
                clauses.append(f"-{(j+k-1)*colors + 1} -{subexp} {subexp+1} 0")
    cnf = f"p cnf {number_of_var + (vertex_count - constraint)*constraint} {len(clauses)}\n"
    cnf += '\n'.join(clauses)
    filename = f"Sinz_Encoding_McGregor_{order}.cnf"
    with open(filename,"w") as file:
        file.write(cnf)

def generate_McGregor_SAT_Tree_method(order:int = 10, colors:int = 4, constraint:int = 7) -> None:
    ''' Tree type constraints: (Bailleaux and Boufkhad) '''
    number_of_var,clauses = generate_McGregor_SAT_aux(order=order,colors=colors)
    base_count = number_of_var
    vertex_count = number_of_var//colors
    leaf_count_in_subtree = [0 for _ in range(2*vertex_count)]
    for i in range(vertex_count,2*vertex_count):
        leaf_count_in_subtree[i] = 1
    for i in range(vertex_count-1,0,-1):
        leaf_count_in_subtree[i] = min(constraint,leaf_count_in_subtree[2*i] + leaf_count_in_subtree[2*i + 1])
    new_vars = [[],[]]
    for i in range(2,len(leaf_count_in_subtree)):
        new_var = [0]
        if leaf_count_in_subtree[i] == 1:
            new_var.append((i-vertex_count)*colors + 1)
        else:
            for j in range(leaf_count_in_subtree[i]):
                base_count = base_count + 1
                new_var.append(base_count)
        new_vars.append(new_var)
    for k in range(2,vertex_count):
        for i in range(leaf_count_in_subtree[2*k] + 1):
            for j in range(leaf_count_in_subtree[2*k + 1] + 1):
                if (i+j) >= 1 and (i+j) <= leaf_count_in_subtree[k]+1:
                    included_literal = -new_vars[2*k][i] 
                    included_literal1= -new_vars[2*k + 1][j] 
                    included_literal2= new_vars[k][i+j] if (i+j) < constraint+1 else 0
                    if included_literal == 0 and included_literal1 == 0 and included_literal2 == 0:
                        continue
                    clause = ''
                    if included_literal != 0:
                        clause += str(included_literal) + ' '
                    if included_literal1 != 0:
                        clause += str(included_literal1) + ' '
                    if included_literal2 != 0:
                        clause += str(included_literal2) + ' '
                    clause += '0'
                    clauses.append(clause)
    for i in range(leaf_count_in_subtree[2]+1):
        for j in range(leaf_count_in_subtree[3]+1):
            if i+j == constraint+1:
                included_literal = -new_vars[2][i]
                included_literal1 = -new_vars[3][j]
                if included_literal == 0 and included_literal1 == 0:
                    continue
                clause = ''
                if included_literal != 0:
                    clause += str(included_literal) + ' '
                if included_literal1 != 0:
                    clause += str(included_literal1) + ' '
                clause += '0'
                clauses.append(clause)
    cnf = f"p cnf {base_count} {len(clauses)}\n"
    cnf += '\n'.join(clauses)
    filename=f"Tree_Encoding_McGregor_{order}.cnf"
    with open(filename,"w") as file:
        file.write(cnf)

def generate_random_graph(vertex_count_upper_limit: int = 1000,
                          vertex_count_lower_limit: int = 10) -> list:
    assert vertex_count_lower_limit > 1, 'Lower limit invalid. [2,...] is valid.'
    assert vertex_count_upper_limit >= vertex_count_lower_limit, '''Upper limit invalid. 
    Upper limit should be >= Lower limit.'''
    vertex_cnt = randint(vertex_count_lower_limit,vertex_count_upper_limit)
    edge_list = []
    number_of_edges = randint(vertex_cnt-1,(vertex_cnt*(vertex_cnt-1))//2)
    for _ in range(number_of_edges):
        edge = sample(range(1,vertex_cnt+1),2)
        while edge_list.count(edge) > 0 or edge_list.count(list(reversed(edge))) > 0:
            edge = sample(range(1,vertex_cnt+1),2)
        edge_list.append(edge)
    print(edge_list)
    return [vertex_cnt,edge_list]

def generate_random_graph_SAT(vertex_count_upper_limit: int = 1000,
                              vertex_count_lower_limit: int = 10,
                              colors:int = 4,
                              index:int = 1) -> None:
    G = generate_random_graph(vertex_count_upper_limit=vertex_count_upper_limit,
                              vertex_count_lower_limit=vertex_count_lower_limit)
    vertex_count = G[0]
    edges = G[1]
    clauses = []
    number_of_variables = colors*vertex_count
    for vertex in range(1,vertex_count+1):
        start = (vertex-1)*colors
        clause = []
        for vertex_color_var in range(1,colors+1):
            clause.append(f"{start+vertex_color_var}")
        clause.append("0")
        clauses.append(' '.join(clause))
    for edge in edges:
        for color in range(1,colors+1):
            clauses.append(f"-{(edge[0]-1)*colors + color} -{(edge[1]-1)*colors + color} 0")
    cnf = f"p cnf {number_of_variables} {len(clauses)}\n"
    cnf += '\n'.join(clauses)
    filename=f"Naive_Encoding_Random_{index}.cnf"
    with open(filename,'w') as file:
        file.write(cnf)

if __name__ == "__main__":
    for order in range(10,101,10):
        generate_McGregor_SAT(order=order, colors=4)
    #generate_McGregor_SAT_Sinz(order=order,colors=4,constraint=7)
    #generate_McGregor_SAT_Tree_method(order=order,colors=4,constraint=7)
    #generate_random_graph_SAT(vertex_count_upper_limit=upper, vertex_count_lower_limit=lower, colors=4,index=i)

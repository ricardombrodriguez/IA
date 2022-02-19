from tree_search import *
from cidades import *

class MyNode(SearchNode):

    def __init__(self,state,parent,cost,heuristic,eval):
        super().__init__(state,parent)
        self.cost = cost
        self.heuristic = heuristic
        self.eval = eval

class MyTree(SearchTree):

    def __init__(self,problem, strategy='breadth',seed=0): 

        super().__init__(problem,strategy,seed)
        self.root = MyNode(problem.initial,None,0,self.problem.domain.heuristic(problem.initial,problem.goal),None)
        self.all_nodes = [self.root]
        self.solution_tree = None
        self.added_states = {}
        self.added_states[problem.initial] = self.root
        self.used_shortcuts = []

    def astar_add_to_open(self,lnewnodes):

        self.open_nodes.extend(lnewnodes)
        self.open_nodes.sort(key=lambda id: self.all_nodes[id].heuristic + self.all_nodes[id].cost)


    def propagate_eval_upwards(self,node):
        
        if node.parent is None:
            return
        parent_children = [child for child in self.all_nodes if node.parent == child.parent]
        self.all_nodes[node.parent].eval = min(parent_children, key=lambda child: child.eval).eval
        return self.propagate_eval_upwards(self.all_nodes[node.parent])


    def search2(self,atmostonce=False):

        while self.open_nodes != []:

            nodeID = self.open_nodes.pop(0)
            node = self.all_nodes[nodeID]
            if self.problem.goal_test(node.state):
                self.solution = node
                self.terminals = len(self.open_nodes)+1
                self.path = self.get_path(node)
                return self.path

            lnewnodes = []
            self.non_terminals += 1

            for a in self.problem.domain.actions(node.state):
                newstate = self.problem.domain.result(node.state,a)
                newnode_cost = node.cost+self.problem.domain.cost(node.state,a)
                newnode_heuristic = self.problem.domain.heuristic(newstate,self.problem.goal)
                newnode_eval = newnode_heuristic + newnode_cost
                newnode = MyNode(newstate,nodeID,newnode_cost,newnode_heuristic,newnode_eval)
                if atmostonce:
                    if newstate not in self.added_states.keys():
                        self.added_states[newstate] = newnode
                        self.all_nodes.append(newnode)
                        lnewnodes.append(len(self.all_nodes)-1)
                    else:
                        othernode = self.added_states[newstate]
                        if newnode.cost < othernode.cost:
                            self.added_states[newstate] = newnode
                            for id in self.open_nodes:
                                if self.all_nodes[id] == othernode:
                                    self.open_nodes.remove(id)
                                    break
                            self.all_nodes.append(newnode)
                            lnewnodes.append(len(self.all_nodes)-1)
                else:
                    if newstate not in self.get_path(node):
                        self.all_nodes.append(newnode)
                        self.propagate_eval_upwards(newnode)
                        lnewnodes.append(len(self.all_nodes)-1)

            self.add_to_open(lnewnodes)

        return None

    def repeated_random_depth(self,numattempts=3,atmostonce=False):

        trees = []
        for attempt in range(0,numattempts):
            t = MyTree(self.problem,'rand_depth',attempt)
            t.search2()
            trees.append(t)
        self.solution_tree = min(trees, key=lambda tree: tree.solution.cost)
        return self.solution_tree.path

    def make_shortcuts(self):

        shortcut_path = self.path[:]
        for i in range(0,len(shortcut_path)-2):
            for j in range(len(shortcut_path)-1,i+1,-1):
                city_actions = self.problem.domain.actions(shortcut_path[i])
                if (shortcut_path[i],shortcut_path[j]) in city_actions or (shortcut_path[j],shortcut_path[i]) in city_actions:
                    self.used_shortcuts.append((shortcut_path[i],shortcut_path[j]))
                    for k in range(i+1,j):
                        shortcut_path.pop(k)
                    break
        return shortcut_path



class MyCities(Cidades):

    def maximum_tree_size(self,depth):   # assuming there is no loop prevention

        num_actions = 0
        for city in self.coordinates.keys():
            num_actions += len(self.actions(city))
        avg_branching_factor = num_actions / len(self.coordinates.keys())
        max_tree_size = (avg_branching_factor**(depth+1)-1) / (avg_branching_factor-1)
        return max_tree_size



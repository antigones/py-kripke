import networkx as nx
from sympy import *
from sympy.logic.boolalg import BooleanFunction

class L(BooleanFunction):
    """ L, necessarily """
    @classmethod
    def eval(cls, arg):
        return None

class M(BooleanFunction):
    """ M, possibly """
    @classmethod
    def eval(cls, arg):
        return None

p, q = symbols('p,q')

G = nx.DiGraph()

content_1 = {p: False, q: False}
content_2 = {p: True, q: True}
content_3 = {p: True, q: False}

# every node is a world with its own set of literals and interpretations
G.add_nodes_from([(1, content_1), (2, content_2),(3, content_3)])

G.add_edge(1, 1)
G.add_edge(1, 2)
G.add_edge(1, 3)

G.add_edge(2, 2)
G.add_edge(2, 3)

G.add_edge(3, 1)

def eval_formula(G, world, formula):

    if isinstance(formula, And):
        return all(eval_formula(G, world, arg) for arg in formula.args)

    if isinstance(formula, Or):
        return any(eval_formula(G, world, arg) for arg in formula.args)

    if isinstance(formula, Not):
        return not eval_formula(G, world, formula.args[0])
 
    if isinstance(formula, Implies):
        A, B = formula.args
        return (not eval_formula(G, world, A)) or eval_formula(G, world, B)

    if isinstance(formula, M):
        arg = formula.args[0]
        return any(eval_formula(G, succ, arg) for succ in G.successors(world))

    if isinstance(formula, L):
        arg = formula.args[0]
        succs = list(G.successors(world))
        if not succs:
            return True  # "by design"
        return all(eval_formula(G, succ, arg) for succ in succs)

    return formula.subs(G.nodes[world])

import networkx as nx
import pytest
from sympy import And, Implies, Or, symbols, Not

from main import L, M, eval_formula


p, q = symbols('p,q')

def build_frame():
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
    return G

@pytest.fixture
def setup_env():
    G = build_frame()
    yield G


@pytest.mark.parametrize(
    "w, formula, expected",
    [
        (1, L(p), False),
        (2, L(p), True),
        (3, L(p), False),

        (1, L(q), False),
        (2, L(q), False),
        (3, L(q), False),

        (1, M(p), True),
        (2, M(p), True),
        (3, M(p), False),

        (1, M(q), True),
        (2, M(q), True),
        (3, M(q), False),

        (1, L(~p), False),
        (2, L(~p), False),
        (3, L(~p), True),

        (1, L(Or(p, q)), False),
        (2, L(Or(p, q)), True),
        (3, L(Or(p, q)), False),

        (1, M(And(p, q)), True),
        (2, M(And(p, q)), True),
        (3, M(And(p, q)), False),

        (1, L(Implies(p, q)), False),
        (2, L(Implies(p, q)), False),
        (3, L(Implies(p, q)), True),

        (1, M(M(p)), True),
        (2, M(M(p)), True),
        (3, M(M(p)), True),

        (1, Implies(L(p), M(q)), True),
        (2, Implies(L(p), M(q)), True),
        (3, Implies(L(p), M(q)), True),
    ]
)
def test_evaluate_formula(setup_env, w, formula, expected):
    G = setup_env
    assert eval_formula(G, w, formula) == expected

 
"""Tests for sparsity"""


from tspwplib import (
    ProfitsProblem,
    is_complete_with_self_loops,
    build_path_to_oplib_instance,
)


def test_remove_random_edges_from_graph(
    oplib_root, generation, graph_name, edge_removal_probability
):
    """Test the right number of edges are removed"""
    filepath = build_path_to_oplib_instance(oplib_root, generation, graph_name)
    problem = ProfitsProblem.load(
        filepath, edge_removal_probability=edge_removal_probability, seed=5
    )
    complete_problem = ProfitsProblem.load(filepath)
    complete_graph = complete_problem.get_graph()
    smaller_graph = problem.get_graph()
    assert problem.edge_removal_probability == edge_removal_probability

    # edge cases
    if edge_removal_probability == 0:
        assert smaller_graph.number_of_edges() == complete_graph.number_of_edges()
    elif edge_removal_probability == 1.0:
        assert smaller_graph.number_of_edges() == smaller_graph.number_of_nodes()
    # sufficient number of nodes for randomness to not have big effect
    elif smaller_graph.number_of_nodes() > 50:
        assert not is_complete_with_self_loops(smaller_graph)
        num_edges_not_self_loops = (
            complete_graph.number_of_edges() - complete_graph.number_of_nodes()
        )
        num_edges_lower_bound = float(num_edges_not_self_loops) * (
            1.0 - edge_removal_probability - 0.1
        )
        num_edges_upper_bound = float(num_edges_not_self_loops) * (
            1.0 - edge_removal_probability + 0.1
        )
        assert (
            num_edges_lower_bound
            <= smaller_graph.number_of_edges() - smaller_graph.number_of_nodes()
            <= num_edges_upper_bound
        )

import matplotlib.pyplot as plt
import networkx as nx

def draw_probability_tree():
    # Create a directed graph
    G = nx.DiGraph()

    # Define nodes and edges
    nodes = ["Root", "Niveau1A", "Niveau1B", "Niveau1C", "Niveau2A", "Niveau2B", "Niveau2C"]
    edges = [("Root", "Niveau1A"), ("Root", "Niveau1B"), ("Root", "Niveau1C"),
             ("Niveau1A", "Niveau2A"), ("Niveau1B", "Niveau2B"), ("Niveau1C", "Niveau2C")]

    # Add nodes and edges to the graph
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    # Define positions for the nodes
    pos = {"Root": (0, 0), "Niveau1A": (-1, -1), "Niveau1B": (0, -1), "Niveau1C": (1, -1),
           "Niveau2A": (-1, -2), "Niveau2B": (0, -2), "Niveau2C": (1, -2)}

    # Draw nodes and edges
    nx.draw(G, pos, with_labels=True, node_size=700, node_color="skyblue", font_size=8, font_color="black", font_weight="bold", arrowsize=20)

    # Display the plot
    plt.show()

# Call the function to draw the probability tree
draw_probability_tree()

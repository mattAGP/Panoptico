import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Create a directed graph (to show influence direction)
G = nx.DiGraph()

# List of individuals and their roles based on the document (page 135 and additional information)
people = {
    "Liz Patricia Benavides Vargas": "Fiscal de la Nación",
    "Jaime Javier Villanueva Barreto": "Asesor",
    "Miguel Ángel Girao Isidro": "Asesor",
    "Abel Conrado Hurtado Espinoza": "Asesor",
    "Enma Benavides Vargas": "Jueza Superior",
    "Bersabeth Felicitas Revilla Corrales": "Ex Fiscal Suprema Provisional",
    "Juan Carlos Checkley Soria": "Juez Supremo",
    "Helder Uriel Terán Dianderas": "Fiscal Supremo Provisional",
    "Azucena Petronila Solari Labán": "Fiscal (removida)",
    "Eduardo Pachas Roy Gates": "Abogado"
}

# Add nodes with attributes for different types of actors
for person, role in people.items():
    G.add_node(person, role=role)

# Add edges with labels to represent relationships and actions
G.add_edge("Liz Patricia Benavides Vargas", "Jaime Javier Villanueva Barreto", label="asesor")
G.add_edge("Liz Patricia Benavides Vargas", "Miguel Ángel Girao Isidro", label="asesor")
G.add_edge("Liz Patricia Benavides Vargas", "Abel Conrado Hurtado Espinoza", label="asesor")
G.add_edge("Liz Patricia Benavides Vargas", "Enma Benavides Vargas", label="hermana")
G.add_edge("Liz Patricia Benavides Vargas", "Bersabeth Felicitas Revilla Corrales", label="destituyó")
G.add_edge("Liz Patricia Benavides Vargas", "Helder Uriel Terán Dianderas", label="nombró")
G.add_edge("Liz Patricia Benavides Vargas", "Azucena Petronila Solari Labán", label="destituyó")
G.add_edge("Bersabeth Felicitas Revilla Corrales", "Enma Benavides Vargas", label="investigó")
G.add_edge("Juan Carlos Checkley Soria", "Enma Benavides Vargas", label="juez en el caso")
G.add_edge("Helder Uriel Terán Dianderas", "Enma Benavides Vargas", label="investigó")
G.add_edge("Eduardo Pachas Roy Gates", "Enma Benavides Vargas", label="defendió")

# Set larger figure size
plt.figure(figsize=(10, 10))  # Increased size for better readability

# Create a spider web layout
root_node = "Liz Patricia Benavides Vargas"
other_nodes = list(set(G.nodes()) - {root_node})
num_nodes = len(other_nodes)
radius = 5
angles = np.linspace(0, 2*np.pi, num_nodes, endpoint=False)

pos = {root_node: (0, 0)}
for i, node in enumerate(other_nodes):
    x = radius * np.cos(angles[i])
    y = radius * np.sin(angles[i])
    pos[node] = (x, y)

# Node colors and shapes based on role
node_colors = {
    "Fiscal de la Nación": "lightblue",
    "Jueza Superior": "lightblue",
    "Ex Fiscal Suprema Provisional": "lightblue",
    "Fiscal Supremo Provisional": "lightblue",
    "Juez Supremo": "lightgreen",
    "Asesor": "yellow",
    "Abogado": "orange",
    "Institución": "gray"
}

node_shapes = {
    "Fiscal de la Nación": "s",
    "Jueza Superior": "s",
    "Ex Fiscal Suprema Provisional": "s",
    "Fiscal Supremo Provisional": "s",
    "Juez Supremo": "o",
    "Asesor": "^",
    "Abogado": "v",
    "Institución": "8"
}

# Draw nodes with custom colors and shapes
for node in G.nodes():
    nx.draw_networkx_nodes(G, pos, nodelist=[node], node_color=node_colors.get(G.nodes[node].get('role'), 'gray'), node_shape=node_shapes.get(G.nodes[node].get('role'), 'o'), node_size=300)

# Draw edges with labels and curved arrows
edge_labels = {(u, v): d['label'] for u, v, d in G.edges(data=True)}
curved_edges = [edge for edge in G.edges() if edge[0] != root_node]
straight_edges = [edge for edge in G.edges() if edge[0] == root_node]

nx.draw_networkx_edges(G, pos, edgelist=straight_edges, arrows=True, arrowsize=20)
arc_rad = 0.25
nx.draw_networkx_edges(G, pos, edgelist=curved_edges, arrows=True, arrowsize=20, connectionstyle=f'arc3, rad={arc_rad}')

# Draw edge labels
edge_label_pos = {}
for (u, v), label in edge_labels.items():
    if u == root_node:
        edge_label_pos[(u, v)] = ((pos[u][0] + pos[v][0])/2, (pos[u][1] + pos[v][1])/2)
    else:
        # Calculate the position for curved edge labels
        w = 1 - arc_rad
        edge_label_pos[(u, v)] = (
            w * pos[u][0] + (1-w) * pos[v][0],
            w * pos[u][1] + (1-w) * pos[v][1]
        )

nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, bbox=dict(facecolor='white', alpha=0.7), label_pos=0.5)

# Draw node labels
nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold', font_color="blue")

# Add legend
legend_elements = [
    plt.Line2D([0], [0], marker='s', color='w', label='Fiscal', markerfacecolor='lightblue', markersize=10),
    plt.Line2D([0], [0], marker='o', color='w', label='Juez', markerfacecolor='lightgreen', markersize=10),
    plt.Line2D([0], [0], marker='^', color='w', label='Asesor', markerfacecolor='yellow', markersize=10),
    plt.Line2D([0], [0], marker='v', color='w', label='Abogado', markerfacecolor='orange', markersize=10),
    plt.Line2D([0], [0], marker='8', color='w', label='Institución', markerfacecolor='gray', markersize=10),
]
plt.legend(handles=legend_elements, loc='upper right')

# Show the plot with adjusted title
plt.title("Red de personas involucradas en presuntos actos de corrupción (4.1 HECHO 1)", fontsize=16)
plt.axis("off")  # Turn off axis for cleaner look
plt.tight_layout()
plt.show()

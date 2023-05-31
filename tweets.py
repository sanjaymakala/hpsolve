import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

# Read CSV file
df = pd.read_csv(r'C:\Users\MY PC\IdeaProjects\tweets.py\twitter_data.csv')

# Create an empty knowledge graph
graph = nx.DiGraph()

# Iterate over the rows of the DataFrame
for index, row in df.iterrows():
    user = row['user']
    model = row['model']
    sentiment = row['sentiment']

    # Add user node if it doesn't exist
    if not graph.has_node(user):
        graph.add_node(user, type='user')

    # Add model node if it doesn't exist
    if not graph.has_node(model):
        graph.add_node(model, type='model')

    # Add sentiment edge from user to model
    graph.add_edge(user, model, sentiment=sentiment)

# Set the positions of the nodes using different layouts
user_pos = nx.spring_layout(graph, seed=42, k=0.15, iterations=50)
model_pos = nx.circular_layout(graph, scale=0.8)

# Set node colors and sizes based on types
node_colors = {'user': 'lightblue', 'model': 'lightgreen'}
node_sizes = {'user': 500, 'model': 800}

# Create separate lists of nodes and labels for users and models
user_nodes = [node for node, attr in graph.nodes(data=True) if attr['type'] == 'user']
user_labels = {node: node for node in user_nodes}
model_nodes = [node for node, attr in graph.nodes(data=True) if attr['type'] == 'model']
model_labels = {node: node for node in model_nodes}


# Visualize the knowledge graph
def draw_graph():
    plt.figure(figsize=(10, 6))
    nx.draw_networkx_nodes(graph, user_pos, nodelist=user_nodes, node_color=node_colors['user'], node_size=node_sizes['user'], alpha=0.9)
    nx.draw_networkx_nodes(graph, model_pos, nodelist=model_nodes, node_color=node_colors['model'], node_size=node_sizes['model'], alpha=0.9)
    nx.draw_networkx_edges(graph, user_pos, alpha=0.7)
    nx.draw_networkx_labels(graph, user_pos, labels=user_labels, font_size=10, font_color='black')
    nx.draw_networkx_labels(graph, model_pos, labels=model_labels, font_size=10, font_color='black')
    edge_labels = nx.get_edge_attributes(graph, 'sentiment')
    nx.draw_networkx_edge_labels(graph, user_pos, edge_labels=edge_labels, font_size=8)
    plt.title("Knowledge Graph")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

# Query the knowledge graph




# Read data from the CSV file


# Create an empty knowledge graph


# Build the knowledge graph
for _, row in df.iterrows():
    user = row['user']
    model = row['model']

    sentiment = row['sentiment']


    # Add user and model nodes to the graph
    graph.add_node(user, node_type='user')
    graph.add_node(model, node_type='model')

    # Add sentiment as an edge with complaint details as an attribute

    # Add feature node and connect it to the model


# Interactive loop for querying the knowledge graph
while True:
    query = input("Enter your query (e.g., 'complaints about hp laptop'): ")
    if query.lower() == 'exit':
        break

    keywords = query.lower().split()
    results = []

    # Traverse the knowledge graph based on query keywords
    for node in graph.nodes:
        if isinstance(node, str) and all(keyword in node.lower() for keyword in keywords):
            results.append(node)

    # Print the retrieved information
    if results:
        for result in results:
            print(f"Node: {result}")
            for neighbor in graph.neighbors(result):
                relationship = graph.edges[result, neighbor]['relationship']
                complaint = graph.edges[result, neighbor]['complaint']
                print(f"Connected to: {neighbor} | Relationship: {relationship} | Complaint: {complaint}")
            print()
    else:
        print("No matching results found.")
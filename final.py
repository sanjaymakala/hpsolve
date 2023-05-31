import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv('twitter_data.csv')

# Create a directed graph
graph = nx.DiGraph()

# Add nodes and edges to the graph
for _, row in df.iterrows():
    user = row['user']
    model = row['model']
    sentiment = row['sentiment']

    graph.add_node(user)
    graph.add_node(model)
    graph.add_edge(user, model, sentiment=sentiment)

# Visualize the graph
pos = nx.spring_layout(graph, seed=42)
plt.figure(figsize=(10, 8))
nx.draw_networkx(graph, pos, with_labels=True, node_color='lightblue', node_size=800, font_size=10, font_weight='bold', edge_color='gray', alpha=0.7)
edge_labels = nx.get_edge_attributes(graph, 'sentiment')
nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=8)
plt.title("Knowledge Graph")
plt.axis('off')
plt.tight_layout()
plt.show()

# Interactive loop for querying the knowledge graph
while True:
    print("Enter a node to query (or 'exit' to quit):")
    query = input("> ")

    if query == "exit":
        break

    if query in graph:
        related_nodes = [n for n in graph.neighbors(query)]
        print(f"The node '{query}' is connected to the following nodes:")
        for node in related_nodes:
            sentiment = graph[query][node]['sentiment']
            print(f"- {node} (Sentiment: {sentiment})")
            if sentiment == "COMPLAINT":
                print(f"   - {query} complains about {node}")
            elif sentiment == "APPRECIATION":
                print(f"   - {query} appreciates {node}")
    else:
        print(f"The node '{query}' does not exist in the graph.")

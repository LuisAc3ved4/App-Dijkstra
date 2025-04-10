from flask import Flask, request, jsonify, render_template
from dijkstra import dijkstra
import networkx as nx
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dijkstra', methods=['POST'])
def run_dijkstra():
    data = request.get_json()
    graph = data['graph']
    start = data['start']
    end = data['end']

    # Asegurarse de convertir los pesos a enteros
    formatted_graph = {
        node: [(neighbor, int(weight)) for neighbor, weight in edges]
        for node, edges in graph.items()
    }

    distances, previous, visited = dijkstra(formatted_graph, start)

    # Reconstruir camino más corto
    path = []
    node = end
    while node:
        path.insert(0, node)
        node = previous[node]

    draw_graph(formatted_graph, path, visited)

    return jsonify({
        'distances': distances,
        'path': path,
        'visited_order': visited,
        'image': '/static/graph.png'
    })

def draw_graph(graph, path, visited_order):
    G = nx.DiGraph()
    for node in graph:
        for neighbor, weight in graph[node]:
            G.add_edge(node, neighbor, weight=weight)

    pos = nx.spring_layout(G)
    edge_labels = nx.get_edge_attributes(G, 'weight')

    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=700, font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    if path:
        edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color='red', width=2)

    plt.title("Dijkstra - Camino más corto")
    plt.savefig('static/graph.png')
    plt.close()

if __name__ == '__main__':
    if not os.path.exists('static'):
        os.makedirs('static')
    app.run(debug=True)

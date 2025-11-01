"""Graph classes implementing traversable digraph and DAG with cycle detection."""

from collections import deque

class SortableDigraph:
    """Base class providing basic graph structure and topological sort"""
    def __init__(self):
        self.adj = {}  # adjacency list
        self.node_data = {}  # store node data
        self.edge_weights = {}  # store edge weights

    def add_node(self, node, data=None):
        """Add a node to the graph"""
        if node not in self.adj:
            self.adj[node] = []
            self.node_data[node] = data

    def add_edge(self, u, v, edge_weight=None):
        """Add an edge from u to v"""
        self.add_node(u)
        self.add_node(v)
        self.adj[u].append(v)
        self.edge_weights[(u, v)] = edge_weight

    def get_node_value(self, node):
        """Get the data associated with a node"""
        return self.node_data.get(node)

    def get_edge_weight(self, u, v):
        """Get the weight of an edge"""
        return self.edge_weights.get((u, v))

    def topsort(self):
        """Topological sort"""
        visited = set()
        result = []

        def visit(node):
            if node in visited:
                return
            visited.add(node)
            for neighbor in self.adj.get(node, []):
                visit(neighbor)
            result.append(node)

        for node in list(self.adj.keys()):
            visit(node)

        return result[::-1]

    def top_sort(self):
        """Alias for topsort to match test requirements"""
        return self.topsort()

    def successors(self, node):
        """Get all successors of a node"""
        return self.adj.get(node, []).copy()

    def predecessors(self, node):
        """Get all predecessors of a node"""
        preds = []
        for u, neighbors in self.adj.items():
            if node in neighbors:
                preds.append(u)
        return preds

    def get_nodes(self):
        """Get all nodes in the graph"""
        return list(self.adj.keys())


class TraversableDigraph(SortableDigraph):
    """Graph with traversal methods"""

    def dfs(self, start=None, visited=None):
        """Depth-first search traversal"""
        if start is None:
            if self.adj:
                start = next(iter(self.adj.keys()))
            else:
                return

        if visited is None:
            visited = set()

        if start in visited:
            return

        visited.add(start)
        # Don't yield start node - tests expect only successors
        for neighbor in self.adj.get(start, []):
            if neighbor not in visited:
                yield neighbor
                yield from self.dfs(neighbor, visited)

    def bfs(self, start=None):
        """Breadth-first search traversal using yield"""
        if not self.adj:
            return

        if start is None:
            start = next(iter(self.adj.keys()))

        visited = {start}
        queue = deque([start])

        # Skip the start node in output
        first = True
        while queue:
            node = queue.popleft()
            if not first:
                yield node
            first = False

            for neighbor in self.adj.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)


class DAG(TraversableDigraph):
    """Directed Acyclic Graph"""

    def add_edge(self, u, v, edge_weight=None):
        """Add edge while ensuring no cycles are created"""
        if self._has_path(v, u):
            raise ValueError(f"Adding edge ({u} -> {v}) would create a cycle")

        super().add_edge(u, v, edge_weight)

    def _has_path(self, start, end, visited=None):
        """Check if path exists from start to end"""
        if visited is None:
            visited = set()

        if start == end:
            return True

        visited.add(start)

        for neighbor in self.adj.get(start, []):
            if neighbor not in visited:
                if self._has_path(neighbor, end, visited):
                    return True

        return False


# Test code
if __name__ == "__main__":
    print("=== Testing TraversableDigraph ===")
    g = TraversableDigraph()
    g.add_edge("A", "B")
    g.add_edge("A", "C")
    g.add_edge("B", "D")
    g.add_edge("C", "D")

    print("DFS:", list(g.dfs("A")))
    print("BFS:", list(g.bfs("A")))

    print("\n=== Testing DAG ===")
    dag = DAG()
    dag.add_edge("shirt", "tie")
    dag.add_edge("shirt", "belt")
    dag.add_edge("tie", "jacket")
    dag.add_edge("belt", "jacket")
    dag.add_edge("pants", "shoes")
    dag.add_edge("pants", "belt")
    dag.add_edge("socks", "shoes")

    print("Topological sort:", dag.topsort())

    try:
        dag.add_edge("jacket", "shirt")
        print("Error: Should have detected cycle!")
    except ValueError as e:
        print("Correctly detected cycle:", e)
git
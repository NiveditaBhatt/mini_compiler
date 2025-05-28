def generate_parse_tree():
    import networkx as nx
    import matplotlib.pyplot as plt
    import re

    code = code_area.get(1.0, tk.END).strip()
    lines = [line.strip() for line in code.splitlines() if line.strip()]

    G = nx.DiGraph()
    root = "Program"
    G.add_node(root)

    def add_subtree(parent, label, children):
        """Helper to add a parent node with multiple children"""
        G.add_node(label)
        G.add_edge(parent, label)
        for child_label in children:
            G.add_node(child_label)
            G.add_edge(label, child_label)

    for i, line in enumerate(lines):
        # Remove trailing semicolon if exists
        if line.endswith(";"):
            line = line[:-1].strip()

        # Match declaration like: int a
        decl_match = re.match(r"^(int|float|char|double)\s+([a-zA-Z_][a-zA-Z0-9_]*)$", line)
        if decl_match:
            dtype, varname = decl_match.groups()
            decl_node = f"Declaration_{i+1}"
            add_subtree(root, decl_node, [f"Type: {dtype}", f"Variable: {varname}"])
            continue

        # Match assignment like: a = 5 or b = a + 1
        assign_match = re.match(r"^([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.+)$", line)
        if assign_match:
            var, expr = assign_match.groups()
            assign_node = f"Assignment_{i+1}"
            add_subtree(root, assign_node, [f"Variable: {var}", f"Expression: {expr}"])
            continue

        # Match if, while, for control structures
        ctrl_match = re.match(r"^(if|while|for)\s*\((.*)\)\s*(\{)?", line)
        if ctrl_match:
            ctrl_type, condition, brace = ctrl_match.groups()
            ctrl_node = f"{ctrl_type.capitalize()}_{i+1}"
            G.add_node(ctrl_node)
            G.add_edge(root, ctrl_node)

            cond_node = f"Condition: {condition}"
            G.add_node(cond_node)
            G.add_edge(ctrl_node, cond_node)

            # Optionally, if there's a block start, could parse nested lines
            continue

        # Otherwise, treat as generic statement
        stmt_node = f"Statement_{i+1}"
        G.add_node(stmt_node)
        G.add_edge(root, stmt_node)
        G.add_node(f"Code: {line}")
        G.add_edge(stmt_node, f"Code: {line}")

    # Draw the graph nicely
    plt.figure(figsize=(14, 10))
    pos = nx.spring_layout(G, seed=123)  # fixed layout for consistency
    nx.draw(G, pos, with_labels=True, node_color="lightcyan", edge_color="gray",
            node_size=2500, font_size=9, font_weight="bold", arrows=True)
    plt.title("C Code Parse Tree")
    plt.show()

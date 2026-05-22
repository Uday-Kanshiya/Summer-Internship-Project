import os
import tree_sitter_python as tspython
from tree_sitter import Language, Parser
import networkx as nx
import matplotlib.pyplot as plt
from google import genai

SAMPLE_CODE = """
def average_score(marks):
    return sum(marks) / len(marks)

def get_grade(avg):
    if avg >= 90:
        return \"A\"
    elif avg >= 75:
        return \"B\"
    elif avg >= 60:
        return \"C\"
    else:
        return \"D\"

def main():
    marks = [87, 92, 94, 95, 90]
    avg = average_score(marks)
    grade = get_grade(avg)
    print(grade)
"""

# ---------- GEMINI SETUP ----------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Set your Gemini API key first. In terminal: set GEMINI_API_KEY=your_key (Windows) or export GEMINI_API_KEY=your_key (Mac/Linux)")

client = genai.Client(api_key=GEMINI_API_KEY)


def pick_generate_model():
    preferred = [
        "gemini-2.5-flash",
        "gemini-2.0-flash",
        "gemini-2.0-flash-lite",
    ]
    names = []
    for m in client.models.list():
        name = getattr(m, "name", "")
        names.append(name)

    for p in preferred:
        for n in names:
            if n.endswith(p) or n == p:
                return n

    if names:
        return names[0]
    raise ValueError("No Gemini models found for this API key.")


MODEL_NAME = pick_generate_model()
print("Using Gemini model:", MODEL_NAME)


def call_llm(system_prompt, user_prompt):
    full_prompt = system_prompt + "\n\n" + user_prompt
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=full_prompt,
    )
    return response.text


# ---------- PARSE ----------
PY_LANGUAGE = Language(tspython.language())
ts_parser = Parser(PY_LANGUAGE)
code_bytes = SAMPLE_CODE.encode("utf8")
tree = ts_parser.parse(code_bytes)
print("Root:", tree.root_node.type)
print("Errors:", tree.root_node.has_error)


def get_text(node):
    return code_bytes[node.start_byte:node.end_byte].decode("utf8", errors="replace")


# ---------- EXTRACT ----------
def extract_entities(root):
    functions = []
    calls = []

    def walk(node, fn_stack=None):
        if fn_stack is None:
            fn_stack = []

        if node.type == "function_definition":
            n = node.child_by_field_name("name")
            fname = get_text(n) if n else "Unknown"
            entry = {
                "name": fname,
                "kind": "function",
                "line": node.start_point[0] + 1,
                "code": get_text(node),
            }
            functions.append(entry)
            for child in node.children:
                walk(child, fn_stack + [entry])
            return

        elif node.type == "call":
            fn = node.child_by_field_name("function")
            if fn:
                caller = fn_stack[-1]["name"] if fn_stack else None
                calls.append({
                    "call": get_text(fn).strip(),
                    "caller": caller,
                    "line": node.start_point[0] + 1,
                })

        for child in node.children:
            walk(child, fn_stack)

    walk(root)
    return functions, calls


functions, calls = extract_entities(tree.root_node)
print("\nFunctions:")
for f in functions:
    print(f"- {f['name']} (line {f['line']})")

print("\nCalls:")
for c in calls:
    print(c)


# ---------- BUILD GRAPH ----------
G = nx.DiGraph()
fn_names = {f["name"] for f in functions}

G.add_node("MODULE", kind="module")

for f in functions:
    G.add_node(f["name"], kind="function", line=f["line"], code=f["code"])
    G.add_edge("MODULE", f["name"], relation="DEFINES")

for c in calls:
    caller = c["caller"]
    callee = c["call"].split(".")[-1]
    if caller and callee in fn_names and caller != callee:
        G.add_edge(caller, callee, relation="CALLS")

print("\nEdges:")
for u, v, d in G.edges(data=True):
    print(f"{u} --[{d['relation']}]--> {v}")


# ---------- VISUALIZE ----------
kind_colors = {
    "module": "#7B68EE",
    "function": "#2ECC71",
}
edge_colors = {
    "DEFINES": "#4A90D9",
    "CALLS": "#E74C3C",
}

node_colors = [kind_colors.get(G.nodes[n].get("kind"), "#CCCCCC") for n in G.nodes()]
edge_color_list = [edge_colors.get(G[u][v]["relation"], "#999999") for u, v in G.edges()]

plt.figure(figsize=(10, 6))
pos = nx.spring_layout(G, seed=42)
nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=2200)
nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold")
nx.draw_networkx_edges(G, pos, edge_color=edge_color_list, arrows=True, arrowsize=20, width=2)
nx.draw_networkx_edge_labels(
    G,
    pos,
    edge_labels={(u, v): G[u][v]["relation"] for u, v in G.edges()},
    font_size=8,
)
plt.title("CodeGraph with Gemini Query Support")
plt.axis("off")
plt.tight_layout()
plt.savefig("codegraph_gemini_demo.png", dpi=150, bbox_inches="tight")
plt.show()


# ---------- SIMPLE GRAPH QUERY ----------
def count_words(text):
    return len(text.split())


def find_anchor_nodes(query):
    query_lower = query.lower()
    anchors = []

    for name in G.nodes():
        if name == "MODULE":
            continue
        if name.lower() in query_lower:
            anchors.append(name)

    return anchors


def query_subgraph(query, hops=1):
    anchors = find_anchor_nodes(query)
    visited = set()

    for anchor in anchors:
        frontier = {anchor}
        for _ in range(hops):
            next_nodes = set()
            for node in frontier:
                next_nodes |= set(G.successors(node))
                next_nodes |= set(G.predecessors(node))
            visited |= frontier
            frontier = next_nodes - visited
        visited |= frontier

    subgraph = G.subgraph(visited).copy()
    return anchors, subgraph


def build_context(subgraph):
    lines = []
    lines.append("ENTITIES:")
    for n, d in subgraph.nodes(data=True):
        lines.append(f"- {n} [{d.get('kind', '?')}]")

    lines.append("RELATIONSHIPS:")
    for u, v, d in subgraph.edges(data=True):
        lines.append(f"- {u} --[{d['relation']}]--> {v}")

    lines.append("FUNCTION BODIES:")
    for n, d in subgraph.nodes(data=True):
        if d.get("kind") == "function":
            lines.append(f"\n### {n}")
            lines.append(d.get("code", ""))

    return "\n".join(lines)


def ask(query, hops=1):
    anchors, subgraph = query_subgraph(query, hops=hops)
    context = build_context(subgraph)

    full_code_words = count_words(SAMPLE_CODE)
    context_words = count_words(context)

    print("\nQUERY:", query)
    print("ANCHORS:", anchors)
    print("SUBGRAPH:", subgraph.number_of_nodes(), "nodes,", subgraph.number_of_edges(), "edges")
    print("CONTEXT REDUCTION:", f"{full_code_words} words -> {context_words} words")
    print("\nCONTEXT:\n")
    print(context)

    if subgraph.number_of_nodes() == 0:
        print("\nANSWER:\n")
        print("No matching graph context found. Try using an exact function name like get_grade or main.")
        return None

    system_prompt = "You are a helpful code assistant. Answer only from the provided graph context and function bodies. If the context is insufficient, say so clearly."
    user_prompt = "CONTEXT:\n" + context + "\n\nQUESTION:\n" + query
    answer = call_llm(system_prompt, user_prompt)

    print("\nANSWER:\n")
    print(answer)
    return answer


print("\nask() is ready")
print("Try this:")
print("ask('How does get_grade decide the grade?')")
print("ask('What does main do?')")

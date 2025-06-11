import tkinter as tk
from tkinter import ttk, messagebox
import heapq
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx 


# lop Node
class Node:
    def __init__(self, name, h_value):
        self.name = name
        self.h = h_value
        self.g = float('inf')
        self.f = float('inf')
        self.parent = None
    
    def __lt__(self, other):
        return self.f < other.f

# Lop do thi 
class Graph:
    def __init__(self):
        self.edges = {}

    def add_edge(self, from_node, to_node, distance):
        if from_node not in self.edges:
            self.edges[from_node] = {}
        self.edges[from_node][to_node] = distance

# thuat toan A*
def astar(graph, start, goal, heuristics, output_text):
    open_list = []
    closed_list = []
    node_map = {}

    start_node = Node(start, heuristics[start])
    goal_node = Node(goal, heuristics[goal])
    start_node.g = 0
    start_node.f = start_node.h

    heapq.heappush(open_list,(start_node.f, start_node))
    node_map[start] = start_node

    output_text.insert(tk.END, f"Khởi tạo:\n")
    output_text.insert(tk.END, f"Thêm đỉnh{start_node.name} vào OPEN với:\n")
    output_text.insert(tk.END, f" g({start_node.name}) = {start_node.g}\n")
    output_text.insert(tk.END, f" h({start_node.name}) = {start_node.g}\n")
    output_text.insert(tk.END, f" f({start_node.name}) = {start_node.g}\n")
    output_text.insert(tk.END, f" OPEN:{[start_node.name]}\n")
    output_text.insert(tk.END, f" CLOSED:{closed_list}\n")

    while open_list:
        current_f,current_node = heapq.heappop(open_list)
        output_text.insert(tk.END, f"\nXử lý đỉnh: {current_node.name}\n")

        if current_node.name == goal:
            path=[]
            while current_node:
                path.append(current_node.name)
                current_node = current_node.parent
            output_text.insert(tk.END, f"Đường đi từ {start} đến {goal}:{path[::-1]}\n")
            output_text.insert(tk.END, f"Chi phi từ {start} đến {goal}:{node_map[goal].g}\n")
            output_text.insert(tk.END," Mối quan hệ cha con:\n")
            for node_name, node in node_map.items():
                parent_name = node.parent.name if node.parent else "None"
                output_text.insert(tk.END, f" Đỉnh {node_name}: Cha = {parent_name}\n")
            return path[::-1]
        if current_node.name in graph.edges:
            output_text.insert(tk.END, "Các đỉnh kề:\n")
            for neighbor, distance in graph.edges[current_node.name].items():
                if neighbor not in node_map:
                    neighbor_node = Node(neighbor, heuristics[neighbor]) 
                    node_map[neighbor] = neighbor_node
                else:
                    neighbor_node = node_map[neighbor]
                tentative_g = current_node.g + distance
                output_text.insert(tk.END, f" Xem xét đỉnh {neighbor}: khoảng cách từ {current_node.name} = {distance}, heuristic = {neighbor_node.h}")
                output_text.insert(tk.END, f" Tentative g = {tentative_g}\n")

                if tentative_g < neighbor_node.g:
                    neighbor_node.g = tentative_g
                    neighbor_node.f = neighbor_node.g + neighbor_node.h
                    neighbor_node.parent = current_node
                    output_text.insert(tk.END, f" Cập nhật: g={neighbor_node.g}, h = {neighbor_node.h}, f={neighbor_node.f}\n")

                    if all(neighbor_node.name != node.name for _, node in open_list):
                        heapq.heappush(open_list, (neighbor_node.f, neighbor_node))
                    else:
                        open_list =[(f, node) if node.name != neighbor_node.name else(neighbor_node.f, neighbor_node) for f, node in open_list]
                        heapq.heapify(open_list)
        closed_list.append(current_node.name)

        output_text.insert(tk.END, f" OPEN: {[node.name for _, node in open_list]}\n")
        closed_list_diplay = closed_list.copy()
        if start in closed_list_diplay:
            closed_list_diplay.remove(start)
            closed_list_diplay.insert(0, start)
        output_text.insert(tk.END, f" CLOSED:{closed_list_diplay}\n")
    
    output_text.insert(tk.END, f" Không tìm thấy đường đi từ {start} đến {goal}\n")
    return None


# ham ve do thi
def draw_graph(graph,path = None):
    G = nx.Graph()

    for from_node, neighbors in graph.edges.items():
        for to_node, distance in neighbors.items():
            G.add_edge(from_node, to_node, weight=distance)

    pos = nx.spring_layout(G, seed = 42)

    labels = {node : f'{node}\n h={heuristics.get(node,"N/A")}' for node in G.nodes()}

    nx.draw(G, pos, with_labels = False, node_color = 'lightblue', node_size = 500, font_size=10)
    nx.draw_networkx_labels(G, pos,labels, font_size = 10, font_weight = 'bold')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    if path:
        edge_list = [(path[i],path[i+1]) for i in range(len(path)-1)]
        nx.draw_networkx_edges(G, pos, edgelist = edge_list, edge_color = 'r', width = 2)

    return plt.gcf(), pos

# ve do thi trong giao dien
def plot_graph_in_gui(graph, canvas, path = None):
    fig, pos = draw_graph(graph, path)

    fig.set_size_inches(6,6)

    canvas.figure = fig 
    canvas.draw()

# chay thuat toan A*
def run_astar():
    start = start_entry.get().strip()
    goal = goal_entry.get().strip()

    if start not in heuristics or goal not in heuristics:
        messagebox.showerror("Error","Điểm bắt đầu hoặc điểm đích không hợp lệ!")
        return
    
    output_text.delete(1.0, tk.END)
    path = astar(graph, start, goal, heuristics, output_text)

    plot_graph_in_gui(graph, canvas,path)


#tao giao dien
def create_gui():
    global start_entry, goal_entry, output_text, canvas

    root = tk.Tk()
    root.title("Thuật Toán A*")
    root.geometry("1400x800")

    title_label = tk.Label(root, text = "Thuật Toán A* - Bài toán tìm đường đi", font=("Helvetica",20,"bold"))
    title_label.pack(pady=8)

    input_frame = tk.Frame(root)
    input_frame.pack(pady=5)

    tk.Label(input_frame, text="Điểm đầu: ", font=("Helvetica",12)).grid(row = 0, column = 0, padx = 5, pady = 5)
    start_entry = ttk.Entry(input_frame, font=("Helvetica", 12), width = 10)
    start_entry.grid(row=0, column = 1,padx = 5, pady =5)

    tk.Label(input_frame, text = "Điểm đích: ", font=("Helvetica", 12)).grid(row=1, column = 0,padx = 5,pady = 5)
    goal_entry = ttk.Entry(input_frame, font=("Helvetica",12),width=10)
    goal_entry.grid(row=1,column = 1,padx = 5, pady = 5)

    run_button = ttk.Button(input_frame, text ="Run", command =run_astar)
    run_button.grid(row = 2, column = 1, columnspan = 3, pady = 15)


    # them khum ve do thi
    canvas_frame = tk.Frame(root)
    canvas_frame.pack(side = tk.RIGHT, padx = 20, pady=20)

    fig = plt.figure(figsize=(6,6))
    canvas = FigureCanvasTkAgg(fig, master = canvas_frame)
    canvas.get_tk_widget().pack(side=tk.TOP, fill = tk.BOTH, expand=True)

    # ve do thi lan dau khi giao dien khoi tao
    plot_graph_in_gui(graph, canvas, path=None)
    # hop van ban hien thi qua trinh va ket qua
    output_text = tk.Text(root, height=31, width =110, font=("Consolas", 13),wrap="word", borderwidth=1,relief="groove")
    output_text.pack(side = tk.LEFT, pady=12, padx=12)
    root.mainloop()

#khai bao heuristic cho cac dinh
heuristics = {
    'A' :14,
    'C' : 15,
    'D' : 6,
    'E' : 8,
    'F' : 7,
    'G' : 12,
    'H' : 10,
    'K' : 2,
    'I' : 4,
    'B' : 5,
    'L' : 8,
    'J' : 7,
}

#khai bao do thi va cac khoang cach giua cac dinh

graph = Graph()
graph.add_edge('A', 'C',1)
graph.add_edge('A', 'D', 2)
graph.add_edge('A', 'B', 4)
graph.add_edge('A','E',4)
graph.add_edge('C','H',1)
graph.add_edge('D','H',1)
graph.add_edge('H','G',1)
graph.add_edge('H','I',1)
graph.add_edge('G','F',1)
graph.add_edge('G','K',1)
graph.add_edge('F','L',3)
graph.add_edge('K','L',3)
graph.add_edge('J','L',2)
graph.add_edge('I','J',1)
graph.add_edge('B','F',3)
graph.add_edge('E','J',2)
graph.add_edge('I','K',1)

#chay phan giao dien
create_gui()


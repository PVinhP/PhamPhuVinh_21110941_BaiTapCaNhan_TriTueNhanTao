import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import heapq
import copy
import math
from collections import deque
import threading

# Định nghĩa lớp Node để biểu diễn trạng thái trong thuật toán tìm kiếm
class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0, depth=0, heuristic=0):
        self.state = state           # Trạng thái hiện tại của puzzle
        self.parent = parent         # Node cha (trạng thái trước đó)
        self.action = action         # Hành động dẫn đến trạng thái này
        self.path_cost = path_cost   # Chi phí đường đi tới trạng thái này
        self.depth = depth           # Độ sâu trong cây tìm kiếm
        self.heuristic = heuristic   # Giá trị heuristic (đánh giá)
        self.f = path_cost + heuristic  # Tổng chi phí + heuristic (dùng cho A*)
    
    def __lt__(self, other):
        return self.f < other.f  # So sánh để sắp xếp các node trong hàng đợi ưu tiên

# Lớp chính của ứng dụng
class EightPuzzle:
    def __init__(self):
        # Khởi tạo cửa sổ chính
        self.root = tk.Tk() 
        self.root.title("Phạm Phú Vinh-21110941-Puzzle Solver")
        self.root.geometry("800x800")
        self.root.resizable(False, False)
        
        # Khởi tạo trạng thái ban đầu và trạng thái đích
        self.initial_state = [[2, 6, 5], [0, 8, 7], [4, 3, 1]]
        #self.initial_state = [[1, 0, 3], [5, 2, 6], [4, 7, 8]]   # Trạng thái bắt đầu
        self.goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]    # Trạng thái đích
        
        # Sao chép trạng thái ban đầu để sử dụng
        self.current_state = copy.deepcopy(self.initial_state)
        self.solution_path = []      # Lưu đường đi giải
        self.solution_index = 0      # Vị trí hiện tại trong đường đi
        self.is_solving = False      # Cờ đánh dấu đang giải
        self.speed = 500             # Tốc độ hiển thị (milliseconds)
        
        # Tạo các thành phần giao diện
        self.create_widgets()
        
        # Khởi chạy vòng lặp chính của ứng dụng
        self.root.mainloop()
    
    
    def create_widgets(self):
        # Tạo khung header
        header_frame = tk.Frame(self.root, pady=10)
        header_frame.pack(fill=tk.X)
        
        # Khung hiển thị trạng thái ban đầu và đích
        states_frame = tk.Frame(header_frame)
        states_frame.pack()
        
        # Nhãn và khung cho trạng thái ban đầu
        initial_label = tk.Label(states_frame, text="Trạng thái ban đầu:")
        initial_label.grid(row=0, column=0, padx=10)
        
        self.initial_state_frame = tk.Frame(states_frame, borderwidth=2, relief="ridge")
        self.initial_state_frame.grid(row=0, column=1, padx=10)
        
        # Nhãn và khung cho trạng thái đích
        goal_label = tk.Label(states_frame, text="Trạng thái mục tiêu:")
        goal_label.grid(row=0, column=2, padx=10)
        
        self.goal_state_frame = tk.Frame(states_frame, borderwidth=2, relief="ridge")
        self.goal_state_frame.grid(row=0, column=3, padx=10)
        
        # Cập nhật hiển thị các trạng thái
        self.update_state_display(self.initial_state_frame, self.initial_state)
        self.update_state_display(self.goal_state_frame, self.goal_state)
        
        # Khung điều khiển
        controls_frame = tk.Frame(header_frame, pady=10)
        controls_frame.pack()
        
        # Nút tạo trạng thái ngẫu nhiên
        random_button = tk.Button(controls_frame, text="Ngẫu nhiên", command=self.randomize_initial_state)
        random_button.grid(row=0, column=0, padx=10)
        
        # Thanh trượt điều chỉnh tốc độ
        speed_label = tk.Label(controls_frame, text="Tốc dộ:")
        speed_label.grid(row=0, column=1, padx=10)
        
        self.speed_scale = ttk.Scale(controls_frame, from_=100, to=1000, length=200, orient=tk.HORIZONTAL, value=self.speed)
        self.speed_scale.grid(row=0, column=2, padx=10)
        self.speed_scale.bind("<ButtonRelease-1>", self.update_speed)
        
        # Nhãn hiển thị giá trị tốc độ
        speed_value_label = tk.Label(controls_frame, text="500 ms")
        speed_value_label.grid(row=0, column=3, padx=5)
        
        # Cập nhật hiển thị tốc độ khi thay đổi
        self.speed_scale.bind("<Motion>", lambda e: speed_value_label.config(text=f"{int(self.speed_scale.get())} ms"))
        
        # Khung nội dung chính với lựa chọn thuật toán và hiển thị puzzle
        content_frame = tk.Frame(self.root)
        content_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Phần lựa chọn thuật toán
        algorithm_frame = tk.Frame(content_frame, padx=10)
        algorithm_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        algo_label = tk.Label(algorithm_frame, text="Lựa chọn thuật toán:", font=("Arial", 12, "bold"))
        algo_label.pack(pady=(0, 5), anchor=tk.W)
        
        # Danh sách các thuật toán
        algorithms = ["DFS", "BFS", "UCS", "IDS", "Greedy", "A*", "IDA*", 
              "Simple Hill Climbing", "Steepest-Ascent Hill Climbing", 
              "Stochastic Hill Climbing", "Simulated Annealing", "Beam Search","Genetic Algorithm","AND-OR Graph Search",
              "Searching with No Observation",  "Partially Observable Search", "Test-Based Search", "Backtracking search algorithm", "AC3", "Q-Learning"]
        
        # Tạo listbox để hiển thị và chọn thuật toán
        self.algorithm_listbox = tk.Listbox(algorithm_frame, height=len(algorithms))
        self.algorithm_listbox.pack(fill=tk.BOTH, expand=True)
        
        # Thêm các thuật toán vào listbox
        for algo in algorithms:
            self.algorithm_listbox.insert(tk.END, algo)
        
        # Chọn thuật toán mặc định là DFS
        self.algorithm_listbox.selection_set(0)
        
        # Các nút điều khiển: Solve, Stop, Reset
        solve_button = tk.Button(algorithm_frame, text="Giải pháp", command=self.start_solving)
        solve_button.pack(pady=10, fill=tk.X)
        
        stop_button = tk.Button(algorithm_frame, text="Dừng", command=self.stop_solving)
        stop_button.pack(fill=tk.X)
        
        reset_button = tk.Button(algorithm_frame, text="Tải lại", command=self.reset_puzzle)
        reset_button.pack(pady=10, fill=tk.X)
        
        # Khung hiển thị puzzle
        puzzle_frame = tk.Frame(content_frame)
        puzzle_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20)
        
        self.puzzle_display = tk.Frame(puzzle_frame, width=300, height=300)
        self.puzzle_display.pack(pady=20)
        
        # Tạo các ô cho puzzle
        self.tiles = []
        for i in range(3):
            row_tiles = []
            for j in range(3):
                # Tạo khung cho mỗi ô
                tile_frame = tk.Frame(self.puzzle_display, width=80, height=80, borderwidth=2, relief="raised")
                tile_frame.grid(row=i, column=j, padx=5, pady=5)
                tile_frame.grid_propagate(False)
                
                # Tạo nhãn hiển thị số trong mỗi ô
                tile_label = tk.Label(tile_frame, font=("Arial", 24, "bold"))
                tile_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
                
                row_tiles.append(tile_label)
            self.tiles.append(row_tiles)
        
        # Khung hiển thị thống kê
        stats_frame = tk.Frame(self.root, pady=0)
        stats_frame.pack(fill=tk.X)
        
        # Hiển thị thời gian và số bước
        time_steps_frame = tk.Frame(stats_frame)
        time_steps_frame.pack()
        
        tk.Label(time_steps_frame, text="Thời gian: ").grid(row=0, column=0, padx=5)
        self.time_label = tk.Label(time_steps_frame, text="0.00 s")
        self.time_label.grid(row=0, column=1, padx=5)
        
        tk.Label(time_steps_frame, text="Các bước: ").grid(row=0, column=2, padx=5)
        self.steps_label = tk.Label(time_steps_frame, text="0")
        self.steps_label.grid(row=0, column=3, padx=5)
        
        # Thanh tiến trình
        tk.Label(stats_frame, text="Tiến trình giải:").pack()
        self.progress_bar = ttk.Progressbar(stats_frame, length=600, mode='determinate')
        self.progress_bar.pack(pady=0)
        
        # Hiển thị các bước giải
        steps_frame = tk.Frame(self.root, pady=10)
        steps_frame.pack(fill=tk.BOTH, expand=True)
        
        step_label = tk.Label(steps_frame, text="Blog quá trình:", font=("Arial", 12, "bold"))
        step_label.pack(anchor=tk.W, padx=10)
        
        # Vùng text hiển thị các bước giải
        self.steps_text = tk.Text(steps_frame, height=8, wrap=tk.WORD)
        self.steps_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=0)
        
        # Khởi tạo hiển thị puzzle
        self.update_puzzle_display(self.initial_state)
    
    def update_state_display(self, frame, state):
        # Xóa tất cả widget con trong frame
        for widget in frame.winfo_children():
            widget.destroy()
        
        # Tạo các nhãn hiển thị số cho từng trạng thái
        for i in range(3):
            for j in range(3):
                value = state[i][j]
                if value == 0:
                    text = " "  # Ô trống hiển thị khoảng trắng
                else:
                    text = str(value)
                label = tk.Label(frame, text=text, width=3, height=1, font=("Arial", 12), relief="ridge")
                label.grid(row=i, column=j)
    
    def update_puzzle_display(self, state):
        # Cập nhật hiển thị puzzle với trạng thái mới
        for i in range(3):
            for j in range(3):
                value = state[i][j]
                if value == 0:
                    self.tiles[i][j].config(text="")  # Ô trống không hiển thị số
                    self.tiles[i][j].master.config(bg="light gray")  # Đặt màu xám nhạt cho ô trống
                else:
                    self.tiles[i][j].config(text=str(value))
                    self.tiles[i][j].master.config(bg="white")
    
    def randomize_initial_state(self):
        # Tạo một trạng thái ban đầu ngẫu nhiên có thể giải được
        numbers = [i for i in range(9)]
        random.shuffle(numbers)  # Trộn ngẫu nhiên các số từ 0-8
        
        # Chuyển đổi sang định dạng 2D (ma trận 3x3)
        state = [numbers[i:i+3] for i in range(0, 9, 3)]
        
        # Kiểm tra tính khả thi của trạng thái
        flat_state = [num for row in state for num in row]
        inversions = 0
        for i in range(len(flat_state)):
            if flat_state[i] == 0:
                continue
            for j in range(i + 1, len(flat_state)):
                if flat_state[j] == 0:
                    continue
                if flat_state[i] > flat_state[j]:
                    inversions += 1
        
        # Kiểm tra tính khả giải của puzzle 3x3:
        # - Nếu ô trống nằm ở hàng chẵn (tính từ dưới lên) và số đảo lẻ, có thể giải được
        # - Nếu ô trống nằm ở hàng lẻ (tính từ dưới lên) và số đảo chẵn, có thể giải được
        blank_row = next(i for i, row in enumerate(state) if 0 in row)
        blank_row_from_bottom = 3 - blank_row
        
        if (blank_row_from_bottom % 2 == 0 and inversions % 2 == 1) or \
           (blank_row_from_bottom % 2 == 1 and inversions % 2 == 0):
            self.initial_state = state
        else:
            # Làm cho trạng thái có thể giải được bằng cách đổi chỗ hai ô (không bao gồm ô trống)
            for i in range(3):
                for j in range(3):
                    if state[i][j] != 0 and (i > 0 or j > 0):  # Không đổi với vị trí đầu tiên
                        # Đổi chỗ với vị trí (0, 0) nếu không phải ô trống, nếu không thì với (0, 1)
                        swap_i, swap_j = (0, 1) if state[0][0] == 0 else (0, 0)
                        if state[swap_i][swap_j] != 0:
                            state[i][j], state[swap_i][swap_j] = state[swap_i][swap_j], state[i][j]
                            self.initial_state = state
                            break
                else:
                    continue
                break
        
        # Cập nhật hiển thị trạng thái ban đầu và reset puzzle
        self.update_state_display(self.initial_state_frame, self.initial_state)
        self.reset_puzzle()
    
    def update_speed(self, event):
        # Cập nhật tốc độ khi thanh trượt thay đổi
        self.speed = int(self.speed_scale.get())
    
    def start_solving(self):
        # Bắt đầu giải puzzle
        if self.is_solving:
            return
        
        self.is_solving = True
        self.current_state = copy.deepcopy(self.initial_state)
        self.update_puzzle_display(self.current_state)
        self.solution_path = []
        self.solution_index = 0
        self.steps_text.delete(1.0, tk.END)
        
        # Lấy thuật toán được chọn
        selected_index = self.algorithm_listbox.curselection()
        if not selected_index:
            messagebox.showinfo("Error", "Hãy chọn lại thuật toán")
            self.is_solving = False
            return
        
        algorithm = self.algorithm_listbox.get(selected_index[0])
        
        # Bắt đầu luồng giải puzzle để không làm đơ giao diện
        threading.Thread(target=self.solve_puzzle, args=(algorithm,), daemon=True).start()
    
    def stop_solving(self):
        # Dừng quá trình giải
        self.is_solving = False
    
    def reset_puzzle(self):
        # Reset puzzle về trạng thái ban đầu
        self.stop_solving()
        self.current_state = copy.deepcopy(self.initial_state)
        self.update_puzzle_display(self.current_state)
        self.solution_path = []
        self.solution_index = 0
        self.steps_text.delete(1.0, tk.END)
        self.time_label.config(text="0.00 s")
        self.steps_label.config(text="0")
        self.progress_bar["value"] = 0
    
    def solve_puzzle(self, algorithm):
        # Giải puzzle bằng thuật toán được chọn
        start_time = time.time()
        
        # Gọi thuật toán phù hợp
        if algorithm == "DFS":
            path = self.depth_first_search()  # Tìm kiếm theo chiều sâu
        elif algorithm == "BFS":
            path = self.breadth_first_search()  # Tìm kiếm theo chiều rộng
        elif algorithm == "UCS":
            path = self.uniform_cost_search()  # Tìm kiếm theo chi phí đồng nhất
        elif algorithm == "IDS":
            path = self.iterative_deepening_search()  # Tìm kiếm theo độ sâu tăng dần
        elif algorithm == "Greedy":
            path = self.greedy_search()  # Tìm kiếm tham lam
        elif algorithm == "A*":
            path = self.a_star_search()  # Tìm kiếm A*
        elif algorithm == "IDA*":
            path = self.ida_star_search()  # Tìm kiếm IDA*
        elif algorithm == "Simple Hill Climbing":
            path = self.simple_hill_climbing()  # Leo đồi đơn giản
        elif algorithm == "Steepest-Ascent Hill Climbing":
            path = self.steepest_ascent_hill_climbing()  # Leo đồi theo hướng dốc nhất
        elif algorithm == "Stochastic Hill Climbing":
            path = self.stochastic_hill_climbing()  # Leo đồi ngẫu nhiên
        elif algorithm == "Simulated Annealing":
            path = self.simulated_annealing()
        elif algorithm == "Genetic Algorithm":
            path = self.genetic_algorithm()
        elif algorithm == "Beam Search":
            path = self.beam_search(beam_width=5)  # Độ rộng beam mặc định là 5
        elif algorithm == "AND-OR Graph Search":
            path = self.and_or_graph_search()
        elif algorithm == "Searching with No Observation":
            path = self.searching_with_no_observation()
        elif algorithm == "Partially Observable Search":
            path = self.partially_observable_search()
        elif algorithm == "Test-Based Search":
            path = self.test_based_search()
        elif algorithm == "Backtracking search algorithm":
            path = self.backtracking_search()   # Thuật toán tìm kiếm bằng kiểm thử
        elif algorithm == "AC3":
            path = self.ac3_search()  # Thêm thuật toán AC3
        elif algorithm == "Q-Learning":
            path = self.qlearning_solve()
        else:
            path = []
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # Cập nhật giao diện với kết quả
        if not self.is_solving:
            return
        
        self.root.after(0, lambda: self.time_label.config(text=f"{elapsed_time:.2f} s"))
        
        if not path:
            self.root.after(0, lambda: messagebox.showinfo("Result", "Không tìm thấy giải pháp!"))
            self.is_solving = False
            return
        
        self.solution_path = path
        self.root.after(0, lambda: self.steps_label.config(text=str(len(path) - 1)))
        
        # Hiển thị các bước giải trong vùng text
        solution_text = ""
        for i, node in enumerate(path):
            solution_text += f"Step {i}: {self.state_to_string(node.state)}\n"
        
        self.root.after(0, lambda: self.steps_text.delete(1.0, tk.END))
        self.root.after(0, lambda: self.steps_text.insert(tk.END, solution_text))
        
        # Animate giải pháp
        self.solution_index = 0
        self.animate_solution()
    
    def animate_solution(self):
        # Hiển thị từng bước giải theo thời gian thực
        if not self.is_solving or self.solution_index >= len(self.solution_path):
            self.is_solving = False
            return
        
        # Cập nhật thanh tiến trình
        progress = (self.solution_index / (len(self.solution_path) - 1)) * 100
        self.progress_bar["value"] = progress
        
        # Cập nhật hiển thị puzzle
        current_node = self.solution_path[self.solution_index]
        self.update_puzzle_display(current_node.state)
        
        self.solution_index += 1
        
        # Lên lịch cho bước hiển thị tiếp theo
        if self.solution_index < len(self.solution_path) and self.is_solving:
            self.root.after(self.speed, self.animate_solution)
        else:
            self.is_solving = False
    
    def state_to_string(self, state):
        # Chuyển đổi trạng thái thành chuỗi để hiển thị
        return str([row for row in state])
    
    def get_blank_position(self, state):
        # Tìm vị trí của ô trống (giá trị 0)
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    return i, j
        return -1, -1
    
    def get_successors(self, node):
        # Lấy các trạng thái kế tiếp từ trạng thái hiện tại
        successors = []
        i, j = self.get_blank_position(node.state)
        
        # Các hướng di chuyển có thể: lên, phải, xuống, trái
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        direction_names = ["up", "right", "down", "left"]
        
        for idx, (di, dj) in enumerate(directions):
            ni, nj = i + di, j + dj
            
            # Kiểm tra nếu vị trí mới hợp lệ
            if 0 <= ni < 3 and 0 <= nj < 3:
                # Tạo trạng thái mới bằng cách di chuyển ô trống
                new_state = copy.deepcopy(node.state)
                new_state[i][j], new_state[ni][nj] = new_state[ni][nj], new_state[i][j]
                
                # Tạo node kế tiếp
                successor = Node(
                    state=new_state,
                    parent=node,
                    action=direction_names[idx],
                    path_cost=node.path_cost + 1,
                    depth=node.depth + 1,
                    heuristic=self.calculate_heuristic(new_state)
                )
                
                successors.append(successor)
        
        return successors
    
    def calculate_heuristic(self, state):
        # Tính toán hàm heuristic (khoảng cách Manhattan)
        distance = 0
        for i in range(3):
            for j in range(3):
                value = state[i][j]
                if value != 0:
                    # Tính vị trí đích của giá trị hiện tại
                    goal_i, goal_j = (value - 1) // 3, (value - 1) % 3
                    # Cộng khoảng cách Manhattan vào tổng
                    distance += abs(i - goal_i) + abs(j - goal_j)
        return distance
    
    def is_goal(self, state):
        # Kiểm tra xem trạng thái hiện tại có phải là trạng thái đích không
        return state == self.goal_state
    
    def get_solution_path(self, node):
        # Lấy đường đi từ node hiện tại về node gốc
        path = []
        while node:
            path.append(node)
            node = node.parent
        return list(reversed(path))  # Đảo ngược để có đường đi từ gốc đến đích
    
    def depth_first_search(self):
        # Thuật toán tìm kiếm theo chiều sâu (DFS)
        initial_node = Node(state=self.initial_state, heuristic=self.calculate_heuristic(self.initial_state))
        
        if self.is_goal(initial_node.state):
            return [initial_node]
        
        stack = [initial_node]  # Sử dụng ngăn xếp cho DFS
        visited = set()         # Tập hợp các trạng thái đã thăm
        
        while stack and self.is_solving:
            node = stack.pop()  # Lấy node từ đỉnh ngăn xếp
            state_str = str(node.state)
            
            if state_str in visited:
                continue  # Bỏ qua nếu trạng thái đã thăm
            
            visited.add(state_str)
            
            if self.is_goal(node.state):
                return self.get_solution_path(node)  # Tìm thấy đích
            
            successors = self.get_successors(node)
            for successor in reversed(successors):  # Thêm vào theo thứ tự đảo ngược để khám phá theo chiều sâu
                stack.append(successor)
        
        return []  # Không tìm thấy giải pháp
    
    def breadth_first_search(self):
        # Thuật toán tìm kiếm theo chiều rộng (BFS)
        initial_node = Node(state=self.initial_state, heuristic=self.calculate_heuristic(self.initial_state))
        
        if self.is_goal(initial_node.state):
            return [initial_node]
        
        queue = deque([initial_node])  # Sử dụng hàng đợi cho BFS
        visited = set()               # Tập hợp các trạng thái đã thăm
        
        while queue and self.is_solving:
            node = queue.popleft()  # Lấy node từ đầu hàng đợi
            state_str = str(node.state)
            
            if state_str in visited:
                continue  # Bỏ qua nếu trạng thái đã thăm
            
            visited.add(state_str)
            
            if self.is_goal(node.state):
                return self.get_solution_path(node)  # Tìm thấy đích
            
            successors = self.get_successors(node)
            for successor in successors:
                queue.append(successor)  # Thêm các node kế tiếp vào cuối hàng đợi
        
        return []  # Không tìm thấy giải pháp
    
    def uniform_cost_search(self):
        # Thuật toán tìm kiếm theo chi phí đồng nhất (UCS)
        initial_node = Node(state=self.initial_state, heuristic=0)  # Không sử dụng heuristic cho UCS
        
        if self.is_goal(initial_node.state):
            return [initial_node]
        
        # Sử dụng hàng đợi ưu tiên với chi phí đường đi là ưu tiên
        priority_queue = [(initial_node.path_cost, id(initial_node), initial_node)]
        visited = set()
        
        while priority_queue and self.is_solving:
            _, _, node = heapq.heappop(priority_queue)  # Lấy node có chi phí thấp nhất
            state_str = str(node.state)
            
            if state_str in visited:
                continue  # Bỏ qua nếu trạng thái đã thăm
            
            visited.add(state_str)
            
            if self.is_goal(node.state):
                return self.get_solution_path(node)  # Tìm thấy đích
            
            successors = self.get_successors(node)
            for successor in successors:
                successor.heuristic = 0  # Không sử dụng heuristic cho UCS
                successor.f = successor.path_cost
                # Thêm vào hàng đợi ưu tiên với ưu tiên là chi phí đường đi
                heapq.heappush(priority_queue, (successor.path_cost, id(successor), successor))
        
        return []  # Không tìm thấy giải pháp
    
    def iterative_deepening_search(self):
        max_depth = 0
        
        while self.is_solving:
            result = self.depth_limited_search(max_depth)
            if result:
                return result
            max_depth += 1
            if max_depth > 50:  # Avoid infinite loop
                break
        
        return []
    
    def depth_limited_search(self, limit):
        initial_node = Node(state=self.initial_state, heuristic=self.calculate_heuristic(self.initial_state))
        
        if self.is_goal(initial_node.state):
            return [initial_node]
        
        stack = [initial_node]
        visited = set()
        
        while stack and self.is_solving:
            node = stack.pop()
            state_str = str(node.state)
            
            if node.depth > limit:
                continue
            
            if state_str in visited:
                continue
            
            visited.add(state_str)
            
            if self.is_goal(node.state):
                return self.get_solution_path(node)
            
            if node.depth < limit:
                successors = self.get_successors(node)
                for successor in reversed(successors):
                    stack.append(successor)
        
        return []
    
    def greedy_search(self):
        initial_node = Node(state=self.initial_state, heuristic=self.calculate_heuristic(self.initial_state))
        
        if self.is_goal(initial_node.state):
            return [initial_node]
        
        priority_queue = [(initial_node.heuristic, id(initial_node), initial_node)]
        visited = set()
        
        while priority_queue and self.is_solving:
            _, _, node = heapq.heappop(priority_queue)
            state_str = str(node.state)
            
            if state_str in visited:
                continue
            
            visited.add(state_str)
            
            if self.is_goal(node.state):
                return self.get_solution_path(node)
            
            successors = self.get_successors(node)
            for successor in successors:
                # Đối với thuật toán tham lam, chỉ xét giá trị heuristic
                successor.f = successor.heuristic
                heapq.heappush(priority_queue, (successor.heuristic, id(successor), successor))
        
        return []
    
    def a_star_search(self):
        initial_node = Node(state=self.initial_state, heuristic=self.calculate_heuristic(self.initial_state))
        initial_node.f = initial_node.path_cost + initial_node.heuristic
        
        if self.is_goal(initial_node.state):
            return [initial_node]
        
        open_set = []
        heapq.heappush(open_set, (initial_node.f, id(initial_node), initial_node))
        closed_set = set()
        
        while open_set and self.is_solving:
            _, _, node = heapq.heappop(open_set)
            state_str = str(node.state)
            
            if state_str in closed_set:
                continue
            
            closed_set.add(state_str)
            
            if self.is_goal(node.state):
                return self.get_solution_path(node)
            
            successors = self.get_successors(node)
            for successor in successors:
                successor.f = successor.path_cost + successor.heuristic
                heapq.heappush(open_set, (successor.f, id(successor), successor))
        
        return []
    
    def ida_star_search(self):
        initial_node = Node(state=self.initial_state, heuristic=self.calculate_heuristic(self.initial_state))
        threshold = initial_node.heuristic
        
        while self.is_solving:
            result, new_threshold = self.ida_star_search_recursive(initial_node, threshold)
            if result:
                return result
            if new_threshold == float('inf'):
                return []
            threshold = new_threshold
    
    def ida_star_search_recursive(self, node, threshold):
        f = node.path_cost + node.heuristic
        
        if f > threshold:
            return None, f
        
        if self.is_goal(node.state):
            return self.get_solution_path(node), None
        
        min_threshold = float('inf')
        successors = self.get_successors(node)
        
        for successor in successors:
            if not self.is_solving:
                return None, float('inf')
            
            result, new_threshold = self.ida_star_search_recursive(successor, threshold)
            
            if result:
                return result, None
            
            if new_threshold < min_threshold:
                min_threshold = new_threshold
        
        return None, min_threshold
    
    def simple_hill_climbing(self):
        current_node = Node(state=self.initial_state, heuristic=self.calculate_heuristic(self.initial_state))
        
        while self.is_solving:
            if self.is_goal(current_node.state):
                return self.get_solution_path(current_node)
            
            successors = self.get_successors(current_node)
            if not successors:
                break
            
            # Tìm trạng thái gần tốt hơn trạng thái đầu tiên

            found_better = False
            for successor in successors:
                if successor.heuristic < current_node.heuristic:
                    current_node = successor
                    found_better = True
                    break
            
            if not found_better:
                break  # Reached local minimum
        
        if self.is_goal(current_node.state):
            return self.get_solution_path(current_node)
        else:
            return []
    
    def steepest_ascent_hill_climbing(self):
        current_node = Node(state=self.initial_state, heuristic=self.calculate_heuristic(self.initial_state))
        
        while self.is_solving:
            if self.is_goal(current_node.state):
                return self.get_solution_path(current_node)
            
            successors = self.get_successors(current_node)
            if not successors:
                break
            
            # Tìm lân cận tốt nhất
            best_successor = min(successors, key=lambda x: x.heuristic)
            
            if best_successor.heuristic >= current_node.heuristic:
                break  # Reached local minimum
            
            current_node = best_successor
        
        if self.is_goal(current_node.state):
            return self.get_solution_path(current_node)
        else:
            return []
    
    def stochastic_hill_climbing(self):
        current_node = Node(state=self.initial_state, heuristic=self.calculate_heuristic(self.initial_state))
        
        max_iterations = 100
        iteration = 0
        
        while self.is_solving and iteration < max_iterations:
            if self.is_goal(current_node.state):
                return self.get_solution_path(current_node)
            
            successors = self.get_successors(current_node)
            if not successors:
                break
            
            # Lọc các trạng thái kế tiếp có heuristic tốt hơn
            better_successors = [s for s in successors if s.heuristic < current_node.heuristic]
            
            if not better_successors:
                break  # No better successors
            
            # Chọn một trạng thái kế tiếp tốt hơn một cách ngẫu nhiên theo xác suất  
            # Chuẩn hóa để các trạng thái có heuristic thấp hơn có xác suất cao hơn
            max_h = max(s.heuristic for s in better_successors)
            min_h = min(s.heuristic for s in better_successors)
            range_h = max_h - min_h if max_h != min_h else 1
            
            weights = [(max_h - s.heuristic) / range_h for s in better_successors]
            total_weight = sum(weights)
            
            # Thêm kiểm tra để tránh chia cho 0
            if total_weight > 0:
                probs = [w / total_weight for w in weights]
                chosen_index = random.choices(range(len(better_successors)), weights=probs)[0]
            else:
                # Nếu tổng trọng số bằng 0, chọn ngẫu nhiên với xác suất bằng nhau
                chosen_index = random.randint(0, len(better_successors) - 1)
            
            current_node = better_successors[chosen_index]
            
            iteration += 1
        
        if self.is_goal(current_node.state):
            return self.get_solution_path(current_node)
        else:
            return []
    def simulated_annealing(self):
        current_node = Node(state=self.initial_state, heuristic=self.calculate_heuristic(self.initial_state))
        
        # Tham số cho thuật toán
        initial_temp = 100.0
        final_temp = 0.1
        alpha = 0.99  # Hệ số làm mát
        max_iterations = 1000
        
        # Nhiệt độ khởi tạo
        temp = initial_temp
        iteration = 0
        
        while self.is_solving and temp > final_temp and iteration < max_iterations:
            # Kiểm tra nếu đã đạt đến trạng thái đích
            if self.is_goal(current_node.state):
                return self.get_solution_path(current_node)
            
            # Lấy các trạng thái kế tiếp
            successors = self.get_successors(current_node)
            if not successors:
                break
            
            # Chọn một trạng thái kế tiếp ngẫu nhiên
            next_node = random.choice(successors)
            
            # Tính sự khác biệt giữa trạng thái hiện tại và trạng thái kế tiếp
            delta_e = next_node.heuristic - current_node.heuristic
            
            # Quyết định chấp nhận trạng thái kế tiếp hay không
            if delta_e < 0:  # Trạng thái kế tiếp tốt hơn
                current_node = next_node
            else:  # Trạng thái kế tiếp tệ hơn
                # Tính xác suất chấp nhận trạng thái tệ hơn
                probability = math.exp(-delta_e / temp)
                
                # Chấp nhận với xác suất tính được
                if random.random() < probability:
                    current_node = next_node
            
            # Cập nhật nhiệt độ
            temp *= alpha
            iteration += 1
            
            # Hiển thị thông tin tiến trình giải
            if iteration % 10 == 0:
                self.root.after(0, lambda: self.steps_text.insert(tk.END, 
                    f"Iteration {iteration}, Temp: {temp:.2f}, Heuristic: {current_node.heuristic}\n"))
        
        # Sau khi giải, kiểm tra lại nếu đạt đến trạng thái đích
        if self.is_goal(current_node.state):
            return self.get_solution_path(current_node)
        else:
            return []
    def beam_search(self, beam_width=5):
    
    #Thuật toán Beam Search với độ rộng beam (beam width) cho trước.
    
        initial_node = Node(state=self.initial_state, heuristic=self.calculate_heuristic(self.initial_state))
        
        if self.is_goal(initial_node.state):
            return [initial_node]
        
        # Tạo beam ban đầu chỉ với node ban đầu
        beam = [initial_node]
        visited = set([str(initial_node.state)])
        
        # Tiếp tục tìm kiếm cho đến khi beam rỗng
        while beam and self.is_solving:
            # Tạo danh sách chứa tất cả successor từ các node trong beam hiện tại
            all_successors = []
            
            # Mở rộng tất cả các node trong beam hiện tại
            for node in beam:
                successors = self.get_successors(node)
                for successor in successors:
                    state_str = str(successor.state)
                    if state_str not in visited:
                        all_successors.append(successor)
                        visited.add(state_str)
                        
                        # Kiểm tra nếu đã tìm thấy trạng thái đích
                        if self.is_goal(successor.state):
                            return self.get_solution_path(successor)
            
            if not all_successors:
                break
                
            # Sắp xếp tất cả successor theo giá trị heuristic
            all_successors.sort(key=lambda x: x.heuristic)
            
            # Chỉ giữ lại beam_width node tốt nhất
            beam = all_successors[:beam_width]
            
            # Hiển thị thông tin về vòng lặp hiện tại
            self.root.after(0, lambda current_best=beam[0].heuristic if beam else 0: 
                self.steps_text.insert(tk.END, f"Beam Search: beam size={len(beam)}, best heuristic={current_best}\n"))
        
        # Nếu không tìm thấy giải pháp
        return []
    
    def and_or_graph_search(self):
    # Giới hạn độ sâu tối đa để tránh đệ quy vô hạn
        MAX_DEPTH = 30
        
        # Sử dụng set để lưu trữ trạng thái đã thăm
        visited = set()
        
        def or_search(state, depth):
            # Kiểm tra giới hạn độ sâu
            if depth > MAX_DEPTH:
                return None
            
            # Chuyển state thành chuỗi để lưu vào set
            state_str = str(state)
            
            # Kiểm tra xem trạng thái đã được thăm chưa
            if state_str in visited:
                return None
            
            # Thêm trạng thái hiện tại vào danh sách đã thăm
            visited.add(state_str)
            
            # Nếu đạt trạng thái đích, trả về nút đích
            if self.is_goal(state):
                goal_node = Node(state=state, heuristic=0)
                return [goal_node]
            
            # Tạo node hiện tại để tìm các successor
            current_node = Node(state=state, heuristic=self.calculate_heuristic(state))
            successors = self.get_successors(current_node)
            
            # Kiểm tra từng hành động có thể thực hiện
            for successor in successors:
                # Với mỗi successor, tìm kiếm giải pháp tiếp theo từ trạng thái đó
                plan = or_search(successor.state, depth + 1)
                
                # Nếu tìm thấy giải pháp từ successor này
                if plan is not None:
                    # Trả về kế hoạch: nút hiện tại + kế hoạch từ successor
                    return [successor] + plan
            
            # Không tìm thấy giải pháp
            return None
        
        # Bắt đầu tìm kiếm từ trạng thái ban đầu
        initial_node = Node(state=self.initial_state, heuristic=self.calculate_heuristic(self.initial_state))
        
        # Kiểm tra ngay nếu trạng thái ban đầu là trạng thái đích
        if self.is_goal(initial_node.state):
            return [initial_node]
        
        # Gọi hàm or_search với trạng thái ban đầu và độ sâu 0
        solution = or_search(self.initial_state, 0)
        
        # Nếu tìm thấy giải pháp
        if solution is not None:
            # Xây dựng đường đi đầy đủ từ nút gốc đến đích
            full_path = [initial_node] + solution
            
            # Cập nhật parent cho từng node trong đường đi
            for i in range(1, len(full_path)):
                full_path[i].parent = full_path[i-1]
                full_path[i].depth = i
                full_path[i].path_cost = i
            
            return full_path
        else:
            return []  # Không tìm thấy giải pháp
    def genetic_algorithm(self):
        # Tham số cho thuật toán di truyền
        POPULATION_SIZE = 100      # Kích thước quần thể
        MAX_GENERATIONS = 100      # Số thế hệ tối đa
        MUTATION_RATE = 0.2        # Tỷ lệ đột biến
        CROSSOVER_RATE = 0.7       # Tỷ lệ lai ghép
        ELITE_SIZE = 10            # Số cá thể ưu tú giữ lại
        
        class Individual:
            def __init__(self, moves=None, fitness=float('inf')):
                self.moves = moves or []  # Chuỗi các bước di chuyển
                self.fitness = fitness    # Độ thích nghi (nhỏ hơn = tốt hơn)
            
            def __lt__(self, other):
                return self.fitness < other.fitness
        
        # Các hướng di chuyển: lên, phải, xuống, trái
        directions = ["up", "right", "down", "left"]
        
        # Hàm tạo cá thể ngẫu nhiên (chuỗi các bước di chuyển)
        def create_random_individual(length):
            return Individual(moves=[random.choice(directions) for _ in range(length)])
        
        # Hàm tính độ thích nghi (dựa trên heuristic)
        def calculate_fitness(individual):
            # Bắt đầu từ trạng thái ban đầu
            state = copy.deepcopy(self.initial_state)
            
            # Áp dụng các bước di chuyển của cá thể
            for move in individual.moves:
                # Tìm vị trí ô trống
                i, j = self.get_blank_position(state)
                
                # Di chuyển ô trống theo hướng đã chọn
                if move == "up" and i > 0:
                    state[i][j], state[i-1][j] = state[i-1][j], state[i][j]
                elif move == "right" and j < 2:
                    state[i][j], state[i][j+1] = state[i][j+1], state[i][j]
                elif move == "down" and i < 2:
                    state[i][j], state[i+1][j] = state[i+1][j], state[i][j]
                elif move == "left" and j > 0:
                    state[i][j], state[i][j-1] = state[i][j-1], state[i][j]
            
            # Tính độ thích nghi (khoảng cách Manhattan + độ dài chuỗi di chuyển)
            distance = self.calculate_heuristic(state)
            return distance + len(individual.moves) * 0.01
        
        # Hàm lai ghép hai cá thể
        def crossover(parent1, parent2):
            if random.random() > CROSSOVER_RATE:
                return parent1
            
            # Chọn điểm cắt
            min_length = min(len(parent1.moves), len(parent2.moves))
            if min_length < 2:
                return parent1
            
            crossover_point = random.randint(1, min_length - 1)
            
            # Tạo con cái bằng cách kết hợp gen của bố mẹ
            child_moves = parent1.moves[:crossover_point] + parent2.moves[crossover_point:]
            return Individual(moves=child_moves)
        
        # Hàm đột biến cá thể
        def mutate(individual):
            mutated_moves = individual.moves.copy()
            
            for i in range(len(mutated_moves)):
                if random.random() < MUTATION_RATE:
                    mutated_moves[i] = random.choice(directions)
            
            # Có một số trường hợp thêm hoặc bớt gen
            if random.random() < MUTATION_RATE and len(mutated_moves) > 1:
                # Bớt một gen
                idx = random.randint(0, len(mutated_moves) - 1)
                mutated_moves.pop(idx)
            elif random.random() < MUTATION_RATE:
                # Thêm một gen
                mutated_moves.append(random.choice(directions))
            
            return Individual(moves=mutated_moves)
        
        # Hàm chọn cá thể bằng phương pháp tournament selection
        def selection(population):
            tournament_size = 5
            tournament = random.sample(population, tournament_size)
            return min(tournament, key=lambda x: x.fitness)
        
        # Kiểm tra xem một cá thể có giải quyết vấn đề không
        def is_solution(individual):
            state = copy.deepcopy(self.initial_state)
            
            # Áp dụng các bước di chuyển
            for move in individual.moves:
                i, j = self.get_blank_position(state)
                
                if move == "up" and i > 0:
                    state[i][j], state[i-1][j] = state[i-1][j], state[i][j]
                elif move == "right" and j < 2:
                    state[i][j], state[i][j+1] = state[i][j+1], state[i][j]
                elif move == "down" and i < 2:
                    state[i][j], state[i+1][j] = state[i+1][j], state[i][j]
                elif move == "left" and j > 0:
                    state[i][j], state[i][j-1] = state[i][j-1], state[i][j]
            
            return self.is_goal(state), state
        
        # Chuyển đổi chuỗi di chuyển thành đường đi Node
        def moves_to_path(moves, final_state):
            path = []
            state = copy.deepcopy(self.initial_state)
            path.append(Node(state=copy.deepcopy(state), heuristic=self.calculate_heuristic(state)))
            
            for idx, move in enumerate(moves):
                i, j = self.get_blank_position(state)
                
                if move == "up" and i > 0:
                    state[i][j], state[i-1][j] = state[i-1][j], state[i][j]
                elif move == "right" and j < 2:
                    state[i][j], state[i][j+1] = state[i][j+1], state[i][j]
                elif move == "down" and i < 2:
                    state[i][j], state[i+1][j] = state[i+1][j], state[i][j]
                elif move == "left" and j > 0:
                    state[i][j], state[i][j-1] = state[i][j-1], state[i][j]
                
                node = Node(
                    state=copy.deepcopy(state),
                    parent=path[-1],
                    action=move,
                    path_cost=idx + 1,
                    depth=idx + 1,
                    heuristic=self.calculate_heuristic(state)
                )
                path.append(node)
            
            return path
        
        # Khởi tạo quần thể ban đầu
        initial_length = 20  # Độ dài chuỗi gen ban đầu
        population = [create_random_individual(random.randint(10, initial_length)) for _ in range(POPULATION_SIZE)]
        
        # Tính độ thích nghi cho toàn bộ quần thể
        for individual in population:
            individual.fitness = calculate_fitness(individual)
        
        best_solution = None
        best_solution_state = None
        
        # Vòng lặp chính của thuật toán di truyền
        for generation in range(MAX_GENERATIONS):
            if not self.is_solving:
                break
            
            # Sắp xếp quần thể theo độ thích nghi
            population.sort()
            
            # Kiểm tra cá thể tốt nhất
            is_sol, final_state = is_solution(population[0])
            if is_sol:
                best_solution = population[0]
                best_solution_state = final_state
                break
            
            # Hiển thị thông tin về thế hệ hiện tại
            self.root.after(0, lambda gen=generation, best_fit=population[0].fitness:
                self.steps_text.insert(tk.END, f"Generation {gen}: Best fitness={best_fit:.2f}\n"))
            
            # Tạo thế hệ mới
            new_population = []
            
            # Giữ lại elite
            new_population.extend(population[:ELITE_SIZE])
            
            # Tạo phần còn lại của quần thể qua lai ghép và đột biến
            while len(new_population) < POPULATION_SIZE:
                parent1 = selection(population)
                parent2 = selection(population)
                
                child = crossover(parent1, parent2)
                child = mutate(child)
                
                child.fitness = calculate_fitness(child)
                new_population.append(child)
            
            population = new_population
        
        # Kết thúc thuật toán, trả về đường đi nếu tìm thấy giải pháp
        if best_solution:
            return moves_to_path(best_solution.moves, best_solution_state)
        
        # Nếu không tìm thấy giải pháp hoàn hảo, trả về đường đi tốt nhất
        population.sort()
        best_individual = population[0]
        _, final_state = is_solution(best_individual)
        return moves_to_path(best_individual.moves, final_state)
    def searching_with_no_observation(self):
    # Định nghĩa belief state ban đầu (chỉ có một trạng thái - trạng thái ban đầu)
        initial_belief_state = {str(self.initial_state)}
        
        # Hàng đợi chứa các chuỗi hành động và belief state tương ứng
        queue = deque([([], initial_belief_state)])
        
        # Set lưu các belief state đã thăm
        visited_belief_states = {frozenset(initial_belief_state)}
        
        # Giới hạn độ sâu tìm kiếm
        max_depth = 30
        
        while queue and self.is_solving:
            # Lấy ra chuỗi hành động và belief state hiện tại
            actions, current_belief_state = queue.popleft()
            
            # Kiểm tra nếu đã vượt quá độ sâu cho phép
            if len(actions) >= max_depth:
                continue
            
            # Kiểm tra xem belief state hiện tại có chứa trạng thái đích không
            if all(self.is_goal(eval(state)) for state in current_belief_state):
                # Nếu tất cả trạng thái trong belief state là trạng thái đích
                # Tạo đường đi từ chuỗi hành động
                return self.actions_to_path(actions)
            
            # Thử tất cả các hướng di chuyển có thể
            for action in ["up", "right", "down", "left"]:
                # Khởi tạo belief state mới
                new_belief_state = set()
                
                # Áp dụng hành động cho tất cả trạng thái trong belief state hiện tại
                for state_str in current_belief_state:
                    state = eval(state_str)
                    # Tìm vị trí của ô trống
                    i, j = self.get_blank_position(state)
                    
                    # Di chuyển ô trống theo hướng đã chọn nếu có thể
                    new_state = copy.deepcopy(state)
                    moved = False
                    
                    if action == "up" and i > 0:
                        new_state[i][j], new_state[i-1][j] = new_state[i-1][j], new_state[i][j]
                        moved = True
                    elif action == "right" and j < 2:
                        new_state[i][j], new_state[i][j+1] = new_state[i][j+1], new_state[i][j]
                        moved = True
                    elif action == "down" and i < 2:
                        new_state[i][j], new_state[i+1][j] = new_state[i+1][j], new_state[i][j]
                        moved = True
                    elif action == "left" and j > 0:
                        new_state[i][j], new_state[i][j-1] = new_state[i][j-1], new_state[i][j]
                        moved = True
                    
                    if moved:
                        new_belief_state.add(str(new_state))
                    else:
                        # Nếu không thể di chuyển theo hướng này, giữ nguyên trạng thái
                        new_belief_state.add(state_str)
                
                # Chuyển đổi belief state mới thành frozenset để có thể hash
                new_belief_state_frozen = frozenset(new_belief_state)
                
                # Kiểm tra xem belief state mới đã được thăm chưa
                if new_belief_state_frozen not in visited_belief_states:
                    # Thêm vào hàng đợi
                    queue.append((actions + [action], new_belief_state))
                    visited_belief_states.add(new_belief_state_frozen)
        
        # Không tìm thấy giải pháp
        return []

    def actions_to_path(self, actions):
        # Chuyển đổi chuỗi hành động thành đường đi Node
        path = []
        state = copy.deepcopy(self.initial_state)
        path.append(Node(state=copy.deepcopy(state), heuristic=self.calculate_heuristic(state)))
        
        for idx, action in enumerate(actions):
            i, j = self.get_blank_position(state)
            
            moved = False
            if action == "up" and i > 0:
                state[i][j], state[i-1][j] = state[i-1][j], state[i][j]
                moved = True
            elif action == "right" and j < 2:
                state[i][j], state[i][j+1] = state[i][j+1], state[i][j]
                moved = True
            elif action == "down" and i < 2:
                state[i][j], state[i+1][j] = state[i+1][j], state[i][j]
                moved = True
            elif action == "left" and j > 0:
                state[i][j], state[i][j-1] = state[i][j-1], state[i][j]
                moved = True
            
            if moved:
                node = Node(
                    state=copy.deepcopy(state),
                    parent=path[-1],
                    action=action,
                    path_cost=idx + 1,
                    depth=idx + 1,
                    heuristic=self.calculate_heuristic(state)
                )
                path.append(node)
        
        return path
    def partially_observable_search(self):
        """
        Thuật toán tìm kiếm cho môi trường quan sát một phần.
        
        Trong môi trường quan sát một phần, chúng ta không biết chính xác trạng thái hiện tại của hệ thống.
        Thay vào đó, chúng ta duy trì một "belief state" - tập hợp các trạng thái có thể.
        """
        # Đối với puzzle, giả định rằng một số ô bị che khuất (không thể quan sát)
        # Mô phỏng bằng cách che một số ô ngẫu nhiên
        
        # Số ô che khuất (có thể điều chỉnh)
        NUM_HIDDEN_TILES = 3
        
        # Tạo một bản sao của trạng thái ban đầu để không làm ảnh hưởng trạng thái gốc
        observable_state = copy.deepcopy(self.initial_state)
        
        # Chọn ngẫu nhiên các ô để che khuất (không bao gồm ô trống)
        all_positions = [(i, j) for i in range(3) for j in range(3)]
        blank_i, blank_j = self.get_blank_position(observable_state)
        non_blank_positions = [pos for pos in all_positions if pos != (blank_i, blank_j)]
        hidden_positions = random.sample(non_blank_positions, min(NUM_HIDDEN_TILES, len(non_blank_positions)))
        
        # Tạo bản đồ quan sát, với -1 đại diện cho ô bị che khuất
        observation_map = copy.deepcopy(observable_state)
        for i, j in hidden_positions:
            observation_map[i][j] = -1  # -1 đại diện cho ô không biết
        
        # Hiển thị thông tin về bản đồ quan sát
        self.root.after(0, lambda: self.steps_text.insert(tk.END, 
                        f"Partially Observable Search: {NUM_HIDDEN_TILES} ô bị che khuất\n"
                        f"Bản đồ quan sát: {observation_map}\n"))
        
        # Khởi tạo belief state - các trạng thái có thể
        # Ban đầu, chúng ta có thể xem xét tất cả các trạng thái hợp lệ có thể có
        # trong đó các ô không bị che khuất khớp với giá trị quan sát được
        
        # Giới hạn số lượng trạng thái khả thi để tránh không gian tìm kiếm quá lớn
        MAX_BELIEF_SIZE = 50
        
        # Tạo các trạng thái khả thi ngẫu nhiên dựa trên quan sát
        belief_states = []
        
        # Thêm trạng thái thực tế (đã biết) vào belief state
        belief_states.append(self.initial_state)
        
        # Tạo một số trạng thái khả thi khác dựa trên quan sát
        # Lưu ý: Trong thực tế, bạn sẽ tạo ra các trạng thái phù hợp với quan sát một cách có hệ thống
        for _ in range(min(MAX_BELIEF_SIZE - 1, 10)):  # Giới hạn số lượng để đơn giản hóa
            possible_state = copy.deepcopy(observation_map)
            
            # Điền các giá trị ngẫu nhiên vào các ô bị che khuất
            hidden_values = [observable_state[i][j] for i, j in hidden_positions]
            random.shuffle(hidden_values)
            
            for idx, (i, j) in enumerate(hidden_positions):
                possible_state[i][j] = hidden_values[idx]
            
            belief_states.append(possible_state)
        
        # Hiển thị số lượng trạng thái niềm tin
        self.root.after(0, lambda: self.steps_text.insert(tk.END, 
                        f"Số trạng thái niềm tin ban đầu: {len(belief_states)}\n"))
        
        # Thiết lập các thông số cho thuật toán POMDP
        MAX_STEPS = 50
        current_steps = 0
        
        # Lưu lại đường đi tốt nhất
        best_path = []
        best_cost = float('inf')
        
        # Thuật toán chính cho POMDP đơn giản
        while current_steps < MAX_STEPS and self.is_solving:
            # Chọn trạng thái niềm tin có xác suất cao nhất
            # Ở đây đơn giản hóa bằng cách chọn ngẫu nhiên một trạng thái từ belief state
            # Trong thực tế, bạn sẽ sử dụng xác suất và kỳ vọng
            current_belief = random.choice(belief_states)
            
            # Tạo một node từ trạng thái niềm tin hiện tại
            current_node = Node(state=current_belief, heuristic=self.calculate_heuristic(current_belief))
            
            # Thực hiện một bước tìm kiếm A* từ trạng thái niềm tin hiện tại
            # (Giả sử trạng thái này là trạng thái thực tế)
            temp_path = self.a_star_search_from_state(current_belief)
            
            # Nếu tìm thấy đường đi tốt hơn, cập nhật
            if temp_path and len(temp_path) < best_cost:
                best_path = temp_path
                best_cost = len(temp_path)
                
                # Hiển thị thông tin cập nhật
                self.root.after(0, lambda cost=best_cost: self.steps_text.insert(tk.END, 
                                f"Tìm thấy đường đi tốt hơn với chi phí: {cost}\n"))
                
                # Nếu tìm thấy đường đi đủ tốt, dừng lại
                if best_cost < 20:  # Ngưỡng có thể điều chỉnh
                    break
            
            # Cập nhật belief state dựa trên hành động và quan sát mới
            # (Đơn giản hóa - trong thực tế, bạn sẽ cập nhật dựa trên mô hình chuyển đổi)
            if len(belief_states) > 1:
                belief_states.pop(0)  # Đơn giản là loại bỏ trạng thái hiện tại
                
            current_steps += 1
        
        # Trả về đường đi tốt nhất tìm được
        return best_path if best_path else []

    # Hàm bổ sung để thực hiện A* từ một trạng thái bất kỳ
    def a_star_search_from_state(self, start_state):
        initial_node = Node(state=start_state, heuristic=self.calculate_heuristic(start_state))
        initial_node.f = initial_node.path_cost + initial_node.heuristic
        
        if self.is_goal(initial_node.state):
            return [initial_node]
        
        open_set = []
        heapq.heappush(open_set, (initial_node.f, id(initial_node), initial_node))
        closed_set = set()
        
        while open_set and self.is_solving:
            _, _, node = heapq.heappop(open_set)
            state_str = str(node.state)
            
            if state_str in closed_set:
                continue
            
            closed_set.add(state_str)
            
            if self.is_goal(node.state):
                return self.get_solution_path(node)
            
            successors = self.get_successors(node)
            for successor in successors:
                successor.f = successor.path_cost + successor.heuristic
                heapq.heappush(open_set, (successor.f, id(successor), successor))
        
        return []
    def test_based_search(self):
        # Khởi tạo node ban đầu
        initial_node = Node(state=self.initial_state, heuristic=self.calculate_heuristic(self.initial_state))
        
        if self.is_goal(initial_node.state):
            return [initial_node]
        
        # Tham số cho thuật toán
        max_tests = 10000  # Số lượng kiểm thử tối đa
        max_depth = 50    # Độ sâu tối đa cho mỗi kiểm thử
        
        # Lưu trữ trạng thái đã thăm
        visited = set()
        best_node = initial_node
        
        for test in range(max_tests):
            if not self.is_solving:
                break
            
            # Khởi tạo lại từ trạng thái ban đầu cho mỗi kiểm thử
            current_node = Node(state=copy.deepcopy(self.initial_state), 
                            heuristic=self.calculate_heuristic(self.initial_state))
            path = [current_node]
            
            # Thực hiện một chuỗi các bước di chuyển ngẫu nhiên
            for depth in range(max_depth):
                if not self.is_solving:
                    break
                
                # Tìm các bước di chuyển hợp lệ
                successors = self.get_successors(current_node)
                if not successors:
                    break
                
                # Chọn successor ngẫu nhiên có xu hướng tốt hơn
                better_successors = [s for s in successors if s.heuristic <= current_node.heuristic]
                if better_successors and random.random() < 0.7:  # 70% thời gian chọn successor tốt hơn
                    next_node = random.choice(better_successors)
                else:
                    next_node = random.choice(successors)
                
                # Cập nhật node hiện tại
                current_node = next_node
                path.append(current_node)
                
                # Kiểm tra nếu đã đạt được mục tiêu
                if self.is_goal(current_node.state):
                    # Reconstruct path
                    return self.reconstruct_path(path)
                
                # Cập nhật node tốt nhất nếu tìm thấy
                if current_node.heuristic < best_node.heuristic:
                    best_node = current_node
                    
                # Cập nhật thông tin về quá trình tìm kiếm
                if test % 10 == 0 and depth % 5 == 0:
                    self.root.after(0, lambda: self.steps_text.insert(tk.END, 
                        f"Test: {test}, Depth: {depth}, Best heuristic: {best_node.heuristic}\n"))
        
        # Trả về rỗng nếu không tìm thấy giải pháp
        return []

    def reconstruct_path(self, path):
        # Xây dựng lại đường đi từ mảng các node
        result = []
        for i in range(len(path)):
            if i > 0:
                path[i].parent = path[i-1]
            result.append(path[i])
        return result
    
    def backtracking_search(self):
        """
        Thuật toán Backtracking Search cho bài toán 8-puzzle.
        Thử các bước đi có thể và quay lui khi gặp đường cụt.
        """
        initial_node = Node(state=self.initial_state, heuristic=self.calculate_heuristic(self.initial_state))
        
        if self.is_goal(initial_node.state):
            return [initial_node]
        
        # Thiết lập giới hạn độ sâu để tránh tìm kiếm vô hạn
        max_depth = 100
        
        # Tập hợp các trạng thái đã thăm (để tránh lặp)
        visited = set()
        
        # Gọi hàm đệ quy backtracking
        result = self._backtrack(initial_node, max_depth, visited)
        
        return result if result else []
        
    def _backtrack(self, node, max_depth, visited):
        """
        Hàm đệ quy cho thuật toán backtracking.
        
        Args:
            node: Node hiện tại đang xét
            max_depth: Độ sâu tối đa cho phép
            visited: Tập hợp các trạng thái đã thăm
        
        Returns:
            Đường đi giải nếu tìm thấy, None nếu không tìm thấy
        """
        # Kiểm tra nếu đã đạt độ sâu tối đa
        if node.depth > max_depth:
            return None
        
        # Chuyển trạng thái thành chuỗi để lưu vào tập visited
        state_str = str(node.state)
        
        # Kiểm tra nếu đã thăm trạng thái này
        if state_str in visited:
            return None
        
        # Thêm trạng thái hiện tại vào tập visited
        visited.add(state_str)
        
        # Kiểm tra nếu đã đạt đích
        if self.is_goal(node.state):
            return self.get_solution_path(node)
        
        # Nếu thuật toán đã dừng (người dùng nhấn nút dừng)
        if not self.is_solving:
            return None
        
        # Lấy các trạng thái kế tiếp
        successors = self.get_successors(node)
        
        # Sắp xếp các successor theo heuristic để thử các trạng thái có triển vọng nhất trước
        successors.sort(key=lambda x: x.heuristic)
        
        # Thử từng trạng thái kế tiếp
        for successor in successors:
            # Đệ quy với trạng thái kế tiếp
            result = self._backtrack(successor, max_depth, visited)
            
            # Nếu tìm thấy đường đi giải, trả về kết quả
            if result:
                return result
        
        # Nếu không tìm thấy giải pháp từ node hiện tại, quay lui
        return None
    def ac3_search(self):
        """
        Triển khai thuật toán AC3 cho bài toán 8-puzzle.
        """
          # Tạo nút ban đầu
        initial_node = Node(state=self.initial_state, heuristic=self.calculate_heuristic(self.initial_state))
        
        if self.is_goal(initial_node.state):
            return [initial_node]
        
         # Bắt đầu với một biên chứa duy nhất trạng thái ban đầu
        frontier = [initial_node]
        explored = set()
        
        # Tạo miền cho mỗi ô (chúng ta sẽ biểu diễn dưới dạng lưới 2D của các tập hợp)
        # Trong bài toán 8-puzzle tiêu chuẩn, mỗi ô về mặt kỹ thuật có thể chứa bất kỳ giá trị nào (0-8)
        # Nhưng chúng ta sẽ giới hạn dựa trên trạng thái hiện tại và khả năng tiếp cận
        
        while frontier and self.is_solving:
            # Lấy nút tiếp theo từ biên
            current_node = frontier.pop(0)
            current_state_str = str(current_node.state)
            
            if current_state_str in explored:
                continue
                
            explored.add(current_state_str)
            
            # Kiểm tra xem chúng ta đã đạt đến mục tiêu chưa
            if self.is_goal(current_node.state):
                return self.get_solution_path(current_node)
            
            # Áp dụng lan truyền ràng buộc AC3 để giảm không gian tìm kiếm
            # Trong ngữ cảnh 8-puzzle, điều này có nghĩa là loại bỏ các trạng thái không thể đạt được
            # và tập trung vào các nước đi hứa hẹn
            
            # Lấy các trạng thái kế tiếp hợp lệ sau khi áp dụng bộ lọc AC3
            successors = self.get_arc_consistent_successors(current_node)
            
            # Thêm các trạng thái kế tiếp đã lọc vào biên
            # Sắp xếp theo heuristic để ưu tiên các trạng thái hứa hẹn hơn
            successors.sort(key=lambda x: x.heuristic)
            frontier.extend(successors)
            
            # Định kỳ cập nhật giao diện người dùng với tiến trình
            if len(explored) % 10 == 0:
                self.root.after(0, lambda count=len(explored): 
                    self.steps_text.insert(tk.END, f"Tìm kiếm AC3: Đã khám phá {count} trạng thái\n"))
        
        return []  # No solution found

    def get_arc_consistent_successors(self, node):
        """
       Lấy các trạng thái kế tiếp sau khi áp dụng lọc ràng buộc AC3.
        """
          # Lấy tất cả các trạng thái kế tiếp có thể
        all_successors = self.get_successors(node)
        
        #  Nếu có rất ít trạng thái kế tiếp, không cần lọc
        if len(all_successors) <= 2:
            return all_successors
        
        # Tạo bản đồ các vị trí ô đến vị trí mục tiêu của chúng
        goal_positions = {}
        for i in range(3):
            for j in range(3):
                if self.goal_state[i][j] != 0:  # Bỏ qua ô trống
                    goal_positions[self.goal_state[i][j]] = (i, j)
        
        #Lọc các trạng thái kế tiếp dựa trên "tính nhất quán cung" được điều chỉnh cho 8-puzzle
        consistent_successors = []
        
        for successor in all_successors:
            # Kiểm tra bao nhiêu ô đang ở đúng vị trí
            correct_positions = 0
            for i in range(3):
                for j in range(3):
                    if successor.state[i][j] != 0 and successor.state[i][j] == self.goal_state[i][j]:
                        correct_positions += 1
            
            # Kiểm tra xem nước đi này có tạo ra "vi phạm ràng buộc" không - đặt một ô vào vị trí
            # mà sẽ đòi hỏi nhiều nước đi hơn để sửa sau này
            constraint_violations = 0
            
            # Tính toán "khoảng cách từ vị trí mục tiêu" cho mỗi ô
            for i in range(3):
                for j in range(3):
                    value = successor.state[i][j]
                    if value != 0:
                        goal_i, goal_j = goal_positions[value]
                        # Nếu một ô di chuyển xa hơn khỏi vị trí mục tiêu của nó, tính là vi phạm
                        curr_dist = abs(i - goal_i) + abs(j - goal_j)
                        
                         # Tìm cùng giá trị trong trạng thái cha
                        parent_i, parent_j = None, None
                        for pi in range(3):
                            for pj in range(3):
                                if node.state[pi][pj] == value:
                                    parent_i, parent_j = pi, pj
                                    break
                        
                        if parent_i is not None:
                            parent_dist = abs(parent_i - goal_i) + abs(parent_j - goal_j)
                            if curr_dist > parent_dist: # Nếu nước đi này tăng khoảng cách từ mục tiêu, tính là vi phạm
                                constraint_violations += 1
            
           # Mục tiêu ưu tiên:
            # 1. Các nước đi tăng số vị trí đúng
            # 2. Các nước đi với ít vi phạm ràng buộc hơn
            # 3. Các nước đi với giá trị heuristic thấp hơn
            
            # # Thêm điểm tổng hợp cho nút kế tiếp
            successor.arc_score = (
                -correct_positions,  # Âm để giá trị thấp hơn là tốt hơn
                constraint_violations,
                successor.heuristic
            )
            
            consistent_successors.append(successor)
        
        # Sắp xếp theo điểm tính nhất quán cung tổng hợp của chúng ta
        consistent_successors.sort(key=lambda x: x.arc_score)
        
        # Trả về N trạng thái kế tiếp nhất quán nhất (giảm hệ số phân nhánh)
        return consistent_successors[:3]  
    def qlearning_solve(self):
        # Q-table để lưu trữ giá trị Q
        q_table = {}
        
        # Các tham số thuật toán Q-Learning
        learning_rate = 0.2  # Tăng tốc độ học
        discount_factor = 0.99  # Tăng trọng số của phần thưởng tương lai
        exploration_rate = 1.0
        exploration_decay = 0.99  # Giảm exploration nhanh hơn
        min_exploration_rate = 0.01
        
        # Chuyển đổi trạng thái thành khóa để lưu trong Q-table
        def state_to_key(state):
            return tuple(tuple(row) for row in state)
        
        # Tính toán phần thưởng tinh vi hơn
        def calculate_reward(current_state, next_state):
            # Đánh giá mức độ tiến gần đến trạng thái đích
            current_heuristic = self.calculate_heuristic(current_state)
            next_heuristic = self.calculate_heuristic(next_state)
            
            # Phần thưởng dựa trên sự cải thiện heuristic
            if self.is_goal(next_state):
                return 100  # Phần thưởng lớn khi giải được puzzle
            elif next_heuristic < current_heuristic:
                return 10  # Phần thưởng khi tiến gần hơn đến đích
            elif next_heuristic > current_heuristic:
                return -10  # Trừ điểm nếu di chuyển xa mục tiêu hơn
            else:
                return -1  # Phần thưởng nhỏ âm cho các bước không cải thiện
        
        # Khởi tạo node ban đầu
        initial_node = Node(
            state=self.initial_state, 
            heuristic=self.calculate_heuristic(self.initial_state)
        )
        
        # Tăng số lượng episodes và steps
        max_episodes = 10000  # Tăng số lượng episodes
        max_steps_per_episode = 200  # Tăng số bước mỗi episode
        
        # Lưu trữ đường đi giải quyết
        best_solution_path = None
        best_heuristic = float('inf')
        
        for episode in range(max_episodes):
            # Dừng nếu không còn đang giải
            if not self.is_solving:
                break
            
            # Trạng thái hiện tại
            current_state = copy.deepcopy(self.initial_state)
            current_node = Node(
                state=current_state, 
                heuristic=self.calculate_heuristic(current_state)
            )
            
            # Lưu trữ đường đi của episode này
            episode_path = [current_node]
            
            # Chạy từng bước trong episode
            for step in range(max_steps_per_episode):
                # Lấy các trạng thái kế tiếp
                successors = self.get_successors(current_node)
                
                # Nếu không có successor thì thoát
                if not successors:
                    break
                
                # Chiến lược lựa chọn hành động (Epsilon-Greedy)
                if random.random() < exploration_rate:
                    # Khám phá: chọn ngẫu nhiên
                    next_node = random.choice(successors)
                else:
                    # Khai thác: chọn successor tốt nhất dựa trên Q-value
                    state_key = state_to_key(current_state)
                    
                    # Nếu chưa có Q-value cho trạng thái này, khởi tạo
                    if state_key not in q_table:
                        q_table[state_key] = {}
                    
                    # Tìm successor với Q-value cao nhất
                    def get_q_value(successor):
                        action = successor.action
                        return q_table[state_key].get(action, 0)
                    
                    next_node = max(successors, key=get_q_value, default=successors[0])
                
                # Tính toán phần thưởng
                reward = calculate_reward(current_state, next_node.state)
                
                # Cập nhật Q-value
                state_key = state_to_key(current_state)
                next_state_key = state_to_key(next_node.state)
                
                # Khởi tạo Q-value nếu chưa tồn tại
                if state_key not in q_table:
                    q_table[state_key] = {}
                if next_state_key not in q_table:
                    q_table[next_state_key] = {}
                
                # Tìm Q-value tối đa của trạng thái tiếp theo
                max_next_q = max(q_table[next_state_key].values(), default=0)
                
                # Cập nhật Q-value cho hành động
                current_q = q_table[state_key].get(next_node.action, 0)
                new_q = current_q + learning_rate * (
                    reward + discount_factor * max_next_q - current_q
                )
                q_table[state_key][next_node.action] = new_q
                
                # Thêm node vào đường đi
                episode_path.append(next_node)
                
                # Chuyển sang trạng thái mới
                current_state = next_node.state
                current_node = next_node
                
                # Kiểm tra đích
                if self.is_goal(current_state):
                    # Nếu tìm thấy giải pháp, lưu lại
                    solution_path = self.get_solution_path(current_node)
                    return solution_path
                
                # Kiểm tra nếu đã tìm được giải pháp gần nhất
                current_heuristic = self.calculate_heuristic(current_state)
                if current_heuristic < best_heuristic:
                    best_heuristic = current_heuristic
                    best_solution_path = self.get_solution_path(current_node)
            
            # Giảm tỷ lệ khám phá
            exploration_rate = max(
                min_exploration_rate, 
                exploration_rate * exploration_decay
            )
            
            # Ghi nhận tiến trình mỗi 100 episode
            if episode % 100 == 0:
                self.root.after(0, lambda e=episode, er=exploration_rate, h=best_heuristic: 
                    self.steps_text.insert(tk.END, 
                    f"Q-Learning Episode {e}, Exploration Rate: {er:.4f}, Best Heuristic: {h}\n"))
        
        # Nếu không tìm thấy giải pháp hoàn chỉnh, trả về giải pháp gần nhất
        return best_solution_path or [initial_node]
if __name__ == "__main__":
    app = EightPuzzle()
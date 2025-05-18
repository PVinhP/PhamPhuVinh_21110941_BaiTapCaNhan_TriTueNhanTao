# PhamPhuVinh_21110941_BaiTapCaNhan_TriTueNhanTao

# Bài Tập Cá Nhân Trí Tuệ Nhân Tạo – 8-Puzzle
**Sinh viên**: Phạm Phú Vinh  
**MSSV**: 21110941  
**Môn học**: Trí Tuệ Nhân Tạo  
**Đề tài**: Áp dụng các thuật toán tìm kiếm để giải bài toán 8-Puzzle

## 1. Mục tiêu:
- Áp dụng các thuật toán tìm kiếm khác nhau để giải quyết bài toán 8-Puzzle 
- Hiểu được nguyên lý, điểm mạnh, điểm yếu của từng thuật toán, nhóm thuật toán
- So sánh hiệu suất của thuật toán dựa trên:
  - Thời gian thực thi và bộ nhớ sử dụng
  - Độ chính xác (thuật toán có tối ưu hay không)
  - Tính khả thi với bài toán có không gian trạng thái lớn
- Gồm 6 nhóm thuật toán :
  - Tìm kiếm không có thông tin: BFS, DFS, IDS, UCS.
  - Tìm kiếm có thông tin: Greedy Best-First Search, A*, IDA*
  - Tìm kiếm cục bộ: Simple Hill Climbing, Steepest Ascent Hill Climbing, Stochastic Hill Climbing, Beam, Genetic Algorithm
  - Tìm kiếm trong môi trường phức tạp: And-Or Search, Belief, Partially
  - Tìm kiếm trong môi trường ràng buộc: Kiểm thử, Backtracking, AC-3
  - Học tăng cường: Q-Learning
## 2. Nội dung:
### 2.1. Nhóm 1: Thuật toán không có thông tin (Uninformed Search)
#### Breadth-First Search (BFS) – Tìm kiếm theo chiều rộng
Khái Niệm: Breadth-First Search là thuật toán tìm kiếm theo chiều rộng mở rộng các nút theo thứ tự tạo
(FIFO). BFS là thuật toán tìm kiếm mù: không sử dụng thông tin ngoại trừ của
không gian trạng thái và là thuật toán tối ưu nếu tất cả các hành động có cùng chi phí. Gồm 2 biến thể:
- BFS-Tree: Tìm kiếm theo chiều rộng có thể được thực hiện mà không cần
loại bỏ trùng lặp (như tìm kiếm cây)
- BFS-Graph: Tìm kiếm theo chiều rộng có loại bỏ trùng lặp (như tìm kiếm đồ thị)



https://github.com/user-attachments/assets/3086be3e-0090-4a76-8055-e3eae0673b1b




#### Depth-First Search (DFS) – Tìm kiếm theo chiều sâu
Tìm kiếm theo chiều sâu (DFS) mở rộng các nút theo thứ tự nút sâu nhất mở rộng trước (LIFO). danh sách mở được triển khai dưới dạng ngăn xếp.


#### Uniform Cost Search (UCS) – Tìm kiếm theo chi phí thống nhất
UCS là một thuật toán tìm kiếm không có thông tin (Uninformed search algorithms) dựa trên chi phí. Thuật toán sẽ tìm đường đi ngắn nhất giữa hai điểm bằng cách mở rộng các trạng thái theo chi phí thấp nhất. UCS luôn ưu tiên các con đường có chi phí thấp nhất để đạt được đích, giúp đảm bảo rằng tìm được con đường tối ưu nhất trong các môi trường có chi phí thay đổi.



https://github.com/user-attachments/assets/8659a05d-3f4e-45de-ba8b-3048bc561b7f



#### Iterative Deepening DFS (IDS) – Tìm kiếm chiều sâu lặp


https://github.com/user-attachments/assets/ef7222f1-4f82-4de2-a28c-f8be587a6eb3




### 2.2. Nhóm 2: Thuật toán có thông tin (Informed / Heuristic Search)
- Greedy Search – Tìm kiếm tham lam
- A* – Tìm kiếm A sao
- Iterative Deepening A* (IDA*) – Tìm kiếm A sao theo chiều sâu lặp

### 2.3. Nhóm 3: Tìm kiếm cục bộ (Local Search)
- Hill Climbing
  - Simple Hill Climbing
  - Steepest-Ascent Hill Climbing
  - Stochastic Hill Climbing
- Simulated Annealing – Ủ mô phỏng
- Genetic Algorithms – Thuật toán di truyền
- Beam Search – Tìm kiếm chùm tia

### 2.4. Nhóm 4: Tìm kiếm trong môi trường phức tạp
- Tree Search AND–OR
- Partially Observable Search – Quan sát một phần
- Unknown or Dynamic Environment – Môi trường động hoặc không biết trước

### 2.5. Nhóm 5: Tìm kiếm có ràng buộc (Constraint Satisfaction)
- Backtracking Search
- Forward Checking
- AC-3 – Thuật toán kiểm tra tính nhất quán

### 2.6. Nhóm 6: Học tăng cường (Reinforcement Learning)
- Q-Learning

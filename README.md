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

Thuật toán BFS tìm được lời giải tối ưu nếu chi phí đồng đều, nhưng tốn nhiều bộ nhớ. Không phù hợp với không gian trạng thái lớn.


#### Depth-First Search (DFS) – Tìm kiếm theo chiều sâu
Tìm kiếm theo chiều sâu (DFS) mở rộng các nút theo thứ tự nút sâu nhất mở rộng trước (LIFO). danh sách mở được triển khai dưới dạng ngăn xếp.



https://github.com/user-attachments/assets/235d77dc-5ff7-4350-83b1-f0036f9c59e7


Thuật toán DFS(Depth-First Search): Đi càng sâu càng tốt trước khi quay lại. Ít tốn bộ nhớ nhưng có thể rơi vào vòng lặp vô hạn hoặc lời giải không tối ưu.


#### Uniform Cost Search (UCS) – Tìm kiếm theo chi phí thống nhất
UCS là một thuật toán tìm kiếm không có thông tin (Uninformed search algorithms) dựa trên chi phí. Thuật toán sẽ tìm đường đi ngắn nhất giữa hai điểm bằng cách mở rộng các trạng thái theo chi phí thấp nhất. UCS luôn ưu tiên các con đường có chi phí thấp nhất để đạt được đích, giúp đảm bảo rằng tìm được con đường tối ưu nhất trong các môi trường có chi phí thay đổi.



https://github.com/user-attachments/assets/8659a05d-3f4e-45de-ba8b-3048bc561b7f

UCS: Tìm được lời giải tối ưu, thích hợp cho bài toán có chi phí không đồng đều, nhưng chậm hơn BFS trong một số trường hợp.

#### Iterative Deepening DFS (IDS) – Tìm kiếm chiều sâu lặp

IDS là sự kết hợp giữa DFS và BFS. Thuật toán thực hiện DFS giới hạn độ sâu, sau đó tăng dần giới hạn này. IDS có ưu điểm là đảm bảo tìm được lời giải tối ưu giống BFS, nhưng sử dụng ít bộ nhớ như DFS. Đây là một lựa chọn tốt cho bài toán với không gian tìm kiếm lớn.
https://github.com/user-attachments/assets/ef7222f1-4f82-4de2-a28c-f8be587a6eb3


Thuật toán IDS Kết hợp ưu điểm của BFS và DFS, đảm bảo tìm lời giải nếu có, ít tốn bộ nhớ hơn BFS, nhưng thời gian tăng do lặp lại.

### 2.2. Nhóm 2: Thuật toán có thông tin (Informed / Heuristic Search)
#### Greedy Search – Tìm kiếm tham lam
Greedy Search là một thuật toán tìm kiếm có thông tin sử dụng hàm heuristic để đánh giá trạng thái nào có vẻ gần đích nhất và mở rộng nó trước. Tuy nhanh và tiết kiệm tài nguyên, thuật toán không đảm bảo tìm được lời giải tối ưu nếu heuristic không tốt, và có thể bị mắc kẹt tại các điểm cục bộ.


https://github.com/user-attachments/assets/73eac389-cc01-4a1b-9e28-e774ed624d92

Greedy Search: Nhanh nhưng không đảm bảo tìm lời giải tối ưu. Phụ thuộc vào hàm heuristic.

#### Thuật toán tìm kiếm A* 
A* là một thuật toán tìm kiếm có thông tin, cân bằng giữa chi phí và heuristic: chi phí thực tế từ gốc đến nút hiện tại (g(n)) và chi phí ước lượng từ nút đó đến đích (h(n)). A* tìm được lời giải tối ưu nếu hàm heuristic là chấp nhận được (admissible).


https://github.com/user-attachments/assets/7e18126b-b77a-483e-9708-af33d1cad8e0

A*: Cân bằng giữa chi phí và heuristic, tìm lời giải tối ưu nếu hàm heuristic là chấp nhận được (admissible).
#### Thuật toán tìm kiếm IDA* 
Kết hợp giữa A* và IDS, tiết kiệm bộ nhớ, nhưng thời gian có thể lớn hơn A*. Thuật toán thực hiện tìm kiếm theo chiều sâu có giới hạn chi phí (f-limit), lặp đi lặp lại với ngưỡng tăng dần. Nhờ vậy, IDA* có thể giải các bài toán lớn mà A* không đủ bộ nhớ để xử lý.


https://github.com/user-attachments/assets/f4d5a574-8a56-43ae-9ead-9789cdbdec60

IDA*: Kết hợp giữa A* và IDS, tiết kiệm bộ nhớ, nhưng thời gian có thể lớn hơn A*.

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

# 3. Kết luận
Qua việc áp dụng các thuật toán tìm kiếm vào bài toán 8-Puzzle, em rút ra được một số kết luận như sau:

Không có thuật toán nào là tốt nhất trong mọi trường hợp. Mỗi thuật toán có ưu và nhược điểm riêng.

Các thuật toán có thông tin (như A*) thường cho kết quả tối ưu và nhanh hơn, nếu thiết kế được hàm heuristic tốt.

Các thuật toán không có thông tin phù hợp cho việc minh họa nguyên lý tìm kiếm, nhưng kém hiệu quả hơn khi không gian trạng thái lớn.

Thuật toán cục bộ và học tăng cường thể hiện tiềm năng trong các bài toán mở rộng, cần tinh chỉnh tham số để đạt hiệu quả.

Việc so sánh giúp em hiểu rõ hơn về cách lựa chọn thuật toán phù hợp trong các bài toán cụ thể và đánh giá hiệu suất của từng giải pháp một cách có hệ thống.

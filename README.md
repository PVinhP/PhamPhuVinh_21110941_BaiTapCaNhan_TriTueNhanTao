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




https://github.com/user-attachments/assets/91c4862d-c667-40fb-ae2b-b2ba95725bc6



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
### Hill Climbing
Thuật toán leo đồi (Hill Climbing) là thuật toán tìm kiếm thuộc nhóm tìm kiếm cục bộ (local search) lấy cảm hứng từ việc leo lên đỉnh núi. Trong đó, mục tiêu là tìm ra giải pháp tốt nhất từ ​​một tập hợp các giải pháp khả thi nên thường được sử dụng để giải các bài toán tối ưu hóa. Thuật toán hoạt động bằng cách bắt đầu từ một trạng thái ban đầu và liên tục di chuyển đến trạng thái lân cận tốt hơn (theo một hàm đánh giá) cho đến khi không còn trạng thái lân cận nào tốt hơn hoặc đạt được mục tiêu.

#### Simple Hill Climbing
Simple hill Climbing (Leo đồi đơn giản) là cách đơn giản nhất để triển khai thuật toán leo đồi , thuật toán chỉ kiểm tra từng trạng thái lận cận của nó và nếu nó tìm thấy trạng thái tốt hơn trạng thái hiện tại thì di chuyển.


https://github.com/user-attachments/assets/78603334-dfc8-49c0-acfc-7cdabba87d6b

Simple Hill Climbing: Luôn chọn bước tiếp theo tốt hơn hiện tại. Dễ bị kẹt ở đỉnh cục bộ, không đảm bảo tìm được lời giải tối ưu.
#### Steepest-Ascent Hill Climbing
Steepest-Ascent hill climbing (Leo đồi dốc nhất) Là một biến thể của thuật toán leo đồi đơn giản. Thuật toán này kiểm tra tất cả các nút lân cận của trạng thái hiện tại và chọn một nút lân cận gần nhất với trạng thái mục tiêu.


https://github.com/user-attachments/assets/e2a2c3bd-42f3-4f7f-a434-c7269637d813
Steepest-Ascent Hill Climbing: Xét tất cả lân cận và chọn bước cải thiện tốt nhất. Giảm xác suất kẹt tại điểm xấu, nhưng vẫn không thoát được các đỉnh cục bộ.

#### Stochastic Hill Climbing
Stochastic hill Climbing (Leo đồi ngẫu nhiên) Là một biến thể của thuật toán leo đồi đơn giản. Thay vì tìm ra hàng xóm tốt nhất, phiên bản này lựa chọn ngẫu nhiên một hàng xóm. Nếu hàng xóm đó tốt hơn trạng thái hiện thời, hàng xóm đó sẽ được chọn làm trạng thái hiện thời và thuật toán lặp lại. Ngược lại, nếu hàng xóm được chọn không tốt hơn, thuật toán sẽ chọn ngẫu nhiên một hàng xóm khác và so sánh. Thuật toán kết thúc và trả lại trạng thái hiện thời khi đã hết “kiên nhẫn”. 


Stochastic Hill Climbing: Chọn ngẫu nhiên một bước cải thiện trong số các bước tốt hơn hiện tại. Tăng tính đa dạng, có thể thoát khỏi bẫy cục bộ.


#### Simulated Annealing 
Simulated Annealing là thuật toán cục bộ cho phép chọn trạng thái "xấu hơn" với một xác suất giảm dần theo thời gian. Cách làm này giúp thoát khỏi cực trị cục bộ và tăng khả năng tìm được lời giải tốt hơn về lâu dài.


https://github.com/user-attachments/assets/bfe61243-5167-48ea-b391-3438abab482a


Simulated Annealing: Cho phép chấp nhận trạng thái xấu hơn với xác suất giảm dần theo thời gian. Hiệu quả trong việc tránh đỉnh cục bộ, nhưng cần điều chỉnh tham số nhiệt độ hợp lý.
#### Genetic Algorithms – Thuật toán di truyền
Thuật toán di truyền (Genetic Algorithm - GA) là một phương pháp tìm kiếm theo cơ chế tự nhiên của quá trình tiến hóa, bao gồm các bước chọn lọc, lai ghép và đột biến để tìm ra lời giải tối ưu. Trong trò chơi đua cá, thuật toán này có thể dùng để tìm ra chiến lược tối ưu cho việc di chuyển, dựa trên các cá thể khác nhau và cải thiện qua các thế hệ.

Beam Search: Duy trì k trạng thái tốt nhất tại mỗi bước. Tối ưu bộ nhớ hơn BFS, nhưng có thể bỏ sót lời giải tối ưu nếu k quá nhỏ.
#### Beam Search 
Beam Search là một dạng tìm kiếm có giới hạn, chỉ giữ lại k trạng thái tốt nhất tại mỗi bước mở rộng. Nó tiết kiệm bộ nhớ và thời gian nhưng có thể bỏ lỡ lời giải tối ưu nếu k quá nhỏ.

Genetic Algorithm: Mô phỏng quá trình tiến hóa tự nhiên bằng chọn lọc, lai ghép, đột biến. Phù hợp với không gian tìm kiếm lớn, nhưng độ chính xác phụ thuộc vào thiết kế bộ gen và hàm đánh giá.
### 2.4. Nhóm 4: Tìm kiếm trong môi trường phức tạp
#### Tree Search AND–OR
AND-OR Search là một thuật toán tìm kiếm trong không gian trạng thái phức tạp, nơi các hành động cần phải kết hợp với nhau để đạt được mục tiêu. Thuật toán này phân chia bài toán thành các nhánh AND (cần thỏa mãn tất cả các điều kiện) và OR (chỉ cần thỏa mãn một trong các điều kiện). Đây là một phương pháp phù hợp cho những bài toán có sự phụ thuộc lẫn nhau giữa các hành động.

#### Partially Observable Search – Quan sát một phần
Tìm kiếm trong môi trường mà chỉ thấy được một phần, không phải lúc nào cũng biết chính xác trạng thái hiện tại. Cần dùng tập hợp các trạng thái có thể xảy ra (belief states) và cập nhật dần theo quan sát. Ở thuật toán này, phần không nhìn thấy được đánh dấu là -1.

####  Searching with No Observation – Tìm kiếm không quan sát
Tìm kiếm không quan sát (Searching with No Observation) là một dạng tìm kiếm trong môi trường hoàn toàn không có khả năng quan sát trạng thái hiện tại hoặc kết quả của hành động. Agent (tác nhân) phải đưa ra kế hoạch hành động dựa vào kiến thức ban đầu mà không có bất kỳ thông tin cập nhật nào trong suốt quá trình thực hiện.

### 2.5. Nhóm 5: Tìm kiếm có ràng buộc (Constraint Satisfaction)
#### Backtracking Search
Backtracking là thuật toán tìm kiếm trong môi trường có ràng buộc, phương pháp tìm kiếm dựa trên việc thử và sai (trial-and-error). Khi gặp một ngõ cụt (Không thỏa các ràng buộc), thuật toán sẽ quay lại bước trước đó để thử lựa chọn khác. Backtracking được sử dụng chủ yếu trong các bài toán tổ hợp và tối ưu.

#### Test-Based Search- Kiểm thử
Kiểm thử là thuật toán tìm kiếm có ràng buộc (Constraint Satisfaction). Thuật toán hoạt động bằng cách tạo ra toàn bộ các tổ hợp giá trị có thể cho các biến, sau đó kiểm tra từng tổ hợp để xem có thoả mãn tất cả ràng buộc không.
#### AC-3 
AC-3 là một thuật toán trong nhóm tìm kiếm có ràng buộc (Constraint Satisfaction) dùng để kiểm tra và duy trì tính nhất quán cung (arc-consistency) giữa các biến có ràng buộc nhị phân. Thuật toán này hoạt động bằng cách lặp lại việc loại bỏ các giá trị không hợp lệ khỏi miền giá trị của các biến, cho đến khi không còn thay đổi nào nữa.

### 2.6. Nhóm 6: Học tăng cường (Reinforcement Learning)
#### Q-Learning
Q-Learning là một thuật toán học máy thuộc nhánh học tăng cường (reinforcement learning), trong đó một tác nhân học cách tối ưu hóa hành động của mình thông qua việc nhận phản hồi (thưởng hoặc phạt) từ môi trường. 

# 3. Kết luận
Qua việc áp dụng các thuật toán tìm kiếm vào bài toán 8-Puzzle, em rút ra được một số kết luận như sau:

Không có thuật toán nào là tốt nhất trong mọi trường hợp. Mỗi thuật toán có ưu và nhược điểm riêng.

Các thuật toán có thông tin (như A*) thường cho kết quả tối ưu và nhanh hơn, nếu thiết kế được hàm heuristic tốt.

Các thuật toán không có thông tin phù hợp cho việc minh họa nguyên lý tìm kiếm, nhưng kém hiệu quả hơn khi không gian trạng thái lớn.

Thuật toán cục bộ và học tăng cường thể hiện tiềm năng trong các bài toán mở rộng, cần tinh chỉnh tham số để đạt hiệu quả.

Việc so sánh giúp em hiểu rõ hơn về cách lựa chọn thuật toán phù hợp trong các bài toán cụ thể và đánh giá hiệu suất của từng giải pháp một cách có hệ thống.

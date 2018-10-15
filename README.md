# A* Algorithm
## Class Architecture
### Class Coord: Lưu thông tin toạ độ của một ô trong bản đồ
* Hàm get_successor_list(): Trả về một danh sách toạ độ của các ô liền kề. Kiểm tra điều kiện xem toạ độ đó có tồn tại trong bản đồ hay không (Kiểm tra hoành độ và tung độ >=0 và <n)
* Hàm calculate_heuristic():
* Cài đặt khoảng cách euclide giữa hai ô và heuristic do nhóm định nghĩa.
### Class Cell: Lưu thông tin của một ô trong bản đồ
1. Các trường dữ liệu
    * coord: Lưu toạ độ của ô đó trong bản đồ
    * g: Khoảng cách thực từ ô bắt đầu
    * h: heuristic ước lượng khoảng cách đến ô đích
    * parent: Lưu thông tin của ô trước đó trong đường đi, dùng để truy vết và in đường đi sau khi đã tìm được đường đi từ điểm đầu đến điểm kết thúc
    * type: Loại của ô. 0: ô trống, 1: vật cản
2. Các hàm
    * trace_path(): Là một hàm đệ quy dùng để in đường đi tìm được dựa vào trường parent
### Class Map: Lưu bản đồ bao gồm các Cell
1. Các trường dữ liệu
    * grid_map: mảng 2 chiều lưu các ô ở trong bản đồ
    * n: Kích thước bản đồ (n x n)
    * start: Toạ độ điểm bắt đầu
    * goal: Toạ độ điểm kết thúc
2. Các hàm
    * import_from_file: đọc một file và xây dựng bản đồ
    * get_cell: Lấy một ô trong bản đồ dựa vào toạ độ
    * print_map: In bản đồ dựa trên kí hiệu của từng loại ô trong bản đồ
## Data Structure: Priority Queue
* Dùng Binary Heap để cài đặt hàng đợi ưu tiên. Dùng giá trị f = g + h để làm giá trị xây dựng heap.
* Các hàm được hỗ trợ trong Binary Heap:
    * insert_new_key(): Thêm một ô vào heap sau đó cân bằng lại heap
    * extract(): Lấy ô có giá trị f nhỏ nhất ra khỏi heap (ô nằm ở vị trí gốc)
    * insert_key(): Thêm một ô vào heap. Nếu ô đó đã có trong heap thì so sánh giá trị f với ô đã có sẵn. Nếu ô mới thêm vào có giá trị f nhỏ hơn thì mới được thêm vào, ngược lại thì bỏ qua.

# Cần làm gì khi thêm Input
* Tạo một ma trận 2 chiều nxn để chứa các ô
* Khởi tạo g cho các ô là inf
* Tính heuristic cho mỗi ô không phải là vật cản
* Xác định điểm bắt đầu và kết thúc
* Khởi tạo g cho điểm bắt đầu là 0
## 🕹️ Menu Chính & Các Chế Độ
Giao diện chính được thiết kế theo phong cách **Futuristic Snake** (Rắn săn mồi tương lai), mang lại cảm giác công nghệ hiện đại.
Các chức năng chính bao gồm:
* **Start Game:** Bắt đầu chế độ chơi tay truyền thống (Human Mode).
* **AI Auto:** Mở menu phụ với các tính năng AI:
    * `Train New Model`: Huấn luyện mô hình mới.
    * `Watch Best AI`: Xem màn trình diễn của AI tốt nhất.
* **Settings:** Truy cập màn hình tùy chỉnh cài đặt trò chơi.
* **Exit:** Thoát khỏi trò chơi.
<img width="701" height="424" alt="image" src="https://github.com/user-attachments/assets/65150ee9-e63b-49bd-b8b0-6c4a7fee8ee2" />

### 1. Giao diện Đang Chơi (Gameplay Interface)
Đây là màn hình chính nơi trò chơi diễn ra:
* **Visual:** Hiển thị rắn (màu xanh), thức ăn (màu đỏ) và lưới nền (grid) giúp người chơi dễ canh chỉnh hướng đi.
* **Score:** Điểm số hiện tại được hiển thị trực tiếp ở góc trên bên trái.
* **Cơ chế:** Rắn di chuyển trong phạm vi khung viền đỏ. Trò chơi kết thúc nếu rắn va chạm vào viền hoặc chính mình.
<img width="985" height="603" alt="image" src="https://github.com/user-attachments/assets/7e1fd8f8-47c8-4078-aa3a-cf6820c28f51" />

### 2. Giao diện Game Over (Game Over Interface)
Màn hình xuất hiện khi lượt chơi kết thúc:
* **Thông báo:** Hiển thị dòng chữ "GAME OVER" nổi bật.
* **Tổng kết:** Hiển thị điểm số cuối cùng người chơi đạt được ("YOUR SCORE").
* **Điều hướng:** Hướng dẫn người chơi nhấn phím `ESC` để quay trở lại Menu chính.
<img width="985" height="586" alt="image" src="https://github.com/user-attachments/assets/51f61f87-6e96-42cf-96bc-c3a0d57294ec" />

⚙️ Cài đặt & Hướng dẫn sử dụng
Dự án sử dụng Python cùng các thư viện: Pygame (cho giao diện), PyTorch (cho Deep Learning), và NumPy (xử lý ma trận).

Dưới đây là hướng dẫn thiết lập môi trường bằng Micromamba.

1. Khởi tạo môi trường ảo (Virtual Environment)
Mở terminal tại thư mục dự án và chạy các lệnh sau để tạo môi trường sạch:
```text
micromamba create -n snake_ai python=3.10 -c conda-forge
micromamba activate snake_ai
```
2. Cài đặt thư viện
```text
pip install -r requirements.txt
```
3. Chạy game
```text
python main.py
```
## 🧠 Kiến trúc Deep Learning 

Mô hình sử dụng thuật toán **Deep Q-Learning (DQN)** với kiến trúc mạng nơ-ron truyền thẳng (Feed Forward). Dưới đây là cấu hình chi tiết:

| Thành phần | Cấu hình / Giá trị | Mô tả kỹ thuật |
| :--- | :--- | :--- |
| **Kiến trúc mạng** | `Linear_QNet` | Mạng 3 lớp: Input -> Hidden -> Output. |
| **Input Layer** | `11` Neurons | Vector trạng thái bao gồm: Hướng đi, Mối nguy hiểm kề bên, Vị trí mồi. |
| **Hidden Layer** | `256` Neurons | Lớp ẩn sử dụng hàm kích hoạt **ReLU** để học dữ liệu phi tuyến tính. |
| **Output Layer** | `3` Neurons | Đầu ra quyết định hành động: `[0,0,0]` tương ứng [Đi thẳng, Rẽ phải, Rẽ trái]. |
| **Optimizer** | `Adam` | Thuật toán tối ưu hóa thích nghi (Adaptive Moment Estimation). |
| **Loss Function** | `MSELoss` | Hàm mất mát Mean Squared Error (Bình phương trung bình sai số). |
| **Learning Rate** | `0.001` | Tốc độ học của mô hình. |
| **Gamma** | `0.9` | Hệ số chiết khấu (Discount factor), ưu tiên phần thưởng ngắn hạn hay dài hạn. |
| **Batch Size** | `1000` | Số lượng mẫu được lấy ngẫu nhiên từ bộ nhớ để huấn luyện lại (Replay). |
| **Memory** | `100,000` | Bộ nhớ đệm (Experience Replay) lưu trữ các bước đi trước đó. |

---

### ℹ️ Chi tiết Vector đầu vào (Input State - 11 tham số):
1.  **Nguy hiểm (3):** Có tường hoặc thân mình ở phía trước, bên trái, hoặc bên phải không?
2.  **Hướng đi (4):** Rắn đang đi hướng nào (Lên, Xuống, Trái, Phải)?
3.  **Vị trí mồi (4):** Mồi đang ở phía nào so với đầu rắn (Lên, Xuống, Trái, Phải)?

📂 Cấu trúc Dự án (Project Structure)
```text
Snake-AI-Game/
│
├── main.py                # File chạy chính của chương trình
├── assets/                # Tài nguyên game (hình ảnh, âm thanh)
│   └── images/            # Chứa ảnh nền menu (menu_bg.png)
├── model/                 # Thư mục chứa file model đã train (model.pth)
│
└── snake/                 # Package chính của trò chơi
    ├── __init__.py
    ├── settings.py        # Các cấu hình chung (Màu sắc, FPS, Grid size)
    │
    ├── core/              # Xử lý logic cốt lõi
    │   ├── __init__.py
    │   └── env_snake.py   # Môi trường game, xử lý di chuyển, va chạm
    │
    ├── scenes/            # Giao diện hiển thị (UI)
    │   ├── __init__.py
    │   ├── intro.py       # Menu chính, nút bấm, chọn chế độ
    │   └── board.py       # Vẽ đồ họa bàn chơi (Rắn, mồi, lưới)
    │
    └── rl/                # Reinforcement Learning (AI)
        ├── __init__.py
        ├── agent_dqn.py   # Agent AI xử lý hành động
        ├── dqn_model.py   # Kiến trúc mạng nơ-ron (Linear_QNet)
        ├── memory.py      # Bộ nhớ Replay Memory
        └── train_dqn.py   # Vòng lặp huấn luyện AI
```
## 👥 Danh sách Thành viên Nhóm

**HCMUS-NHÓM 1-25CTT3A-GROUP BUG LỰC**

| STT | Họ và tên | MSSV |
| :---: | :--- | :---: |
| 1 | **Tăng Nguyễn Trường Giang** | 25120186 |
| 2 | **Hoàng Kim Bảo** | 25120164 |
| 3 | **Vũ Văn Duy** | 25120185 |
| 4 | **Trần Nguyễn Gia Bảo** | 25120166 |
| 5 | **Nguyễn Hoàng Huy** | 25120193 |
| 6 | **Nguyễn Hoàng Tuấn Hưng** | 25120190 |

**Intructor: LÊ ĐỨC KHOAN**
![grantt](https://github.com/user-attachments/assets/a37177e4-45be-4311-b1b0-56f2948fa776)


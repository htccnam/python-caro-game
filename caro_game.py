import tkinter as tk
from tkinter import messagebox
import math

# ==================== CẤU HÌNH ====================
BOARD_SIZE = 15          # Bàn cờ 15x15
CELL_SIZE = 40           # Kích thước mỗi ô (px)
BOARD_MARGIN = 30        # Lề xung quanh bàn cờ
WINDOW_SIZE = BOARD_MARGIN * 2 + BOARD_SIZE * CELL_SIZE

# Màu sắc
COLOR_BOARD = "#DEB887"   # Màu nền bàn cờ (nâu nhạt)
COLOR_LINE = "#8B4513"    # Màu đường kẻ
COLOR_PLAYER = "blue"     # Màu quân O (người chơi)
COLOR_AI = "red"          # Màu quân X (máy)

# ==================== LỚP CHÍNH ====================
class CaroGame:
    def __init__(self):
        # Khởi tạo cửa sổ chính
        self.window = tk.Tk()
        self.window.title("Cờ Caro - Python")
        self.window.geometry(f"{WINDOW_SIZE}x{WINDOW_SIZE + 50}")
        self.window.resizable(False, False)

        # Biến trạng thái game
        self.board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]  # 0: trống, 1: O, 2: X
        self.current_player = 1  # 1: người chơi, 2: máy
        self.game_over = False
        self.move_count = 0

        # Tạo canvas để vẽ
        self.canvas = tk.Canvas(
            self.window,
            width=WINDOW_SIZE,
            height=WINDOW_SIZE,
            bg=COLOR_BOARD
        )
        self.canvas.pack(pady=10)

        # Nút chơi lại
        self.reset_btn = tk.Button(
            self.window,
            text="Chơi lại",
            font=("Arial", 14),
            command=self.reset_game
        )
        self.reset_btn.pack()

        # Vẽ bàn cờ và bắt lắng nghe sự kiện chuột
        self.draw_board()
        self.canvas.bind("<Button-1>", self.on_click)

    # ================ VẼ BÀN CỜ ================
    def draw_board(self):
        """Vẽ bàn cờ với các đường kẻ và đánh dấu các quân cờ đã có"""
        self.canvas.delete("all")

        # Vẽ các đường kẻ
        for i in range(BOARD_SIZE):
            x = BOARD_MARGIN + i * CELL_SIZE
            y = BOARD_MARGIN + i * CELL_SIZE
            # Đường dọc
            self.canvas.create_line(
                x, BOARD_MARGIN,
                x, BOARD_MARGIN + (BOARD_SIZE - 1) * CELL_SIZE,
                fill=COLOR_LINE, width=1
            )
            # Đường ngang
            self.canvas.create_line(
                BOARD_MARGIN, y,
                BOARD_MARGIN + (BOARD_SIZE - 1) * CELL_SIZE, y,
                fill=COLOR_LINE, width=1
            )

        # Vẽ các quân cờ đã có trên bàn
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col] == 1:
                    self.draw_piece(row, col, COLOR_PLAYER, "O")
                elif self.board[row][col] == 2:
                    self.draw_piece(row, col, COLOR_AI, "X")

    def draw_piece(self, row, col, color, text):
        """Vẽ một quân cờ tại vị trí (row, col)"""
        x = BOARD_MARGIN + col * CELL_SIZE
        y = BOARD_MARGIN + row * CELL_SIZE
        radius = CELL_SIZE // 2 - 4

        # Vẽ hình tròn
        self.canvas.create_oval(
            x - radius, y - radius,
            x + radius, y + radius,
            fill=color, outline=color
        )
        # Vẽ chữ O/X bên trong
        self.canvas.create_text(
            x, y,
            text=text,
            font=("Arial", 16, "bold"),
            fill="white"
        )

    # ================ XỬ LÝ SỰ KIỆN ================
    def on_click(self, event):
        """Xử lý khi người chơi click chuột"""
        if self.game_over or self.current_player != 1:
            return

        # Tính toán ô được click
        col = round((event.x - BOARD_MARGIN) / CELL_SIZE)
        row = round((event.y - BOARD_MARGIN) / CELL_SIZE)

        # Kiểm tra click hợp lệ
        if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
            return
        if self.board[row][col] != 0:
            return

        # Đánh dấu quân cờ
        self.board[row][col] = 1
        self.move_count += 1
        self.draw_board()

        # Kiểm tra thắng cuộc
        if self.check_win(row, col, 1):
            self.game_over = True
            messagebox.showinfo("🎉 Chiến thắng!", "Bạn đã thắng máy!")
            return

        if self.move_count == BOARD_SIZE * BOARD_SIZE:
            self.game_over = True
            messagebox.showinfo("Hòa!", "Bàn cờ đã đầy, hai bên hòa nhau!")
            return

        # Đến lượt máy
        self.current_player = 2
        self.window.after(300, self.ai_move)  # Delay 0.3s để máy "suy nghĩ"

    # ================ AI CỦA MÁY ================
    def ai_move(self):
        """Máy tính chọn nước đi tốt nhất"""
        if self.game_over or self.current_player != 2:
            return

        best_score = -1
        best_moves = []

        # Duyệt tất cả các ô trống
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col] == 0:
                    # Đánh giá điểm cho ô này
                    score = self.evaluate_position(row, col)
                    if score > best_score:
                        best_score = score
                        best_moves = [(row, col)]
                    elif score == best_score:
                        best_moves.append((row, col))

        if not best_moves:
            return

        # Chọn ngẫu nhiên một trong các nước đi tốt nhất
        import random
        row, col = random.choice(best_moves)

        # Đánh dấu quân cờ
        self.board[row][col] = 2
        self.move_count += 1
        self.draw_board()

        # Kiểm tra thắng cuộc
        if self.check_win(row, col, 2):
            self.game_over = True
            messagebox.showinfo("😢 Thua rồi!", "Máy đã thắng bạn!")
            return

        if self.move_count == BOARD_SIZE * BOARD_SIZE:
            self.game_over = True
            messagebox.showinfo("Hòa!", "Bàn cờ đã đầy, hai bên hòa nhau!")
            return

        self.current_player = 1

    def evaluate_position(self, row, col):
        """
        Đánh giá một ô trống dựa trên số quân cờ cùng màu xung quanh.
        Hàm này đánh giá từ góc độ của máy (màu 2).
        """
        # Các hướng cần kiểm tra: ngang, dọc, chéo chính, chéo phụ
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        total_score = 0

        for dx, dy in directions:
            count = 1  # Tính cả ô hiện tại
            # Đếm về 2 phía
            for sign in (-1, 1):
                for step in range(1, 5):  # Kiểm tra tối đa 4 ô mỗi phía
                    r = row + sign * step * dx
                    c = col + sign * step * dy
                    if not (0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE):
                        break
                    if self.board[r][c] == 2:  # Quân của máy
                        count += 1
                    elif self.board[r][c] == 1:  # Quân của người chơi (chặn)
                        count -= 1
                        break
                    else:  # Ô trống
                        break

            # Tính điểm dựa trên số lượng quân liên tiếp
            if count >= 5:
                total_score += 100
            elif count == 4:
                total_score += 30
            elif count == 3:
                total_score += 10
            elif count == 2:
                total_score += 3

        return total_score

    # ================ KIỂM TRA THẮNG ================
    def check_win(self, row, col, player):
        """Kiểm tra xem nước đi tại (row, col) có tạo thành 5 quân liên tiếp không"""
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for dx, dy in directions:
            count = 1
            # Kiểm tra 2 phía
            for sign in (-1, 1):
                for step in range(1, 5):
                    r = row + sign * step * dx
                    c = col + sign * step * dy
                    if not (0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE):
                        break
                    if self.board[r][c] == player:
                        count += 1
                    else:
                        break
            if count >= 5:
                return True
        return False

    # ================ RESET GAME ================
    def reset_game(self):
        """Khởi động lại ván cờ"""
        self.board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.current_player = 1
        self.game_over = False
        self.move_count = 0
        self.draw_board()

    # ================ CHẠY GAME ================
    def run(self):
        self.window.mainloop()


# ==================== CHẠY CHƯƠNG TRÌNH ====================
if __name__ == "__main__":
    game = CaroGame()
    game.run()
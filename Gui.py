"""
環境設定
py -m venv env
env/Scripts/activate
pip install customtkinter
pip install selenium
"""

import customtkinter as ctk
import threading
from WebCrawer import crawl_job
from WebCrawer import sort_jobs
from WebCrawer import setting
from WebCrawer import csvs


# GUI設置
windows = ctk.CTk()
windows.title("網路職缺資訊快速查詢系統介面 NJVIQISI")

# 取得螢幕的寬高
screen_width = windows.winfo_screenwidth()
screen_height = windows.winfo_screenheight()

# 初始化 customtkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# 視窗位置及大小設定
center_x = int((screen_width / 2) - (900 / 2))
center_y = int((screen_height / 2) - (640 / 2))
windows.geometry(f"900x640+{center_x}+{center_y}")
windows.minsize(900, 640)
windows.resizable(True, True)

# 設定介紹文字
intro_frame = ctk.CTkFrame(windows, fg_color="transparent", height=50)
intro_frame.pack(side="top", fill="x", padx=5, pady=5)

""" 版本號 """
version_label = ctk.CTkLabel(
    intro_frame,
    text="版本 : 1.06.87",
    font=("Arial", 12),
    text_color="white"
)
version_label.pack(side="left", padx=10,anchor="nw")  # 版本號靠右顯示

intro_label = ctk.CTkLabel(
    intro_frame,
    text="歡迎使用　網路職缺資訊快速查詢系統",
    font=("Arial", 20, "bold"),
    text_color="white"
)
intro_label.pack(side="top", pady=10)


# 搜尋區域
search_frame = ctk.CTkFrame(windows, fg_color="transparent", height=100)
search_frame.pack(side="top", fill="x", padx=5, pady=10)


# 更新結果函數
def update_result(result):
    result_text.configure(state="normal")
    result_text.delete(1.0, "end")
    result_text.insert("insert", result)
    result_text.configure(state="disabled")


# 動畫面板類別
class SlidePanel(ctk.CTkFrame):
    def __init__(self, parent, start_pos, end_pos):
        super().__init__(
            master = parent,
            border_color = "#E38EFF",
            border_width = 2
        )
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.pos = self.start_pos
        self.in_start_pos = True
        self.place(relx=self.start_pos, rely=0.05, relwidth=0.3, relheight=0.9)

    def animate(self):
        self.lift()
        if self.in_start_pos:
            self.animate_forward()
        else:
            self.animate_backwards()

    def animate_forward(self):
        if self.pos > self.end_pos:
            self.pos -= 0.008
            self.place(relx=self.pos, rely=0.05, relwidth=0.3, relheight=0.9)
            self.after(10, self.animate_forward)
        else:
            self.in_start_pos = False

    def animate_backwards(self):
        if self.pos < self.start_pos:
            self.pos += 0.008
            self.place(relx=self.pos, rely=0.05, relwidth=0.3, relheight=0.9)
            self.after(10, self.animate_backwards)
        else:
            self.in_start_pos = True


# 動畫面板
animated_panel = SlidePanel(
    windows,
    1.0,
    0.7,
)

"""選擇單功能"""
ctk.CTkLabel(
    animated_panel,
    text="__ 排序 ___________________",
    font=("微軟正黑體", 14),
).pack(side="top", anchor="nw", padx=10, pady=3)
#由北到南
ctk.CTkButton(
    animated_panel,
    text='由北到南',
    font=("Arial", 16),
    command=lambda: threading.Thread(target=lambda: update_result(sort_jobs("location")), daemon=True).start()
).pack(expand=True, fill='both', padx=10, pady=10)
#薪水高低
ctk.CTkButton(
    animated_panel,
    text='薪水由高到低',
    font=("Arial", 16),
    command=lambda: threading.Thread(target=lambda: update_result(sort_jobs("salary")), daemon=True).start()
).pack(expand=True, fill='both', padx=10, pady=10)

#設定及下載功能
ctk.CTkLabel(
    animated_panel,
    text="__ 設定及下載功能 _________",
    font=("微軟正黑體", 14),
).pack(side="top", anchor="nw", padx=10, pady=1)

ctk.CTkButton(  #設定按鈕
    animated_panel,
    text = "設定",
    font=("unicode", 16),
    command=lambda: threading.Thread(target=setting, args=(windows,), daemon=True).start()
).pack(expand=True, fill="both", padx=10, pady=10)

ctk.CTkButton(  #下載csv檔按鈕
    animated_panel,
    text = "下載 CSV 檔",
    font=("unicode", 16),
    command=lambda: threading.Thread(target=csvs, daemon=True).start()
).pack(expand=True, fill="both", padx=10, pady=10)


"""搜尋功能"""
def start_search(job):
    if job.strip():
        result_text.configure(state="normal")
        result_text.delete(1.0, "end")
        result_text.insert("insert", "正在搜尋中...請稍後...")
        result_text.configure(state="disabled")
        threading.Thread(target=crawl_job, args=(job, update_result), daemon=True).start()
    else:
        result_text.configure(state="normal")
        result_text.delete(1.0, "end")
        result_text.insert("insert", "請輸入有效的職業名稱！")
        result_text.configure(state="disabled")


# 搜尋區域
button_menu = ctk.CTkButton(
    search_frame, text="選擇單",
    height=40,
    width=40,
    corner_radius=30,
    command=animated_panel.animate)
button_menu.pack(side="left", padx=5, pady=10)

search_entry = ctk.CTkEntry(
    search_frame,
    placeholder_text="關鍵字......",
    width=650, height=40,
    corner_radius=20,
    border_width=3,
    border_color="#008B8B"
)
search_entry.pack(side="left", padx=5, pady=10, fill="x", expand=True)

search_entry.bind("<Return>", lambda event: start_search(search_entry.get()))

search_button = ctk.CTkButton(
    search_frame, text="搜尋",
    width=45, height=40,
    corner_radius=100,
    command=lambda: start_search(search_entry.get())
)
search_button.pack(side="right", padx=5, pady=10)

# 搜尋結果區域
result_frame = ctk.CTkFrame(
    windows,
    fg_color="transparent"
)
result_frame.pack(side="top", fill="both", padx=5, pady=20)

result_text = ctk.CTkTextbox(
    result_frame, width=800,
    height=800, font=("Arial", 12),
    border_color="#00CACA",
    border_width=2
)
result_text.pack(padx=5, pady=10, fill="both", expand=True)



# 動態調整字體大小
def adjust_font_size(event=None):
    window_width = windows.winfo_width()
    font_size = max(12, min(window_width // 70, 20))
    result_text.configure(font=("Arial", font_size))

windows.bind("<Configure>", adjust_font_size)

version_label = ctk.CTkLabel(windows, text="版本號: 0.21.87", font=("Arial", 12, "italic"), text_color="white")
version_label.pack(side="right", padx=10)

# 主循環
windows.mainloop()

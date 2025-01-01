from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import sqlite3
import csv
import customtkinter as ctk
from tkinter import filedialog


# 初始化資料庫並創建 jobs 表格
def initialize_database():
    conn = sqlite3.connect("enterprise.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location TEXT NOT NULL,
        company_name TEXT NOT NULL,
        salary TEXT,
        company_url TEXT
    )
    """)
    conn.commit()
    conn.close()


# 爬取職缺資料
def crawl_job(job, update_result):
    """爬蟲主邏輯"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 無頭模式
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--incognito")

    browser = webdriver.Chrome(options=chrome_options)
    browser.maximize_window()
    browser.get("https://www.104.com.tw/")

    sleep(1.5)

    try:
        # 定位到搜索框並輸入內容
        search_box = browser.find_element(By.CSS_SELECTOR, "input.form-control")
        search_box.send_keys(job)

        # 定位到“搜尋”按鈕並點擊
        search_button = browser.find_element(By.XPATH, "//button[@class='btn btn-secondary btn-block btn-lg']")
        search_button.click()

        sleep(1.5)

        # 點擊「最近更新」按鈕
        newest_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='最近更新']"))
        )
        newest_button.click()
        sleep(1.5)
    except Exception as e:
        print(f"爬取過程中發生錯誤: {e}")
        browser.quit()
        return

    # 滾動頁面，直到抓取到足夠的資料
    job_titles, location_salary, company_links = [], [], []

    while len(job_titles) < 30:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(2)
        job_titles = [elem.text.strip() for elem in browser.find_elements(By.CLASS_NAME, "info-job__text")]
        location_salary = [elem.text.strip() for elem in browser.find_elements(By.CLASS_NAME, "info-tags__text")]
        company_links = [elem.get_attribute("href") for elem in browser.find_elements(By.CSS_SELECTOR, "a.info-job__text")]

    result = ""
    conn = sqlite3.connect("enterprise.db")
    cursor = conn.cursor()

    # 刪除資料庫中舊的資料並重置主鍵
    cursor.execute("DELETE FROM jobs")
    conn.commit()

    # 將新資料插入資料庫
    for i in range(30):
        if i >= len(job_titles) or i >= len(location_salary) or i >= len(company_links):
            break

        title = job_titles[i]
        location = location_salary[i * 4] if i * 4 < len(location_salary) else "未知地點"
        salary = location_salary[i * 4 + 3] if (i * 4 + 3) < len(location_salary) else "未知待遇"
        company_link = company_links[i]

        result += f"{location:<15}{title}\n{salary}\n公司網址: {company_link}\n{'-'*60}\n\n"
        cursor.execute("INSERT INTO jobs (location, company_name, salary, company_url) VALUES (?, ?, ?, ?)",
                       (location, title, salary, company_link))

    conn.commit()
    conn.close()
    update_result(result)
    browser.quit()


# 排序職缺資料
def sort_jobs(order_by):
    """排序職缺資料"""
    conn = sqlite3.connect("enterprise.db")
    cursor = conn.cursor()
    if order_by == "location":
        query = """
            SELECT location, company_name, salary, company_url
            FROM jobs
            ORDER BY CASE
                WHEN location LIKE '基隆%' THEN 1
                WHEN location LIKE '台北%' THEN 2
                WHEN location LIKE '新北%' THEN 3
                WHEN location LIKE '桃園%' THEN 4
                WHEN location LIKE '新竹%' THEN 5
                WHEN location LIKE '苗栗%' THEN 6
                WHEN location LIKE '台中%' THEN 7
                WHEN location LIKE '彰化%' THEN 8
                WHEN location LIKE '南投%' THEN 9
                WHEN location LIKE '雲林%' THEN 10
                WHEN location LIKE '嘉義%' THEN 11
                WHEN location LIKE '台南%' THEN 12
                WHEN location LIKE '高雄%' THEN 13
                WHEN location LIKE '屏東%' THEN 14
                WHEN location LIKE '台東%' THEN 15
                WHEN location LIKE '花蓮%' THEN 16
                WHEN location LIKE '宜蘭%' THEN 17
                ELSE 18
            END, location
        """
    elif order_by == "salary":
        query = """
            SELECT location, company_name, salary, company_url
            FROM jobs
            ORDER BY CASE
                WHEN salary LIKE '%月薪%' THEN CAST(REPLACE(REPLACE(salary, '月薪', ''), ',', '') AS INTEGER)
                WHEN salary LIKE '%時薪%' THEN CAST(REPLACE(REPLACE(salary, '時薪', ''), ',', '') AS INTEGER) / 8
                ELSE 0
            END DESC
        """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    return "\n\n".join(
        f"{'地區:':<20}{row[0]}\n"
        f"{'公司名稱:':<14}{row[1]}\n"
        f"{'薪資:':<20}{row[2]}\n"
        f"{'公司網址:':<14}{row[3]}\n"
        f"{'-' * 60}"
        for row in rows
    )


# 按鈕功能設定
def setting(windows):
    """設定視窗"""
    setting_windows = ctk.CTkToplevel(windows)
    setting_windows.title("設定")

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    setting_windows.geometry("300x400")
    setting_windows.resizable(False, False)

    ctk.CTkLabel(
        setting_windows,
        text="功能開發中，預計完成日:無\n作者：楊凱翔\n作者：徐鈺程",
        font=("微軟正黑體", 14)
    ).pack(pady=20)

    ctk.CTkButton(
        setting_windows,
        text="確定",
        font=("微軟正黑體", 16),
        command=setting_windows.destroy
    ).pack(pady=20)


# 資料庫資料以CSV檔案下載
def csvs():
    try:
        conn = sqlite3.connect('enterprise.db')
        cursor = conn.cursor()
        cursor.execute("SELECT location, company_name, salary, company_url FROM jobs")
        rows = cursor.fetchall()

        if not rows:
            print("沒有找到任何資料！")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="保存檔案為"
        )

        if file_path:
            with open(file_path, mode='w', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                writer.writerow(["地區", "公司名稱", "薪資", "公司網址"])
                writer.writerows(rows)
            print(f"資料已成功保存到 {file_path}")
        else:
            print("用戶取消了保存。")

    except Exception as e:
        print(f"導出過程中發生錯誤：{e}")

    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    initialize_database()

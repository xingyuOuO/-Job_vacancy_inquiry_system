#  Job_vacancy_inquiry_system
 職缺查詢系統

![Python](https://img.shields.io/badge/Language-Python_3-3776AB?style=flat-square)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-1F425F?style=flat-square)

> 結合網頁自動化爬蟲技術與GUI 介面的職缺資訊檢索工具，提供快速搜尋、動態顯示、自動化資料庫整理與 CSV 資料匯出功能。

---

## 專案簡介

**網路職缺資訊快速查詢系統 (NJVIQISI)** 旨在為求職者與數據分析者提供的職缺資訊收集方案。傳統手動瀏覽求職網站耗時且資訊分散，本系統透過 **Selenium** 爬蟲技術自動抓取目標頁面上的職缺資料，並搭配 **CustomTkinter** 打造質感優異的深色桌面介面。

### 專案開發團隊-負責項目
**xingyu(我)  - 爬蟲邏輯開發、系統整合與匯出功能實現、PEP 8 格式調整**

**組員 (一人)  - CustomTkinter GUI 動態介面開發、資料庫設計**

---

## 核心功能特色

* **精準欄位抓取**：系統自動爬取職位名稱、工作地點、薪資結構與相關福利資訊。
* **多元薪資型態解析**：完整支援月薪、時薪、年薪、待遇面議及論件計酬等多種計薪方式的識別。
* **現代化 GUI 介面**：採用 CustomTkinter 打造深色主題 (Dark Mode) 與藍色系配色，並具備流暢的動畫視覺效果。
* **智慧資料庫重置**：預設每次搜尋抓取 30 筆資料。執行全新搜尋時自動清空歷史紀錄並重新排序，避免資料大量堆疊或重複問題 。
* **流暢的操作互動**：支援按下 `Enter` 快捷鍵直接發動搜尋。
* **排版與閱讀優化**：薪資欄位獨立換行顯示，並添加適當空行與排序邏輯，顯著提升資訊易讀性。
* **資料庫 CSV 匯出**：內建資料庫下載功能，可一鍵將搜尋結果匯出為 CSV 格式檔案，便利後續統計與分析 。
* **軟體設定按鈕**：介面整合設定入口按鈕，提升使用者介面完整度與擴充性 。

---

## 技術堆疊 (Tech Stack)

* **核心語言**：Python 3 
* **網頁自動化 / 爬蟲**：Selenium (搭配 Xpath/CSS 選擇器與 `job__text` 等屬性定位)
* **使用者介面 (GUI)**：CustomTkinter 
* **程式碼規範**：專案原始碼遵循 PEP 8 規範重構 

---

## 專案架構說明

專案採用模組化設計，將邏輯判斷與視覺呈現拆分：

```text
NJVIQISI/
├── Gui.py           # 主介面程式：負責 900x600 視窗繪製、主題設定、元件佈局與互動 
├── WebCrawer.py     # 爬蟲模組：負責 Selenium 自動化網頁定位、資料抓取與資料庫維護 
├── requirements.txt # 專案依賴套件清單 
└── README.md        # 專案說明文件
```

---
## 快速開始 (Quick Start)

### 1. 複製與準備專案目錄
下載或 Clone 本專案原始碼至本地端資料夾。

### 2. 建立 Python 虛擬環境 (Virtual Environment)
建議建立獨立的虛擬環境以確保套件版本獨立：
```bash
py -m venv env
```

### 3. 啟動虛擬環境
Windows 系統:
  ```bash
  env/Scripts/activate
  ```

### 4. 安裝依賴套件
在虛擬環境啟用狀態下，執行以下安裝指令：
```bash
pip install selenium
pip install customtkinter
```

### 5. 啟動應用程式
完成套件安裝後，直接運行 GUI 主程式即可啟動視窗：
```bash
python Gui.py
```

> **小提示**：如需離開虛擬環境，可在命令列輸入 `deactivate`。

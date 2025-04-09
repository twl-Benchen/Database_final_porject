![image](https://github.com/user-attachments/assets/49b890ba-63ae-4e3f-8608-c275dc42c259)![image](https://github.com/user-attachments/assets/5d8ce184-a15b-42c8-a796-d23ddef90e9f)# Database_final_porject (資料庫系統_第八組)
### 題目 ETF 投資組合管理系統
- **專案簡介**  
    協助投資者整合與管理其 ETF 投資資訊，並提供即時的績效及配置。

### 功能概述  

- **用戶管理**  
    註冊、登入及個人資料設定

- **ETF 資料整合**  
    儲存各 ETF 的基本資料（如代碼、名稱、管理公司、規模等）
    記錄歷史價格與市場成交資訊 

- **交易與持倉管理**  
    記錄用戶的每筆買賣交易
    即時計算並更新持倉狀態、成本與盈虧

- **績效與風險評估**  
    產生投資組合資料（收益率、ETF 配置等圖表）
### 成員

- **組員一**：資工系 - 41143210 - 田晉嘉 [JustinTien10](https://github.com/JustinTien10)
  - 負責項目：[主要負責的部分]
  - 自我介紹：[]

- **組員二**：資工系 - 41143239 - 陳億穎 [yiyingg1226](https://github.com/yiyingg1226)
  - 負責項目：[主要負責的部分]
  - 自我介紹：[]

- **組員三**：資工系 - 41143238 -  陳峻宇 [twl-Benchen](https://github.com/twl-Benchen)
  - 負責項目：[主要負責的部分]
  - 自我介紹：[]

- **組員四**：資工系 - 41143219 -  周偉宸 [WeiChen-Zhou](https://github.com/WeiChen-Zhou)
  - 負責項目：[主要負責的部分]
  - 自我介紹：[]

## 應用情境與使用案例
**應用情境**
1. 小美已經投資了多個ETF和股票，她想要快速了解自己資產的整體表現。透過投資組合管理系統的資產管理功能，她能夠在主頁面上看到當日投資組合的總市值變動及過去一個月的資產趨勢圖。
2. 小張看到晚間新聞說近期因為政府打房措施，使營建相關產業快速崩跌，於是他通過投資組合管理系統檢視該ETF的成分股，發現到他的ETF中有20%的成分股是營建相關產業，這些成分股的股價在近一周跌了約30%。
3. 小王的朋友跟他推薦了一檔ETF，波動低報酬又高，但他想先了解該ETF過去的模擬表現。於是使用我們的投資組合管理系統進行回測分析，計算出該ETF在歷史最大跌幅及年化報酬率，並比較了該ETF與市場上其他ETF的波動差異。

**使用案例**  
![image](https://github.com/twl-Benchen/Database_final_porject/blob/main/%E4%BD%BF%E7%94%A8%E8%80%85.jpg) ![image](https://github.com/twl-Benchen/Database_final_porject/blob/main/%E7%AE%A1%E7%90%86%E8%80%85.jpg)
 - 使用者
   - 檢視ETF資訊與技術指標
   - 使用ETF篩選器
   - 建立與追蹤自訂投資組合
 - 說明
   - 使用者可以查看ETF的歷史走勢、技術指標（如MACD、RSI等），對應「ETF_HistoryPrice(ETF歷史價格) 」​
   - 依據主題、報酬率、產業等條件，快速找到符合需求的ETF ，對應「 Category_Level1(第一分類) 」與「 Category_Level2(第二分類) 」​
   - 建立個人化投資組合，追蹤其報酬變化與模擬股息再投入，對應「 Transaction(交易紀錄表) 」​
 - 管理者
   - 查看使用者資料
   - 更新ETF資料
   - 管理資料庫內容
 - 說明
   - 查看使用者資料，包括登入帳號、持股資料、投資組合等資訊，對應「 Users(使用者基本資料) 」與​「Portfolio(持倉資料表) 」
   - 每日更新ETF數據、技術指標、股息資訊等，對應「ETF(基本資料表) 」
   - 管理資料庫結構與資料，處理資料異常或系統升級
## 系統需求說明
- **交易與持倉管理**
  - 紀錄用戶每筆交易（含交易成本、價格、數量等）
  - 根據交易自動更新用戶當前持倉狀態與盈虧
  - 支援用戶調整 ETF 投資組合以因應市場變動

- **ETF 資料篩選**
  - 儲存與管理 ETF 基本資料（代碼、名稱、管理公司、規模等）
  - 記錄 ETF 的歷史價格與市場每日成交資訊
  - 提供 ETF 分類、查詢與比較功能
  - 支援自訂篩選條件以滿足用戶查詢需求

- **績效與風險評估**
  - 自動計算年化報酬率、波動度、最大跌幅等績效指標
  - 生成績效走勢圖

- **用戶管理**
  - 註冊與個人資料設定（姓名、信箱、單日買賣上限等）
  - 允許用戶登入與修改個人資訊
  - 用戶可查詢歷史交易記錄與投資組合變化
  - 管理員僅可查詢用戶統計數據（無法查看個人持股資料）

- **安全性**
  - 確保用戶個人資料與交易記錄的隱私性
  - 提供資料備份以確保系統穩定性

## 完整性限制
- Category_Level1(第一分類)
| Category1_Id(PK) | Category1_Name |
| --- | --- |
| 1 | 股票型 |
| 2 | 高股息 |
| 3 | 債券型 |
- Category_Level2(第二分類)
| Category2_Id(PK) | Category1_Id(FK) | Category2_Name |
| --- | --- | --- |
| 1 | 大型權值 | 1 |
| 2 | 中小型權值 | 1 |
| 3 | 高息低波動 | 2 |
- ETF_Category(紀錄分類)
| Category_Id(PK) | ETF_Id(FK) | Category2_Id(FK) |
| --- | --- | --- |
| 1 | 0050 | 1 |
| 2 | 0050 | 3 |
|3 | 0051 | 2 |
- Users(使用者基本資料)
| 欄位名稱 | 欄位說明 | 資料型態 | 是否可為空 | 值域 |
| --- | --- | --- | --- | ---|
| User_Id(PK) |	使用者代號 |	INT	| N |	從 1 開始遞增的整數 |
| User_Name |	使用者名稱 |	VARCHAR(50) |	N |	長度 1~50 的文字|
| Full_Name	| 全名 |	VARCHAR(100) |	N |	長度 1~100 的文字|
| Email	| 電子郵件 |	VARCHAR(100) |	N |	必須符合 Email 格式|
| Phone_Number	| 電話號碼 |	VARCHAR(10) |	N |	固定長度 10 碼（例如：09xxxxxxxx）|
| Role |	權限 |	ENUM('user','admin') |	N |	僅限 'user' 或 'admin' |
| Max_Amount |	當日最大交易量 |	INT |	N |	大於或等於 0 的整數 |
| Users_Creat_At |	帳號創建日期 |	TIMESTAMP |	N |	時間格式：yyyy-mm-dd |
## ER Diagram及詳細說明
![image](https://github.com/twl-Benchen/Database_final_porject/blob/main/ER%20Diagram.png)


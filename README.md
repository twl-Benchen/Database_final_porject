[查看投影片](https://github.com/twl-Benchen/Database_final_porject/blob/main/%E7%AC%AC%E5%85%AB%E7%B5%84_ETF%20%E6%8A%95%E8%B3%87%E7%B5%84%E5%90%88%E7%AE%A1%E7%90%86%E7%B3%BB%E7%B5%B1.pdf)

### 題目 ETF 投資組合管理系統(第八組)
- **專案簡介**  
    協助投資者整合與管理其 ETF 投資資訊，提供利用標籤查詢ETF、即時交易與持倉更新，並產生投資組合明細與統計。

### 功能概述  

- **用戶管理**  
    註冊、登入及個人資料設定

- **ETF列表與篩選**  
    儲存各 ETF 的基本資料（如代碼、名稱、管理公司、規模等）
    下拉選單顯示所有ETF並支援查詢
  
- **歷史價格與漲跌幅**  
    可以查看台灣所有ETF創立至今(2025/6月)K線圖走勢
    查詢指定期間收盤價並計算漲跌幅百分比
  
- **交易與持倉管理**  
    記錄用戶的每筆買賣交易
    即時計算並更新持倉狀態、成本與盈虧

- **績效與風險評估**  
    產生投資組合資料（收益率、ETF 配置等圖表）
### 成員

>組員一：資工系 - 41143210 - 田晉嘉 [JustinTien10](https://github.com/JustinTien10)<br>
>負責項目：[ETF歷史走勢爬取、編排文件、協助View製作]<br>
>Email：41143210@nfu.edu.tw

>組員四：資工系 - 41143219 -  周偉宸 [WeiChen-Zhou](https://github.com/WeiChen-Zhou)<br>
>負責項目：[權限設計&實作、建立View]<br>
>Email：41143219@nfu.edu.tw

>組員三：資工系 - 41143238 -  陳峻宇 [twl-Benchen](https://github.com/twl-Benchen)<br>
>負責項目：[值域規劃、MariaDB建立&實作、建立View、ETF分類標籤整理、網頁實作]<br>
>Email：41143238@nfu.edu.tw

>組員二：資工系 - 41143239 - 陳億穎 [yiyingg1226](https://github.com/yiyingg1226)<br>
>負責項目：[資料庫概念層建立、ER digram製作]<br>
>Email：41143239@nfu.edu.tw


## 應用情境與使用案例
**應用情境**
1. 小美登入後，系統立刻顯示她所有持有的ETF明細（名稱、股數、平均成本及總成本），並自動彙總出不同檔數、總持股與投資金額，同時在下方列出近期交易紀錄，讓她方便掌握自身的資產配置與操作狀況。
2. 小張想找到特定類型的ETF，只要在分類介面先選「股票型」、再點「大型權值」，系統便列出所有符合條件的標的；若他需要更精準，也能直接輸入關鍵字（例如「元大」）進行搜尋，迅速鎖定符合策略的ETF。
3. 小王若要分析一檔ETF的歷史表現，只要選擇期間（如2024至2025年），系統會計算該段漲跌幅，並提供每日K線與成交量資料，協助他評估這檔ETF。

**使用案例**  
![image](image/使用者案例圖資料庫.png) ![image](image/管理者案例圖資料庫.png) ![image](image/資料庫管理者案例圖資料庫.png)
 - 使用者
   - 紀錄ETF買賣
   - 使用ETF篩選器
   - 建立與追蹤自訂投資組合
 - 說明
   - 使用者可以買入或賣出ETF，，對應「 Transaction(交易紀錄表) 」​
   - 依據標籤（如科技、能源、金融、高股息、ESG等），快速找到符合需求的ETF ，對應「 Category_Level1(第一分類) 」與「 Category_Level2(第二分類) 」​
   - 建立個人化投資組合，追蹤其報酬變化，對應「 Portfolio (持倉資料表) 」​
 - 管理者
   - 查看使用者資料
   - 更新ETF資料
 - 說明
   - 查看使用者帳號資料，對應「 Users(使用者基本資料) 」
   - 更新ETF歷史數據、對應「ETF(基本資料表) 」、 「ETF_HistoryPrice(ETF 歷史價格表)」
 - 資料庫管理者
   - 管理資料庫內容
 - 說明
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
  - 生成K線走勢圖、以及交易量 

- **用戶管理**
  - 個人資料設定（姓名、信箱、單日買賣上限等）
  - 用戶可查詢歷史交易記錄與投資組合變化

- **安全性**
  - 確保用戶個人資料與交易記錄的隱私性
  - 帳號與密碼分成兩個資料庫
## ER Diagram及詳細說明
<!--![image](image/ER%20Diagram.png)-->
**簡略圖**

![image](image/ERD_simp2.png)

**完整圖**

![image](image/ETF.drawio.png)
<br><br>
**密碼資料庫圖**<br>
<img src="image/PASSWORD.drawio.png" width="300px"><br><br>
**1. 使用者密碼 (User_Auth) 資料表屬性**
- 使用者代號 (User_Id)
- 使用者密碼 (Password)
- 最近登入 (Last_Login)

**2. 使用者基本資料 (Users) 資料表屬性**
- 使用者代號 (User_Id)
- 使用者名稱 (User_Name)
- 全名 (Full_Name)
- 電子郵件 (Email)
- 電話號碼 (Phone_Number)
- 權限 (Role)
- 當日最大交易量 (Max_Amount)
- 帳號創建日期 (Users_Created_At)

**3. 交易紀錄表 (Transaction) 資料表屬性**
- 交易代號 (Transaction_Id)
- 使用者代號 (User_Id)
- ETF 代號 (ETF_Id)
- 交易類型 (Transaction_Type)
- 買賣股數 (Shares)
- 交易價格 (Price)
- 交易時間 (Transaction_Date)

**4. 持倉資料 (Portfolio) 資料表屬性**
- 持倉代號 (Portfolio_Id)
- 使用者代號 (User_Id)
- ETF 代號 (ETF_Id)
- 持有股數 (Shares_Held)
- 平均成本 (Average_Cost)
- 最後更新日期 (Last_Updated)

**5. ETF 基本資料 (ETF) 資料表屬性**
- ETF 代號 (ETF_Id)
- ETF 名稱 (ETF_Name)
- 持有人數 (Holders)
- 追蹤指數 (IndexName)
- 規模 (Scale)
- 創立時間 (ETF_Created_At)

**6. ETF 歷史價格 (ETF_HistoryPrice) 資料表屬性**
- 價格紀錄代號 (PriceRecord_Id)
- ETF 代號 (ETF_Id)
- 開盤價 (Open_Price)
- 收盤價 (Close_Price)
- 最高價 (High_Price)
- 最低價 (Low_Price)
- 交易量 (Volume)
- 日期 (History_Date)

**7. 紀錄分類 (ETF_Category) 資料表屬性**
- 紀錄分類代號 (Category_Id)
- ETF 代號 (ETF_Id)
- 第二分類代號 (Category2_Id)

**8. 第二分類 (Category_Level2) 資料表屬性**
- 第二分類代號 (Category2_Id)
- 第一分類代號 (Category1_Id)
- 第二分類名稱 (Category2_Name)

**9. 第一分類 (Category_Level1) 資料表屬性**
- 第一分類代號 (Category1_Id)
- 第一分類名稱 (Category1_Name)

**10. 關聯**
- 「使用者密碼（Auth）」與「使用者基本資料表（Users）」實體有一對一 (1..1) 的關係，表示：1..1 和 1..1。每筆使用者密碼只能對應一位使用者，而每位使用者也只能有一筆密碼資料。
- 「使用者基本資料表（Users）」與「交易紀錄表（Transaction）」實體有一對多 (1..N) 的關係，表示：1..1 和 0..*。一位使用者可以有零到多筆交易紀錄，但每筆交易紀錄只能屬於一位使用者。
- 「使用者基本資料表（Users）」與「持倉資料表（Portfolio）」實體有一對多 (1..N) 的關係，表示：1..1 和 0..*。一位使用者可以持有零到多筆持倉資料，但每筆持倉資料只能屬於一位使用者。
- 「持倉資料表（Portfolio）」與「ETF」實體有一對多 (1..N) 的關係，表示：1..1 和 0..*。每個 ETF 可以出現在多筆持倉資料中，但一筆持倉只能包含一個 ETF。
- 「ETF」與「ETF 歷史價格表（ETF_HistoryPrice）」實體有一對多 (1..N) 的關係，表示：1..1 和 0..*。一個 ETF 可以有零到多筆歷史價格紀錄，但每筆歷史價格紀錄只能對應一個 ETF。
- 「ETF」與「紀錄分類表（ETF_Category）」實體有一對多 (1..N) 的關係，表示：1..1 和 0..*。每筆分類可以對應多個 ETF，但每個 ETF 只能歸類於一個分類。
- 「紀錄分類表（ETF_Category）」與「第二分類表（Category_Level2）」實體有多對多 (M..N) 的關係，表示：0..* 和 0..*。一筆分類可以包含多個次分類，而一個次分類也可以屬於多個分類。
- 「第一分類表（Category_Level1）」與「第二分類表（Category_Level2）」實體有一對多 (1..N) 的關係，表示：1..1 和 0..*。一個第一分類可以包含多個第二分類，但每個第二分類只能屬於一個第一分類。


## 完整性限制(Database Schema)


### ETF 基本資料表 (ETF)

| 欄位名稱            | 資料型態       | 是否可為空 | 欄位說明   | 值域                               | 實際資料舉例            |
| ------------------- | -------------- | ---------- | ---------- | -------------------------------- | ---------------------- |
| ETF_Id (PK)         | VARCHAR(10)    | N          | ETF 代號   | 數字 + 英文字串                  | 0050                  |
| ETF_Name            | VARCHAR(100)   | N          | ETF 名稱   | 長度 1~100 的文字                | 元大台灣50             |
| Holders             | INT            | N          | 持有人數   | ≥ 0 的整數                       | 900000                |
| IndexName           | VARCHAR(50)    | N          | 追蹤指數   | 長度 1~50 的文字                 | 台灣50指數             |
| Scale               | INT            | N          | 規模 (億)  | ≥ 0 的整數                       | 5000                 |
| ETF_Created_At      | TIMESTAMP      | N          | 創立時間   | 時間格式：YYYY-MM-DD              | 2025-05-06    |

| 欄位名稱             | 值域限制說明                                                               | 確認方式（MySQL）                                         |
| ---------------- | -------------------------------------------------------------------- | ------------------------------------------------- |
| ETF\_Id (PK)     | 必須為 1 到 10 個字元長度的字串，僅可包含阿拉伯數字（0–9）與英文字母（A–Z、a–z），且不可為空，用以唯一識別每檔 ETF。 | `CHECK (ETF_Id REGEXP '^[0-9A-Za-z]{1,10}$')`          |
| ETF\_Name        | 必須為 1 到 100 個字元長度的文字，可包含中英文、數字、空格及常見標點符號，且不可為空，用以顯示 ETF 的完整名稱。       | `CHECK (CHAR_LENGTH(ETF_Name) BETWEEN 1 AND 100)` |
| Holders          | 必須為大於或等於 0 的整數，且不可為空，用以統計目前持有該 ETF 的投資人總數。                           | `CHECK (Holders >= 0)`                            |
| IndexName        | 必須為 1 到 50 個字元長度的文字，可包含中英文、空格及常見標點符號，且不可為空，用以記錄該 ETF 所追蹤的基準指數名稱。     | `CHECK (CHAR_LENGTH(IndexName) BETWEEN 1 AND 50)` |
| Scale            | 必須為大於或等於 0 的整數，且不可為空，以「億元」為單位表示該 ETF 的管理規模，實際儲存時以整數形式存放。             | `CHECK (Scale >= 0)`                              |
| ETF\_Created\_At | 必須時間格式：YYYY-MM-DD                                                                                      | 無需額外CHECK約束（MySQL內建驗證）    |



```sql
-- 建立 ETF 資料表
CREATE TABLE ETF (
  ETF_Id VARCHAR(10) PRIMARY KEY,
  ETF_Name VARCHAR(100) NOT NULL,
  Holders INT NOT NULL,
  IndexName VARCHAR(50) NOT NULL,
  Scale INT NOT NULL,
  ETF_Created_At DATE NOT NULL,
  CHECK (ETF_Id REGEXP '^[0-9A-Za-z]{1,10}$'),
  CHECK (CHAR_LENGTH(ETF_Name) BETWEEN 1 AND 100),
  CHECK (Holders >= 0),
  CHECK (CHAR_LENGTH(IndexName) BETWEEN 1 AND 50),
  CHECK (Scale >= 0)
);

-- 範例：插入0050 (台灣50) 之ETF資料
INSERT INTO ETF (ETF_Id, ETF_Name, Holders, IndexName, Scale, ETF_Created_At)
VALUES ('0050', '元大台灣50', 500000, '臺灣50指數', 250, '2003-06-25');
``` 
---
### 交易紀錄表 (Transaction)
 
| 欄位名稱               | 資料型態                 | 是否可為空 | 欄位說明     | 值域                                     | 實際資料舉例          |
| ---------------------- | ------------------------ | ---------- | ------------ | ------------------------------------- | -------------------- |
| Transaction_Id (PK)    | INT                      | N          | 交易代號     |         ≥ 1 的整數                     | 1                    |
| User_Id (FK)           | VARCHAR(50)              | N          | 使用者代號   | 參考 Users.User_Id                     | U000001                    |
| ETF_Id (FK)            | VARCHAR(10)              | N          | ETF 代號     | 參考 ETF.ETF_Id                        | 0050                |
| Transaction_Type       | ENUM('Buy','Sell')       | N          | 交易類型     | 僅可為 'Buy' 或 'Sell'                  | Buy                  |
| Shares                 | INT                      | N          | 買賣股數     | > 0 的整數                             | 100                  |
| Price                  | DECIMAL(10,2)            | N          | 交易價格     | ≥ 0，最多小數第 2 位                    | 125.50                |
| Transaction_Date       | TIMESTAMP                | N          | 交易時間     | 時間格式：YYYY-MM-DD HH:MM:SS          | 2025-05-06 10:00:00    |

| 欄位名稱                 | 值域限制說明                                                | 確認方式（MySQL）                                    |
| -------------------- | ----------------------------------------------------- | -------------------------------------------- |
| Transaction\_Id (PK) | 必須為大於等於 1 的整數，且不可為空，用於唯一識別每一筆交易                   | `CHECK (Transaction_Id >= 1)`                |
| User\_Id (FK)        | 必須為長度不超過 50 個字元的字串，且不可為空，且其值必須對應至 Users 表中的 User\_Id。 | `CHECK (char_length(User_Id) <= 50)`         |
| ETF\_Id (FK)         | 必須為長度 1 至 10 個字元的字串，且不可為空，且其值必須對應至 ETF 表中的 ETF\_Id。   | `CHECK (ETF_Id REGEXP '^[0-9A-Za-z]{1,10}$')`     |
| Transaction\_Type    | 僅可接受字串 'Buy' 或 'Sell'，且不可為空，用以區分買入或賣出交易類型。            | 已使用 ENUM('Buy','Sell') 約束 |
| Shares               | 必須為大於 0 的整數，且不可為空，用以表示此筆交易的股數。                        | `CHECK (Shares > 0)`                         |
| Price                | 必須為大於或等於 0 且最多保留兩位小數的十進位數，且不可為空，用以記錄每單位交易價格。          | `CHECK (Price >= 0)`                         |
| Transaction\_Date    | 必須時間格式：YYYY-MM-DD HH:MM:SS                                                        | 無需額外CHECK約束（MySQL內建驗證）    |



```sql
-- 建立交易紀錄表
CREATE TABLE `Transaction` (
  Transaction_Id INT PRIMARY KEY,
  User_Id VARCHAR(50) NOT NULL,
  ETF_Id VARCHAR(10) NOT NULL,
  Transaction_Type ENUM('Buy','Sell') NOT NULL,
  Shares INT NOT NULL,
  Price DECIMAL(10,2) NOT NULL,
  Transaction_Date TIMESTAMP NOT NULL,
  FOREIGN KEY (User_Id) REFERENCES Users(User_Id),
  FOREIGN KEY (ETF_Id) REFERENCES ETF(ETF_Id),
  CHECK (Shares > 0),
  CHECK (Price >= 0),
  CHECK (Transaction_Type IN ('Buy','Sell'))
);


-- 範例：記錄001使用者於2025-04-29買進0050 100股，單價167.80
INSERT INTO `Transaction` (User_Id, ETF_Id, Transaction_Type, Shares, Price, Transaction_Date)
VALUES ('U000001', '0050', 'Buy', 100, 168.80, '2025-04-29');
```

---
### 持倉資料表 (Portfolio)

| 欄位名稱               | 資料型態       | 是否可為空 | 欄位說明     | 值域                                     | 實際資料舉例          |
| ---------------------- | -------------- | ---------- | ------------ | ------------------------------------- | -------------------- |
| Portfolio_Id (PK)      | INT            | N          | 持倉代號     | ≥ 1 的整數                             | 1                    |
| User_Id (FK)           | VARCHAR(50)    | N          | 使用者代號   | 參考 Users.User_Id                      | U000001              |
| ETF_Id (FK)            | VARCHAR(10)    | N          | ETF 代號     | 參考 ETF.ETF_Id                        | 0050                |
| Shares_Held            | INT            | N          | 持有股數     | >= 0 的整數                             | 500                   |
| Average_Cost           | DECIMAL(10,2)  | N          | 平均成本     | ≥ 0，最多小數第 2 位                    | 175                |
| Last_Updated           | TIMESTAMP      | N          | 最後更新日期 | 時間格式：YYYY-MM-DD HH:MM:SS           | 2025-05-06 10:00:00    |

| 欄位名稱               | 值域限制說明                                      | 確認方式（MySQL）                                |
| ------------------ | ------------------------------------------- | ---------------------------------------- |
| Portfolio\_Id (PK) | 必須為大於等於 1 的整數，且不可為空，用以唯一識別持倉紀錄             | `CHECK (Portfolio_Id >= 1)`              |
| User\_Id (FK)      | 必須為長度不超過 50 個字元的字串，且不可為空，對應 Users.User\_Id。 | `CHECK (CHAR_LENGTH(User_Id) <= 50)`     |
| ETF\_Id (FK)       | 必須為長度 1 至 10 個字元的字串，且不可為空，對應 ETF.ETF\_Id。   | `CHECK (ETF_Id REGEXP '^[0-9A-Za-z]{1,10}$')` |
| Shares\_Held       | 必須為大於等於 0 的整數，且不可為空，用以表示目前持有該檔 ETF 的股數。       | `CHECK (Shares_Held >= 0)`                |
| Average\_Cost      | 必須為大於或等於 0 且最多保留兩位小數的十進位數，且不可為空，用以記錄每股平均成本。 | `CHECK (Average_Cost >= 0)`              |
| Last\_Updated      | 必須時間格式：YYYY-MM-DD HH:MM:SS                                           | 無需額外CHECK約束（MySQL內建驗證）    |



```sql
-- 建立持倉資料表
CREATE TABLE Portfolio (
  Portfolio_Id INT PRIMARY KEY ,
  User_Id VARCHAR(50) NOT NULL,
  ETF_Id VARCHAR(10) NOT NULL,
  Shares_Held INT NOT NULL,
  Average_Cost DECIMAL(10,2) NOT NULL,
  Last_Updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (User_Id) REFERENCES Users(User_Id),
  FOREIGN KEY (ETF_Id) REFERENCES ETF(ETF_Id),
  CHECK (Portfolio_Id >= 1),                  
  CHECK (CHAR_LENGTH(User_Id) <= 50),      
  CHECK (Shares_Held >= 0),
  CHECK (Average_Cost >= 0)
);


-- 範例：使用者代號1持有0050 100股，平均成本167.80
INSERT INTO Portfolio (User_Id, ETF_Id, Shares_Held, Average_Cost)
VALUES ('U000001', '0050', 100, 167.80);
```

---

### ETF 歷史價格表 (ETF_HistoryPrice)

| 欄位名稱               | 資料型態       | 是否可為空 | 欄位說明     | 值域                                    | 實際資料舉例          |
| ---------------------- | -------------- | ---------- | ------------ | ------------------------------------ | -------------------- |
| PriceRecord_Id (PK)    | INT            | N          | 價格紀錄代號 | 從 1 開始遞增的整數                     | 1                    |
| ETF_Id (FK)            | VARCHAR(10)    | N          | ETF 代號     | 參考 ETF.ETF_Id                       | 0050              |
| Open_Price             | DECIMAL(10,2)  | N          | 開盤價       | ≥ 0，最多小數第 2 位                   | 125.00                |
| Close_Price            | DECIMAL(10,2)  | N          | 收盤價       | ≥ 0，最多小數第 2 位                   | 125.50                |
| High_Price             | DECIMAL(10,2)  | N          | 最高價       | ≥ 0，最多小數第 2 位                   | 126.00                |
| Low_Price              | DECIMAL(10,2)  | N          | 最低價       | ≥ 0，最多小數第 2 位                   | 124.80                |
| Volume                 | BIGINT         | N          | 交易量       | ≥ 0 的整數                            | 3500000              |
| History_Date           | DATE           | N          | 日期         | 時間格式：YYYY-MM-DD                   | 2025-05-05           |

| 欄位名稱                 | 值域限制說明                                     | 確認方式（MySQL）                                |
| -------------------- | ------------------------------------------ | ---------------------------------------- |
| PriceRecord\_Id (PK) | 必須為從 1 開始連續遞增且大於等於 1 的整數，且不可為空，用以唯一識別每筆紀錄。 | 使用 AUTO_INCREMENT 已確保遞增            |
| ETF\_Id (FK)         | 必須為長度 1 至 10 個字元的字串，且不可為空，對應 ETF.ETF\_Id。  | `CHECK (ETF_Id REGEXP '^[0-9A-Za-z]{1,10}$')` |
| Open\_Price          | 必須為大於或等於 0 且最多保留兩位小數的十進位數，且不可為空，記錄當日開盤價。   | `CHECK (Open_Price >= 0)`                |
| Close\_Price         | 必須為大於或等於 0 且最多保留兩位小數的十進位數，且不可為空，記錄收盤價。     | `CHECK (Close_Price >= 0)`               |
| High\_Price          | 必須為大於或等於 0 且最多保留兩位小數的十進位數，且不可為空，記錄當日最高價。   | `CHECK (High_Price >= 0)`                |
| Low\_Price           | 必須為大於或等於 0 且最多保留兩位小數的十進位數，且不可為空，記錄當日最低價。   | `CHECK (Low_Price >= 0)`                 |
| Volume               | 必須為大於或等於 0 的整數，且不可為空，用以表示當日成交量。            | `CHECK (Volume >= 0)`                    |
| History\_Date        | 必須時間格式：YYYY-MM-DD                                          | 無需額外CHECK約束（MySQL內建驗證）    |



```sql
-- 建立歷史價格表
CREATE TABLE ETF_HistoryPrice (
  PriceRecord_Id INT PRIMARY KEY AUTO_INCREMENT,
  ETF_Id VARCHAR(10) NOT NULL,
  Open_Price DECIMAL(10,2) NOT NULL,
  Close_Price DECIMAL(10,2) NOT NULL,
  High_Price DECIMAL(10,2) NOT NULL,
  Low_Price DECIMAL(10,2) NOT NULL,
  Volume BIGINT NOT NULL,
  History_Date DATE NOT NULL,
  FOREIGN KEY (ETF_Id) REFERENCES ETF(ETF_Id),
  CHECK (Open_Price >= 0),
  CHECK (Close_Price >= 0),
  CHECK (High_Price >= 0),
  CHECK (Low_Price >= 0),
  CHECK (Volume >= 0)
);


-- 範例：紀錄2025-04-29 之0050開盤167.15、收盤167.80、最高168.00、最低166.50、成交量10830
INSERT INTO ETF_HistoryPrice (ETF_Id, Open_Price, Close_Price, High_Price, Low_Price, Volume, History_Date)
VALUES ('0050', 167.15, 167.80, 168.00, 166.50, 10830, '2025-04-28');
```

---
### 第一分類表 (Category_Level1)

| 欄位名稱           | 資料型態    | 是否可為空 | 欄位說明     | 值域                               | 實際資料舉例    |
| ------------------ | ----------- | ---------- | ------------ | ------------------------------- | -------------- |
| Category1_Id (PK)  | INT         | N          | 第一分類代號 | 從 1 開始遞增的整數               | 1              |
| Category1_Name     | VARCHAR(20) | N          | 第一分類名稱 | 長度 1~20 的文字                 | 股票型          |

| 欄位名稱               | 值域限制說明                                 | 確認方式（MySQL）                                              |
| ------------------ | -------------------------------------- | ------------------------------------------------------ |
| Category1\_Id (PK) | 必須為從 1 開始連續遞增且大於等於 1 的整數，且不可為空。        | 使用 AUTO_INCREMENT 已確保遞增                            |
| Category1\_Name    | 必須為長度 1 到 20 個字元的文字，且不可為空，僅可包含中、英文與數字。 | `CHECK (CHAR_LENGTH(Category1_Name) BETWEEN 1 AND 20)` |



```sql
-- 建立第一分類表
CREATE TABLE Category_Level1 (
  Category1_Id INT PRIMARY KEY AUTO_INCREMENT,
  Category1_Name VARCHAR(20) NOT NULL,
  CHECK (CHAR_LENGTH(Category1_Name) BETWEEN 1 AND 20)
);


-- 範例：新增第一分類「股票型」
INSERT INTO Category_Level1 (Category1_Name) VALUES ('股票型');
```

---
### 第二分類表 (Category_Level2)

| 欄位名稱              | 資料型態    | 是否可為空 | 欄位說明       | 值域                                      | 實際資料舉例  |
| --------------------- | ----------- | ---------- | -------------- | -------------------------------------- | ------------ |
| Category2_Id (PK)     | INT         | N          | 第二分類代號   | 從 1 開始遞增的整數                      | 1            |
| Category1_Id (FK)     | INT         | N          | 第一分類代號   | 參考 Category_Level1.Category1_Id       | 1            |
| Category2_Name        | VARCHAR(20) | N          | 第二分類名稱   | 長度 1~20 的文字                        | 市值型        |

| 欄位名稱               | 值域限制說明                                                      | 確認方式（MySQL）                                              |
| ------------------ | ----------------------------------------------------------- | ------------------------------------------------------ |
| Category2\_Id (PK) | 必須為從 1 開始連續遞增且大於等於 1 的整數，且不可為空。                             | 使用 AUTO_INCREMENT 已確保遞增                            |
| Category1\_Id (FK) | 必須為大於等於 1 的整數，且不可為空，其值必須對應至 Category\_Level1.Category1\_Id。 | 外鍵約束已確保參照完整性                            |
| Category2\_Name    | 必須為長度 1 到 20 個字元的文字，且不可為空，僅可包含中、英文與數字。                      | `CHECK (CHAR_LENGTH(Category2_Name) BETWEEN 1 AND 20)` |



```sql
-- 建立第二分類表
CREATE TABLE Category_Level2 (
  Category2_Id INT PRIMARY KEY AUTO_INCREMENT,
  Category1_Id INT NOT NULL,
  Category2_Name VARCHAR(20) NOT NULL,
  FOREIGN KEY (Category1_Id) REFERENCES Category_Level1(Category1_Id),
  CHECK (CHAR_LENGTH(Category2_Name) BETWEEN 1 AND 20)
);

-- 範例：新增第二分類「大型權值」屬於第一分類1
INSERT INTO Category_Level2 (Category1_Id, Category2_Name) VALUES (1, '大型權值');
```

---
### 紀錄分類表 (ETF_Category)

| 欄位名稱            | 資料型態    | 是否可為空 | 欄位說明       | 值域                                   | 實際資料舉例    |
| ------------------- | ----------- | ---------- | -------------- | ------------------------------------ | -------------- |
| Category_Id (PK)    | INT         | N          | 紀錄分類代號   | 從 1 開始遞增的整數                    | 1              |
| ETF_Id (FK)         | VARCHAR(10) | N          | ETF 代號       | 參考 ETF.ETF_Id                      | 0050        |
| Category2_Id (FK)   | INT         | N          | 第二分類代號   | 參考 Category_Level2.Category2_Id     | 1              |

| 欄位名稱               | 值域限制說明                                                      | 確認方式（MySQL）                                |
| ------------------ | ----------------------------------------------------------- | ---------------------------------------- |
| Category\_Id (PK)  | 必須為從 1 開始連續遞增且大於等於 1 的整數，且不可為空。                             | 使用 AUTO_INCREMENT 已確保遞增               |
| ETF\_Id (FK)       | 必須為長度 1 到 10 個字元的字串，且不可為空，其值必須對應至 ETF.ETF\_Id。              | 外鍵約束已確保參照完整性 |
| Category2\_Id (FK) | 必須為大於等於 1 的整數，且不可為空，其值必須對應至 Category\_Level2.Category2\_Id。 | 外鍵約束已確保參照完整性              |


```sql
-- 建立ETF與分類對應表
CREATE TABLE ETF_Category (
  Category_Id INT PRIMARY KEY AUTO_INCREMENT,
  ETF_Id VARCHAR(10) NOT NULL,
  Category2_Id INT NOT NULL,
  FOREIGN KEY (ETF_Id) REFERENCES ETF(ETF_Id),
  FOREIGN KEY (Category2_Id) REFERENCES Category_Level2(Category2_Id)
);

-- 範例：將0050歸類至第二分類1 (大型權值)
INSERT INTO ETF_Category (ETF_Id, Category2_Id) VALUES ('0050', 1);
```

---
### 使用者基本資料表 (Users)

| 欄位名稱              | 資料型態             | 是否可為空 | 欄位說明       | 值域                              | 實際資料舉例             |
| --------------------- | -------------------- | ---------- | -------------- | ------------------------------- | ----------------------- |
| User_Id (PK)          | VARCHAR(50)          | N          | 使用者代號     | 長度 1~50 的文字                 | U000001                  |
| User_Name             | VARCHAR(50)          | N          | 使用者名稱     | 長度 1~50 的文字                 | alice                   |
| Full_Name             | VARCHAR(100)         | N          | 全名           | 長度 1~100 的文字                 | Alice Chen              |
| Email                 | VARCHAR(100)         | N          | 電子郵件       | Email 格式                       | alice@example.com       |
| Phone_Number          | VARCHAR(10)          | N          | 電話號碼       | 長度固定為 10 碼                  | 0912345678              |
| Role                  | ENUM('user','admin') | N          | 權限           | 僅限 'user' 或 'admin'           | user                    |
| Max_Amount            | INT                  | N          | 當日最大交易量 | ≥ 0 的整數                        | 1000000                 |
| Users_Created_At      | TIMESTAMP            | N          | 帳號創建日期   | 時間格式：YYYY-MM-DD HH:MM:SS     | 2025-05-06 10:00:00    |

| 欄位名稱               | 值域限制說明                                                                      | 確認方式（MySQL）                                                          |
| ------------------ | ----------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| User\_Id (PK)      | 必須為長度 1~50 的文字，且不可為空，由程式依需產生                                        | `CHECK (CHAR_LENGTH(User_Id) BETWEEN 1 AND 50)`                        |
| User\_Name         | 必須為長度 1 到 50 個字元的文字，且不可為空，可包含英數字、底線及常見標點。                 | `CHECK (CHAR_LENGTH(User_Name) BETWEEN 1 AND 50)`                     |
| Full\_Name         | 必須為長度 1 到 100 個字元的文字，且不可為空，可包含中英文及空格。                          | `CHECK (CHAR_LENGTH(Full_Name) BETWEEN 1 AND 100)`                    |
| Email              | 必須符合標準電子郵件格式，且長度不超過 100 個字元，不可為空，用以作為聯絡與驗證依據。          | `CHECK (Email REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$')` |
| Phone\_Number      | 必須為長度固定 10 碼且僅包含數字的字串，格式如 0912345678，且不可為空。                     | `CHECK (Phone_Number REGEXP '^[0-9]{10}$')`                                |
| Role               | 僅可接受字串 'user' 或 'admin' 其中之一，且不可為空，用以設定使用者權限等級。                | `CHECK (Role IN ('user','admin'))`                                          |
| Max\_Amount        | 必須為大於或等於 0 的整數，且不可為空，用以限制使用者於單日內可執行之最大交易數量。            | `CHECK (Max_Amount >= 0)`                                                  |
| Users\_Created\_At | 日期時間格式：YYYY-MM-DD HH:MM:SS，預設為當前時間                                       | 無需額外CHECK約束（MySQL內建驗證）                                                |



```sql
-- 建立使用者資料表
CREATE TABLE Users (
  User_Id VARCHAR(50) PRIMARY KEY,
  User_Name VARCHAR(50) NOT NULL,
  Full_Name VARCHAR(100) NOT NULL,
  Email VARCHAR(100) NOT NULL UNIQUE,
  Phone_Number VARCHAR(10) NOT NULL,
  Role ENUM('user','admin') NOT NULL,
  Max_Amount INT NOT NULL DEFAULT 0,
  Users_Created_At TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CHECK (CHAR_LENGTH(User_Id) BETWEEN 1 AND 50),
  CHECK (CHAR_LENGTH(User_Name) BETWEEN 1 AND 50),
  CHECK (CHAR_LENGTH(Full_Name) BETWEEN 1 AND 100),
  CHECK (Email REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'),
  CHECK (Phone_Number REGEXP '^[0-9]{10}$'),
  CHECK (Role IN ('user','admin')),
  CHECK (Max_Amount >= 0)
);

-- 範例：新增使用者 Bob
INSERT INTO Users (User_Name, Full_Name, Email, Phone_Number, Role, Max_Amount)
VALUES ('bob', 'Bob Lee', 'bob@example.com', '0987654321', 'user', 500000);
```


---
### (在其他資料庫)使用者密碼 (Auth)
| 欄位名稱            | 資料型態         | 是否可為空 | 欄位說明  | 值域                         | 實際資料舉例               |
| -------------- | ------------ | ----- | ----- | ------------------------------------------ | ------------------------ |
| User_Id (PK)    | VARCHAR(50)  | N     | 使用者代號 | 參考 Users.User_Id                      | U000001              |
| Password        | VARCHAR(255) | N     | 使用者密碼 | 長度 1~255 的文字                      | abcdef                 |
| Last_Login      | TIMESTAMP    | N     | 最近登入  | 時間格式：YYYY-MM-DD HH:MM:SS           | 2025-05-06 10:00:00    |

```sql
-- 建立使用者密碼資料表 Auth
CREATE TABLE Auth (
  User_Id VARCHAR(50) PRIMARY KEY,
  Password VARCHAR(255) NOT NULL,
  Last_Login TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
);

-- 範例：新增使用者密碼為 'abcd'
INSERT INTO Auth (User_Id, Password) VALUES ('U000001', '王小明');
```
---

## 使用者權限設定

#### 1. 使用者
ETF_DB
| 資料表 | 權限 | 說明 |
|---------|---------|------|
| ETF | SELECT | 查看ETF |
| Transaction | SELECT,INSERT,UPDATE,DELETE | 讀寫交易紀錄 |
| Portfolio | SELECT,INSERT,UPDATE,DELETE | 讀寫持倉 |
| ETF_HistoryPrice | SELECT | 查看歷史價格 |
| Category_Level1 | SELECT | 查看第一分類 |
| Category_Level2 | SELECT | 查看第二分類 |
| ETF_Category | SELECT | 查看分類 |
| Users | SELECT | 查看使用者基本資料 |

AUTH_DB
| 資料表 | 權限 | 說明 |
|---------|---------|------|
| Auth | SELECT | 比對密碼輸入是否正確 |

#### SQL語法

```sql
CREATE USER 'user'@'%' IDENTIFIED BY '222';
GRANT SELECT ON etf_db.* TO 'user'@'%';
GRANT INSERT,UPDATE,DELETE ON etf_db.Transaction TO 'user'@'%';
GRANT INSERT,UPDATE,DELETE ON etf_db.Portfolio TO 'user'@'%';
GRANT SELECT ON auth_db.* TO 'user'@'%';
FLUSH PRIVILEGES;
```

#### 2. 管理者
ETF_DB
| 資料表 | 權限 | 說明 |
|---------|---------|------|
| ETF | SELECT,INSERT,UPDATE,DELETE,CREATE VIEW,LOCK TABLES,SHOW VIEW,DROP | 讀寫ETF及備份 |
| Transaction | SELECT,INSERT,UPDATE,DELETE,CREATE VIEW,LOCK TABLES,SHOW VIEW,DROP | 讀寫交易紀錄及備份 |
| Portfolio | SELECT,INSERT,UPDATE,DELETE,CREATE VIEW,LOCK TABLES,SHOW VIEW,DROP | 讀寫持倉及備份 |
| ETF_HistoryPrice | SELECT,INSERT,UPDATE,DELETE,CREATE VIEW,LOCK TABLES,SHOW VIEW,DROP | 讀寫歷史價格及備份 |
| Category_Level1 | SELECT,INSERT,UPDATE,DELETE,CREATE VIEW,LOCK TABLES,SHOW VIEW,DROP | 讀寫第一分類及備份 |
| Category_Level2 | SELECT,INSERT,UPDATE,DELETE,CREATE VIEW,LOCK TABLES,SHOW VIEW,DROP | 讀寫第二分類及備份 |
| ETF_Category | SELECT,INSERT,UPDATE,DELETE,CREATE VIEW,LOCK TABLES,SHOW VIEW,DROP | 讀寫分類及備份 |
| Users | SELECT,INSERT,UPDATE,DELETE,CREATE VIEW,LOCK TABLES,SHOW VIEW,DROP | 讀寫使用者基本資料及備份 |

AUTH_DB
| 資料表 | 權限 | 說明 |
|---------|---------|------|
| Auth | SELECT | 比對密碼輸入是否正確 |


#### SQL語法

```sql
CREATE USER 'admin'@'%' IDENTIFIED BY '111';
GRANT SELECT,INSERT,UPDATE,DELETE,CREATE VIEW,LOCK TABLES,SHOW VIEW,DROP ON etf_db.* TO 'admin'@'%';
GRANT SELECT ON auth_db.* TO 'admin'@'%';
FLUSH PRIVILEGES;
```

#### 3. 資料庫管理者
ETF_DB
| 資料表 | 權限 | 說明 |
|---------|---------|------|
| ETF | ALL | 讀寫ETF |
| Transaction | ALL  | 讀寫交易紀錄 |
| Portfolio | ALL  | 讀寫持倉 |
| ETF_HistoryPrice | ALL  | 讀寫歷史價格 |
| Category_Level1 | ALL  | 讀寫第一分類 |
| Category_Level2 | ALL  | 讀寫第二分類 |
| ETF_Category | ALL  | 讀寫分類 |
| Users | ALL | 讀寫使用者基本資料 |

AUTH_DB
| 資料表 | 權限 | 說明 |
|---------|---------|------|
| Auth | ALL | 讀寫密碼及更新最後登入 |

#### SQL語法

```sql
CREATE USER 'DBA'@'localhost' IDENTIFIED BY '000';
GRANT ALL PRIVILEGES ON etf_db.* TO 'DBA'@'localhost';
GRANT ALL PRIVILEGES ON auth_db.* TO 'DBA'@'localhost';
FLUSH PRIVILEGES;
```
---
## 使用者View

```sql
-- 1.ETF 標籤層次結構 View
CREATE OR REPLACE VIEW vw_etf_category_overview AS
SELECT
    c1.Category1_Id,
    c1.Category1_Name AS 父標籤名稱,
    c2.Category2_Id,
    c2.Category2_Name AS 子標籤名稱
FROM
    Category_Level1 c1
LEFT JOIN
    Category_Level2 c2
ON
    c2.Category1_Id = c1.Category1_Id
ORDER BY
    c1.Category1_Name,
    c2.Category2_Name;
```
### 使用方式
```sql
--1.1查看所有標籤層次結構
SELECT * FROM vw_etf_category_overview;
```
### 說明
- 功能：此查詢用於檢索ETF的標籤列表，包含父標籤及其對應的子標籤。
- 目的：提供ETF分類層次的結構化視圖，展示ETF在廣泛的父分類及其更具體的子分類下組織。
- 詳情：
   - 選擇 Category1_Id、 Category1_Name（父標籤名稱）、 Category2_Id 和 Category2_Name（子標籤名稱）。
   - 使用 LEFT JOIN 確保包含所有父標籤，即使某些父標籤沒有對應的子標籤
   - 按父標籤名稱和子標籤名稱排序。
### 執行結果:
<img src="image/DB1.png" width="700px"><br><br>

---

```sql
-- 2.建立特定分類 ETF View
CREATE OR REPLACE VIEW vw_etf_by_category AS
SELECT DISTINCT 
    e.ETF_Id, 
    e.ETF_Name, 
    e.Holders, 
    e.Scale, 
    e.ETF_Created_At, 
    c1.Category1_Name AS 父標籤名稱, 
    c2.Category2_Name AS 子標籤名稱
FROM ETF e
LEFT JOIN ETF_Category ec 
    ON e.ETF_Id = ec.ETF_Id
LEFT JOIN Category_Level2 c2 
    ON ec.Category2_Id = c2.Category2_Id
LEFT JOIN Category_Level1 c1 
    ON c2.Category1_Id = c1.Category1_Id
ORDER BY e.ETF_Id;
```
### 使用方式
```sql
--2.1查看特定父標籤和子標籤的 ETF
SELECT * FROM vw_etf_by_category 
WHERE 父標籤名稱 = '股票型' AND 子標籤名稱 = '大型權值';
```
### 說明
- 功能：此查詢檢索符合特定父標籤(ex:股票型)和子標籤(ex:大型權值)的 ETF。
- 目的：根據特定分類條件過濾ETF並輸出。
- 詳情：
  - 選擇不重複的 ETF 詳細資訊，包括 ETF_Id、ETF_Name、Holders、Scale、ETF_Created_At、父標籤名稱和子標籤名稱。
  - 關聯 ETF、ETF_Category、Category_Level2和Category_Level1表，以連結ETF與其分類。
  - 篩選條件為父標籤(ex:股票型)和子標籤(ex:大型權值)。
  - 按 ETF_Id 排序。
### 執行結果:
<img src="image/DB2.png" width="700px"><br><br>

---

```sql
-- 3.建立 ETF 下拉選單 View
CREATE OR REPLACE VIEW vw_etf_dropdown AS
SELECT 
    ETF_Id, 
    ETF_Name
FROM ETF
ORDER BY ETF_Id;
```
### 使用方式
```sql
-- 3.1取得所有 ETF 列表（用於下拉選單）
SELECT * FROM vw_etf_dropdown;
```
```sql
-- 3.2搜尋包含特定關鍵字的 ETF
SELECT * FROM vw_etf_dropdown 
WHERE ETF_Name LIKE '%元大%';
```
### 說明
- 功能：此查詢檢索所有 ETF 的列表，用於填充下拉選單。
- 目的：提供簡單的 ETF ID 和名稱列表，供用戶在介面中選擇。
- 詳情：
  - 從 ETF 表選擇 ETF_Id 和 ETF_Name。
  - 使用(ex:元大)匹配名稱包含「元大」的 ETF。
  - 按 ETF_Id 排序。
### 執行結果:
(3.1)<br>
<img src="image/DB3.png" width="400px"><br><br>
(3.2)<br>
<img src="image/DB3.1.png" width="400px"><br><br>

---

```sql
-- 4建立 ETF 歷史價格 View 
CREATE OR REPLACE VIEW vw_etf_price_history AS
SELECT
    hp.ETF_Id,
    e.ETF_Name,
    hp.History_Date,
    hp.Close_Price
FROM ETF_HistoryPrice hp
JOIN ETF e ON hp.ETF_Id = e.ETF_Id
ORDER BY hp.ETF_Id, hp.History_Date;
```
### 使用方式
```sql
-- 4.1期間漲跌幅計算
SELECT 
    start_data.ETF_Id,
    start_data.ETF_Name,
    start_data.History_Date AS 起始日期,
    start_data.Close_Price AS 起始價格,
    end_data.History_Date AS 結束日期,
    end_data.Close_Price AS 結束價格,
    ROUND((end_data.Close_Price - start_data.Close_Price) / start_data.Close_Price * 100, 2) AS 漲跌幅
FROM 
    (SELECT * FROM vw_etf_price_history 
     WHERE ETF_Id = '0050' AND History_Date >= '2024-01-01' 
     ORDER BY History_Date ASC LIMIT 1) start_data
JOIN 
    (SELECT * FROM vw_etf_price_history 
     WHERE ETF_Id = '0050' AND History_Date <= '2025-05-30' 
     ORDER BY History_Date DESC LIMIT 1) end_data
ON start_data.ETF_Id = end_data.ETF_Id;
```
### 說明
- 功能：此查詢計算 ETF '0050' 在 2024 年 1 月 1 日至 2025 年 5 月 30 日期間的價格漲跌幅百分比。
- 目的：展示ETF在指定期間價格漲跌幅的表現。
- 詳情：
  - 選取指定日期範圍內最早（t_start）和最晚（t_end）的收盤價。
  - 計算漲跌幅百分比：((結束價 - 起始價) / 起始價) * 100，四捨五入至小數點後兩位。
  - 返回實際起始日、起始收盤價、實際結束日、結束收盤價和漲跌幅百分比。
### 執行結果:
<img src="image/DB4.png" width="700px"><br><br>

---
```sql
-- 5. 用戶持倉查看視圖（相同ETF合併顯示）
CREATE VIEW v_user_portfolio AS
SELECT 
    p.User_Id,
    p.ETF_Id,
    e.ETF_Name,
    SUM(p.Shares_Held) as Shares_Held,
    SUM(p.Shares_Held * p.Average_Cost) / SUM(p.Shares_Held) as Average_Cost,
    MAX(p.Last_Updated) as Last_Updated
FROM 
    Portfolio p
JOIN 
    ETF e ON p.ETF_Id = e.ETF_Id
GROUP BY 
    p.User_Id, p.ETF_Id, e.ETF_Name;
```
### 使用方式
```sql
-- 5.1查看 user001 的持倉
SELECT * FROM v_user_portfolio WHERE User_Id = 'user001';
```

```sql
-- 5.2買入操作 - 直接SQL（修改引號內的參數）
INSERT INTO Transaction (
    Transaction_Id, 
    User_Id, 
    ETF_Id, 
    Transaction_Type, 
    Shares, 
    Price, 
    Transaction_Date
) VALUES (
    (SELECT COALESCE(MAX(Transaction_Id), 0) + 1 FROM Transaction t),
    'user001',      -- 修改：用戶ID
    '0057',         -- 修改：ETF代碼
    'Buy',          -- 固定：買入
    100,            -- 修改：股數
    150.50,         -- 修改：價格
    NOW()
);

-- 買入後更新投資組合（修改引號內的參數）
INSERT INTO Portfolio (
    Portfolio_Id,
    User_Id, 
    ETF_Id, 
    Shares_Held, 
    Average_Cost, 
    Last_Updated
) VALUES (
    (SELECT COALESCE(MAX(Portfolio_Id), 0) + 1 FROM Portfolio p),
    'user001',      -- 修改：用戶ID
    '0057',         -- 修改：ETF代碼
    100,            -- 修改：股數
    150.50,         -- 修改：價格
    NOW()
) ON DUPLICATE KEY UPDATE
    Shares_Held = Shares_Held + VALUES(Shares_Held),
    Average_Cost = ((Shares_Held * Average_Cost) + (VALUES(Shares_Held) * VALUES(Average_Cost))) / (Shares_Held + VALUES(Shares_Held)),
    Last_Updated = NOW();
SELECT * FROM v_user_portfolio WHERE User_Id = 'user001';

```
```sql
--5.3使用者賣出後更新交易紀錄跟投資組合(股數為0則刪除ETF)

-- 1. 插入賣出交易紀錄
INSERT INTO `Transaction` (
    Transaction_Id, User_Id, ETF_Id, Transaction_Type, 
    Shares, Price, Transaction_Date
) VALUES (
    (SELECT COALESCE(MAX(Transaction_Id), 0) + 1 FROM `Transaction` t),
    'user001', '0057', 'Sell', 50, 160.00, NOW()
);

-- 2. 更新持倉股數
UPDATE Portfolio
SET 
    Shares_Held = Shares_Held - 50,
    Last_Updated = NOW()
WHERE 
    User_Id = 'user001'
    AND ETF_Id = '0057'
    AND Shares_Held >= 50;

-- 3. 刪除股數為 0 的持倉
DELETE FROM Portfolio
WHERE User_Id = 'user001'
  AND ETF_Id = '0057'
  AND Shares_Held = 0;
SELECT * FROM v_user_portfolio WHERE User_Id = 'user001';
```

### 說明
(5.2)
- 功能：此程式碼處理ETF買入交易，並相應更新用戶的投資組合。
- 目的：記錄購買交易，並在投資組合中新增或更新相應記錄。
- 詳情：
  - 插入交易記錄：
  - 記錄買入交易，包含唯一的 Transaction_Id、用戶 ID、ETF ID、交易類型（'Buy'）、股數、價格和時間。
  - 插入/更新投資組合：
  - 若用戶首次持有該 ETF，則插入新記錄，包含指定股數和成本。
  - 若用戶已持有該 ETF，則更新 Shares_Held，並使用加權平均公式重新計算 Average_Cost。
  - 新增或更新投資組合記錄：
  - 更新 Last_Updated 時間<br>
  
(5.3)
- 功能：此程式碼處理ETF賣出交易，並更新或移除用戶的投資組合記錄。<br>
- 目的：記錄賣出交易，並調整投資組合，若剩餘股數為零則移除該ETF。<br>
- 詳情：<br>
  - 插入交易記錄：<br>
  - 記錄賣出交易，包含唯一的Transaction_Id、用戶 ID、ETF ID、交易類型（'Sell'）、股數、價格和時間戳。<br>
  - 更新投資組合：<br>
  - 減少Shares_Held並更新Last_Updated時間戳，確保持有股數足夠。<br>
  - 刪除投資組合記錄：<br>
  - 若 Shares_Held變為零，則移除該投資組合記錄。
### 執行結果:
(5.1初始持倉)<br>
<img src="image/start.png" width="900px"><br><br>
(5.2買入100股的0057)<br>
<img src="image/buy.png" width="900px"><br><br>
(5.3賣出50股的0057)<br>
<img src="image/sell.png" width="900px"><br><br>

---

```sql
-- 6.建立 ETF K線資料與每日變動 View
CREATE OR REPLACE VIEW vw_etf_daily_kline AS
SELECT 
    ETF_Id,
    History_Date,
    Open_Price,
    High_Price,
    Low_Price,
    Close_Price,
    Volume,
    LAG(Close_Price) OVER (PARTITION BY ETF_Id ORDER BY History_Date) AS prev_close,
    Close_Price - LAG(Close_Price) OVER (PARTITION BY ETF_Id ORDER BY History_Date) AS daily_change,
    CASE 
        WHEN LAG(Close_Price) OVER (PARTITION BY ETF_Id ORDER BY History_Date) IS NOT NULL 
        THEN ROUND(((Close_Price - LAG(Close_Price) OVER (PARTITION BY ETF_Id ORDER BY History_Date)) / LAG(Close_Price) OVER (PARTITION BY ETF_Id ORDER BY History_Date)) * 100, 2)
        ELSE NULL 
    END AS daily_change_percent
FROM ETF_HistoryPrice
ORDER BY ETF_Id, History_Date;
```
### 使用方式
```sql
-- 6.1查看特定 ETF 在特定期間的 K 線資料
SELECT * FROM vw_etf_daily_kline
WHERE ETF_Id = '0050'
  AND History_Date BETWEEN '2025-01-10' AND '2025-03-16'
ORDER BY History_Date;
```
```sql
-- 6.2查看特定日期所有 ETF 的表現
SELECT * FROM vw_etf_daily_kline
WHERE History_Date = '2025-06-07';

```
### 說明
- 功能：此查詢檢索 ETF '0050' 在 2025 年 1 月 10 日至 3 月 16 日期間的每日 K 線資料（開盤、最高、最低、收盤價）及每日價格變動百分比。<br>
- 目的：提供詳細的每日價格數據和表現指標，供技術分析使用。<br>
- 詳情：<br>
  - 選擇 ETF_Id、 History_Date、 Open_Price、 High_Price、 Low_Price、 Close_Price 和 Volume。<br>
  - 使用LAG函數取得前一日收盤價。<br>
  - 計算每日變動金額（當日收盤價 - 前日收盤價）和每日變動百分比（變動金額 / 前日收盤價 * 100，四捨五入至小數點後兩位）。<br>
  - 篩選 ETF '0050' 在指定日期範圍內的數據。<br>
  - 按History_Date排序。
### 執行結果:
(6.1 ETF 0050在區間內價格變動)<br>
<img src="image/DB5.png" width="900px"><br><br>
(6.2 特定日期所有ETF的價格變動)<br>
<img src="image/DB5.2.png" width="900px"><br><br>

## 管理員View
```sql
-- 7.建立用戶投資組合持股明細 View
CREATE OR REPLACE VIEW vw_portfolio_detail AS
SELECT 
    p.Portfolio_Id,
    p.User_Id,
    u.Full_Name,
    p.ETF_Id,
    e.ETF_Name,
    p.Shares_Held,
    p.Average_Cost,
    (p.Shares_Held * p.Average_Cost) AS Cost_Basis,
    p.Last_Updated
FROM Portfolio p
JOIN Users u ON p.User_Id = u.User_Id
JOIN ETF e ON p.ETF_Id = e.ETF_Id
WHERE p.Shares_Held > 0
ORDER BY p.User_Id, e.ETF_Id;
```
### 使用方式
```sql
-- 7.1查看所有用戶的投資組合詳細
SELECT * FROM vw_portfolio_detail;
```
```sql
-- 7.2查看特定用戶的投資組合詳細
SELECT * FROM vw_portfolio_detail 
WHERE User_Id = 'user001';
```
```sql
-- 7.3統計用戶投資分佈
SELECT
    ETF_Id,
    ETF_Name,
    COUNT(*) AS Holders,
    SUM(Shares_Held) AS Total_Shares,
    SUM(Cost_Basis) AS Total_Cost
FROM vw_portfolio_detail
GROUP BY ETF_Id, ETF_Name
ORDER BY Holders DESC;

```
### 說明
(7.1)<br>
  - 功能：此視圖vw_portfolio_detail提供用戶投資組合持股的詳細摘要。
  - 目的：展示每個用戶的 ETF 持股詳情，包括用戶資訊和成本基礎。
  - 詳情：<br>
    - 關聯Portfolio、Users和ETF表，檢索Portfolio_Id、User_Id、Full_Name、ETF_Id、ETF_Name、Shares_Held、Average_Cost、計算的Cost_Basis（股數 * 平均成本）和Last_Updated。
    - 篩選持有股數大於零的投資組合。
    - 按User_Id和ETF_Id排序。
(7.2)<br>
  - 功能：此查詢使用 vw_portfolio_detail視圖檢索特定用戶（ex:user001）的投資組合詳情。
  - 目的：提供特定用戶的投資組合持股快照。
  - 詳情：
    - 從 vw_portfolio_detail 選擇所有欄位，篩選 User_Id = 'user001'。
### 執行結果:
( 8.1 查看所有用戶投資組合)<br>
<img src="image/DB6.png" width="800px"><br><br>
( 8.2 查看特定用戶投資組合)<br>
<img src="image/DB6.2.png" width="800px"><br><br>
( 8.3 查看ETF持有狀況)<br>
<img src="image/DB6.3.png" width="800px"><br><br>
---

```sql
-- 8.建立近期交易記錄 View
CREATE OR REPLACE VIEW vw_recent_transactions AS
SELECT 
    t.Transaction_Id,
    t.User_Id,
    u.Full_Name,
    t.ETF_Id,
    e.ETF_Name,
    t.Transaction_Type,
    t.Shares,
    t.Price,
    (t.Shares * t.Price) AS Total_Amount,
    t.Transaction_Date
FROM `Transaction` t
JOIN Users u ON t.User_Id = u.User_Id
JOIN ETF e ON t.ETF_Id = e.ETF_Id
ORDER BY t.Transaction_Date DESC;
```
### 使用方式
```sql
-- 8.1查看最新 10 筆交易記錄
SELECT * FROM vw_recent_transactions LIMIT 10;
```
```sql
-- 8.2查看今日所有交易
SELECT * FROM vw_recent_transactions 
WHERE DATE(Transaction_Date) = CURDATE();
```
```sql
-- 8.3統計交易量分析
SELECT
    ETF_Id,
    ETF_Name,
    Transaction_Type,
    COUNT(*) AS Transactions_Time,
    SUM(Shares) AS Total_Shares,
    SUM(Total_Amount) AS Total_Amount
FROM vw_recent_transactions
WHERE Transaction_Date >= DATE_SUB(NOW(), INTERVAL 30 DAY)
GROUP BY ETF_Id, ETF_Name, Transaction_Type
ORDER BY Total_Amount DESC;
```
```sql
-- 8.4查看用戶交易活躍度
SELECT
    User_Id,
    Full_Name,
    COUNT(*) AS Transaction_Count,
    SUM(Total_Amount) AS Transaction_Amount
FROM vw_recent_transactions
WHERE Transaction_Date >= DATE_SUB(NOW(), INTERVAL 30 DAY)
GROUP BY User_Id, Full_Name
ORDER BY Transaction_Count DESC;
```
### 說明
- 功能：此視圖（ vw_recent_transactions ）提供所有用戶的近期 ETF 交易摘要。
- 目的：展示交易詳情，包括用戶和 ETF 資訊，供監控或報表使用。
- 詳情：
    - 關聯Transaction、Users 和ETF表，檢索Transaction_Id、Full_Name、ETF_Name、Transaction_Type、Shares、Price、計算的Total_Amount（股數 * 價格）和Transaction_Date。
    - 按Transaction_Date降序排序。
    - 查詢顯示最新的10筆交易記錄。
### 執行結果:

(8.1 查看最新十筆交易)<br>
<img src="image/DB8.png" width="800px"><br><br>
(8.2 統計今日所有交易)<br>
<img src="image/DB8.2.png" width="900px"><br><br>
(8.3 統計ETF近30天買賣次數與金額)<br>
<img src="image/DB8.3.png" width="800px"><br><br>
(8.4 統計用戶近30天總交易次數與金額)<br>
<img src="image/DB8.4.png" width="900px"><br><br>

---

## 資料筆數
<img src="image/total_data_count.png" width="600px">

## DEMO
[![IMAGE ALT TEXT](http://img.youtube.com/vi/Hx2qvtQ5Txk/0.jpg)](https://www.youtube.com/watch?v=Hx2qvtQ5Txk "YouTube Video")

## 資料來源 & 處理方式
**ETF 基本資料表 (ETF):**
- 證交所api: https://www.twse.com.tw/zh/ETFortune/ajaxProductsResult
- 櫃買中心api: https://info.tpex.org.tw/api/etfFilter 

**ETF 歷史價格表 (ETF_HistoryPrice):**
- 2008年以前資料：finmind https://finmindtrade.com/analysis/#/data/document
- 2008年以後資料：Yahoo finance套件: yfinance (官網頁面顯示，以ETF:0050舉例 https://finance.yahoo.com/quote/0050.TW/history/)

**紀錄分類表 (ETF_Category)、第一分類表 (Category_Level1)、第二分類表 (Category_Level2):**
- 利用證交所、櫃買中心篩選器的篩選結果: https://www.twse.com.tw/zh/ETFortune/products <br>
比如總共有A~E這些ETF，選擇"股票型"標籤後，剩下A、C、D這些ETF，就可以將"股票型"這個標籤分配給A、C、D這三檔ETF，其餘標籤同理
- 配息月份標籤 : https://www.twse.com.tw/zh/ETFortune/dividendCalendar

**網頁端即時股價**
- 證交所api(以ETF:0050舉例) : https://mis.twse.com.tw/stock/api/getStockInfo.jsp?json=1&delay=0&ex_ch=tse_0050.tw

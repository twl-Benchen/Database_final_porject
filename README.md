# Database_final_porject (資料庫系統_第八組)
[查看投影片](https://github.com/twl-Benchen/Database_final_porject/blob/main/%E7%AC%AC%E5%85%AB%E7%B5%84_ETF%20%E6%8A%95%E8%B3%87%E7%B5%84%E5%90%88%E7%AE%A1%E7%90%86%E7%B3%BB%E7%B5%B1.pdf)

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

## 完整性限制(Database Schema)

### ETF 基本資料表 (ETF)

| 欄位名稱            | 資料型態       | 是否可為空 | 欄位說明   | 值域                             |
| ------------------- | -------------- | ---------- | ---------- | --------------------------------|
| ETF_Id (PK)         | VARCHAR(10)    | N          | ETF 代號   | 數字 + 英文字串                  |
| ETF_Name            | VARCHAR(100)   | N          | ETF 名稱   | 長度 1~100 的文字                |
| Devidend_Yield      | DECIMAL(5,2)   | N          | 殖利率     | ≥ 0，最多小數第 2 位             |
| Holders             | INT            | N          | 持有人數   | ≥ 0 的整數                       |
| IndexName           | VARCHAR(50)    | N          | 追蹤指數   | 長度 1~50 的文字                 |
| Scale               | INT            | N          | 規模 (億)  | ≥ 0 的整數                       |
| ETF_Created_At      | TIMESTAMP      | N          | 創立時間   | 時間格式：YYYY-MM-DD             |

```sql
-- 建立 ETF 資料表
CREATE TABLE ETF (
  ETF_Id VARCHAR(10) PRIMARY KEY,
  ETF_Name VARCHAR(100) NOT NULL,
  Devidend_Yield DECIMAL(5,2) NOT NULL,
  Holders INT NOT NULL,
  IndexName VARCHAR(50) NOT NULL,
  Scale INT NOT NULL,
  ETF_Created_At DATE NOT NULL
);

-- 範例：插入0050 (台灣50) 之ETF資料
INSERT INTO ETF (ETF_Id, ETF_Name, Devidend_Yield, Holders, IndexName, Scale, ETF_Created_At)
VALUES ('0050', '元大台灣50', 4.20, 500000, '臺灣50指數', 250, '2003-06-25');
``` 
---
### 交易紀錄表 (Transaction)

| 欄位名稱               | 資料型態                 | 是否可為空 | 欄位說明     | 值域                                  |
| ---------------------- | ------------------------ | ---------- | ------------ | ------------------------------------- |
| Transaction_Id (PK)    | INT                      | N          | 交易代號     | 從 1 開始遞增的整數                   |
| User_Id (FK)           | VARCHAR(50)              | N          | 使用者代號   | 參考 Users.User_Id                    |
| ETF_Id (FK)            | VARCHAR(10)              | N          | ETF 代號     | 參考 ETF.ETF_Id                       |
| Transaction_Type       | ENUM('Buy','Sell')       | N          | 交易類型     | 僅可為 'Buy' 或 'Sell'                |
| Shares                 | INT                      | N          | 買賣股數     | > 0 的整數                           |
| Price                  | DECIMAL(10,2)            | N          | 交易價格     | ≥ 0，最多小數第 2 位                  |
| Transaction_Date       | TIMESTAMP                | N          | 交易時間     | 時間格式：YYYY-MM-DD                  |

```sql
-- 建立交易紀錄表
CREATE TABLE `Transaction` (
  Transaction_Id INT PRIMARY KEY AUTO_INCREMENT,
  User_Id VARCHAR(50) NOT NULL,
  ETF_Id VARCHAR(10) NOT NULL,
  Transaction_Type ENUM('Buy','Sell') NOT NULL,
  Shares INT NOT NULL,
  Price DECIMAL(10,2) NOT NULL,
  Transaction_Date DATE NOT NULL,
  FOREIGN KEY (User_Id) REFERENCES Users(User_Id),
  FOREIGN KEY (ETF_Id) REFERENCES ETF(ETF_Id)
);

-- 範例：記錄001使用者於2025-04-29買進0050 100股，單價167.80
INSERT INTO `Transaction` (User_Id, ETF_Id, Transaction_Type, Shares, Price, Transaction_Date)
VALUES (1, '0050', 'Buy', 100, 168.80, '2025-04-29');
```

---
### 持倉資料表 (Portfolio)

| 欄位名稱               | 資料型態       | 是否可為空 | 欄位說明     | 值域                                  |
| ---------------------- | -------------- | ---------- | ------------ | ------------------------------------- |
| Portfolio_Id (PK)      | INT            | N          | 持倉代號     | 從 1 開始遞增的整數                   |
| User_Id (FK)           | VARCHAR(50)    | N          | 使用者代號   | 參考 Users.User_Id                    |
| ETF_Id (FK)            | VARCHAR(10)    | N          | ETF 代號     | 參考 ETF.ETF_Id                       |
| Shares_Held            | INT            | N          | 持有股數     | > 0 的整數                           |
| Average_Cost           | DECIMAL(10,2)  | N          | 平均成本     | ≥ 0，最多小數第 2 位                  |
| Last_Updated           | TIMESTAMP      | N          | 最後更新日期 | 時間格式：YYYY-MM-DD                  |

```sql
-- 建立持倉資料表
CREATE TABLE Portfolio (
  Portfolio_Id INT PRIMARY KEY AUTO_INCREMENT,
  User_Id VARCHAR(50) NOT NULL,
  ETF_Id VARCHAR(10) NOT NULL,
  Shares_Held INT NOT NULL,
  Average_Cost DECIMAL(10,2) NOT NULL,
  Last_Updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (User_Id) REFERENCES Users(User_Id),
  FOREIGN KEY (ETF_Id) REFERENCES ETF(ETF_Id)
);

-- 範例：使用者代號1持有0050 100股，平均成本167.80
INSERT INTO Portfolio (User_Id, ETF_Id, Shares_Held, Average_Cost)
VALUES (1, '0050', 100, 167.80);
```

---
### ETF 歷史價格表 (ETF_HistoryPrice)

| 欄位名稱               | 資料型態       | 是否可為空 | 欄位說明     | 值域                                  |
| ---------------------- | -------------- | ---------- | ------------ | ------------------------------------- |
| PriceRecord_Id (PK)    | INT            | N          | 價格紀錄代號 | 從 1 開始遞增的整數                   |
| ETF_Id (FK)            | VARCHAR(10)    | N          | ETF 代號     | 參考 ETF.ETF_Id                       |
| Open_Price             | DECIMAL(10,2)  | N          | 開盤價       | ≥ 0，最多小數第 2 位                  |
| Close_Price            | DECIMAL(10,2)  | N          | 收盤價       | ≥ 0，最多小數第 2 位                  |
| High_Price             | DECIMAL(10,2)  | N          | 最高價       | ≥ 0，最多小數第 2 位                  |
| Low_Price              | DECIMAL(10,2)  | N          | 最低價       | ≥ 0，最多小數第 2 位                  |
| Volume                 | BIGINT         | N          | 交易量       | ≥ 0 的整數                           |
| History_Date           | DATE           | N          | 日期         | 時間格式：YYYY-MM-DD                  |

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
  FOREIGN KEY (ETF_Id) REFERENCES ETF(ETF_Id)
);

-- 範例：紀錄2025-04-29 之0050開盤167.15、收盤167.80、最高168.00、最低166.50、成交量10830
INSERT INTO ETF_HistoryPrice (ETF_Id, Open_Price, Close_Price, High_Price, Low_Price, Volume, History_Date)
VALUES ('0050', 167.15, 167.80, 168.00, 166.50, 10830, '2025-04-28');
```

---
### 第一分類表 (Category_Level1)

| 欄位名稱           | 資料型態    | 是否可為空 | 欄位說明     | 值域                            |
| ------------------ | ----------- | ---------- | ------------ | ------------------------------- |
| Category1_Id (PK)  | INT         | N          | 第一分類代號 | 從 1 開始遞增的整數              |
| Category1_Name     | VARCHAR(20) | N          | 第一分類名稱 | 長度 1~20 的文字                 |

```sql
-- 建立第一分類表
CREATE TABLE Category_Level1 (
  Category1_Id INT PRIMARY KEY AUTO_INCREMENT,
  Category1_Name VARCHAR(20) NOT NULL
);

-- 範例：新增第一分類「股票型」
INSERT INTO Category_Level1 (Category1_Name) VALUES ('股票型');
```

---
### 第二分類表 (Category_Level2)

| 欄位名稱              | 資料型態    | 是否可為空 | 欄位說明       | 值域                                   |
| --------------------- | ----------- | ---------- | -------------- | -------------------------------------- |
| Category2_Id (PK)     | INT         | N          | 第二分類代號   | 從 1 開始遞增的整數                  |
| Category1_Id (FK)     | INT         | N          | 第一分類代號   | 參考 Category_Level1.Category1_Id      |
| Category2_Name        | VARCHAR(20) | N          | 第二分類名稱   | 長度 1~20 的文字                     |

```sql
-- 建立第二分類表
CREATE TABLE Category_Level2 (
  Category2_Id INT PRIMARY KEY AUTO_INCREMENT,
  Category1_Id INT NOT NULL,
  Category2_Name VARCHAR(20) NOT NULL,
  FOREIGN KEY (Category1_Id) REFERENCES Category_Level1(Category1_Id)
);

-- 範例：新增第二分類「大型權值」屬於第一分類1
INSERT INTO Category_Level2 (Category1_Id, Category2_Name) VALUES (1, '大型權值');
```

---
### 紀錄分類表 (ETF_Category)

| 欄位名稱            | 資料型態    | 是否可為空 | 欄位說明       | 值域                                   |
| ------------------- | ----------- | ---------- | -------------- | -------------------------------------- |
| Category_Id (PK)    | INT         | N          | 紀錄分類代號   | 從 1 開始遞增的整數                  |
| ETF_Id (FK)         | VARCHAR(10) | N          | ETF 代號       | 參考 ETF.ETF_Id                      |
| Category2_Id (FK)   | INT         | N          | 第二分類代號   | 參考 Category_Level2.Category2_Id     |

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

| 欄位名稱              | 資料型態             | 是否可為空 | 欄位說明       | 值域                            |
| --------------------- | -------------------- | ---------- | -------------- | ------------------------------- |
| User_Id (PK)          | INT                  | N          | 使用者代號     | 從 1 開始遞增的整數              |
| User_Name             | VARCHAR(50)          | N          | 使用者名稱     | 長度 1~50 的文字                 |
| Full_Name             | VARCHAR(100)         | N          | 全名           | 長度 1~100 的文字                |
| Email                 | VARCHAR(100)         | N          | 電子郵件       | Email 格式                     |
| Phone_Number          | VARCHAR(10)          | N          | 電話號碼       | 長度固定為 10 碼               |
| Role                  | ENUM('user','admin') | N          | 權限           | 僅限 'user' 或 'admin'          |
| Max_Amount            | INT                  | N          | 當日最大交易量 | ≥ 0 的整數                    |
| Users_Created_At      | TIMESTAMP            | N          | 帳號創建日期   | 時間格式：YYYY-MM-DD           |

```sql
-- 建立使用者資料表
CREATE TABLE Users (
  User_Id INT PRIMARY KEY AUTO_INCREMENT,
  User_Name VARCHAR(50) NOT NULL,
  Full_Name VARCHAR(100) NOT NULL,
  Email VARCHAR(100) NOT NULL UNIQUE,
  Phone_Number VARCHAR(10) NOT NULL,
  Role ENUM('user','admin') NOT NULL,
  Max_Amount INT NOT NULL DEFAULT 0,
  Users_Created_At TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 範例：新增使用者 Bob (User_Id 自動產生為1)
INSERT INTO Users (User_Name, Full_Name, Email, Phone_Number, Role, Max_Amount)
VALUES ('bob', 'Bob Lee', 'bob@example.com', '0987654321', 'user', 500000);
```


## ER Diagram及詳細說明
![image](https://github.com/twl-Benchen/Database_final_porject/blob/main/ER%20Diagram.png)


import pandas as pd
import mysql.connector
from mysql.connector import Error
import os

def connect_to_database():
    """連接到MariaDB資料庫"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='benchen',
            password='000',
            database='etf_db',
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci'
        )
        
        if connection.is_connected():
            print("成功連接到MariaDB資料庫")
            return connection
            
    except Error as e:
        print(f"連接資料庫時發生錯誤: {e}")
        return None

def clear_old_data(connection):
    """清理舊的ETF資料"""
    try:
        cursor = connection.cursor()
        
        # 先查看現有資料
        cursor.execute("SELECT COUNT(*) FROM ETF_Holdings")
        old_count = cursor.fetchone()[0]
        
        if old_count > 0:
            print(f"發現 {old_count} 筆舊的ETF持股資料")
            
            # 詢問是否要清理
            choice = input("是否要清除所有舊的ETF持股資料？(y/n): ").strip().lower()
            
            if choice == 'y':
                cursor.execute("DELETE FROM ETF_Holdings")
                connection.commit()
                print(f"已清除 {old_count} 筆舊的ETF持股資料")
            else:
                print("保留舊資料，使用ON DUPLICATE KEY UPDATE更新")
        else:
            print("沒有發現舊的ETF持股資料")
        
        cursor.close()
        
    except Error as e:
        print(f"清理舊資料時發生錯誤: {e}")
        connection.rollback()

def import_stock_list(connection, csv_file_path):
    """匯入股票清單資料"""
    try:
        # 讀取CSV檔案，指定dtype為str以保留前導零
        df = pd.read_csv(csv_file_path, encoding='utf-8', dtype=str)
        print(f"讀取到 {len(df)} 筆股票資料")
        
        cursor = connection.cursor()
        
        # 準備INSERT語句
        insert_query = """
        INSERT INTO Stock_list (Ticker_Symbol, Stock_Name, Sector) 
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE 
        Stock_Name = VALUES(Stock_Name), 
        Sector = VALUES(Sector)
        """
        
        # 轉換資料為元組列表，確保保留字串格式
        data_tuples = []
        for _, row in df.iterrows():
            ticker_symbol = str(row['Ticker_Symbol']).strip()
            stock_name = str(row['Stock_Name']).strip()
            sector = str(row['Sector']).strip() if pd.notna(row['Sector']) and str(row['Sector']).strip() != 'nan' else None
            data_tuples.append((ticker_symbol, stock_name, sector))
        
        # 批量插入資料
        cursor.executemany(insert_query, data_tuples)
        connection.commit()
        
        print(f"成功匯入 {cursor.rowcount} 筆股票資料到 Stock_list 資料表")
        cursor.close()
        
    except Error as e:
        print(f"匯入股票清單時發生錯誤: {e}")
        connection.rollback()
    except Exception as e:
        print(f"處理股票清單檔案時發生錯誤: {e}")

def import_etf_holdings(connection, csv_file_path):
    """匯入ETF持股資料"""
    try:
        # 讀取CSV檔案，指定dtype為str以保留前導零，但Weight保持為數字
        dtype_dict = {
            'ETF_Id': str,
            'Ticker_Symbol': str,
            'Weight': float
        }
        df = pd.read_csv(csv_file_path, encoding='utf-8', dtype=dtype_dict)
        print(f"讀取到 {len(df)} 筆ETF持股資料")
        
        # 確保ETF_Id和Ticker_Symbol保持字串格式並去除空白
        df['ETF_Id'] = df['ETF_Id'].astype(str).str.strip()
        df['Ticker_Symbol'] = df['Ticker_Symbol'].astype(str).str.strip()
        
        # 顯示讀取的資料範例
        print("\n=== 讀取的資料範例 ===")
        print(df.head())
        print(f"\nETF_Id 範例: {df['ETF_Id'].unique()[:5].tolist()}")
        print(f"Ticker_Symbol 範例: {df['Ticker_Symbol'].unique()[:5].tolist()}")
        
        cursor = connection.cursor()
        
        # 先取得現有的股票代號清單
        cursor.execute("SELECT Ticker_Symbol FROM Stock_list")
        existing_stocks = set(str(row[0]).strip() for row in cursor.fetchall())
        print(f"資料庫中現有 {len(existing_stocks)} 個股票代號")
        
        # 清理ETF資料中的股票代號
        df_stocks = set(df['Ticker_Symbol'])
        
        print(f"ETF資料中有 {len(df_stocks)} 個不同的股票代號")
        
        # 顯示一些範例來檢查格式
        print("\n資料庫中的股票代號範例:", sorted(list(existing_stocks))[:10])
        print("ETF資料中的股票代號範例:", sorted(list(df_stocks))[:10])
        
        # 檢查哪些股票代號不存在
        missing_stocks = df_stocks - existing_stocks
        
        if missing_stocks:
            print(f"\n發現 {len(missing_stocks)} 個不存在的股票代號:")
            missing_list = sorted(missing_stocks)
            for i, stock in enumerate(missing_list[:20]):  # 只顯示前20個
                print(f"  - {repr(stock)}")  # 使用repr來顯示特殊字符
            if len(missing_list) > 20:
                print(f"  ... 和其他 {len(missing_list) - 20} 個")
            
            # 詢問是否要自動加入缺少的股票
            print(f"\n選項:")
            print("1. 自動將缺少的股票加入Stock_list表")
            print("2. 過濾掉不存在的股票代號")
            print("3. 取消匯入")
            
            choice = input("請選擇 (1/2/3): ").strip()
            
            if choice == '1':
                # 自動加入缺少的股票（名稱和產業設為預設值）
                insert_missing_query = """
                INSERT INTO Stock_list (Ticker_Symbol, Stock_Name, Sector) 
                VALUES (%s, %s, %s)
                """
                missing_data = [(stock, f"股票_{stock}", "未分類") for stock in missing_stocks]
                cursor.executemany(insert_missing_query, missing_data)
                connection.commit()
                print(f"已自動加入 {len(missing_stocks)} 個缺少的股票")
            elif choice == '2':
                # 過濾掉不存在的股票代號
                print("將過濾掉不存在的股票代號...")
                original_len = len(df)
                df = df[df['Ticker_Symbol'].isin(existing_stocks)]
                filtered_len = len(df)
                print(f"過濾掉 {original_len - filtered_len} 筆資料，剩餘 {filtered_len} 筆資料")
            else:
                print("取消匯入")
                return
        
        if len(df) == 0:
            print("沒有有效的資料可以匯入")
            return
        
        # 顯示準備匯入的資料統計
        print(f"\n準備匯入 {len(df)} 筆資料:")
        etf_stats = df.groupby('ETF_Id').agg({
            'Ticker_Symbol': 'count',
            'Weight': 'sum'
        }).round(2)
        for etf_id, stats in etf_stats.iterrows():
            print(f"  ETF {etf_id}: {stats['Ticker_Symbol']} 檔股票, 總權重: {stats['Weight']}%")
        
        # 準備INSERT語句
        insert_query = """
        INSERT INTO ETF_Holdings (ETF_Id, Ticker_Symbol, Weight) 
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE 
        Weight = VALUES(Weight)
        """
        
        # 轉換資料為元組列表，確保保持正確的資料格式
        data_tuples = []
        for _, row in df.iterrows():
            etf_id = str(row['ETF_Id']).strip()  # 確保為字串格式
            ticker = str(row['Ticker_Symbol']).strip()  # 確保為字串格式
            weight = float(row['Weight'])  # 確保為數字格式
            data_tuples.append((etf_id, ticker, weight))
        
        # 顯示即將插入的資料範例
        print(f"\n=== 即將插入的資料範例 ===")
        for i, (etf_id, ticker, weight) in enumerate(data_tuples[:5]):
            print(f"ETF_Id: '{etf_id}' (type: {type(etf_id)}), Ticker: '{ticker}', Weight: {weight}")
        
        print(f"\n開始批量插入 {len(data_tuples)} 筆資料...")
        
        # 批量插入資料
        cursor.executemany(insert_query, data_tuples)
        connection.commit()
        
        print(f"成功匯入 {len(data_tuples)} 筆ETF持股資料到 ETF_Holdings 資料表")
        cursor.close()
        
    except Error as e:
        print(f"匯入ETF持股時發生錯誤: {e}")
        print("正在回滾事務...")
        connection.rollback()
    except Exception as e:
        print(f"處理ETF持股檔案時發生錯誤: {e}")
        import traceback
        traceback.print_exc()

def verify_import(connection):
    """驗證匯入結果"""
    try:
        cursor = connection.cursor()
        
        # 檢查Stock_list資料表
        cursor.execute("SELECT COUNT(*) FROM Stock_list")
        stock_count = cursor.fetchone()[0]
        print(f"Stock_list 資料表共有 {stock_count} 筆資料")
        
        # 檢查ETF_Holdings資料表
        cursor.execute("SELECT COUNT(*) FROM ETF_Holdings")
        holdings_count = cursor.fetchone()[0]
        print(f"ETF_Holdings 資料表共有 {holdings_count} 筆資料")
        
        # 檢查有多少個不同的ETF
        cursor.execute("SELECT COUNT(DISTINCT ETF_Id) FROM ETF_Holdings")
        etf_count = cursor.fetchone()[0]
        print(f"共有 {etf_count} 個不同的ETF")
        
        # 顯示各ETF的持股數量
        cursor.execute("""
            SELECT ETF_Id, COUNT(*) as holdings_count, SUM(Weight) as total_weight
            FROM ETF_Holdings 
            GROUP BY ETF_Id 
            ORDER BY ETF_Id
        """)
        print(f"\n=== 各ETF持股統計 ===")
        for row in cursor.fetchall():
            print(f"ETF {row[0]}: {row[1]} 檔股票, 總權重: {row[2]:.2f}%")
        
        # 顯示範例資料
        print("\n=== Stock_list 範例資料 ===")
        cursor.execute("SELECT * FROM Stock_list LIMIT 5")
        for row in cursor.fetchall():
            print(f"代號: {row[0]}, 名稱: {row[1]}, 產業: {row[2]}")
        
        print("\n=== ETF_Holdings 範例資料 ===")
        cursor.execute("SELECT * FROM ETF_Holdings ORDER BY Weight DESC LIMIT 10")
        for row in cursor.fetchall():
            print(f"ETF: '{row[0]}', 股票: '{row[1]}', 權重: {row[2]}%")
        
        # 特別檢查ETF_Id格式
        print("\n=== ETF_Id 格式檢查 ===")
        cursor.execute("SELECT DISTINCT ETF_Id FROM ETF_Holdings ORDER BY ETF_Id")
        etf_ids = [row[0] for row in cursor.fetchall()]
        print(f"所有ETF_Id: {etf_ids}")
        
        cursor.close()
        
    except Error as e:
        print(f"驗證資料時發生錯誤: {e}")

def main():
    """主函數"""
    # CSV檔案路徑
    stock_csv_path = "stock/stocks_format.csv"
    etf_csv_path = "stock/etf_holdings_format.csv"
    
    # 檢查檔案是否存在
    if not os.path.exists(stock_csv_path):
        print(f"找不到檔案: {stock_csv_path}")
        return
    
    if not os.path.exists(etf_csv_path):
        print(f"找不到檔案: {etf_csv_path}")
        return
    
    # 連接資料庫
    connection = connect_to_database()
    if not connection:
        return
    
    try:
        print("開始匯入資料...")
        
        # 清理舊資料
        print("\n0. 清理舊資料...")
        clear_old_data(connection)
        
        # 先匯入股票清單（因為有外鍵約束）
        print("\n1. 匯入股票清單...")
        import_stock_list(connection, stock_csv_path)
        
        # 再匯入ETF持股資料
        print("\n2. 匯入ETF持股資料...")
        import_etf_holdings(connection, etf_csv_path)
        
        # 驗證匯入結果
        print("\n3. 驗證匯入結果...")
        verify_import(connection)
        
        print("\n資料匯入完成！")
        
    except Exception as e:
        print(f"匯入過程中發生錯誤: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if connection and connection.is_connected():
            connection.close()
            print("資料庫連接已關閉")

if __name__ == "__main__":
    main()
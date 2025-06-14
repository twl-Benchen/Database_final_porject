import pandas as pd
import mysql.connector
from datetime import datetime
import os

# 資料庫連接配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'database': 'etf_db',
    'user': 'benchen',  # 改使用者名稱
    'password': '000',  # 改密碼
    'charset': 'utf8mb4'
}

def connect_to_db():
    """建立資料庫連接"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print("✅ 資料庫連接成功")
            return connection
        else:
            print("❌ 資料庫連接失敗")
            return None
    except mysql.connector.Error as err:
        print(f"❌ 資料庫連接錯誤: {err}")
        return None

def parse_date(date_str):
    """解析日期字符串，支援多種格式"""
    date_formats = ['%Y/%m/%d', '%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y']
    
    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    
    # 如果都無法解析，返回None
    print(f"⚠️  無法解析日期: {date_str}")
    return None

def check_and_create_etf(connection, etf_id, etf_name=None):
    """檢查ETF是否存在，如果不存在則創建"""
    cursor = connection.cursor()
    
    # 檢查ETF是否已存在
    check_query = "SELECT COUNT(*) FROM ETF WHERE ETF_Id = %s"
    cursor.execute(check_query, (etf_id,))
    result = cursor.fetchone()
    
    if result[0] == 0:
        print(f"⚠️  ETF {etf_id} 不存在於資料庫中")
        
        # 如果沒有提供ETF名稱，使用預設值
        if not etf_name:
            etf_name = f"ETF {etf_id}"
        
        print(f"🆕 正在創建 ETF 記錄: {etf_id}")
        
        # 創建ETF記錄（使用預設值）
        insert_etf_query = """
        INSERT INTO ETF (ETF_Id, ETF_Name, Holders, IndexName, Scale, ETF_Created_At)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        # 使用預設值
        default_data = (
            etf_id,
            etf_name,
            0,  # Holders
            f"{etf_id} Index",  # IndexName
            0,  # Scale
            datetime.now().date()  # ETF_Created_At
        )
        
        try:
            cursor.execute(insert_etf_query, default_data)
            connection.commit()
            print(f"✅ 成功創建 ETF {etf_id}")
            return True
        except Exception as e:
            print(f"❌ 創建 ETF {etf_id} 失敗: {e}")
            return False
    else:
        print(f"✅ ETF {etf_id} 已存在於資料庫中")
        return True
    
    cursor.close()

def import_csv_to_db(csv_file_path, etf_id, etf_name=None):
    """將CSV檔案匯入到資料庫"""
    
    # 檢查檔案是否存在
    if not os.path.exists(csv_file_path):
        print(f"❌ 檔案不存在: {csv_file_path}")
        return False
    
    # 讀取CSV檔案
    try:
        # 嘗試不同的編碼格式
        encodings = ['utf-8', 'big5', 'gbk', 'cp950']
        df = None
        
        for encoding in encodings:
            try:
                df = pd.read_csv(csv_file_path, encoding=encoding)
                print(f"✅ 成功以 {encoding} 編碼讀取檔案")
                break
            except UnicodeDecodeError:
                continue
        
        if df is None:
            print("❌ 無法讀取CSV檔案，請檢查檔案編碼")
            return False
            
    except Exception as e:
        print(f"❌ 讀取CSV檔案失敗: {e}")
        return False
    
    print(f"📊 讀取到 {len(df)} 筆資料")
    print(f"📋 欄位名稱: {list(df.columns)}")
    
    # 顯示前幾筆資料供確認
    print("\n前5筆資料預覽:")
    print(df.head())
    
    # 建立資料庫連接
    connection = connect_to_db()
    if not connection:
        return False
    
    # 檢查並創建ETF記錄
    if not check_and_create_etf(connection, etf_id, etf_name):
        connection.close()
        return False
    
    cursor = connection.cursor()
    
    # 準備SQL語句
    insert_query = """
    INSERT INTO ETF_HistoryPrice 
    (ETF_Id, Open_Price, Close_Price, High_Price, Low_Price, Volume, History_Date)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    # 開始匯入資料
    success_count = 0
    error_count = 0
    
    print(f"\n🚀 開始匯入資料到資料庫...")
    
    for index, row in df.iterrows():
        try:
            # 解析日期
            date_obj = parse_date(str(row['date']))
            if date_obj is None:
                print(f"⚠️  第 {index+1} 筆資料日期格式錯誤，跳過")
                error_count += 1
                continue
            
            # 準備資料
            data = (
                etf_id,
                float(row['Open']),
                float(row['Close']),
                float(row['High']),
                float(row['Low']),
                int(row['Volume']),
                date_obj
            )
            
            # 執行插入
            cursor.execute(insert_query, data)
            success_count += 1
            
            # 每100筆提交一次
            if success_count % 100 == 0:
                connection.commit()
                print(f"✅ 已成功匯入 {success_count} 筆資料")
                
        except Exception as e:
            print(f"❌ 第 {index+1} 筆資料匯入失敗: {e}")
            error_count += 1
            continue
    
    # 最終提交
    connection.commit()
    
    # 關閉連接
    cursor.close()
    connection.close()
    
    print(f"\n📈 匯入完成!")
    print(f"✅ 成功匯入: {success_count} 筆")
    print(f"❌ 失敗: {error_count} 筆")
    
    return success_count > 0

def check_etf_history_exists(connection, etf_id):
    """檢查ETF是否已有歷史資料"""
    cursor = connection.cursor()
    
    check_query = "SELECT COUNT(*) FROM ETF_HistoryPrice WHERE ETF_Id = %s"
    cursor.execute(check_query, (etf_id,))
    result = cursor.fetchone()
    cursor.close()
    
    return result[0] > 0

def batch_import_etf_files(directory_path):
    """批量匯入ETF檔案 - 自動處理所有檔案"""
    
    if not os.path.exists(directory_path):
        print(f"❌ 目錄不存在: {directory_path}")
        return
    
    # 掃描目錄中的CSV檔案
    csv_files = [f for f in os.listdir(directory_path) if f.endswith('.csv')]
    
    if not csv_files:
        print("❌ 目錄中沒有找到CSV檔案")
        return
    
    print(f"📁 在目錄 {directory_path} 中找到 {len(csv_files)} 個CSV檔案")
    
    # 建立資料庫連接用於檢查
    connection = connect_to_db()
    if not connection:
        print("❌ 無法連接資料庫")
        return
    
    processed_count = 0
    skipped_count = 0
    error_count = 0
    
    for csv_file in csv_files:
        print(f"\n{'='*50}")
        print(f"處理檔案: {csv_file}")
        
        # 從檔案名稱提取ETF代碼 (假設格式為 XXXX_history.csv 或 XXXX.csv)
        etf_id = csv_file.replace('_history.csv', '').replace('.csv', '')
        print(f"ETF代碼: {etf_id}")
        
        try:
            # 檢查該ETF是否已有歷史資料
            if check_etf_history_exists(connection, etf_id):
                print(f"⏭️  ETF {etf_id} 已有歷史資料，跳過匯入")
                skipped_count += 1
                continue
            
            # 匯入檔案
            file_path = os.path.join(directory_path, csv_file)
            print(f"🚀 開始匯入 {etf_id} 的資料...")
            
            if import_csv_to_db(file_path, etf_id, None):
                print(f"✅ {etf_id} 匯入成功")
                processed_count += 1
            else:
                print(f"❌ {etf_id} 匯入失敗")
                error_count += 1
                
        except Exception as e:
            print(f"❌ 處理 {csv_file} 時發生錯誤: {e}")
            error_count += 1
    
    # 關閉資料庫連接
    connection.close()
    
    print(f"\n{'='*50}")
    print(f"📊 批量匯入完成統計:")
    print(f"✅ 成功處理: {processed_count} 個檔案")
    print(f"⏭️  跳過 (已存在): {skipped_count} 個檔案") 
    print(f"❌ 處理失敗: {error_count} 個檔案")
    print(f"📁 總檔案數: {len(csv_files)} 個")

def main():
    """主程式"""
    print("🎯 ETF歷史價格CSV匯入工具")
    print("="*50)
    
    while True:
        print("\n選擇操作:")
        print("1. 匯入單一CSV檔案")
        print("2. 批量匯入目錄中的CSV檔案 (自動處理)")
        print("3. 測試資料庫連接")
        print("4. 退出")
        
        choice = input("\n請選擇 (1-4): ")
        
        if choice == '1':
            csv_path = input("請輸入CSV檔案路徑: ").strip()
            etf_id = input("請輸入ETF代碼 (例如: 0050): ").strip()
            etf_name = input("請輸入ETF名稱 (按Enter使用預設值): ").strip()
            
            if csv_path and etf_id:
                # 檢查是否已有歷史資料
                connection = connect_to_db()
                if connection:
                    if check_etf_history_exists(connection, etf_id):
                        overwrite = input(f"⚠️  ETF {etf_id} 已有歷史資料，是否要覆蓋? (y/n): ").lower()
                        if overwrite != 'y':
                            print("取消匯入")
                            connection.close()
                            continue
                    connection.close()
                
                if not etf_name:
                    etf_name = None
                import_csv_to_db(csv_path, etf_id, etf_name)
            else:
                print("❌ 請提供有效的檔案路徑和ETF代碼")
        
        elif choice == '2':
            directory = input("請輸入CSV檔案目錄路徑: ").strip()
            if directory:
                print("🚀 開始自動批量匯入...")
                batch_import_etf_files(directory)
            else:
                print("❌ 請提供有效的目錄路徑")
        
        elif choice == '3':
            connection = connect_to_db()
            if connection:
                connection.close()
        
        elif choice == '4':
            print("👋 再見!")
            break
        
        else:
            print("❌ 無效的選擇，請重新輸入")

if __name__ == "__main__":
    main()
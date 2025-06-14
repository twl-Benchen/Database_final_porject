import mysql.connector
import json
from datetime import datetime
import os

# 資料庫連接配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'database': 'etf_db',
    'user': 'benchen',
    'password': '000',
    'charset': 'utf8mb4'
}

# 改良版標籤資料 - 更清楚的階層結構
DETAILED_TAGS_MAP = {
    "股票型": {
        "子分類": ["大型權值", "中小型權值", "因子投資", "主動式", "ESG", "等權重"],
    },
    "高股息": {
        "特性": ["高息低波動", "ESG"],
        "配息頻率": ["月配", "季配", "半年配"],
    },
    "債券型": {
        "期限": ["長債", "中長債", "中短債"],
        "類型": ["主權債", "金融債", "公債", "投等債"],
        "地區": ["全球債", "美債", "亞債", "新興市場債", "歐債", "中國債"],
        "特性": ["槓桿型"],
        "配息": ["月配", "季配", "半年配"]
    },
    "主題": ["不動產", "生技", "科技", "綠能", "金融", "電信通訊", "電動車", "半導體", "ESG"],
    "投信": ["元大", "富邦", "永豐", "兆豐", "國泰", "第一金", "復華", "群益", "新光", "台新", 
            "中國信託", "統一", "街口", "富蘭克林", "凱基", "大華銀", "野村", "保德信", "聯邦"],
    "其他": ["槓桿型", "反向型", "貨幣型", "加權指數", "期貨型(原物料)"],
    "配息月份": ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]
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

def flatten_tags_map(tags_map):
    """將巢狀的標籤結構展開為平面結構"""
    flattened = {}
    
    for parent_tag, children in tags_map.items():
        if isinstance(children, dict):
            # 如果子項目是字典，將所有子分類合併
            all_children = []
            for sub_category, sub_items in children.items():
                all_children.extend(sub_items)
            flattened[parent_tag] = all_children
        else:
            # 如果子項目是列表，直接使用
            flattened[parent_tag] = children
    
    return flattened

def check_existing_data(connection, table_name):
    """檢查資料表中是否已有資料"""
    cursor = connection.cursor()
    try:
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        return count
    except Exception as e:
        print(f"❌ 檢查 {table_name} 資料失敗: {e}")
        return 0
    finally:
        cursor.close()

def clear_existing_data(connection, clear_type="all"):
    """清除現有資料 - 改良版，處理外鍵約束"""
    cursor = connection.cursor()
    
    try:
        print(f"🗑️  開始清除 {clear_type} 資料...")
        
        # 暫時停用外鍵檢查
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        if clear_type in ["all", "tags"]:
            # 按照依賴順序清除標籤相關資料
            tables_to_clear = ["ETF_Category", "Category_Level2", "Category_Level1"]
            for table in tables_to_clear:
                cursor.execute(f"DELETE FROM {table}")
                print(f"  ✅ 已清除 {table}")
        
        if clear_type in ["all", "etf"]:
            # 清除ETF相關資料
            cursor.execute("DELETE FROM ETF_Category")
            cursor.execute("DELETE FROM Portfolio") 
            cursor.execute("DELETE FROM Transaction")
            cursor.execute("DELETE FROM ETF_HistoryPrice")
            cursor.execute("DELETE FROM ETF")
            print("  ✅ 已清除ETF相關資料")
        
        # 重新啟用外鍵檢查
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        
        connection.commit()
        print("🗑️  資料清除完成")
        return True
        
    except Exception as e:
        print(f"❌ 清除資料失敗: {e}")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")  # 確保重新啟用外鍵檢查
        connection.rollback()
        return False
    finally:
        cursor.close()

def clean_duplicate_etf_data(connection):
    """清理重複的ETF資料"""
    cursor = connection.cursor()
    
    try:
        print("🧹 正在清理重複的ETF資料...")
        
        # 找出重複的ETF記錄（保留最新的一筆）
        cleanup_query = """
        DELETE e1 FROM ETF e1
        INNER JOIN ETF e2 
        WHERE e1.ETF_Id = e2.ETF_Id AND e1.ETF_Created_At < e2.ETF_Created_At
        """
        
        cursor.execute(cleanup_query)
        deleted_count = cursor.rowcount
        
        connection.commit()
        print(f"✅ 已清理 {deleted_count} 筆重複的ETF資料")
        return True
        
    except Exception as e:
        print(f"❌ 清理重複資料失敗: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()

def insert_tags_improved(connection):
    """改良版標籤插入函數"""
    cursor = connection.cursor()
    
    try:
        # 展開巢狀標籤結構
        flat_tags = flatten_tags_map(DETAILED_TAGS_MAP)
        
        print("📝 開始插入標籤資料...")
        print(f"共有 {len(flat_tags)} 個父分類")
        
        # 插入第一層分類（父標籤）
        insert_level1_query = "INSERT INTO Category_Level1 (Category1_Name) VALUES (%s)"
        level1_ids = {}
        
        for parent_tag in flat_tags.keys():
            try:
                cursor.execute(insert_level1_query, (parent_tag,))
                level1_id = cursor.lastrowid
                level1_ids[parent_tag] = level1_id
                print(f"  ✅ 插入父分類: {parent_tag} (ID: {level1_id})")
            except mysql.connector.IntegrityError as e:
                print(f"  ⚠️  父分類 {parent_tag} 可能已存在: {e}")
                continue
        
        connection.commit()
        print("📋 第一層分類插入完成")
        
        # 插入第二層分類（子標籤）
        print("\n📝 開始插入第二層分類...")
        insert_level2_query = "INSERT INTO Category_Level2 (Category1_Id, Category2_Name) VALUES (%s, %s)"
        
        total_level2_count = 0
        level2_ids = {}  # 儲存子分類ID，方便後續使用
        
        for parent_tag, child_tags in flat_tags.items():
            if parent_tag not in level1_ids:
                print(f"  ⚠️  找不到父分類 {parent_tag} 的ID，跳過其子分類")
                continue
                
            parent_id = level1_ids[parent_tag]
            print(f"\n  處理 '{parent_tag}' 的子分類 ({len(child_tags)} 個):")
            
            for child_tag in child_tags:
                try:
                    cursor.execute(insert_level2_query, (parent_id, child_tag))
                    level2_id = cursor.lastrowid
                    level2_ids[child_tag] = level2_id
                    print(f"    ✅ {child_tag} (ID: {level2_id})")
                    total_level2_count += 1
                except mysql.connector.IntegrityError as e:
                    print(f"    ⚠️  子分類 {child_tag} 可能已存在: {e}")
                    continue
        
        connection.commit()
        print(f"\n📋 第二層分類插入完成，共 {total_level2_count} 個子分類")
        
        return True, level1_ids, level2_ids
        
    except Exception as e:
        print(f"❌ 插入標籤資料失敗: {e}")
        connection.rollback()
        return False, {}, {}
    finally:
        cursor.close()

def get_category_mapping(connection):
    """取得分類名稱與ID的對應關係"""
    cursor = connection.cursor()
    
    try:
        query = """
        SELECT c2.Category2_Name, c2.Category2_Id, c1.Category1_Name
        FROM Category_Level2 c2
        JOIN Category_Level1 c1 ON c2.Category1_Id = c1.Category1_Id
        """
        cursor.execute(query)
        results = cursor.fetchall()
        
        # 建立名稱到ID的對應字典
        category_map = {}
        parent_map = {}
        
        for child_name, child_id, parent_name in results:
            category_map[child_name] = child_id
            parent_map[child_name] = parent_name
            
        print(f"✅ 取得 {len(category_map)} 個分類對應關係")
        return category_map, parent_map
        
    except Exception as e:
        print(f"❌ 取得分類對應關係失敗: {e}")
        return {}, {}
    finally:
        cursor.close()

def parse_scale(scale_str):
    """解析規模字串，將其轉換為整數（以億為單位）"""
    if not scale_str or scale_str == 'N/A':
        return 0
    
    # 移除逗號
    scale_str = scale_str.replace(',', '')
    
    try:
        return int(float(scale_str))
    except ValueError:
        return 0

def parse_holders(holders_str):
    """解析持有人數字串"""
    if not holders_str or holders_str == 'N/A':
        return 0
    
    # 移除逗號
    holders_str = holders_str.replace(',', '')
    
    try:
        return int(float(holders_str))
    except ValueError:
        return 0

def parse_date(date_str):
    """解析日期字串，轉換為 MySQL 日期格式"""
    try:
        # 假設輸入格式為 "2003/06/30"
        return datetime.strptime(date_str, "%Y/%m/%d").date()
    except ValueError:
        try:
            # 嘗試其他可能的格式
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            # 如果解析失敗，返回預設日期
            return datetime(2000, 1, 1).date()

def insert_etf_data_improved(connection, json_file_path):
    """改良版ETF資料插入函數"""
    
    # 檢查檔案是否存在
    if not os.path.exists(json_file_path):
        print(f"❌ 找不到檔案: {json_file_path}")
        current_dir = os.getcwd()
        print(f"目前工作目錄: {current_dir}")
        print("請確認檔案路徑是否正確")
        return False
    
    # 讀取JSON檔案
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            etf_data = json.load(file)
        print(f"📂 成功讀取 {len(etf_data)} 筆ETF資料")
    except Exception as e:
        print(f"❌ 讀取JSON檔案失敗: {e}")
        return False
    
    # 取得分類對應關係
    category_map, parent_map = get_category_mapping(connection)
    if not category_map:
        print("❌ 無法取得分類對應關係，請先插入標籤資料")
        return False
    
    cursor = connection.cursor()
    
    try:
        # 準備插入ETF的SQL語句
        insert_etf_query = """
        INSERT INTO ETF (ETF_Id, ETF_Name, Holders, IndexName, Scale, ETF_Created_At) 
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        ETF_Name = VALUES(ETF_Name),
        Holders = VALUES(Holders),
        IndexName = VALUES(IndexName),
        Scale = VALUES(Scale),
        ETF_Created_At = VALUES(ETF_Created_At)
        """
        
        # 準備插入ETF分類關聯的SQL語句
        insert_category_query = """
        INSERT IGNORE INTO ETF_Category (ETF_Id, Category2_Id) VALUES (%s, %s)
        """
        
        success_count = 0
        error_count = 0
        total_categories = 0
        skipped_tags = set()
        
        print("\n📊 開始插入ETF資料...")
        
        for i, etf in enumerate(etf_data, 1):
            try:
                # 解析ETF基本資料
                etf_id = etf.get('stockNo', '')
                etf_name = etf.get('stockName', '')
                holders = parse_holders(etf.get('holders', '0'))
                index_name = etf.get('indexName', 'N/A')
                scale = parse_scale(etf.get('totalAv_100million', '0'))
                created_date = parse_date(etf.get('listingDate', '2000/01/01'))
                
                if not etf_id or not etf_name:
                    print(f"  ⚠️  ETF ID 或名稱為空，跳過第 {i} 筆資料")
                    error_count += 1
                    continue
                
                # 插入ETF基本資料
                cursor.execute(insert_etf_query, (
                    etf_id, etf_name, holders, index_name, scale, created_date
                ))
                
                # 插入所有相關的分類關聯
                tags = etf.get('tags', [])
                category_inserted = 0
                
                for tag in tags:
                    if tag in category_map:
                        category_id = category_map[tag]
                        cursor.execute(insert_category_query, (etf_id, category_id))
                        category_inserted += 1
                        total_categories += 1
                    else:
                        skipped_tags.add(tag)
                
                print(f"  ✅ [{i:3d}/{len(etf_data)}] {etf_id} - {etf_name} (標籤: {category_inserted}個)")
                success_count += 1
                
                # 每100筆提交一次，避免記憶體問題
                if i % 100 == 0:
                    connection.commit()
                    print(f"    💾 已提交前 {i} 筆資料")
                
            except mysql.connector.IntegrityError as e:
                if "Duplicate entry" in str(e):
                    print(f"  ⚠️  ETF {etf.get('stockNo', 'Unknown')} 已存在，更新資料")
                else:
                    print(f"  ❌ ETF {etf.get('stockNo', 'Unknown')} 資料完整性錯誤: {e}")
                    error_count += 1
            except Exception as e:
                print(f"  ❌ 插入ETF {etf.get('stockNo', 'Unknown')} 失敗: {e}")
                error_count += 1
                continue
        
        # 最終提交
        connection.commit()
        
        print(f"\n📊 ETF資料插入完成:")
        print(f"  成功: {success_count} 筆ETF")
        print(f"  失敗: {error_count} 筆ETF")
        print(f"  標籤關聯: {total_categories} 筆")
        
        if skipped_tags:
            print(f"\n⚠️  未找到對應的標籤 ({len(skipped_tags)} 個):")
            for tag in sorted(skipped_tags):
                print(f"    - {tag}")
            print("  建議檢查標籤資料或更新 DETAILED_TAGS_MAP")
        
        return success_count > 0
        
    except Exception as e:
        print(f"❌ 插入ETF資料過程發生錯誤: {e}")
        connection.rollback()
        return False
        
    finally:
        cursor.close()

def verify_tag_insertion(connection):
    """驗證標籤插入結果"""
    cursor = connection.cursor()
    
    try:
        print("\n🔍 驗證標籤插入結果...")
        
        # 檢查第一層分類
        cursor.execute("SELECT Category1_Id, Category1_Name FROM Category_Level1 ORDER BY Category1_Id")
        level1_results = cursor.fetchall()
        
        print(f"\n第一層分類 ({len(level1_results)} 個):")
        for id, name in level1_results:
            print(f"  ID: {id}, 名稱: {name}")
        
        # 檢查第二層分類統計
        query = """
        SELECT c1.Category1_Name, COUNT(c2.Category2_Id) as count
        FROM Category_Level1 c1
        LEFT JOIN Category_Level2 c2 ON c1.Category1_Id = c2.Category1_Id
        GROUP BY c1.Category1_Id, c1.Category1_Name
        ORDER BY c1.Category1_Id
        """
        cursor.execute(query)
        level2_stats = cursor.fetchall()
        
        print(f"\n第二層分類統計:")
        total_level2 = 0
        for parent, count in level2_stats:
            print(f"  {parent}: {count} 個子分類")
            total_level2 += count
        
        print(f"總計第二層分類: {total_level2} 個")
        
        return True
        
    except Exception as e:
        print(f"❌ 驗證標籤插入失敗: {e}")
        return False
    finally:
        cursor.close()

def show_detailed_summary(connection):
    """顯示詳細的資料庫摘要"""
    cursor = connection.cursor()
    
    try:
        print("\n📊 詳細資料庫摘要:")
        print("=" * 60)
        
        # 標籤統計
        cursor.execute("SELECT COUNT(*) FROM Category_Level1")
        level1_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM Category_Level2") 
        level2_count = cursor.fetchone()[0]
        
        print(f"標籤系統:")
        print(f"  第一層分類: {level1_count} 個")
        print(f"  第二層分類: {level2_count} 個")
        
        # ETF統計
        cursor.execute("SELECT COUNT(*) FROM ETF")
        etf_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM ETF_Category")
        category_relation_count = cursor.fetchone()[0]
        
        print(f"\nETF資料:")
        print(f"  ETF總數: {etf_count} 支")
        print(f"  標籤關聯: {category_relation_count} 筆")
        
        if etf_count > 0:
            avg_tags = category_relation_count / etf_count
            print(f"  平均每支ETF標籤數: {avg_tags:.1f} 個")
        
        # 各分類的ETF數量統計
        if etf_count > 0:
            query = """
            SELECT c1.Category1_Name, COUNT(DISTINCT ec.ETF_Id) as etf_count
            FROM Category_Level1 c1
            LEFT JOIN Category_Level2 c2 ON c1.Category1_Id = c2.Category1_Id
            LEFT JOIN ETF_Category ec ON c2.Category2_Id = ec.Category2_Id
            GROUP BY c1.Category1_Id, c1.Category1_Name
            ORDER BY etf_count DESC
            """
            cursor.execute(query)
            category_stats = cursor.fetchall()
            
            print(f"\n各分類ETF數量:")
            for category, count in category_stats:
                print(f"  {category}: {count} 支ETF")
        
    except Exception as e:
        print(f"❌ 查詢摘要資料失敗: {e}")
    finally:
        cursor.close()

def main():
    """主程式 - 完整版"""
    print("🏷️  ETF標籤與資料插入工具 (完整版)")
    print("=" * 60)
    
    # 建立資料庫連接
    connection = connect_to_db()
    if not connection:
        print("❌ 無法連接資料庫，程式結束")
        return
    
    try:
        # 檢查現有資料
        existing_level1 = check_existing_data(connection, "Category_Level1")
        existing_level2 = check_existing_data(connection, "Category_Level2")
        existing_etf = check_existing_data(connection, "ETF")
        existing_relations = check_existing_data(connection, "ETF_Category")
        
        print(f"\n📋 現有資料狀況:")
        print(f"  第一層分類: {existing_level1} 個")
        print(f"  第二層分類: {existing_level2} 個") 
        print(f"  ETF資料: {existing_etf} 支")
        print(f"  標籤關聯: {existing_relations} 筆")
        
        # 第一步：處理標籤資料
        print(f"\n🏷️  第一步：標籤資料處理")
        print("-" * 30)
        
        tags_ready = False
        
        if existing_level1 > 0 or existing_level2 > 0:
            print("⚠️  發現現有標籤資料")
            choice = input("選擇操作 (1:清除重建 2:跳過標籤插入 3:查看現有標籤): ").strip()
            
            if choice == "1":
                if clear_existing_data(connection, "tags"):
                    success, level1_ids, level2_ids = insert_tags_improved(connection)
                    if success:
                        verify_tag_insertion(connection)
                        tags_ready = True
                else:
                    print("❌ 清除資料失敗")
                    return
            elif choice == "3":
                verify_tag_insertion(connection)
                tags_ready = True
            else:
                print("⏭️  跳過標籤插入")
                tags_ready = True
        else:
            print("🆕 開始插入標籤資料...")
            success, level1_ids, level2_ids = insert_tags_improved(connection)
            if success:
                verify_tag_insertion(connection)
                tags_ready = True
            else:
                print("❌ 標籤插入失敗")
                return
        
        # 第二步：處理ETF資料
        if tags_ready:
            print(f"\n📊 第二步：ETF資料處理")
            print("-" * 30)
            
            # 檢查是否需要清理重複資料
            cursor = connection.cursor()
            cursor.execute("SELECT ETF_Id, COUNT(*) FROM ETF GROUP BY ETF_Id HAVING COUNT(*) > 1")
            duplicates = cursor.fetchall()
            cursor.close()
            
            if duplicates:
                print(f"⚠️  發現 {len(duplicates)} 個ETF有重複資料")
                clean_duplicates = input("是否要清理重複的ETF資料? (y/n): ").lower().strip()
                if clean_duplicates == 'y':
                    clean_duplicate_etf_data(connection)
            
            # 詢問JSON檔案路徑
            json_file_path = input("請輸入 combined_etf_data.json 的完整路徑 (直接按Enter使用預設路徑): ").strip()
            if not json_file_path:
                json_file_path = "combined_etf_data.json"  # 預設檔名
            
            # 確認是否要處理ETF資料
            if existing_etf > 0:
                print(f"⚠️  發現現有 {existing_etf} 支ETF資料")
                etf_choice = input("選擇操作 (1:清除並重新插入 2:更新現有資料 3:跳過ETF插入): ").strip()
                
                if etf_choice == "1":
                    if clear_existing_data(connection, "etf"):
                        if insert_etf_data_improved(connection, json_file_path):
                            print("\n🎉 ETF資料插入成功!")
                        else:
                            print("\n❌ ETF資料插入失敗")
                elif etf_choice == "2":
                    if insert_etf_data_improved(connection, json_file_path):
                        print("\n🎉 ETF資料更新成功!")
                    else:
                        print("\n❌ ETF資料更新失敗")
                else:
                    print("⏭️  跳過ETF資料插入")
            else:
                # 沒有現有ETF資料，直接插入
                if insert_etf_data_improved(connection, json_file_path):
                    print("\n🎉 ETF資料插入成功!")
                else:
                    print("\n❌ ETF資料插入失敗")
        
        # 第三步：顯示最終摘要
        print(f"\n📊 第三步：最終摘要")
        print("-" * 30)
        show_detailed_summary(connection)
        
        print("\n✅ 程式執行完成！")
        
        # 提供後續操作建議
        print("\n💡 後續可以執行的操作:")
        print("  1. 查詢特定分類的ETF: SELECT * FROM ETF WHERE ETF_Id IN (...)")
        print("  2. 統計各標籤的使用情況")
        print("  3. 分析ETF的標籤分布")
        print("  4. 建立ETF推薦系統")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  程式被使用者中斷")
    except Exception as e:
        print(f"\n❌ 程式執行錯誤: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if connection and connection.is_connected():
            connection.close()
            print("\n👋 資料庫連接已關閉，程式結束")

if __name__ == "__main__":
    main()
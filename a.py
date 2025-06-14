
import streamlit as st
import mysql.connector
import pandas as pd
from datetime import datetime, date
import plotly.express as px
import plotly.graph_objects as go
import time
import hashlib
import price  

# 配置頁面
st.set_page_config(
    page_title="ETF 投資管理系統",
    page_icon="📈",
    layout="wide"
)

# 資料庫連接配置
def get_db_config():
    """獲取資料庫配置"""
    if 'db_config' not in st.session_state:
        st.session_state.db_config = {
            'host': 'localhost',
            'port': 3306,
            'database': 'etf_db',
            'user': 'benchen',  # 改成自己的
            'password': '000',  # 改成自己的
            'charset': 'utf8mb4'
        }
    return st.session_state.db_config

def get_auth_db_config():
    """獲取驗證資料庫配置"""
    if 'auth_db_config' not in st.session_state:
        st.session_state.auth_db_config = {
            'host': 'localhost',
            'port': 3306,
            'database': 'auth_db',
            'user': 'user',  # 改成自己的
            'password': '222',  # 改成自己的
            'charset': 'utf8mb4'
        }
    return st.session_state.auth_db_config

def test_connection():
    """測試資料庫連接"""
    config = get_db_config()
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            connection.close()
            return True, "連接成功"
    except mysql.connector.Error as err:
        return False, str(err)
    return False, "未知錯誤"

def init_connection():
    """初始化資料庫連接"""
    config = get_db_config()
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            return connection
        else:
            return None
    except mysql.connector.Error as err:
        st.error(f"資料庫連接失敗: {err}")
        return None
    except Exception as err:
        st.error(f"連接錯誤: {err}")
        return None

def init_auth_connection():
    """初始化驗證資料庫連接"""
    config = get_auth_db_config()
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            return connection
        else:
            return None
    except mysql.connector.Error as err:
        st.error(f"驗證資料庫連接失敗: {err}")
        return None
    except Exception as err:
        st.error(f"連接錯誤: {err}")
        return None

# 執行查詢
def run_query(query, params=None):
    """執行資料庫查詢"""
    conn = init_connection()
    if conn is None:
        st.error("無法建立資料庫連接")
        return None
    
    try:
        df = pd.read_sql(query, conn, params=params)
        return df
    except Exception as err:
        st.error(f"查詢失敗: {err}")
        return None
    finally:
        if conn and conn.is_connected():
            conn.close()

# 執行更新操作
def execute_query(query, params=None):
    """執行資料庫更新操作"""
    conn = init_connection()
    if conn is None:
        st.error("無法建立資料庫連接")
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        return True
    except Exception as err:
        st.error(f"執行失敗: {err}")
        return False
    finally:
        if conn and conn.is_connected():
            conn.close()

def hash_password(password):
    """密碼雜湊處理"""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def verify_login(user_id, password):
    """驗證登入資訊 - 支援分離的認證和用戶資料庫"""
    # 步驟 1: 從 auth_db 驗證帳號密碼
    auth_conn = init_auth_connection()
    if auth_conn is None:
        return False, "無法連接驗證資料庫", None
    
    try:
        auth_cursor = auth_conn.cursor()
        # 驗證帳號密碼
        auth_query = "SELECT User_Id FROM Auth WHERE User_Id = %s AND Password = %s"
        auth_cursor.execute(auth_query, (user_id, password))
        auth_result = auth_cursor.fetchone()
        
        if not auth_result:
            auth_cursor.close()
            return False, "帳號或密碼錯誤", None
        
        # 更新最後登入時間
        try:
            update_query = "UPDATE Auth SET Last_Login = CURRENT_TIMESTAMP WHERE User_Id = %s"
            auth_cursor.execute(update_query, (user_id,))
            auth_conn.commit()
        except Exception as update_err:
            print(f"更新登入時間失敗: {update_err}")
        
        auth_cursor.close()
        
    except Exception as err:
        return False, f"驗證過程發生錯誤: {err}", None
    finally:
        if auth_conn and auth_conn.is_connected():
            auth_conn.close()
    
    # 步驟 2: 從 etf_db 獲取用戶角色資訊
    etf_conn = init_connection()
    if etf_conn is None:
        # 如果無法連接 etf_db，就給予預設角色
        return True, "登入成功（預設權限）", 'user'
    
    try:
        etf_cursor = etf_conn.cursor()
        # 獲取用戶角色
        role_query = "SELECT Role FROM Users WHERE User_Id = %s"
        etf_cursor.execute(role_query, (user_id,))
        role_result = etf_cursor.fetchone()
        
        if role_result:
            user_role = role_result[0]
        else:
            # 如果在 Users 表中找不到用戶，給予預設角色
            user_role = 'user'
        
        etf_cursor.close()
        return True, "登入成功", user_role
        
    except Exception as err:
        # 如果查詢角色失敗，給予預設角色但仍允許登入
        print(f"獲取用戶角色失敗: {err}")
        return True, "登入成功（預設權限）", 'user'
    finally:
        if etf_conn and etf_conn.is_connected():
            etf_conn.close()

def show_login():
    """顯示登入頁面"""
    st.title("🔐 ETF 投資管理系統")
    st.markdown("### 請登入您的帳戶")
    
    # 建立登入表單
    with st.form("login_form"):
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("---")
            user_id = st.text_input("👤 帳號", placeholder="請輸入您的帳號")
            password = st.text_input("🔒 密碼", type="password", placeholder="請輸入您的密碼")
            st.markdown("---")
            
            login_button = st.form_submit_button("🚀 登入", use_container_width=True)
            
            if login_button:
                if user_id and password:
                    success, message, user_role = verify_login(user_id, password)
                    
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.user_id = user_id
                        st.session_state.user_role = user_role
                        st.session_state.login_time = datetime.now()
                        st.success(message)
                        time.sleep(1)  # 短暫延遲讓用戶看到成功訊息
                        st.rerun()  # 重新載入頁面
                    else:
                        st.error(message)
                else:
                    st.warning("請輸入帳號和密碼")
    
    # 測試帳號資訊顯示
    with st.expander("📋 測試帳號資訊"):
        st.info("一般用戶 - 帳號: user001, 密碼: 1234")
        st.info("管理員 - 帳號: adminbenchen, 密碼: 000")
        st.warning("注意：管理員帳號需要在兩個資料庫中都有對應記錄")

def check_user_data_consistency():
    """檢查用戶資料一致性"""
    try:
        # 獲取 auth_db 中的用戶
        auth_query = "SELECT User_Id FROM Auth"
        auth_df = run_auth_query(auth_query)
        
        # 獲取 etf_db 中的用戶
        etf_query = "SELECT User_Id, Role FROM Users"
        etf_df = run_query(etf_query)
        
        if auth_df is not None and etf_df is not None:
            auth_users = set(auth_df['User_Id'].tolist())
            etf_users = set(etf_df['User_Id'].tolist())
            
            # 找出不一致的資料
            only_in_auth = auth_users - etf_users
            only_in_etf = etf_users - auth_users
            
            return {
                'auth_users': auth_users,
                'etf_users': etf_users,
                'only_in_auth': only_in_auth,
                'only_in_etf': only_in_etf,
                'consistent': len(only_in_auth) == 0 and len(only_in_etf) == 0
            }
    except Exception as err:
        st.error(f"檢查資料一致性時發生錯誤: {err}")
        return None

def run_auth_query(query, params=None):
    """執行驗證資料庫查詢"""
    conn = init_auth_connection()
    if conn is None:
        st.error("無法建立驗證資料庫連接")
        return None
    
    try:
        df = pd.read_sql(query, conn, params=params)
        return df
    except Exception as err:
        st.error(f"驗證資料庫查詢失敗: {err}")
        return None
    finally:
        if conn and conn.is_connected():
            conn.close()

def logout():
    """登出功能"""
    if st.sidebar.button("🚪 登出"):
        # 清除 session state
        for key in ['logged_in', 'user_id', 'user_role', 'login_time']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

def show_user_info():
    """顯示使用者資訊"""
    if 'user_id' in st.session_state:
        st.sidebar.info(f"**帳號:** {st.session_state.user_id}")
        role_display = "管理員" if st.session_state.get('user_role') == 'admin' else "一般用戶"
        st.sidebar.info(f"**身份:** {role_display}")
        if 'login_time' in st.session_state:
            st.sidebar.info(f"**登入時間:** {st.session_state.login_time.strftime('%Y-%m-%d %H:%M:%S')}")

# 主頁面
def main():
    # 檢查登入狀態
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        show_login()
        return
    
    st.title("📈 ETF 投資管理系統")
    st.markdown("---")
    
    # 側邊欄選單
    st.sidebar.title("功能選單")
    
    # 顯示使用者資訊
    show_user_info()
    
    # 登出按鈕
    logout()
    
    # 資料庫連接測試
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔌 資料庫連接")

    # 只有管理員才能看到連接設定
    if st.session_state.get('user_role') == 'admin':
        # 連接設定
        with st.sidebar.expander("連接設定"):
            config = get_db_config()
            config['host'] = st.text_input("主機", value=config['host'])
            config['port'] = st.number_input("埠號", value=config['port'], min_value=1, max_value=65535)
            config['database'] = st.text_input("資料庫名稱", value=config['database'])
            config['user'] = st.text_input("使用者名稱", value=config['user'])
            config['password'] = st.text_input("密碼", value=config['password'], type="password")
            
            if st.button("測試連接"):
                success, message = test_connection()
                if success:
                    st.sidebar.success(message)
                else:
                    st.sidebar.error(f"連接失敗: {message}")

    # 檢查連接狀態
    success, status = test_connection()
    if success:
        st.sidebar.success("✅ 資料庫已連接")
    else:
        st.sidebar.error("❌ 資料庫未連接")
        if st.session_state.get('user_role') == 'admin':
            st.sidebar.error(f"錯誤: {status}")
    
    st.sidebar.markdown("---")
    
    # 根據用戶角色顯示不同選單
    if st.session_state.get('user_role') == 'admin':
        menu_options = ["系統概覽", "ETF 資訊", "用戶管理", "交易記錄", "價格圖表"]
    else:
        menu_options = ["ETF 資訊", "交易記錄", "價格圖表"]

    page = st.sidebar.selectbox("選擇功能", menu_options)
    
    if page == "系統概覽":
        show_dashboard()
    elif page == "ETF 資訊":
        show_etf_info()
    elif page == "用戶管理":
        show_user_management()
    elif page == "交易記錄":
        show_transactions()
    elif page == "價格圖表":
        show_price_charts()

def show_dashboard():
    """系統概覽頁面"""
    st.header("🎯 系統概覽")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # 獲取統計數據
    etf_count = run_query("SELECT COUNT(*) as count FROM ETF")
    user_count = run_query("SELECT COUNT(*) as count FROM Users")
    transaction_count = run_query("SELECT COUNT(*) as count FROM `Transaction`")
    total_volume = run_query("SELECT SUM(Shares * Price) as total FROM `Transaction`")
    
    with col1:
        st.metric("ETF 總數", etf_count['count'].iloc[0] if etf_count is not None else 0)
    
    with col2:
        st.metric("用戶數量", user_count['count'].iloc[0] if user_count is not None else 0)
    
    with col3:
        st.metric("交易筆數", transaction_count['count'].iloc[0] if transaction_count is not None else 0)
    
    with col4:
        total_val = total_volume['total'].iloc[0] if total_volume is not None and total_volume['total'].iloc[0] else 0
        st.metric("總交易金額", f"${total_val:,.2f}")
    
    st.markdown("---")
    
    # 最近交易
    st.subheader("📊 最近交易記錄")
    recent_transactions = run_query("""
        SELECT t.Transaction_Id, u.Full_Name, e.ETF_Name, t.Transaction_Type, 
               t.Shares, t.Price, t.Transaction_Date
        FROM `Transaction` t
        JOIN Users u ON t.User_Id = u.User_Id
        JOIN ETF e ON t.ETF_Id = e.ETF_Id
        ORDER BY t.Transaction_Date DESC
        LIMIT 10
    """)
    
    if recent_transactions is not None:
        st.dataframe(recent_transactions, use_container_width=True)

    # 各表格記錄數量
    tables = [ '`Transaction`', 'Portfolio', 'ETF_HistoryPrice', 
              'Category_Level1', 'Category_Level2', 'ETF_Category']
    
    col1, col2 = st.columns(2)
    
    for i, table in enumerate(tables):
        count_data = run_query(f"SELECT COUNT(*) as count FROM {table}")
        count = count_data['count'].iloc[0] if count_data is not None else 0
        
        if i % 2 == 0:
            col1.metric(f"{table.replace('`', '')} 記錄數", count)
        else:
            col2.metric(f"{table.replace('`', '')} 記錄數", count)

def show_etf_info():
    """ETF 資訊頁面"""
    st.header("💼 ETF 資訊管理")
    
    # 篩選區域
    st.subheader("🔍 篩選條件")
    col1, col2, col3 = st.columns(3)
    
    # 獲取所有父類別
    category1_data = run_query("SELECT Category1_Id, Category1_Name FROM Category_Level1 ORDER BY Category1_Name")
    
    with col1:
        if category1_data is not None:
            category1_options = ["全部"] + category1_data['Category1_Name'].tolist()
            selected_category1 = st.selectbox("選擇父類別", category1_options)
        else:
            selected_category1 = "全部"
    
    with col2:
        category2_options = ["全部"]
        selected_category2 = "全部"
        
        if selected_category1 != "全部" and category1_data is not None:
            # 根據選擇的父類別獲取子類別
            category1_id = int(category1_data[category1_data['Category1_Name'] == selected_category1]['Category1_Id'].iloc[0])
            category2_data = run_query("""
                SELECT Category2_Id, Category2_Name 
                FROM Category_Level2 
                WHERE Category1_Id = %s 
                ORDER BY Category2_Name
            """, (category1_id,))
            
            if category2_data is not None:
                category2_options = ["全部"] + category2_data['Category2_Name'].tolist()
        
        selected_category2 = st.selectbox("選擇子類別", category2_options)
    
    st.markdown("---")
    
    # 根據篩選條件構建查詢
    base_query = """
        SELECT DISTINCT e.ETF_Id, e.ETF_Name, e.Holders, e.IndexName, e.Scale, 
               e.ETF_Created_At, c1.Category1_Name, c2.Category2_Name
        FROM ETF e
        LEFT JOIN ETF_Category ec ON e.ETF_Id = ec.ETF_Id
        LEFT JOIN Category_Level2 c2 ON ec.Category2_Id = c2.Category2_Id
        LEFT JOIN Category_Level1 c1 ON c2.Category1_Id = c1.Category1_Id
    """
    
    params = []
    where_conditions = []
    
    # 根據篩選條件添加WHERE子句
    if selected_category1 != "全部":
        where_conditions.append("c1.Category1_Name = %s")
        params.append(selected_category1)
    
    if selected_category2 != "全部":
        where_conditions.append("c2.Category2_Name = %s")
        params.append(selected_category2)
    
    if where_conditions:
        base_query += " WHERE " + " AND ".join(where_conditions)
    
    base_query += " ORDER BY e.ETF_Id"
    
    # 執行查詢
    etf_data = run_query(base_query, tuple(params) if params else None)
    
    # 顯示篩選結果統計
    if etf_data is not None:
        total_count = len(etf_data)
        st.info(f"📊 共找到 {total_count} 個符合條件的 ETF")
        
        # 顯示ETF列表
        if total_count > 0:
            # 添加搜尋框
            search_term = st.text_input("🔍 搜尋 ETF 名稱或代碼", placeholder="輸入關鍵字進行搜尋...")
            
            # 根據搜尋條件過濾資料
            if search_term:
                filtered_data = etf_data[
                    etf_data['ETF_Id'].str.contains(search_term, case=False, na=False) |
                    etf_data['ETF_Name'].str.contains(search_term, case=False, na=False)
                ]
                st.info(f"🔍 搜尋結果: {len(filtered_data)} 個 ETF")
            else:
                filtered_data = etf_data
            
            # 顯示資料表
            if len(filtered_data) > 0:
                # 格式化顯示
                display_data = filtered_data.copy()
                if 'ETF_Created_At' in display_data.columns:
                    display_data['ETF_Created_At'] = pd.to_datetime(display_data['ETF_Created_At']).dt.strftime('%Y-%m-%d')
                
                st.dataframe(
                    display_data,
                    use_container_width=True,
                    column_config={
                        "ETF_Id": st.column_config.TextColumn("ETF 代碼", width="small"),
                        "ETF_Name": st.column_config.TextColumn("ETF 名稱", width="medium"),
                        "Holders": st.column_config.NumberColumn("持有人數", width="small"),
                        "IndexName": st.column_config.TextColumn("指數名稱", width="medium"),
                        "Scale": st.column_config.NumberColumn("規模 (億)", width="small"),
                        "ETF_Created_At": st.column_config.TextColumn("成立日期", width="small"),
                        "Category1_Name": st.column_config.TextColumn("父類別", width="small"),
                        "Category2_Name": st.column_config.TextColumn("子類別", width="small")
                    }
                )
                
            
            else:
                st.warning("沒有找到符合搜尋條件的 ETF")
        else:
            st.warning("沒有找到符合篩選條件的 ETF")
    else:
        st.error("無法獲取 ETF 資料")
    
    st.markdown("---")

def show_user_management():
    """用戶管理頁面"""
    st.header("👥 用戶管理")
    
    # 顯示所有用戶
    users_data = run_query("""
        SELECT User_Id, User_Name, Full_Name, Email, Phone_Number, Role, Max_Amount, Users_Created_At
        FROM Users
    """)
    
    if users_data is not None:
        st.dataframe(users_data, use_container_width=True)

def show_transactions():
    """交易記錄頁面（包含投資組合）"""
    st.header("💰 交易記錄與投資組合")
    
    # 建立頁籤
    tab1, tab2 = st.tabs(["📝 新增交易", "📊 投資組合"])
    
    with tab1:
        # 新增交易區域
        st.subheader("➕ 新增交易")
        
        # 獲取用戶列表和ETF列表
        users_data = run_query("SELECT User_Id, Full_Name FROM Users ORDER BY Full_Name")
        etf_data = run_query("SELECT ETF_Id, ETF_Name FROM ETF ORDER BY ETF_Id")
        
        if users_data is not None and etf_data is not None:
            # 準備ETF選項
            etf_options = [(row['ETF_Id'], row['ETF_Name']) for _, row in etf_data.iterrows()]
            
            # **關鍵修正：將ETF選擇移到表單外部**
            st.markdown("##### 📊 選擇ETF")
            selected_etf = st.selectbox(
                "選擇ETF*",
                options=[etf[0] for etf in etf_options],
                format_func=lambda x: f"{x} - {next(etf[1] for etf in etf_options if etf[0] == x)}",
                help="必填欄位",
                key="etf_selector"
            )
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # 交易表單
                with st.form("add_transaction_form"):
                    # 使用當前登入用戶，不允許選擇
                    current_username = st.session_state.user_id
                    selected_user = current_username
                    
                    # 從資料庫獲取顯示名稱
                    user_info = users_data[users_data['User_Id'] == selected_user]
                    if len(user_info) > 0:
                        current_user_name = user_info['Full_Name'].iloc[0]
                    else:
                        current_user_name = selected_user
                        st.error(f"❌ 無法找到用戶資訊: {selected_user}")
                        return
                    
                    # 第一行：交易用戶 | 交易類型*
                    row1_col1, row1_col2 = st.columns(2)
                    with row1_col1:
                        st.text_input("交易用戶", value=current_user_name, disabled=True, help="當前登入用戶")
                    with row1_col2:
                        transaction_type = st.selectbox(
                            "交易類型*",
                            options=["Buy", "Sell"],
                            format_func=lambda x: "買入" if x == "Buy" else "賣出",
                            help="必填欄位"
                        )
                    
                    # 第二行：股數* | 交易價格*
                    row2_col1, row2_col2 = st.columns(2)
                    with row2_col1:
                        shares = st.number_input(
                            "股數*",
                            min_value=1,
                            value=1000,
                            step=1000,
                            help="必填欄位，最小1股"
                        )
                    with row2_col2:
                        default_price = st.session_state.get('suggested_price', 50.0)
                        price = st.number_input(
                            "交易價格*",
                            min_value=0.01,
                            value=default_price,
                            step=0.01,
                            format="%.2f",
                            help="必填欄位，用戶實際交易價格",
                            key="price_input"
                        )
                    
                    # 第三行：交易日期 | 交易時間
                    row3_col1, row3_col2 = st.columns(2)
                    with row3_col1:
                        transaction_date = st.date_input(
                            "交易日期",
                            value=datetime.now().date(),
                            help="選擇交易日期"
                        )
                    with row3_col2:
                        transaction_time = st.time_input(
                            "交易時間",
                            value=datetime.now().time(),
                            help="選擇交易時間"
                        )
                    
                    # 合併日期和時間
                    transaction_datetime = datetime.combine(transaction_date, transaction_time)
                    
                    # 計算總金額
                    total_amount = shares * price
                    st.info(f"💰 交易總金額: ${total_amount:,.2f}")
                    
                    # 提交按鈕
                    submitted = st.form_submit_button("🚀 提交交易", use_container_width=True)
                    
                    if submitted:
                        # 先獲取下一個Transaction_Id
                        max_id_result = run_query("SELECT COALESCE(MAX(Transaction_Id), 0) + 1 as next_id FROM `Transaction`")
                        next_transaction_id = int(max_id_result['next_id'].iloc[0]) if max_id_result is not None else 1
                        
                        # 插入交易記錄
                        insert_query = """
                        INSERT INTO `Transaction` (Transaction_Id, User_Id, ETF_Id, Transaction_Type, Shares, Price, Transaction_Date)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """
                        params = (
                            int(next_transaction_id), 
                            str(selected_user),
                            str(selected_etf), 
                            str(transaction_type), 
                            int(shares), 
                            float(price), 
                            transaction_datetime
                        )
                        if execute_query(insert_query, params):
                            st.success(f"✅ 交易記錄新增成功！")
                            st.success(f"用戶: {current_user_name}")
                            st.success(f"ETF: {selected_etf}")
                            st.success(f"類型: {'買入' if transaction_type == 'Buy' else '賣出'}")
                            st.success(f"股數: {shares:,} 股")
                            st.success(f"價格: ${price:.2f}")
                            st.success(f"總金額: ${total_amount:,.2f}")
                            
                            # 更新投資組合
                            update_portfolio(str(selected_user), str(selected_etf), transaction_type, shares, price)
                            
                            # 重新載入頁面以顯示新的交易記錄
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("❌ 交易記錄新增失敗")
            
            with col2:
                # ETF即時資訊區域 - **修正後的邏輯**
                st.subheader("📊 ETF 即時資訊")
                
                # 直接使用選中的ETF
                if selected_etf:
                    try:
                        from price import ETFPriceCrawler
                        
                        crawler = ETFPriceCrawler()
                        etf_real_time = crawler.get_single_etf_smart(selected_etf)
                        
                        if etf_real_time:
                            st.success(f"🎯 {etf_real_time['ETF_Name']} ({etf_real_time['ETF_Id']})")
                            
                            # 價格資訊
                            price_col1, price_col2 = st.columns(2)
                            
                            with price_col1:
                                current_price = etf_real_time['當前價格']
                                price_status = etf_real_time['價格狀態']
                                status_emoji = "🔴" if price_status == "即時" else "🟡"
                                st.metric("當前價格", f"${current_price:.2f}", help=f"{status_emoji} {price_status}")
                                
                                st.metric("開盤價", f"${etf_real_time['開盤價']:.2f}")
                            
                            with price_col2:
                                st.metric("最高價", f"${etf_real_time['最高價']:.2f}")
                                st.metric("最低價", f"${etf_real_time['最低價']:.2f}")
                            
                            st.metric("昨收價", f"${etf_real_time['昨日收盤價']:.2f}")
                            st.metric("累積成交量", etf_real_time['累積成交量'])
                            
                            # 計算漲跌
                            if etf_real_time['昨日收盤價'] > 0:
                                change = current_price - etf_real_time['昨日收盤價']
                                change_pct = (change / etf_real_time['昨日收盤價']) * 100
                                
                                if change > 0:
                                    st.success(f"📈 漲 ${change:.2f} (+{change_pct:.2f}%)")
                                elif change < 0:
                                    st.error(f"📉 跌 ${abs(change):.2f} ({change_pct:.2f}%)")
                                else:
                                    st.info("➡️ 平盤")
                            
                            # 更新時間
                            st.caption(f"⏰ 更新時間: {etf_real_time['更新時間']}")
                            
                            # 建議價格按鈕
                            if st.button("💡 使用當前價格", help="將當前價格填入交易價格欄位", key="use_current_price"):
                                st.session_state.suggested_price = current_price
                                st.success(f"✅ 已設定建議價格: ${current_price:.2f}")
                                st.rerun()  # 立即重新整理以套用新價格
                        
                        else:
                            st.warning("⚠️ 無法取得即時資料")
                            st.info("可能原因：")
                            st.info("• 非交易時間")
                            st.info("• 網路連線問題")  
                            st.info("• ETF代碼錯誤")
                    
                    except ImportError:
                        st.error("❌ 無法載入價格爬蟲模組")
                        st.info("請確保 price.py 檔案在正確位置")
                    except Exception as e:
                        st.error(f"❌ 取得即時資料時發生錯誤: {str(e)}")
                else:
                    st.info("📊 請先選擇ETF")
        
        else:
            st.error("❌ 無法載入用戶或ETF資料，請檢查資料庫連接")
        
        st.markdown("---")

        # 交易記錄查詢，只顯示當前登入用戶
        st.subheader("📋 交易記錄查詢")

        # 1. 取得當前登入的使用者 ID（確保是字串）
        current_user_id = str(st.session_state.user_id)

        # 2. 修改 SQL，加上 WHERE 條件篩選出「自己」的交易
        transactions = run_query(
            """
            SELECT 
                t.Transaction_Id, 
                u.Full_Name, 
                e.ETF_Name, 
                t.Transaction_Type, 
                t.Shares, 
                t.Price, 
                (t.Shares * t.Price) AS Total_Amount, 
                t.Transaction_Date
            FROM `Transaction` t
            JOIN Users u ON t.User_Id = u.User_Id
            JOIN ETF e ON t.ETF_Id = e.ETF_Id
            WHERE t.User_Id = %s
            ORDER BY t.Transaction_Date DESC
            """,
            (current_user_id,)
        )

        if transactions is not None and len(transactions) > 0:
            # 格式化欄位名稱與資料
            display_transactions = transactions.copy()
            display_transactions['Transaction_Type'] = display_transactions['Transaction_Type'].map({
                'Buy': '買入', 'Sell': '賣出'
            })
            display_transactions['Transaction_Date'] = pd.to_datetime(
                display_transactions['Transaction_Date']
            ).dt.strftime('%Y-%m-%d %H:%M:%S')
            
            st.dataframe(
                display_transactions,
                use_container_width=True,
                column_config={
                    "Transaction_Id": st.column_config.NumberColumn("交易ID", width="small"),
                    "Full_Name": st.column_config.TextColumn("用戶", width="medium"),
                    "ETF_Name": st.column_config.TextColumn("ETF名稱", width="medium"),
                    "Transaction_Type": st.column_config.TextColumn("類型", width="small"),
                    "Shares": st.column_config.NumberColumn("股數", width="small", format="%d"),
                    "Price": st.column_config.NumberColumn("價格", width="small", format="$%.2f"),
                    "Total_Amount": st.column_config.NumberColumn("總金額", width="medium", format="$%.2f"),
                    "Transaction_Date": st.column_config.TextColumn("交易時間", width="medium")
                }
            )
            
            # 交易統計
            st.markdown("---")
            st.subheader("📈 交易統計")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # 買賣分布
                transaction_type_counts = transactions['Transaction_Type'].value_counts()
                fig_pie = px.pie(
                    values=transaction_type_counts.values,
                    names=['買入' if x == 'Buy' else '賣出' for x in transaction_type_counts.index],
                    title="買賣交易分布"
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                # 交易金額統計
                buy_total = transactions[transactions['Transaction_Type'] == 'Buy']['Total_Amount'].sum()
                sell_total = transactions[transactions['Transaction_Type'] == 'Sell']['Total_Amount'].sum()
                
                st.metric("買入總金額", f"${buy_total:,.2f}")
                st.metric("賣出總金額", f"${sell_total:,.2f}")
                st.metric("淨投入", f"${buy_total - sell_total:,.2f}")
        else:
            st.info("📝 尚無交易記錄")
    
    with tab2:
        # 投資組合頁面
        st.subheader("📊 投資組合總覽")
        
        current_user_id = str(st.session_state.user_id)  # 確保是字串
        
        portfolio_data = run_query("""
            SELECT p.Portfolio_Id, u.Full_Name, e.ETF_Id, e.ETF_Name, p.Shares_Held, 
                p.Average_Cost, (p.Shares_Held * p.Average_Cost) as Cost_Basis, p.Last_Updated
            FROM Portfolio p
            JOIN Users u ON p.User_Id = u.User_Id
            JOIN ETF e ON p.ETF_Id = e.ETF_Id
            WHERE p.Shares_Held > 0 AND p.User_Id = %s
            ORDER BY e.ETF_Id
        """, (current_user_id,))
        
        if portfolio_data is not None and len(portfolio_data) > 0:
            # 添加即時價格和損益計算
            portfolio_display = portfolio_data.copy()
            
            # 嘗試獲取即時價格
            try:
                from price import ETFPriceCrawler
                crawler = ETFPriceCrawler()
                
                current_prices = {}
                for etf_id in portfolio_data['ETF_Id'].unique():
                    try:
                        etf_real_time = crawler.get_single_etf_smart(etf_id)
                        if etf_real_time:
                            current_prices[etf_id] = etf_real_time['當前價格']
                        else:
                            current_prices[etf_id] = None
                    except:
                        current_prices[etf_id] = None
                
                # 添加即時價格和損益計算
                portfolio_display['Current_Price'] = portfolio_display['ETF_Id'].map(current_prices)
                portfolio_display['Market_Value'] = portfolio_display.apply(
                    lambda row: row['Shares_Held'] * row['Current_Price'] if row['Current_Price'] is not None else None, 
                    axis=1
                )
                portfolio_display['Unrealized_PL'] = portfolio_display.apply(
                    lambda row: row['Market_Value'] - row['Cost_Basis'] if row['Market_Value'] is not None else None,
                    axis=1
                )
                portfolio_display['Return_Pct'] = portfolio_display.apply(
                    lambda row: (row['Unrealized_PL'] / row['Cost_Basis']) * 100 if row['Unrealized_PL'] is not None and row['Cost_Basis'] > 0 else None,
                    axis=1
                )
                
            except ImportError:
                st.warning("⚠️ 無法載入價格爬蟲模組，將只顯示成本資訊")
                portfolio_display['Current_Price'] = None
                portfolio_display['Market_Value'] = None
                portfolio_display['Unrealized_PL'] = None
                portfolio_display['Return_Pct'] = None
            
            # 格式化顯示時間
            portfolio_display['Last_Updated'] = pd.to_datetime(
                portfolio_display['Last_Updated']
            ).dt.strftime('%Y-%m-%d %H:%M:%S')
            
            # 顯示投資組合
            st.dataframe(
                portfolio_display,
                use_container_width=True,
                column_config={
                    "Portfolio_Id": st.column_config.NumberColumn("組合ID", width="small"),
                    "Full_Name": st.column_config.TextColumn("用戶", width="medium"),
                    "ETF_Id": st.column_config.TextColumn("ETF代碼", width="small"),
                    "ETF_Name": st.column_config.TextColumn("ETF名稱", width="medium"),
                    "Shares_Held": st.column_config.NumberColumn("持有股數", width="small", format="%d"),
                    "Average_Cost": st.column_config.NumberColumn("平均成本", width="small", format="$%.2f"),
                    "Cost_Basis": st.column_config.NumberColumn("成本基礎", width="medium", format="$%.2f"),
                    "Current_Price": st.column_config.NumberColumn("當前價格", width="small", format="$%.2f"),
                    "Market_Value": st.column_config.NumberColumn("市值", width="medium", format="$%.2f"),
                    "Unrealized_PL": st.column_config.NumberColumn("未實現損益", width="medium", format="$%.2f"),
                    "Return_Pct": st.column_config.NumberColumn("報酬率%", width="small", format="%.2f%%"),
                    "Last_Updated": st.column_config.TextColumn("更新時間", width="medium")
                }
            )
            
            # 投資組合統計
            st.markdown("---")
            st.subheader("📈 投資組合統計")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                total_cost = portfolio_display['Cost_Basis'].sum()
                st.metric("總成本基礎", f"${total_cost:,.2f}")
            
            with col2:
                if 'Market_Value' in portfolio_display.columns:
                    valid_market_values = portfolio_display['Market_Value'].dropna()
                    if len(valid_market_values) > 0:
                        total_market_value = valid_market_values.sum()
                        st.metric("總市值", f"${total_market_value:,.2f}")
                    else:
                        st.metric("總市值", "無法取得")
                else:
                    st.metric("總市值", "無法取得")
            
            with col3:
                if 'Unrealized_PL' in portfolio_display.columns:
                    valid_pl = portfolio_display['Unrealized_PL'].dropna()
                    if len(valid_pl) > 0:
                        total_pl = valid_pl.sum()
                        delta_color = "normal" if total_pl >= 0 else "inverse"
                        st.metric("總未實現損益", f"${total_pl:,.2f}", delta=f"{(total_pl/total_cost)*100:.2f}%" if total_cost > 0 else "0%")
                    else:
                        st.metric("總未實現損益", "無法計算")
                else:
                    st.metric("總未實現損益", "無法計算")
            # ETF配置圓餅圖
            st.markdown("---")
            st.subheader("🥧 ETF 配置分析")

            col1, col2 = st.columns(2)

            with col1:
                # 按持有股數分配
                if len(portfolio_display) > 0:
                    fig_shares = px.pie(
                        portfolio_display,
                        values='Shares_Held',
                        names='ETF_Name',
                        title="ETF 持股分配（按股數）"
                    )
                    fig_shares.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig_shares, use_container_width=True)
                else:
                    st.info("無投資組合資料")

            with col2:
                # 按投資金額分配
                if len(portfolio_display) > 0:
                    # 使用市值（如果有的話），否則使用成本基礎
                    value_column = 'Market_Value' if 'Market_Value' in portfolio_display.columns and portfolio_display['Market_Value'].notna().any() else 'Cost_Basis'
                    
                    fig_value = px.pie(
                        portfolio_display,
                        values=value_column,
                        names='ETF_Name',
                        title=f"ETF 配置分配（按{'市值' if value_column == 'Market_Value' else '成本'}）"
                    )
                    fig_value.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig_value, use_container_width=True)
                else:
                    st.info("無投資組合資料")
                    
            
        else:
            st.info("📊 尚無投資組合記錄")
            st.info("💡 完成第一筆買入交易後，投資組合將會自動建立")


def update_portfolio(user_id, etf_id, transaction_type, shares, price):
    """更新投資組合（修正賣出邏輯）"""
    try:
        # 確保參數都是正確的類型
        user_id = str(user_id)  # 確保是字串
        etf_id = str(etf_id)    # 確保是字串
        shares = int(shares)     # 確保是整數
        price = float(price)     # 確保是浮點數
        
        print(f"Debug: update_portfolio called with user_id={user_id}, etf_id={etf_id}, type={transaction_type}, shares={shares}, price={price}")
        
        # 檢查是否已有此ETF的投資組合記錄
        existing_portfolio = run_query("""
            SELECT Portfolio_Id, Shares_Held, Average_Cost
            FROM Portfolio
            WHERE User_Id = %s AND ETF_Id = %s
        """, (user_id, etf_id))
        
        if existing_portfolio is not None and len(existing_portfolio) > 0:
            # 更新現有記錄
            current_shares = int(existing_portfolio['Shares_Held'].iloc[0])
            current_avg_cost = float(existing_portfolio['Average_Cost'].iloc[0])
            portfolio_id = int(existing_portfolio['Portfolio_Id'].iloc[0])
            
            print(f"Debug: Found existing portfolio - shares={current_shares}, avg_cost={current_avg_cost}")
            
            if transaction_type == 'Buy':
                # 買入：增加股數，重新計算平均成本
                total_cost = (current_shares * current_avg_cost) + (shares * price)
                new_shares = current_shares + shares
                new_avg_cost = total_cost / new_shares if new_shares > 0 else 0
                
                print(f"Debug: Buy - new_shares={new_shares}, new_avg_cost={new_avg_cost}")
                
                # 更新記錄
                update_query = """
                    UPDATE Portfolio
                    SET Shares_Held = %s, Average_Cost = %s, Last_Updated = %s
                    WHERE Portfolio_Id = %s
                """
                update_params = (new_shares, new_avg_cost, datetime.now(), portfolio_id)
                success = execute_query(update_query, update_params)
                
                if success:
                    print(f"Debug: Portfolio updated successfully")
                    st.success(f"✅ 投資組合已更新：{etf_id}")
                else:
                    print(f"Debug: Portfolio update failed")
                    st.error(f"❌ 投資組合更新失敗：{etf_id}")
                    
            else:  # Sell
                # 賣出前先檢查持有股數
                if shares > current_shares:
                    print(f"Debug: Trying to sell {shares} but only have {current_shares}")
                    st.error(f"❌ 賣出失敗：股數不足！持有 {current_shares} 股，嘗試賣出 {shares} 股")
                    return False
                
                # 計算賣出後的股數
                new_shares = current_shares - shares
                
                print(f"Debug: Sell - current_shares={current_shares}, selling={shares}, new_shares={new_shares}")
                
                if new_shares == 0:
                    # 全部賣出，刪除投資組合記錄
                    delete_query = "DELETE FROM Portfolio WHERE Portfolio_Id = %s"
                    success = execute_query(delete_query, (portfolio_id,))
                    
                    if success:
                        print(f"Debug: Portfolio deleted successfully (sold all shares)")
                        st.success(f"✅ 已全部賣出 {etf_id}，投資組合記錄已移除")
                    else:
                        print(f"Debug: Portfolio deletion failed")
                        st.error(f"❌ 投資組合記錄刪除失敗：{etf_id}")
                        
                else:
                    # 部分賣出，更新股數（平均成本不變）
                    update_query = """
                        UPDATE Portfolio
                        SET Shares_Held = %s, Last_Updated = %s
                        WHERE Portfolio_Id = %s
                    """
                    update_params = (new_shares, datetime.now(), portfolio_id)
                    success = execute_query(update_query, update_params)
                    
                    if success:
                        print(f"Debug: Portfolio updated successfully (partial sell)")
                        st.success(f"✅ 投資組合已更新：{etf_id}，剩餘 {new_shares} 股")
                    else:
                        print(f"Debug: Portfolio update failed")
                        st.error(f"❌ 投資組合更新失敗：{etf_id}")
            
        else:
            # 沒有現有記錄
            if transaction_type == 'Buy':
                print(f"Debug: Creating new portfolio entry")
                
                # 手動生成Portfolio_Id
                max_portfolio_id = run_query("SELECT COALESCE(MAX(Portfolio_Id), 0) + 1 as next_id FROM Portfolio")
                next_portfolio_id = int(max_portfolio_id['next_id'].iloc[0]) if max_portfolio_id is not None else 1
                
                insert_query = """
                    INSERT INTO Portfolio (Portfolio_Id, User_Id, ETF_Id, Shares_Held, Average_Cost, Last_Updated)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                insert_params = (next_portfolio_id, user_id, etf_id, shares, price, datetime.now())
                success = execute_query(insert_query, insert_params)
                
                if success:
                    print(f"Debug: New portfolio created successfully")
                    st.success(f"✅ 新投資組合已建立：{etf_id}")
                else:
                    print(f"Debug: New portfolio creation failed")
                    st.error(f"❌ 新投資組合建立失敗：{etf_id}")
            else:
                # 賣出但沒有持倉記錄
                print(f"Debug: Trying to sell but no existing portfolio found")
                st.error(f"❌ 賣出失敗：沒有 {etf_id} 的持倉記錄")
                return False
    
    except Exception as e:
        print(f"Debug: Exception in update_portfolio: {str(e)}")
        st.error(f"更新投資組合時發生錯誤: {str(e)}")
        return False
    
    return True

def show_price_charts():
    """價格圖表頁面"""
    st.header("📈 價格圖表")
    
    # 獲取所有ETF列表
    etf_list = run_query("SELECT ETF_Id, ETF_Name FROM ETF ORDER BY ETF_Id")
    
    if etf_list is not None and not etf_list.empty:
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            selected_etf = st.selectbox(
                "選擇 ETF",
                options=etf_list['ETF_Id'].tolist(),
                format_func=lambda x: f"{x} - {etf_list[etf_list['ETF_Id']==x]['ETF_Name'].iloc[0]}"
            )
        
        with col2:
            start_date = st.date_input(
                "開始日期", 
                value=date(2025, 1, 1),
                min_value=date(2000, 1, 1),
                max_value=datetime.now().date()
            )
        
        with col3:
            end_date = st.date_input(
                "結束日期", 
                value=datetime.now().date(),
                min_value=date(2000, 1, 1),
                max_value=datetime.now().date()
            )
        
        # 構建查詢語句
        price_query = """
            SELECT History_Date, Open_Price, Close_Price, High_Price, Low_Price, Volume
            FROM ETF_HistoryPrice
            WHERE ETF_Id = %s AND History_Date BETWEEN %s AND %s
            ORDER BY History_Date
        """
        params = (selected_etf, start_date, end_date)
        
        # 獲取價格數據
        price_data = run_query(price_query, params)
        
        if price_data is not None and not price_data.empty:
            # 確保日期欄位是datetime類型
            price_data['History_Date'] = pd.to_datetime(price_data['History_Date'])
            
            # 移除任何包含NaN值的行（自動跳過沒有開盤的天數）
            price_data = price_data.dropna(subset=['Open_Price', 'Close_Price', 'High_Price', 'Low_Price'])
            
            if not price_data.empty:
                st.markdown("---")
                
                # 顯示資料統計
                col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
                
                with col_stat1:
                    st.metric("資料筆數", len(price_data))
                
                with col_stat2:
                    date_range_days = (price_data['History_Date'].max() - price_data['History_Date'].min()).days
                    st.metric("期間", f"{date_range_days} 天")
                
                with col_stat3:
                    latest_price = price_data['Close_Price'].iloc[-1]
                    st.metric("最新收盤價", f"${latest_price:.2f}")
                
                with col_stat4:
                    price_change = price_data['Close_Price'].iloc[-1] - price_data['Close_Price'].iloc[0]
                    price_change_pct = (price_change / price_data['Close_Price'].iloc[0]) * 100
                    st.metric(
                        "期間漲跌", 
                        f"{price_change_pct:+.2f}%",
                        delta=f"${price_change:+.2f}"
                    )
                
                # K線圖
                fig = go.Figure()
                
                # 添加K線圖
                fig.add_trace(go.Candlestick(
                    x=price_data['History_Date'],
                    open=price_data['Open_Price'],
                    high=price_data['High_Price'],
                    low=price_data['Low_Price'],
                    close=price_data['Close_Price'],
                    name='價格',
                    increasing_line_color='#00ff00',
                    decreasing_line_color='#ff0000'
                ))
                
                # 設定圖表布局
                fig.update_layout(
                    title=f"{selected_etf} 價格走勢 ({start_date} ~ {end_date})",
                    xaxis_title="日期",
                    yaxis_title="價格 ($)",
                    height=600,
                    xaxis_rangeslider_visible=False,  # 隱藏下方的範圍滑塊
                    xaxis=dict(
                        type='date',
                        tickformat='%Y-%m-%d',
                        showgrid=True,
                        gridwidth=1,
                        gridcolor='lightgray',
                        # 修復 K 線空白問題：只顯示有資料的日期範圍
                        range=[price_data['History_Date'].min(), price_data['History_Date'].max()]
                    ),
                    yaxis=dict(
                        showgrid=True,
                        gridwidth=1,
                        gridcolor='lightgray'
                    ),
                    plot_bgcolor='white',
                    font=dict(size=12)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # 成交量圖表
                st.subheader("📊 成交量")
                volume_fig = go.Figure()
                
                volume_fig.add_trace(go.Bar(
                    x=price_data['History_Date'],
                    y=price_data['Volume'],
                    name='成交量',
                    marker_color='lightblue',
                    opacity=0.7
                ))
                
                volume_fig.update_layout(
                    title=f"{selected_etf} 成交量",
                    xaxis_title="日期",
                    yaxis_title="成交量",
                    height=300,
                    xaxis=dict(
                        type='date',
                        tickformat='%Y-%m-%d',
                        # 成交量圖也使用相同的日期範圍
                        range=[price_data['History_Date'].min(), price_data['History_Date'].max()]
                    ),
                    plot_bgcolor='white'
                )
                
                st.plotly_chart(volume_fig, use_container_width=True)
                
                # 資料表格（顯示最近的資料）
                with st.expander("📋 詳細資料 (最近20筆)", expanded=False):
                    display_data = price_data.tail(20).copy()
                    display_data['History_Date'] = display_data['History_Date'].dt.strftime('%Y-%m-%d')
                    display_data = display_data.sort_values('History_Date', ascending=False)
                    
                    st.dataframe(
                        display_data[['History_Date', 'Open_Price', 'High_Price', 'Low_Price', 'Close_Price', 'Volume']],
                        use_container_width=True,
                        column_config={
                            "History_Date": st.column_config.TextColumn("日期"),
                            "Open_Price": st.column_config.NumberColumn("開盤價", format="$%.2f"),
                            "High_Price": st.column_config.NumberColumn("最高價", format="$%.2f"),
                            "Low_Price": st.column_config.NumberColumn("最低價", format="$%.2f"),
                            "Close_Price": st.column_config.NumberColumn("收盤價", format="$%.2f"),
                            "Volume": st.column_config.NumberColumn("成交量", format="%d")
                        }
                    )
            else:
                st.warning("⚠️ 選擇的日期範圍內沒有有效的價格資料")
        else:
            st.info("📝 暫無價格數據")
            st.markdown("**可能的原因：**")
            st.markdown("- 該 ETF 尚未有歷史價格資料")
            st.markdown("- 選擇的日期範圍內沒有交易資料")
            st.markdown("- 資料庫連接問題")
    else:
        st.error("❌ 無法獲取 ETF 列表，請檢查資料庫連接")

if __name__ == "__main__":
    main()
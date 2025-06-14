import requests
import json
from typing import Dict, List, Optional, Union
import time

class ETFPriceCrawler:
    def __init__(self):
        self.base_url = "https://mis.twse.com.tw/stock/api/getStockInfo.jsp"
        self.session = requests.Session()
        # 設定請求標頭，模擬瀏覽器行為
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://mis.twse.com.tw/',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-TW,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        })
    
    def get_etf_info(self, symbols: Union[str, List[str]]) -> Dict:
        """
        取得ETF資訊
        
        Args:
            symbols: ETF代碼，可以是單一字串或字串列表
                    格式: "tse_0050.tw" 或 ["tse_0050.tw", "otc_00679B.tw"]
        
        Returns:
            返回API回應的JSON資料
        """
        if isinstance(symbols, list):
            ex_ch = "|".join(symbols)
        else:
            ex_ch = symbols
        
        params = {"ex_ch": ex_ch}
        
        try:
            response = self.session.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"請求錯誤: {e}")
            return {}
        except json.JSONDecodeError as e:
            print(f"JSON解析錯誤: {e}")
            return {}
    
    def is_valid_etf_data(self, etf_data: Dict) -> bool:
        """
        檢查ETF資料是否有效（非空）
        
        Args:
            etf_data: ETF資料字典
        
        Returns:
            True if 資料有效，False if 資料為空或無效
        """
        # 檢查基本必要欄位
        etf_code = etf_data.get("c", "")
        etf_name = etf_data.get("n", "")
        
        # 如果ETF代碼或名稱為空，視為無效
        if not etf_code or not etf_name:
            return False
        
        # 檢查是否有任何價格資料
        price_fields = ["z", "o", "h", "l", "y", "a", "b"]
        has_price_data = any(
            etf_data.get(field) and etf_data.get(field) != "-" 
            for field in price_fields
        )
        
        return has_price_data
    
    def parse_etf_price_data(self, etf_data: Dict) -> Dict:
        """
        解析ETF價格資料，處理當盤成交價為空的情況
        
        Args:
            etf_data: 單一ETF的資料字典
        
        Returns:
            處理後的ETF資料
        """
        # 處理累積成交量，加上"張"單位
        volume_str = etf_data.get("v", "0")
        volume_with_unit = f"{volume_str}張" if volume_str else "0張"
        
        result = {
            "ETF_Id": etf_data.get("c", ""),
            "ETF_Name": etf_data.get("n", ""),
            "累積成交量": volume_with_unit,
            "開盤價": self.parse_price(etf_data.get("o", "")),
            "最高價": self.parse_price(etf_data.get("h", "")),
            "最低價": self.parse_price(etf_data.get("l", "")),
            "昨日收盤價": self.parse_price(etf_data.get("y", "")),
            "買價": etf_data.get("b", ""),
            "賣價": etf_data.get("a", ""),
            "時間": etf_data.get("t", ""),
            "日期": etf_data.get("d", ""),
            "更新時間": self.format_datetime(etf_data.get("d", ""), etf_data.get("t", "")),
            "原始資料": etf_data  # 保留原始資料供其他用途
        }
        
        # 處理當盤成交價為空或"-"的情況
        current_price = etf_data.get("z", "")
        if not current_price or current_price == "-":
            estimated_price = self.estimate_price(etf_data)
            result["當前價格"] = estimated_price
            result["價格狀態"] = "推估"
        else:
            result["當前價格"] = self.parse_price(current_price)
            result["價格狀態"] = "即時"
        
        return result
    
    def parse_price(self, price_str: str) -> float:
        """解析價格字串為浮點數"""
        if not price_str or price_str == "-":
            return 0.0
        try:
            return float(price_str)
        except (ValueError, TypeError):
            return 0.0
    
    def format_datetime(self, date_str: str, time_str: str) -> str:
        """
        格式化日期時間為 YYYY/MM/DD HH:MM:SS 格式
        
        Args:
            date_str: 日期字串，格式如 "20250522"
            time_str: 時間字串，格式如 "13:30:00"
        
        Returns:
            格式化後的日期時間字串
        """
        if not date_str or not time_str:
            return ""
        
        try:
            # 處理日期格式 "20250522" -> "2025/05/22"
            if len(date_str) == 8:
                year = date_str[:4]
                month = date_str[4:6]
                day = date_str[6:8]
                formatted_date = f"{year}/{month}/{day}"
                
                # 組合日期和時間
                return f"{formatted_date} {time_str}"
            else:
                return f"{date_str} {time_str}"
        except Exception:
            return f"{date_str} {time_str}"
    
    def estimate_price(self, etf_data: Dict) -> float:
        """
        推測ETF價格的邏輯
        
        Args:
            etf_data: ETF資料字典
        
        Returns:
            推測的價格
        """
        # 取得買賣五檔資料
        a_str = etf_data.get("a", "")  # 賣價
        b_str = etf_data.get("b", "")  # 買價
        
        # 解析賣價
        a_prices = []
        if a_str:
            a_prices = [float(price) for price in a_str.split("_") 
                       if price and price != "" and self.is_valid_price(price)]
        
        # 解析買價
        b_prices = []
        if b_str:
            b_prices = [float(price) for price in b_str.split("_") 
                       if price and price != "" and self.is_valid_price(price)]
        
        # 取得最低賣價和最高買價
        lowest_sell = min(a_prices) if a_prices else None
        highest_buy = max(b_prices) if b_prices else None
        
        # 推測邏輯
        if lowest_sell is not None and highest_buy is not None:
            # 如果兩邊都有資料，取中間值
            estimated_price = (lowest_sell + highest_buy) / 2
            return self.adjust_price_by_tick_size(estimated_price)
        elif lowest_sell is not None:
            # 只有賣價資料
            return lowest_sell
        elif highest_buy is not None:
            # 只有買價資料
            return highest_buy
        else:
            # 都沒有資料，使用備用方案
            return self.fallback_price_estimation(etf_data)
    
    def is_valid_price(self, price_str: str) -> bool:
        """檢查價格字串是否有效"""
        try:
            price = float(price_str)
            return price > 0
        except (ValueError, TypeError):
            return False
    
    def adjust_price_by_tick_size(self, price: float) -> float:
        """
        根據價格區間調整跳動單位
        台股的跳動單位規則：
        - 未滿10元：0.01元
        - 10元以上未滿50元：0.05元
        - 50元以上未滿100元：0.1元
        - 100元以上未滿500元：0.5元
        - 500元以上未滿1000元：1元
        - 1000元以上：5元
        """
        if price < 10:
            tick_size = 0.01
        elif price < 50:
            tick_size = 0.05
        elif price < 100:
            tick_size = 0.1
        elif price < 500:
            tick_size = 0.5
        elif price < 1000:
            tick_size = 1
        else:
            tick_size = 5
        
        return round(price / tick_size) * tick_size
    
    def fallback_price_estimation(self, etf_data: Dict) -> float:
        """
        備用價格推測方案
        """
        # 嘗試使用最高價和最低價的平均
        high_price = etf_data.get("h", "")
        low_price = etf_data.get("l", "")
        
        if high_price and low_price and self.is_valid_price(high_price) and self.is_valid_price(low_price):
            return (float(high_price) + float(low_price)) / 2
        
        # 最後使用昨日收盤價
        yesterday_close = etf_data.get("y", "")
        if yesterday_close and self.is_valid_price(yesterday_close):
            return float(yesterday_close)
        
        return 0.0
    
    def get_single_etf_smart(self, etf_code: str) -> Optional[Dict]:
        """
        智能查詢單一ETF的資料
        先當成上市(TSE)查詢，失敗的再當成上櫃(OTC)查詢
        
        Args:
            etf_code: ETF代碼（純代碼，不含前綴）
        
        Returns:
            處理後的ETF資料，如果找不到則返回None
        """
        # 第一輪：當成上市（TSE）來抓
        tse_symbol = f"tse_{etf_code}.tw"
        tse_data = self.get_etf_info(tse_symbol)
        
        if tse_data and "msgArray" in tse_data:
            for etf_data in tse_data["msgArray"]:
                if self.is_valid_etf_data(etf_data):
                    return self.parse_etf_price_data(etf_data)
        
        # 第二輪：當成上櫃（OTC）來抓
        otc_symbol = f"otc_{etf_code}.tw"
        otc_data = self.get_etf_info(otc_symbol)
        
        if otc_data and "msgArray" in otc_data:
            for etf_data in otc_data["msgArray"]:
                if self.is_valid_etf_data(etf_data):
                    return self.parse_etf_price_data(etf_data)
        
        return None
    
    def get_multiple_etfs_smart(self, etf_codes: List[str]) -> List[Dict]:
        """
        先當成上市(TSE)查詢，失敗的再當成上櫃(OTC)查詢
        只返回有效的ETF資料，過濾掉空資料
        
        Args:
            etf_codes: ETF代碼列表（純代碼，不含前綴）
        
        Returns:
            處理後的有效ETF資料列表
        """
        results = []
        unprocessed_codes = etf_codes.copy()
        
        # 第一輪：全部當成上市（TSE）來抓
        if unprocessed_codes:
            tse_symbols = [f"tse_{code}.tw" for code in unprocessed_codes]
            tse_data = self.get_etf_info(tse_symbols)
            
            if tse_data and "msgArray" in tse_data:
                for etf_data in tse_data["msgArray"]:
                    # 只處理有效的ETF資料
                    if self.is_valid_etf_data(etf_data):
                        parsed_data = self.parse_etf_price_data(etf_data)
                        results.append(parsed_data)
                        # 從未處理列表中移除已成功取得的代碼
                        etf_code = etf_data.get("c", "")
                        if etf_code in unprocessed_codes:
                            unprocessed_codes.remove(etf_code)
        
        # 第二輪：剩下的當成上櫃（OTC）來抓
        if unprocessed_codes:
            otc_symbols = [f"otc_{code}.tw" for code in unprocessed_codes]
            otc_data = self.get_etf_info(otc_symbols)
            
            if otc_data and "msgArray" in otc_data:
                for etf_data in otc_data["msgArray"]:
                    # 只處理有效的ETF資料
                    if self.is_valid_etf_data(etf_data):
                        parsed_data = self.parse_etf_price_data(etf_data)
                        results.append(parsed_data)
                        # 從未處理列表中移除已成功取得的代碼
                        etf_code = etf_data.get("c", "")
                        if etf_code in unprocessed_codes:
                            unprocessed_codes.remove(etf_code)
        
        return results


def main():
    """主程式示範"""
    crawler = ETFPriceCrawler()
    
    # 測試單一ETF查詢
    etf_code = "0050"
    etf_info = crawler.get_single_etf_smart(etf_code)
    
    if etf_info:
        print(f"ETF代碼: {etf_info['ETF_Id']}")
        print(f"ETF名稱: {etf_info['ETF_Name']}")
        print(f"當前價格: {etf_info['當前價格']:.2f}元 ({etf_info['價格狀態']})")
        print(f"開盤價: {etf_info['開盤價']:.2f}元")
        print(f"最高價: {etf_info['最高價']:.2f}元")
        print(f"最低價: {etf_info['最低價']:.2f}元")
        print(f"昨日收盤價: {etf_info['昨日收盤價']:.2f}元")
        print(f"累積成交量: {etf_info['累積成交量']}")
        print(f"更新時間: {etf_info['更新時間']}")
    else:
        print(f"找不到ETF {etf_code} 的資料")


if __name__ == "__main__":
    main()
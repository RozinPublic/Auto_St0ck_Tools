import json
import time
from datetime import datetime
import akshare as ak
import pandas as pd
import configparser
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 交易时间检查函数 返回布尔类型 true false
def check_trading_time():
    now = datetime.now()
    weekday = now.weekday()

    # 判断是否在周一至周五
    if 0 <= weekday <= 4:
        s1 = now.replace(hour=9,minute=30,second=0,microsecond=0)
        e1 = now.replace(hour=11,minute=30,second=0,microsecond=0)
        s2 = now.replace(hour=13,minute=0,second=0,microsecond=0)
        e2 = now.replace(hour=15,minute=0,second=0,microsecond=0)

        # 判断是否在指定时间段内
        if (s1 <= now <= e1) or(s2 <= now <= e2):
            return True
    return False

# 需要监控的股票信息
class MonitorStockInfo:
    def __init__(self, stock_code, stock_name, target_price_buy, target_price_sell, current_price, message):
        self.stock_code = stock_code  # 股票代码
        self.stock_name = stock_name  # 公司名称
        self.target_price_buy = target_price_buy  # 预期加仓价格
        self.target_price_sell = target_price_sell  # 预期清仓价格
        self.current_price = current_price
        self.message = message  # 备注信息

# 根据 需要监控的股票信息和 通过akshare库获取的实时股票数据 使用阿里云服务发送短信
def get_RTprices(monitor_stock_Info: MonitorStockInfo):
    stock_code = monitor_stock_Info.stock_code
    
    stock_bid_ask_em_df = ak.stock_bid_ask_em(symbol = stock_code)
    # print(stock_bid_ask_em_df)
            
    stock_individual_info_em_df = ak.stock_individual_info_em(symbol = stock_code)
    # print(stock_individual_info_em_df)

    stock_name = stock_individual_info_em_df.iloc[1,1]
    current_price = float(stock_bid_ask_em_df.iloc[20,1])

    print(f"__compare_RTprices__ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 股票代码：{stock_code} 公司名：{stock_name} 实时价格：{current_price} 元")

    monitor_stock_Info.stock_name = stock_name
    monitor_stock_Info.current_price = current_price
    
    return current_price

def compare_RTprices(monitor_stock_Info: MonitorStockInfo):
    target_price_buy = monitor_stock_Info.target_price_buy
    target_price_sell = monitor_stock_Info.target_price_sell

    if monitor_stock_Info.current_price <= target_price_buy and target_price_buy != 0:  # 设置涨跌幅度阈值
        compare_result = "买入/加仓/止损"
    elif monitor_stock_Info.current_price >= target_price_sell and target_price_sell != 0:
        compare_result = "卖出/减仓/止盈"
    else:
        compare_result = ""

    monitor_stock_Info.message = compare_result

# 从json文件中读取需要监控的股票信息
def read_stock_info_from_json(json_file_path):
    stock_info_list = []
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        # print(data)

    stock_info_array = data.get('stock_info_monitor', [])
    # print(stock_info_array)

    for stock_data in stock_info_array:
        stock_code = stock_data.get('stock_code')
        stock_name = stock_data.get('stock_name')
        target_price_buy = stock_data.get('target_price_buy')
        target_price_sell = stock_data.get('target_price_sell')
        current_price = None
        message = None

        # 检查前必填字段是否都不为空
        if stock_code and target_price_buy and target_price_sell:
            stock_info = MonitorStockInfo(stock_code, stock_name, target_price_buy, target_price_sell, current_price, message)
            stock_info_list.append(stock_info)
        else:
            print(f"请检查 {json_file_path} 文件")
            exit()

    return stock_info_list

# 通过163发送提示信息
def send_msg_mail_163(subject, content):
    # 读取配置文件
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')

    sender = config.get('email', 'sender')
    password = config.get('email', 'password')

    receiver = 'RozinPrivate@163.com'

    # 创建一个带文本内容的邮件实例
    message = MIMEText(content, 'html', 'utf-8')
    message['From'] = Header(sender)
    message['To'] = Header(receiver)
    message['Subject'] = Header(subject)

    # 连接服务器并发送邮件
    try:
        smtpObj = smtplib.SMTP_SSL("smtp.163.com", 994)
        smtpObj.login(sender, password)
        smtpObj.sendmail(sender, receiver, message.as_string())
        return "邮件发送成功"
    except smtplib.SMTPException as e:
        return f"Error: 无法发送邮件，{e}"
    finally:
        smtpObj.quit()

# 格式化邮件内容并发送
def send_msg_mail_163_html(json_data):
    # 将数据转换为字典（假设json_data是一个具有相关属性的对象，这里可能需要确保其有__dict__属性可访问）
    data_dict = json_data.__dict__

    # 构建邮件内容字符串
    content = ""
    content += f"股票代码: {data_dict['stock_code']}\n <br>"
    content += f"公司名称: {data_dict['stock_name']}\n <br>"
    content += f"预期买入: {data_dict['target_price_buy']} ￥\n <br>"
    content += f"预期卖出: {data_dict['target_price_sell']} ￥\n <br>"
    content += f"当前价格: {data_dict['current_price']} ￥\n <br>"
    content += f"备注信息: {data_dict['message']}\n <br>"

    # 设置邮件主题
    subject = "股票盯盘信息"

    # 发送邮件
    send_msg_mail_163(subject, content)

# 循环函数
def run_loop(info, sleep):
    result = check_trading_time()
    if not result:
        print(f"__run_loop__ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 不在交易时间!")
    else:
        for stock_info in info:
            get_RTprices(stock_info)
            compare_RTprices(stock_info)
            if stock_info.message != "":
                send_msg_mail_163_html(stock_info)
    time.sleep(sleep)  # 适当延迟，避免频繁执行

def main():
    # 读取配置文件
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')

    # 读取需监控的股票信息
    stock_info_list = read_stock_info_from_json(config.get('system', 'stock_info_monitor_json_file_path'))

    sleep_time = int(config.get('system', 'sleep_time'))
    while stock_info_list:
        run_loop(stock_info_list, sleep_time)

if __name__ == "__main__":
    main()

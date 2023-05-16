import multiprocessing
import time
from tkinter import *
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pymongo
import pandas as pd
import numpy as np
import threading
import psutil
import os
import sys
import requests

from selenium import webdriver
import json
import lxml.html as LH
import lxml.html.clean as clean

# 定义图标样式大小参数
f = Figure(figsize=(15, 8), dpi=100)

# 连接MongoDB
host = "localhost"
port = 27017
db_name = "boss"
client = pymongo.MongoClient(host=host, port=port)
db = client[db_name]
collection = db["job"]

# 运行爬虫函数
def start_crawl(kwd):
    # 获取爬虫设置
    process = CrawlerProcess(get_project_settings())
    # 指定爬虫程序
    process.crawl("jobspider", kwd)
    # 运行爬虫
    process.start()


# 运行搜索函数
def search():
    try:
        # 如果条形图存在，清空条形图
        if f:
            f.clf()
        # 修改运行状态
        lable_value.set("正在抓取数据中，请稍等.....")
        # 获得输入框数据
        kwd = entry.get()
        # 判断输入框是否为空
        if kwd == "":
            lable_value.set("请输入关键词")
            return

        print(f"关键词{kwd}")
        # 线程
        the_scrapy = multiprocessing.Process(target=start_crawl, args=(kwd,))
        the_scrapy.start()
        print(the_scrapy.pid)
        while the_scrapy.pid in psutil.pids():
            time.sleep(0.5)


        data_df = pd.DataFrame(list(collection.find()))

        # 改变运行状态
        lable_value.set("数据抓取成功，当前数据库总量为【"+str(len(data_df))+"】，点击获取职责即可再次爬取")
        time.sleep(3)
        # draw(kwd) # 不进行分析了

    except Exception as e:
        print("错误信息---" + str(e))
        lable_value.set("数据抓取失败....")


# 将函数打包进线程
def thread_it(func, *args):
    # 创建
    t = threading.Thread(target=func, args=args)
    # 守护
    t.daemon = True
    # 启动
    t.start()


# 爬取岗位职责函数
def getJbInfo():

    # 实例化
    options = webdriver.EdgeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    # options.add_argument('--proxy-server=http://%s' % PROXY)
    driver = webdriver.Edge(options=options)

    # 读取每一行的_id和jobDescJsonUrl
    data_df = pd.DataFrame(list(collection.find()))
    # 拿postDescription字段为空的数据
    data_df = data_df[data_df["postDescription"].isnull()]
    if len(data_df) == 0:
        lable_value.set("没有需要更新的数据")
        return

    lable_value.set("正在爬取数据中......")
    for i in range(len(data_df)):
        print(data_df.iloc[i]["_id"], data_df.iloc[i]["jobDescJsonUrl"])
        # 根据总数量和当前数量计算进度
        lable_value.set(
            "正在爬取【"
            + str(data_df.iloc[i]["_id"])
            + "】的数据，总进度"
            + str(i + 1)
            + "/"
            + str(len(data_df))
        )
        driver.get(data_df.iloc[i]["jobDescJsonUrl"])
        time.sleep(1)
        # 获取全部文本
        content = driver.page_source
        cleaner = clean.Cleaner()
        content = cleaner.clean_html(content)
        # 只要<div><body><pre>标签中的内容
        content = LH.fromstring(content).xpath("//pre/text()")[0]
        # 字符串转json
        json_data = json.loads(content)
        # print(type(json_data))
        # 判断message是否为Success
        if json_data["message"] == "Success":
            postDescription = json_data["zpData"]["jobCard"]["postDescription"]
            zpData = json_data["zpData"]
        else:
            zpData = []
            postDescription = "无数据"

        # 更新数据库把postDescription字段更新
        db["job"].update_one(
            {"_id": data_df.iloc[i]["_id"]},
            {"$set": {"postDescription": postDescription}},
        )
        # 更新数据库把zpData字段更新
        db["job"].update_one(
            {"_id": data_df.iloc[i]["_id"]}, {"$set": {"zpData": zpData}}
        )
        time.sleep(0.01)
    lable_value.set("更新完成")

# 导出excel
def export_excel():

  data_df = pd.DataFrame(list(collection.find()))
  # 判断有没有数据
  if len(data_df) == 0:
    lable_value.set("没有数据可以导出")
    return

  # 拿出字段 jobkwd，jobName，cityName，companyName，salaryDesc，jobExperience，jobDegree，jobDescJsonUrl，postDescription 字段 生成excel
  data_df = data_df[["jobkwd","jobName","cityName","companyName","salaryDesc","jobExperience","jobDegree","jobDescJsonUrl","postDescription"]]
  data_df.to_excel("boss.xlsx",index=False)
  lable_value.set("导出成功，请打开【boss.xlsx】文件查看")
  # 判断系统是不是windows
  os.system("explorer.exe %s" % os.path.dirname(os.path.abspath(__file__)))

  




# 初始化GUI界面函数
def init_GUI():
    # 实例化GUI界面
    global root
    root = Tk()
    root.geometry("750x200")
    root.title("boss抓取")

    label = Label(root, text="岗位:", font=("宋体", 18), pady=20)
    label.place(x=50, y=15)

    # 岗位输入框
    global pos_var, entry
    pos_var = StringVar()
    entry = Entry(root, font=("宋体", 18), textvariable=pos_var)
    entry.place(x=120, y=35)

    # 查询按钮
    # lambda :thread_it(search, ) 打包线程，避免卡死
    button = Button(
        root, text="1.搜索", font=("宋体", 16), fg="blue", command=lambda: thread_it(search)
    )
    button.place(x=380, y=30)

    # 获取岗位职责
    button2 = Button(
        root, text="2.获取职责", font=("宋体", 16), fg="blue", command=lambda: thread_it(getJbInfo)
    )
    button2.place(x=480, y=30)

    # 导出excel
    button2 = Button(
        root, text="3.导出", font=("宋体", 16), fg="blue", command=lambda: thread_it(export_excel)
    )
    button2.place(x=620, y=30)

    # 运行状态
    global lable_value
    lable_value = StringVar()
    label = Label(root, textvariable=lable_value, font=("宋体", 14), pady=20)
    lable_value.set("")
    label.place(x=50, y=100)

    if check_edge_open() == False:
      if check_shortcut():
        lable_value.set("已打开端口浏览器，请登录boss直聘")
      else:
        lable_value.set("请确保已经打开了端口为9222的Edge浏览器，且已经登录了boss直聘\n开启端口参数：--remote-debugging-port=9222\n开启用户目录自定义参数：--user-data-dir=C:\\temp\\edge_user_data\n")
    else:
      lable_value.set("输入要查询的岗位名称，就可以开始爬取数据了")
    # 窗口常显
    root.mainloop()

# 判断当前目录下有没有快捷方式DebugEdge.lnk
def check_shortcut():
  # 获取当前目录
  current_path = os.path.dirname(os.path.abspath(__file__))
  # 获取当前目录下的所有文件
  file_list = os.listdir(current_path)
  # 判断有没有快捷方式DebugEdge.lnk
  if "DebugEdge.lnk" in file_list:
    # 打开快捷方式
    os.startfile("DebugEdge.lnk")
    return True
  else:
    return False

# 检查用get方式访问http://127.0.0.1:9222/状态是不是200
def check_edge_open():
  try:
    response = requests.get("http://127.0.0.1:9222")
    if response.status_code == 200:
      return True
    else:
      return False
  except:
    return False

# 主函数
if __name__ == "__main__":
    # 初始化GUI界面
    init_GUI()

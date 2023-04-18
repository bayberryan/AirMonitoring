#!/usr/bin/env python
# -*- coding: utf8 -*-
# @file : pm25.py
# @time ： 2023/04/16 14:33
# @copyright ： RickerYan
# @author : RickerYan
# @email : bayberryan@hotmail.com
# @summary :
# 基于selenium模拟用户浏览提取pm2.5站点昨日数据
# 站点地址：https://www.zq12369.com/environment.php?city={}&tab=city
import time
import logging
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By

cities = ["北京", "天津", "上海", "重庆"]
city_stations = {}
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pm2.5 spyder")


def yesterday_csv():
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = today-oneday
    return str(yesterday) + ".csv"


def write():
    dst_file = yesterday_csv()
    with open(dst_file, "w", encoding="utf8") as dst:
        dst.write("city,station,pm2.5\n")
        for city in city_stations.keys():
            stations = city_stations[city][0]
            pm25s = city_stations[city][1]
            station_size = len(stations)
            pm25_size = len(pm25s)
            if station_size != pm25_size:
                logger.error(" station and pm2.5 size conflict. city:{},stations size:{},pm2.5 size:{}"
                             .format(city, station_size, pm25_size))
            for i in range(station_size):
                dst.write("{},{},{}\n".format(city, stations[i], pm25s[i]))


def main():
    station_names = []
    station_pm25s = []
    driver = webdriver.Chrome()
    for city in cities:
        logger.info(" Starting city: {} ...".format(city))
        driver.get("https://www.zq12369.com/environment.php?city={}&tab=city".format(city))
        time.sleep(1)
        # 查找站点图表的指标切换按钮并点击
        require_bottom = driver.find_element(By.CLASS_NAME, 'require_bottom')
        rows = require_bottom.find_elements(By.CLASS_NAME, "row")
        point_row = rows[10]
        btn_group1 = point_row.find_element(By.ID, "btn-group1")
        btn_pm25 = btn_group1.find_elements(By.TAG_NAME, "button")[1]
        btn_pm25.click()
        # 切换pm2.5后暂停1s，防止数据未渲染
        time.sleep(1)
        # 查找图表矢量提取站点和pm2.5
        svg = point_row.find_element(By.TAG_NAME, "svg")
        g_list = svg.find_elements(By.TAG_NAME, "g")
        labels = g_list[-3].find_elements(By.TAG_NAME, "text")
        for label in labels:
            station_names.append(label.text)
        pm25_g_list = g_list[7].find_elements(By.TAG_NAME, "g")
        for pm25_g in pm25_g_list:
            pm25 = pm25_g.find_element(By.TAG_NAME, "text").text
            station_pm25s.append(pm25)
        city_stations[city] = [station_names, station_pm25s]
        logger.info(" Done.")
    logger.info(" Write to file ...")
    write()
    logger.info(" Done.")
    logger.info(" All finished.")


if __name__ == '__main__':
    main()
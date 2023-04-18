# AirMonitoring
空气质量监测

```commandline
目前pm2.5数据能够完成抓取，但存在不稳定性。ide中执行成功，命令行直接调用报错导致部分输出结果为空。错误信息：
ERROR:socket_manager.cc(141)] Failed to resolve address for stun.services.mozilla.com., errorcode: -105
```

- python-3.10.11-embed-amd64

  pyton环境,为方便使用打包所有用到的三方库。使用时只需在设备安装版本为 112.0.5615.x 的 chrome 浏览器

- pm25.py 

  昨日pm2.5抓取代码

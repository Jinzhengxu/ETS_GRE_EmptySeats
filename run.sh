#!/bin/sh
# 记录一下开始时间
cd /Volumes/DATA/Base_API &&
echo `date` >> ./log.txt &&
# 进入helloworld.py程序所在目录
SHELL=/bin/zsh
PATH=/usr/local/bin/:/usr/bin:/usr/sbin:/usr/bin/chromedriver
# 执行python脚本（注意前面要指定python运行环境/usr/bin/python，根据自己的情况改变）
python3 main.py
# 运行完成
echo 'finish' >> ./log.txt

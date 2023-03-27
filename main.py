## 2023/03/21
## author: Otirik

from logger import logger

import uuid
import click
import requests
import logging
import urllib.parse
import socket

protocol = "http"
server_ip = "192.168.7.221"
server_port = "801"

allow_redirects = False  # 不准重定向

ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.97 Safari/537.36"
headers = {
    "Host": f"{server_ip}:{server_port}",
    "User-Agent": ua,
    "Content-Type": "application/x-www-form-urlencoded",
    "Content-Length": "0",
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1",
    "Origin": f"{protocol}://{server_ip}",
    "Accept":
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Referer": f"{protocol}://{server_ip}/",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "close"
}

local_ip = ""


def choice_ip():
    global local_ip
    ips = socket.gethostbyname_ex(socket.gethostname())[2]
    print(f"检测到设备上有{len(ips)}个网络适配器,IP地址列表如下：")
    for i in range(len(ips)):
        print(f"{i+1}. {ips[i]}")
    print(f"{len(ips)+1}. 没有我想选的校园网内网ip地址")
    print("=================================")
    print("如果不知道自己的校园网内网ip地址，可以在命令行通过ipconfig(Windows)或者ifconfig(Linux)命令查看")
    print("如果没有列出校园网内网ip地址，请检查是否已连接校园网wifi，或者尝试重新连接")
    print("=================================")
    inp = int(input("请选择校园网内网ip地址："))
    if inp > len(ips):
        logger.debug("没有选择校园网内网ip地址")
        exit(0)
    local_ip = ips[inp - 1]
    logger.debug("已选择ip地址: %s" % local_ip)


@click.command()
@click.option("-u", "--uname", type=str, prompt="请输入账号", help="账号")
@click.option("-p",
              "--upass",
              type=str,
              prompt="请输入密码(无回显)",
              hide_input=True,
              help="密码")
def login(uname, upass):
    logger.debug("执行登录操作")
    choice_ip()
    login_url = f"{protocol}://{server_ip}:{server_port}/eportal/?c=ACSetting&a=Login&protocol={protocol}:&hostname={server_ip}&iTermType=1&wlanuserip={local_ip}&wlanacip=192.168.130.254&wlanacname=ME60-X8-1&mac=4b-1c-c3-90-17-85&ip={local_ip}&enAdvert=0&queryACIP=0&loginMethod=1"

    post_data = f"DDDDD=%2C0%2C{urllib.parse.quote(uname)}&upass={urllib.parse.quote(upass)}&R1=0&R2=0&R3=0&R6=0&para=00&0MKKey=123456&buttonClicked=&redirect_url=&err_flag=&username=&password=&user=&cmd=&Login="

    r = requests.post(login_url,
                      headers=headers,
                      data=post_data,
                      allow_redirects=allow_redirects)

    location = r.headers.get("Location")
    logger.debug("请求地址：%s" % login_url)
    logger.debug("请求参数：%s" % post_data)
    logger.debug("Http状态码：%d" % r.status_code)
    logger.debug("重定向：%s" % location)
    if location.find("3.htm") != -1:
        logger.info("登录成功")
    else:
        logger.info("登录失败")


@click.command()
def logout():
    logger.debug("执行注销操作")
    choice_ip()
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    logout_url = f"{protocol}://{server_ip}:{server_port}/eportal/?c=ACSetting&a=Logout&wlanuserip={local_ip}&wlanacip=192.168.130.254&wlanacname=ME60-X8-1&port=&hostname=192.168.7.221&iTermType=1&session=&queryACIP=0&mac={mac}"

    post_data = ""

    r = requests.post(logout_url,
                      headers=headers,
                      data=post_data,
                      allow_redirects=allow_redirects)

    location = r.headers.get("Location")
    logger.debug("Http状态码：%d" % r.status_code)
    logger.debug("重定向：%s" % location)

    if location.find("2.htm") != -1:
        logger.info("注销成功")
    else:
        logger.info("注销失败")


@click.group()
@click.option("--debug/--no-debug", default=False, help="是否开启debug")
def main(debug):
    if debug:
        logger.setLevel(level=logging.DEBUG)


main.add_command(login)
main.add_command(logout)

if __name__ == "__main__":
    main()

## update: 2023/06/01
## author: Otirik

import uuid
import click
import logging
import requests
import configparser

from logger import logger
from urllib.parse import quote

## 读取配置文件
config = configparser.ConfigParser()
path = "./config.ini"
config.read(path, encoding="utf8")
local_ip = config.get('xyw', 'local_ip')
account = config.get('xyw', 'account')
password = config.get('xyw', 'password')
## 设置请求所需的一些参数
protocol = "http"
server_ip = "192.168.7.221"
server_port = "801"
allow_redirects = False  # 关闭重定向
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


def check_network() -> bool:

    try:
        r = requests.get("https://www.baidu.com")
        return r.status_code == 200

    except Exception:
        return False


@click.command()
def login() -> None:

    if check_network():
        logger.info("网络正常，请勿重复登录。")
        return

    logger.info("尝试执行登录...")

    login_url = f"{protocol}://{server_ip}:{server_port}/eportal/?c=ACSetting&a=Login&protocol={protocol}:&hostname={server_ip}&iTermType=1&wlanuserip={local_ip}&wlanacip=192.168.130.254&wlanacname=ME60-X8-1&mac=4b-1c-c3-90-17-85&ip={local_ip}&enAdvert=0&queryACIP=0&loginMethod=1"

    post_data = f"DDDDD=%2C0%2C{quote(account)}&upass={quote(password)}&R1=0&R2=0&R3=0&R6=0&para=00&0MKKey=123456&buttonClicked=&redirect_url=&err_flag=&username=&password=&user=&cmd=&Login="

    try:
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

            logger.info("登录成功！")

        else:

            logger.info("登录失败！")

    except requests.exceptions.ProxyError:
        logger.error("无法连接至代理，请检查你的代理设置。")

    except Exception as e:
        print(e)

    return


@click.command()
def logout():

    if not check_network():

        logger.warn("已经注销，请勿重复。")

        return

    logger.info("尝试执行注销...")

    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]

    logout_url = f"{protocol}://{server_ip}:{server_port}/eportal/?c=ACSetting&a=Logout&wlanuserip={local_ip}&wlanacip=192.168.130.254&wlanacname=ME60-X8-1&port=&hostname=192.168.7.221&iTermType=1&session=&queryACIP=0&mac={mac}"

    post_data = ""

    try:
        r = requests.post(logout_url,
                          headers=headers,
                          data=post_data,
                          allow_redirects=allow_redirects)

        location = r.headers.get("Location")
        logger.debug("Http状态码：%d" % r.status_code)
        logger.debug("重定向：%s" % location)

        if location.find("2.htm") != -1:

            logger.info("注销成功！")

        else:

            logger.info("注销失败！")

    except requests.exceptions.ProxyError:
        logger.error("无法连接至代理，请检查你的代理设置。")

    return


@click.group()
@click.option("--debug/--no-debug", default=False, help="是否开启debug")
def main(debug):
    if debug:
        logger.setLevel(level=logging.DEBUG)


main.add_command(login)
main.add_command(logout)

if __name__ == "__main__":
    main()

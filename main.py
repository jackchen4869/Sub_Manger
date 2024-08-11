import re
import time
import requests

from bs4 import BeautifulSoup
from urllib import parse
from urllib.parse import unquote


def get_filename_from_url(url):
    if "sub?target=" in url:
        pattern = r"url=([^&]*)"
        match = re.search(pattern, url)
        if match:
            encoded_url = match.group(1)
            decoded_url = unquote(encoded_url)
            return get_filename_from_url(decoded_url)
    else:
        if ("&flag=clash" not in url) and ("?token=" in url):
            url = url + "&flag=clash"
        else:
            pass
        try:
            response = requests.get(url)
            header = response.headers.get("Content-Disposition")
            if header:
                if "filename*=UTF-8''" in header:
                    pattern = r"filename\*=UTF-8''(.+)"
                    result = re.search(pattern, header)
                    if result:
                        filename = result.group(1)
                        filename = parse.unquote(filename)  # 对文件名进行解码
                        airport_name = filename.replace("%20", " ").replace("%2B", "+")
                        return airport_name
                    return "呜呜,可莉没有看到U8文件名"
                else:
                    header = header.split(";")
                    for i in header:
                        if "filename=" in i:
                            i1 = i.strip().split("=")
                            result = i1[1]
                    if result:
                        filename = parse.unquote(result)  # 对文件名进行解码
                        if "." in filename:
                            filename = filename[: filename.rfind(".")]
                        airport_name = filename.replace("%20", " ").replace("%2B", "+")
                        return airport_name
                    return "呜呜,可莉没有看到普通文件名"
            return "呜呜,可莉没有看到内容描述"
        except:
            # return "v2b文件名获取错误"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) "
                "Chrome/108.0.0.0"
                "Safari/537.36"
            }
            try:
                pattern = r"(https?://)([^/]+)"
                match = re.search(pattern, url)
                base_url = None
                if match:
                    base_url = match.group(1) + match.group(2)
                response = requests.get(
                    url=base_url + "/auth/login", headers=headers, timeout=6
                )
                if response.status_code != 200:
                    response = requests.get(base_url, headers=headers, timeout=1)
                html = response.content
                soup = BeautifulSoup(html, "html.parser")
                title = soup.title.string
                title = str(title).replace("登录 — ", "")
                if "Attention Required! | Cloudflare" in title:
                    title = "该域名仅限国内IP访问"
                elif "Access denied" in title or "404 Not Found" in title:
                    title = "该域名非机场面板域名"
                elif "Just a moment" in title:
                    title = "该域名开启了5s盾"
                else:
                    pass
                return title
            except:
                return "机场名获取错误"


def get_filename_from_res(res, url):
    if "sub?target=" in url:
        pattern = r"url=([^&]*)"
        match = re.search(pattern, url)
        if match:
            encoded_url = match.group(1)
            decoded_url = unquote(encoded_url)
            return get_filename_from_url(decoded_url)
        return "错误 101 请将您的查询内容发送给管理员尝试解决"
    else:
        header = res.headers.get("Content-Disposition")
        if header:
            if "filename*=UTF-8''" in header:
                pattern = r"filename\*=UTF-8''(.+)"
                result = re.search(pattern, header)
                if result:
                    filename = result.group(1)
                    filename = parse.unquote(filename)  # 对文件名进行解码
                    airport_name = filename.replace("%20", " ").replace("%2B", "+")
                    return airport_name
                # return "呜呜,可莉没有看到U8文件名"
            if "filename=" in header:
                header = header.split(";")
                for i in header:
                    if "filename=" in i:
                        i1 = i.strip().split("=")
                        result = i1[1]
                if result:
                    filename = parse.unquote(result)  # 对文件名进行解码
                    if "." in filename:
                        filename = filename[: filename.rfind(".")]
                    airport_name = filename.replace("%20", " ").replace("%2B", "+")
                    return airport_name
                # return "呜呜,可莉没有看到普通文件名"
            return "呜呜,可莉没有看到文件名"
        return "呜呜,可莉没有看到内容描述"


def get_sub_name(res, url):
    airport_name = get_filename_from_res(res, url)
    if airport_name.startswith("呜呜"):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) "
                "Chrome/108.0.0.0"
                "Safari/537.36"
            }
            pattern = r"(https?://)([^/]+)"
            match = re.search(pattern, url)
            base_url = None
            if match:
                base_url = match.group(1) + match.group(2)
            response = requests.get(
                url=base_url + "/auth/login", headers=headers, timeout=6
            )
            if response.status_code != 200:
                response = requests.get(base_url, headers=headers, timeout=1)
            html = response.content
            soup = BeautifulSoup(html, "html.parser")
            title = soup.title.string
            title = str(title).replace("登录 — ", "")
            if "Attention Required! | Cloudflare" in title:
                title = "该域名仅限国内IP访问"
            elif "Access denied" in title or "404 Not Found" in title:
                title = "该域名非机场面板域名"
            elif "Just a moment" in title:
                title = "该域名开启了5s盾"
            else:
                pass
            return title
        except:
            return airport_name
    else:
        return airport_name


def convert_time_to_str(ts, a=2):
    return str(ts).zfill(a)


def sec_to_data(y):
    h = int(y // 3600 % 24)
    d = int(y // 86400)
    h = convert_time_to_str(h)
    d = convert_time_to_str(d)
    m = int(y % 86400 // 60 % 60)
    s = int(y % 86400 % 60)
    m = convert_time_to_str(m)
    s = convert_time_to_str(s)
    # ss = int(y * 1000 % 1000)
    # ss = convert_time_to_str(ss, 3)
    return d + "天" + h + "小时 " + m + "分" + s + "秒"  # + ss + "毫秒"


def StrOfSize(size):
    # size*=114514
    def strofsize(integer, remainder, level):
        if abs(integer) >= 1024:
            remainder = integer % 1024
            integer //= 1024
            level += 1
            return strofsize(integer, remainder, level)
        # elif integer < 0:
        #     integer = 0
        #     return strofsize(integer, remainder, level)
        else:
            return integer, remainder, level

    units = [" B", "KB", "MB", "GB", "TB", "PB"]
    # units = ["2B", "SB", "MB", "JB", "TB", "PB"]
    integer, remainder, level = strofsize(size, 0, 0)
    if level + 1 > len(units):
        level = -1
    return "{}.{:>03d} {}".format(integer, remainder, units[level]).rjust(11)


def cha_v2(text):
    # headers = {"User-Agent": "ClashforWindows/0.18.1"}
    headers = {"User-Agent": "Clashmeta"}
    output_text = None
    try:
        message_raw = text
        final_output = ""
        url_list = re.findall(
            r"https?://(?:[a-zA-Z]|\d|[$-_@.&+]|[!*,]|[\w\u4e00-\u9fa5])+", message_raw
        )  # 使用正则表达式查找订阅链接并创建列表
        for url in url_list:
            try:
                res = requests.get(
                    url, headers=headers, timeout=6
                )  # 设置5秒超时防止卡死
                while res.status_code == 301 or res.status_code == 302:
                    url1 = res.headers["location"]
                    res = requests.get(url1, headers=headers, timeout=5)
            except Exception as e:
                final_output = (
                    final_output
                    + f"啊哦,查询订阅失败了呢,可莉链接不到服务器呀\n"
                    + "\n\n"
                )
                continue
            if res.status_code == 200:
                try:
                    rawinfo = res.headers["subscription-userinfo"]
                    info = rawinfo.split(";")
                    info2 = {"upload": 0, "download": 0, "total": 0, "expire": 0}
                    for i in info:
                        try:
                            i1 = i.strip().split("=")
                            info2[i1[0]] = float(i1[1]) if i1[1] else 0
                        except IndexError:
                            pass
                    time_now = int(time.time())
                    output_text_head = (
                        "订阅链接:"
                        + url
                        + ""
                        + "\n机场名称："
                        + f"{get_sub_name(res,url)}"
                        + "\n订阅流量:"
                        + StrOfSize(int(info2["total"]))
                        + "\n已用上行:"
                        + StrOfSize(int(info2["upload"]))
                        + "\n已用下行:"
                        + StrOfSize(int(info2["download"]))
                        + "\n已用总量:"
                        + StrOfSize(int(info2["upload"]) + int(info2["download"]))
                        + "\n剩余流量:"
                        + StrOfSize(
                            int(info2["total"])
                            - int(info2["upload"])
                            - int(info2["download"])
                        )
                    )
                    if info2["expire"] != 0:
                        timeArray = time.localtime(int(info2["expire"]) + 28800)
                        dateTime = time.strftime("%y-%m-%d %H:%M:%S", timeArray)
                        if time_now <= int(info2["expire"]):
                            lasttime = int(info2["expire"]) - time_now
                            output_text = (
                                output_text_head
                                + "\n过期时间："
                                + dateTime
                                + ""
                                + "\n剩余时间："
                                + sec_to_data(lasttime)
                                + ""
                            )
                        elif time_now > int(info2["expire"]):
                            output_text = (
                                output_text_head
                                + "\n此订阅在"
                                + dateTime
                                + "就过期啦"
                            )
                        else:
                            output_text = output_text_head
                    else:
                        output_text = (
                            output_text_head
                            + "\n过期时间：可莉不知道哦\n剩余时间：可能是不限时吧"
                        )
                    output_text += f"\n调试信息:{rawinfo}"
                except:
                    output_text = (
                        f"订阅链接:{url}\n"
                        + f"机场名称：{get_sub_name(res,url)}\n"
                        + "流量信息：可莉不知道哦"
                    )
            else:
                output_text = f"啊哦,查询订阅出错了呢\n可莉发现状态码不是 200 而是 {res.status_code} 呢"
            final_output = final_output + output_text + "\n\n"
        return final_output
    except Exception as e:
        return f"啊哦,出现了可莉不知道的错误呢\n"


if __name__ == "__main__":
    output = ""
    with open("input.txt", "r", encoding="utf-8") as f:
        texts = f.readlines()
    for line in texts:
        if line:
            output += cha_v2(line)
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(output)

import requests


def sendMsg(title, desp):
    # url根据server酱生成的地址写
    url = 'http://sctapi.ftqq.com/.send'
    data = {
        'title': title,
        'desp': desp
    }
    res = requests.post(url=url, data=data)


if __name__ == '__main__':
    sendMsg("警告：有人跌倒了", "您家老人似乎跌倒了，请及时处理")

import ipywidgets as widgets
from ipywidgets import Layout,Label, HBox, VBox
import os

import Utils

def show(data,cmd_run):
    speed = widgets.Button(
        description='点我自动学术加速',
        disabled=False,
        button_style='info', # 'success', 'info', 'warning', 'danger' or '',
        layout=Layout(width='auto', height='auto'),
        icon='close'
    )
    if os.getenv("http_proxy") != None:
        speed.description = "目前你正处于之前的加速状态,但你依旧可以重新点击自动学术加速"

    def autospeed(self):
        if data["is_speed"] != True:
            speed.description = "正在自动学术加速"
            speed.button_style = "warning"
            speed.icon = "spinner"

            items = Utils.get_speed_ip()
            if items != '-1':
                os.environ['http_proxy'] = 'http://' + items[1] + ':12798'
                os.environ['https_proxy'] = 'http://' + items[1] + ':12798'
                print("加速成功!")
                data["is_speed"] = True

                speed.description = "加速成功,再次点击取消 当前:" + items[0]
                speed.button_style = "success"
                speed.icon = "check"
            else:
                print('加速失败!')

                speed.description = "加速失败,点击再次尝试"
                speed.button_style = "danger"
                speed.icon = "close"
        else:
            del(os.environ["http_proxy"])
            del(os.environ["https_proxy"])
            speed.description = "点我自动学术加速"
            speed.button_style = "info"
            speed.icon = "close"
            data["is_speed"] = False
        
    speed.on_click(autospeed)

    display(speed)
import ipywidgets as widgets
from ipywidgets import Layout,Label, HBox, VBox
import os

import Utils

def show(data,cmd_run):
    # 加速按钮
    speed = widgets.Button(
        description='点我自动学术加速',
        disabled=False,
        button_style='info', # 'success', 'info', 'warning', 'danger' or '',
        layout=Layout(width='auto', height='auto'),
        icon='close'
    )
    
    # 判断是否已经加速
    if Utils.get_is_speed():
        Utils.button_yes_end(speed,"你已处于加速状态,再次点击取消")
        data["is_speed"] = True

    # 自动加速
    def autospeed(self):
        if data["is_speed"] != True:
            Utils.button_start(speed,"正在自动学术加速")

            items = Utils.get_speed_ip()
            if items != '-1':
                os.environ['http_proxy'] = 'http://' + items[1] + ':12798'
                os.environ['https_proxy'] = 'http://' + items[1] + ':12798'
                data["is_speed"] = True
                Utils.button_yes_end(speed,"加速成功,再次点击取消 当前:" + items[0])
            else:
                Utils.button_no_end(speed,"加速失败,点击再次尝试")
        else:
            del(os.environ["http_proxy"])
            del(os.environ["https_proxy"])
            speed.description = "点我自动学术加速"
            speed.button_style = "info"
            speed.icon = "close"
            data["is_speed"] = False
        
    speed.on_click(autospeed)

    display(speed)
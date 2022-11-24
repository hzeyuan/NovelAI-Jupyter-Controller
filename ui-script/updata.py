import ipywidgets as widgets
from ipywidgets import Layout,Label, HBox, VBox
import os
import subprocess
import c_utils

def show(data,cmd_run):
    out = widgets.Output(layout={'border': '1px solid black'})

    # !cd /root/NovelAI-Jupyter-Controller && git fetch --all && git reset --hard origin && git pull
    
    updata_controller_buttom = widgets.Button(
            description='更新启动器(注意这是强制覆盖)',
            style={'description_width': 'initial'},
            layout=Layout(width='auto', height='auto'),
            button_style='primary'
    )
    
    updata_webui_buttom = widgets.Button(
            description='更新WebUi',
            button_style='success'
    )
    
    updata_db_buttom = widgets.Button(
        description='更新DreamBooth',
        button_style='success'
    )
    
    updata_chinese_buttom = widgets.Button(
        description='更新汉化插件',
        button_style='success'
    )

    #运行函数
    def run_click(index):
        out.clear_output()
        with out:
            temp = False
            sd_dir = c_utils.get_sd_dir()

            if sd_dir == "-1":
                print("无法找到程序目录")
            else:
                head = "echo 正在更新，请稍等... && "
                tail = " && echo 更新完成!"
                if index == 0:
                    data["cmd"] = head + "cd /root/NovelAI-Jupyter-Controller && git fetch --all && git reset --hard origin && git pull" + tail + " && echo 请重启所有内核并关闭所有窗口重新打开"
                    cmd_run()
                    
                if index == 1:
                    data["cmd"] = head + "cd " + sd_dir + " && git pull" + tail
                    cmd_run()

                if index == 2:
                    data["cmd"] = head + "cd " + sd_dir + "/extensions/sd_dreambooth_extension" + " && git pull" + tail
                    cmd_run()

                if index == 3:
                    data["cmd"] = head + "cd " + sd_dir + "/extensions/stable-diffusion-webui-localization-zh_CN" + " && git pull" + tail
                    cmd_run()
    
    def updata_controller_buttom_(self):
        run_click(0)   
    
    def updata_webui_buttom_(self):
        run_click(1)

    def updata_db_buttom_(self):
        run_click(2)
    
    def updata_chinese_buttom_(self):
        run_click(3)
    
    #绑定加速函数
    updata_controller_buttom.on_click(updata_controller_buttom_)
    updata_webui_buttom.on_click(updata_webui_buttom_)
    updata_db_buttom.on_click(updata_db_buttom_)
    updata_chinese_buttom.on_click(updata_chinese_buttom_)
    
    display(updata_controller_buttom,updata_webui_buttom,updata_db_buttom,updata_chinese_buttom)
    
    return out
        

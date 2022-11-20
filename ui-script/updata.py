import ipywidgets as widgets
from ipywidgets import Layout,Label, HBox, VBox
import os
import subprocess

def show(data,cmd_run):
    out = widgets.Output(layout={'border': '1px solid black'})

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
            sd_dir = ""
            
            if os.path.exists("/root/stable-diffusion-webui"):
                sd_dir = "/root/stable-diffusion-webui"
            elif os.path.exists("/root/autodl-tmp/stable-diffusion-webui"):
                sd_dir = "/root/autodl-tmp/stable-diffusion-webui"
            else:
                sd_dir = "-1"

            if sd_dir == "-1":
                print("无法找到程序目录")
            else:
                if index == 1:
                    data["cmd"] = "cd " + sd_dir + " && git pull"
                    cmd_run()

                if index == 2:
                    data["cmd"] = "cd " + sd_dir + "/extensions/sd_dreambooth_extension" + " && git pull"
                    cmd_run()

                if index == 3:
                    data["cmd"] = "cd " + sd_dir + "/extensions/stable-diffusion-webui-localization-zh_CN" + " && git pull"
                    cmd_run()
            
    def updata_webui_buttom_(self):
        run_click(1)

    def updata_db_buttom_(self):
        run_click(2)
    
    def updata_chinese_buttom_(self):
        run_click(3)
    
    #绑定加速函数
    updata_webui_buttom.on_click(updata_webui_buttom_)
    updata_db_buttom.on_click(updata_db_buttom_)
    updata_chinese_buttom.on_click(updata_chinese_buttom_)
    
    display(updata_webui_buttom,updata_db_buttom,updata_chinese_buttom)
    
    return out
        

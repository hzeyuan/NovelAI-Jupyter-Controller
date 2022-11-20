import ipywidgets as widgets
from ipywidgets import Layout,Label, HBox, VBox
import os
import subprocess

def show(data,cmd_run):
    out = widgets.Output(layout={'border': '1px solid black'})

    url = widgets.Textarea(
        value='',
        placeholder='请输入下载直链或种子地址',
        description='',
        disabled=False,
        layout=Layout(width='400px', height='80px')
    )
    
    download_buttom = widgets.Button(
        description='下载文件',
        button_style='success'
    )

    #运行函数
    def run_click(self):
        out.clear_output()
        with out:
            data["cmd"] = "cd /root/autodl-tmp/ && aria2c -x8 --seed-time=0 '" + url.value + "' && echo 下载完毕"
            cmd_run()

    
    #绑定加速函数
    download_buttom.on_click(run_click)
    
    display(url,download_buttom)
    
    return out
        

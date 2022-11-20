import ipywidgets as widgets
from ipywidgets import Layout,Label, HBox, VBox
import os
import subprocess
import c_utils

def show(data,cmd_):
    out = widgets.Output(layout={'border': '1px solid black'})

    url = widgets.Textarea(
        value='',
        placeholder='请输入下载直链或种子地址',
        description='',
        disabled=False,
        layout=Layout(width='400px', height='80px')
    )
    
    pos_list = widgets.Dropdown(
        options=[('embeddings目录(PT)', 1), ('hypernetworks目录(PT)', 2), ('大模型目录(CKPT)', 3), ('数据盘(autodl-tmp)', 4)],
        value=4,
        description='你需要安装到的位置:',
        style={'description_width': 'initial'},
        disabled=False,
    )
    
    download_buttom = widgets.Button(
        description='下载文件',
        button_style='success'
    )

    #运行函数
    def run_click(self):
        out.clear_output()
        with out:
            cmd_(c_utils.get_download_command(url.value,pos_list.value))

    
    #绑定加速函数
    download_buttom.on_click(run_click)
    
    display(url,pos_list,download_buttom)
    
    return out
        

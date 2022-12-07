import ipywidgets as widgets
from ipywidgets import Layout,Label, HBox, VBox
import os

import SpeedUi,ModUi,UpdataUi,StartUi,Tool,About

def show(data,cmd_run):
    tab_titles = ['下载器', '更新设置', '工具/帮助', '关于启动器','启动WebUi']
    
    children = [ModUi.getUi(data,cmd_run),UpdataUi.getUi(data,cmd_run),Tool.getUi(data,cmd_run),About.getUi(data,cmd_run),StartUi.getUi(data,cmd_run)]
    tab = widgets.Tab()
    tab.children = children
    
    for i in range(len(tab_titles)):
        tab.set_title(i, tab_titles[i])

    SpeedUi.show(data,cmd_run)
    display(tab)
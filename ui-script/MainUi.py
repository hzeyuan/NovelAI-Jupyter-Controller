import ipywidgets as widgets
from ipywidgets import Layout,Label, HBox, VBox
import os

import SpeedUi,ModUi,UpdataUi,StartUi

def show(data,cmd_run):
    tab_titles = ['下载器', '更新设置', '启动WebUi']
    
    children = [ModUi.getUi(data,cmd_run),UpdataUi.getUi(data,cmd_run),StartUi.getUi(data,cmd_run)]
    tab = widgets.Tab()
    tab.children = children
    
    for i in range(len(tab_titles)):
        tab.set_title(i, tab_titles[i])

    SpeedUi.show(data,cmd_run)
    display(tab)
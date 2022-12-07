import ipywidgets as widgets
from ipywidgets import Layout,Label, HBox, VBox
import os

import Utils

def getUi(data,cmd_run):
    out = widgets.Output(layout={'border': '1px solid black'})
    
    author_tip = widgets.HTML(
        value="<h3>启动器制作作者：小李xiaolxl</h3><h3><font color='#0fa3ff'><a target='_blank' href='https://space.bilibili.com/34590220/'>B站空间</a></font></h3>",
    )
    
    return VBox([author_tip])
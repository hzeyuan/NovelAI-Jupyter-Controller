import ipywidgets as widgets
from ipywidgets import Layout,Label, HBox, VBox
import os

import Utils

def getUi(data,cmd_run):
    out = widgets.Output(layout={'border': '1px solid black'})
    
    version_tip = widgets.HTML(
        value="<h3><font color='#A52A2A'>启动器版本：2.1.1</font></h3>",
    )
    line = widgets.HTML(
        value="<hr>",
    )
    author_tip = widgets.HTML(
        value="<h3>启动器作者：小李xiaolxl</h3><h3><font color='#0fa3ff'><a target='_blank' href='https://space.bilibili.com/34590220/'>作者B站空间</a></font></h3>",
    )
    
    return VBox([version_tip,line,author_tip])
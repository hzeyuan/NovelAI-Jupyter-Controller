import ipywidgets as widgets
from ipywidgets import Layout,Label, HBox, VBox
import os

import Utils

def getUi(data,cmd_run):
    out = widgets.Output(layout={'border': '1px solid black'})
    
    version_tip = widgets.HTML(
        value="<h3><font color='#A52A2A'>启动器版本：2.1.3</font></h3>",
    )
    
    line = widgets.HTML(
        value="<hr>",
    )
    
    author_tip = widgets.HTML(
        value="<h3>启动器作者：小李xiaolxl</h3><h3><font color='#0fa3ff'><a target='_blank' href='https://space.bilibili.com/34590220/'>作者B站空间</a></font></h3>",
    )

    p1_tip = widgets.HTML(
        value="整合版1.0镜像介绍页：<font color='#0fa3ff'><a target='_blank' href='https://www.codewithgpu.com/i/AUTOMATIC1111/stable-diffusion-webui/NovelAI-Consolidation-Package'>点我访问</a></font>",
    )
    
    p2_tip = widgets.HTML(
        value="整合版2.0镜像介绍页：<font color='#0fa3ff'><a target='_blank' href='https://www.codewithgpu.com/i/AUTOMATIC1111/stable-diffusion-webui/NovelAI-Consolidation-Package-2'>点我访问</a></font>",
    )
    
    github_tip = widgets.HTML(
        value="启动器GitHub地址：<font color='#0fa3ff'><a target='_blank' href='https://github.com/xiaolxl/NovelAI-Jupyter-Controller'>点我访问</a></font>",
    )
    
    return VBox([
        version_tip,
        line,
        author_tip,
        line,
        p1_tip,
        p2_tip,
        line,
        github_tip
    ])
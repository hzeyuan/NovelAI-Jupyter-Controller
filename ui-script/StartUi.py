import ipywidgets as widgets
from ipywidgets import Layout,Label, HBox, VBox
import os

import Utils

def getUi(data,cmd_run):
    out = widgets.Output(layout={'border': '1px solid black'})
    
    start_tip = widgets.HTML(
        value="<p>启动完毕后通过自定义服务打开网站</p><p><font color='#0fa3ff'><a href='https://www.autodl.com/console/instance/list'>点击此处打开服务器列表</a><font/></p><p></p>",
    )
    
    # ======================
    
    position_set = widgets.RadioButtons(
            options=['系统盘(root)', '数据盘(root/autodl-tmp)'],
            value='系统盘(root)', # Defaults to 'pineapple'
            style={'description_width': 'initial'},
            layout=Layout(width='100%', height='50px'),
            description='请选择你需要stable-diffusion-webui所运行的目录:',
            disabled=False
        )
    
    position_set_tip = widgets.HTML(
        value="<font size='2' color='red'>推荐在训练的时候选择数据盘，更节约空间。请勿频繁切换，切换至数据盘后尽量别再切换为系统盘，以免空间不足造成移动时失败!</font>",
    )

    info = widgets.Label('请选择需要开启的参数:')
    
    deepdanbooru = widgets.Checkbox(
        value=False,
        description='deepdanbooru(图片反推文本)',
        disabled=False,
        indent=False
    )
    
    xformers = widgets.Checkbox(
        value=False,
        description='xformers(极大改善内存消耗和速度)',
        disabled=False,
        layout=Layout(width='auto', height='auto'),
        indent=False
    )
    
    xformers_tip = widgets.HTML(
        value="<font size='2' color='red'>请勿在训练DreamBooth的时候打开它!</font>",
    )
    
    left_box = HBox([xformers, xformers_tip])

    run_buttom = widgets.Button(
            description='运行WebUi',
            button_style='success'
    )

    #运行函数
    def run_click(self):
        out.clear_output()
        with out:
            temp = False
            sd_dir = ""
            if position_set.value == "系统盘(root)":
                temp = os.path.exists("/root/stable-diffusion-webui")
                sd_dir = "/root/stable-diffusion-webui"
                if not temp:
                    if os.path.exists("/root/autodl-tmp/stable-diffusion-webui"):
                        print("程序目录不正确，正在自动调整...")
                        cmd_run("mv /root/autodl-tmp/stable-diffusion-webui /root/")
                        print("移动完成")
                    else:
                        print("没有找到stable-diffusion-webui程序!")
                        return 0
            else:
                temp = os.path.exists("/root/autodl-tmp/stable-diffusion-webui")
                sd_dir = "/root/autodl-tmp/stable-diffusion-webui"
                if not temp:
                    if os.path.exists("/root/stable-diffusion-webui"):
                        print("程序目录不正确，正在自动调整...")
                        cmd_run("mv /root/stable-diffusion-webui /root/autodl-tmp/")
                        print("移动完成")
                    else:
                        print("没有找到stable-diffusion-webui程序!")
                        return 0


            if data["is_speed"] == True:
                speed = "--share "
            else:
                speed = ""

            if deepdanbooru.value == True:
                deepd = "--deepdanbooru "
            else:
                deepd = ""

            if xformers.value == True:
                xf = "--xformers "
            else:
                xf = ""

            cmd_run("cd " + sd_dir + " && python launch.py --disable-safe-unpickle --port=6006 " + deepd + xf + speed)
        # os.system("cd /root/stable-diffusion-webui/ && python launch.py --disable-safe-unpickle --port=6006 " + deepd + speed)
    
    #绑定加速函数
    run_buttom.on_click(run_click)
    
    return VBox([start_tip,position_set_tip,position_set,info,deepdanbooru,left_box,run_buttom,out])
import ipywidgets as widgets
from ipywidgets import Layout,Label, HBox, VBox
import os
import sys
import time
import subprocess

import Utils,ThreadOut

def getUi(data,cmd_run):
    out = widgets.Output(layout={'border': '1px solid black'})
    
    start_tip = widgets.HTML(
        value="<p>启动完毕后通过自定义服务打开网站</p><p><font color='#0fa3ff'><a href='https://www.autodl.com/console/instance/list' target='_blank'>点击此处打开服务器列表</a><font/></p><p></p>",
    )
    
    # ======================
    
    auth_set_tip = widgets.HTML(
        value="<font size='2' color='red'>为了保证完全，下方设置的用户信息将会在启动share的时候自动设置</font>",
    )
    
    name_input = widgets.Text(
        value='',
        placeholder='留空则随机',
        description='用户名:',
        disabled=False
    )
    pass_input = widgets.Text(
        value='',
        placeholder='留空则随机',
        description='密码:',
        disabled=False
    )
    
    # ======================
    
    position_set_tip = widgets.HTML(
        value="<font size='2' color='red'>推荐在训练的时候选择数据盘，更节约空间。请勿频繁切换，切换至数据盘后尽量别再切换为系统盘，以免空间不足造成移动时失败!</font>",
    )
    
    position_set = widgets.RadioButtons(
            options=['系统盘(root)', '数据盘(root/autodl-tmp)'],
            value='数据盘(root/autodl-tmp)', # Defaults to 'pineapple'
            style={'description_width': 'initial'},
            layout=Layout(width='100%', height='50px'),
            description='请选择你需要stable-diffusion-webui所运行的目录:',
            disabled=False
        )
    
    # ======================
    
    run_stylet_tip = widgets.HTML(
        value="<font size='2' color='red'><p>注意：</p><p>后台版无法查看各类进度输出，导致你会怀疑程序卡住，同时会影响相关数据的查看 </p><p> 正常版运行后无法执行下载模型等操作，点击后不会有反应 </p><p> 自定义版运需要手动在控制台运行(包括学术加速)，但可以同时操作启动器的功能且关闭网页后再打开也能在控制台看到输出</p></font>",
    )
    
    run_style_set = widgets.RadioButtons(
            options=[('后台版(运行后你可以在其它窗口正常执行下载模型等功能)[时间长后会导致卡顿]',1), ('正常版(运行后你无法在其它窗口正常执行下载模型等功能)',2), ('自定义版(你需要复制下方的命令并在控制窗口手动运行)',3)],
            value=2, # Defaults to 'pineapple'
            style={'description_width': 'initial'},
            layout=Layout(width='100%', height='50px'),
            description='请选择stable-diffusion-webui的运行方式:',
            disabled=False
        )
    
    # ======================

    info = widgets.Label('请选择需要开启的参数:')
    
    deepdanbooru = widgets.Checkbox(
        value=False,
        description='deepdanbooru(图片反推文本)',
        disabled=False,
        indent=False
    )
    
    # -------
    
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
    
    xformers_box = HBox([xformers, xformers_tip])
    
    # -------
    
    disable_safe = widgets.Checkbox(
        value=True,
        description='disable-safe-unpickle(是否不启动安全检查)',
        disabled=False,
        indent=False
    )
    
    disable_tip = widgets.HTML(
        value="<font size='2' color='red'>取消勾选可能导致启动报错</font>",
    )
    
    disable_box = HBox([disable_safe, disable_tip])

    # -------
    
    insecure_extension_access = widgets.Checkbox(
        value=False,
        description='extension-access(启用不安全的扩展访问)',
        disabled=False,
        indent=False
    )
    
    insecure_extension_access_tip = widgets.HTML(
        value="<font size='2' color='blue'>勾选后将允许在webui扩展中安装任意扩展 </font><font size='2' color='red'>(注意安装后点重启并应用会报错，记得自行重启)</font>",
    )
    
    insecure_extension_access_box = HBox([insecure_extension_access, insecure_extension_access_tip])
    
    # -------
    
    picture_extension = widgets.Checkbox(
        value=False,
        description='Api+扩图允许(启用Api访问，并允许扩图访问)',
        disabled=False,
        indent=False
    )
    
    picture_extension_tip = widgets.HTML(
        value="<font size='2' color='blue'>勾选后将允许使用扩图功能 </font><font size='2' color='red'>(注意打开后请勿开启学术加速，不然不能访问) </font><font color='#0fa3ff'><a href='https://www.painthua.com/' target='_blank'>点我访问扩图网站</a><font/>",
    )
    
    picture_extension_box = HBox([picture_extension, picture_extension_tip])
    
    # -------
    
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
                name_ = name_input.value
                pass_ = pass_input.value
                if name_ == '':
                    name_ = Utils.generate_random_str()
                if pass_ == '':
                    pass_ = Utils.generate_random_str()
                
                
                speed = "--share --gradio-auth " + name_ + ":" + pass_ + " "
                name_input.value = name_
                pass_input.value = pass_
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
                
            if disable_safe.value == True:
                safe = "--disable-safe-unpickle "
            else:
                safe = ""
                
            if insecure_extension_access.value == True:
                extension = "--enable-insecure-extension-access "
            else:
                extension = ""
               
            if picture_extension.value == True:
                pic_ext = "--api --cors-allow-origins=https://www.painthua.com "
            else:
                pic_ext = ""
        
            python_local = sys.executable
            command_content = r"cd " + sd_dir + " && " + python_local + " launch.py " + safe + " --port=6006 " + deepd + xf + speed + extension + pic_ext
            if run_style_set.value == 1:
                ThreadOut.run_thread_out(r"cd " + sd_dir + " && " + python_local + " -u launch.py " + safe + " --port=6006 " + deepd + xf + speed + extension + pic_ext,out)
            elif run_style_set.value == 2:
                cmd_run(command_content)
            else:
                print("请复制下方命令到控制台中手动运行")
                print("")
                print(command_content)
                print("")
                if data["is_speed"] == True:
                    print("如果需要学术加速打开右侧网址，找到对应加速命令即可：https://www.autodl.com/docs/network_turbo/")
            
            # bash("cd " + sd_dir + " && python launch.py " + safe + " --port=6006 " + deepd + xf + speed)
            # bash("ping baidu.com")
            # temp = subprocess.Popen(r"cd " + sd_dir + " && python launch.py " + safe + " --port=6006 " + deepd + xf + speed,shell=True)
            # cmd_run("cd " + sd_dir + " && python launch.py " + safe + " --port=6006 " + deepd + xf + speed)
            
        # os.system("cd /root/stable-diffusion-webui/ && python launch.py --disable-safe-unpickle --port=6006 " + deepd + speed)
    
    #绑定加速函数
    run_buttom.on_click(run_click)
    
    return VBox([
        start_tip,
        auth_set_tip,name_input,pass_input,
        position_set_tip,position_set,
        run_stylet_tip,run_style_set,
        info,deepdanbooru,xformers_box,disable_box,insecure_extension_access_box,picture_extension_box,run_buttom,out
    ])
import ipywidgets as widgets
from ipywidgets import Layout,Label, HBox, VBox
import os
import subprocess

import Utils

chinese_name = {
    "stable-diffusion-webui-localization-zh_CN":"汉化插件",
    "sd_dreambooth_extension":"Dreambooth插件"
}

def getUi(data,cmd_run):
    out = widgets.Output(layout={'border': '1px solid black'})
    
    updata_tip = widgets.HTML(
        value="<p><font color='#e800e0'>除了启动器与汉化插件除外，其它的非必要不更新</font></p><p><font color='#e800e0'>更新前记得开学术加速</font></p>",
    )
    
    # ====================
    
    updata_controller_buttom = widgets.Button(
            description='更新启动器(注意这是强制覆盖)',
            style={'description_width': 'initial'},
            layout=Layout(width='300px', height='auto'),
            button_style='primary'
    )
    
    updata_webui_buttom = widgets.Button(
            description='更新WebUi',
            button_style='success'
    )
    
    updata_scan = widgets.Button(
            description='扫描可更新程序与插件(记得开学术加速)[绿色代表已最新，黄色代表可更新]',
            style={'description_width': 'initial'},
            layout=Layout(width='600px', height='auto'),
            button_style='info'
    )
    
    updata_line = widgets.HTML(
        value="<hr>",
    )
    
    # ====================

    #运行函数
    def run_click(index):
        out.clear_output()
        with out:
            temp = False
            sd_dir = Utils.get_sd_dir()

            if sd_dir == "-1":
                print("无法找到程序目录")
            else:
                head = "echo 正在更新，请稍等... && "
                tail = " && echo 更新完成!"
                if index == 0:
                    cmd_run(head + "cd /root/NovelAI-Jupyter-Controller && git fetch --all && git reset --hard origin && git pull" + tail + " && echo 请重启所有内核并关闭所有窗口重新打开")
                if index == 1:
                    cmd_run(head + "cd " + sd_dir + " && git pull" + tail)
    
    def updata_controller_buttom_(self):
        run_click(0)   
    
    def updata_webui_buttom_(self):
        run_click(1)
    
    #绑定加速函数
    updata_controller_buttom.on_click(updata_controller_buttom_)
    updata_webui_buttom.on_click(updata_webui_buttom_)

    # ====================

    # 获取插件目录
    def get_extension_dir():
        dir_ = Utils.get_sd_dir()
        if dir_ != "-1":
            return dir_ + "/extensions/"
        else:
            return dir_

    # 扫描插件目录，返回插件列表
    def scan_extension_dir(): 
        dir_ = get_extension_dir()
        
        extension_list = []
        if dir_ != "-1":
            files = os.listdir(dir_)

            for file_name in files:
                if file_name != '.ipynb_checkpoints':
                    d_path = os.path.join(dir_, file_name)
                    if os.path.isdir(d_path):
                        chinese_name_ = ""
                        if chinese_name.get(d_path[d_path.rfind('/')+1:]) != None:
                            chinese_name_ = chinese_name.get(d_path[d_path.rfind('/')+1:])
                        
                        item = {"name":d_path[d_path.rfind('/')+1:],"path":d_path,"chinese_name":chinese_name_}
                        extension_list.append(item)

        return extension_list

    # 判断插件是否需要更新，返回布尔值
    def is_need_update(extension): 
        if 'update' in subprocess.getstatusoutput('cd ' + extension + '&& git remote update && git status ')[1]: 
            return True 
        else: 
            return False
        
    def get_path_by_name(name):
        for item in extension_list:
            if item.get('name') == name or item.get('chinese_name') == name:
                return item.get('path')
        

    # 更新插件，返回布尔值，True表示更新成功，False表示更新失败
    def update_extension(extension,btn): 
        out.clear_output()
        with out:
            cmd_run("echo 正在更新，请稍等... && " + "cd " + get_path_by_name(extension) + " && git pull" + " && echo 更新完成!")
            btn.button_style='success'

    # 获取扫描到的所有插件列表    
    extension_list = scan_extension_dir() 
    def scan_run(self):
        self.description = "正在扫描...(如时间过长请检查学术加速是否打开)"
        self.button_style = "warning"
        button_list = [] # 创建一个空的button列表，用于存储按钮对象    
        for extension in extension_list: 
            # 判断当前插件是否需要更新    
            if is_need_update(extension['path']): 
                # 如果需要更新，则创建一个黄色的按钮    
                if extension.get('chinese_name') != "":
                    btn = widgets.Button(description = extension['chinese_name'], button_style='warning',layout=Layout(width='400px', height='auto')) 
                else:
                    btn = widgets.Button(description = extension['name'], button_style='warning',layout=Layout(width='400px', height='auto')) 

                # 给按钮绑定一个事件处理函数，当点击该按钮时，调用update_extension函数进行更新    
                btn.on_click(lambda btn: update_extension(btn.description))
                button_list.append(btn)# 将创建的按钮对象存储到button列表中  
            else: 
                # 否则创建一个绿色的按钮    
                if extension.get('chinese_name') != "":
                    btn = widgets.Button(description = extension['chinese_name'], button_style='success',layout=Layout(width='400px', height='auto'))
                else:
                    btn = widgets.Button(description = extension['name'], button_style='success',layout=Layout(width='400px', height='auto'))
                btn.on_click(lambda btn: update_extension(btn.description,btn))
                button_list.append(btn)# 将创建的按钮对象存储到button列表中  
        # 显示button列表中的所有按钮
        box_.children = [updata_tip,updata_controller_buttom,updata_webui_buttom,updata_scan,updata_line,VBox(button_list),out]
        self.description = "扫描可更新程序与插件(记得开学术加速)[绿色代表已最新，黄色代表可更新]"
        self.button_style = "info"
        
    updata_scan.on_click(scan_run)
        
    box_ = VBox([updata_tip,updata_controller_buttom,updata_webui_buttom,updata_scan,updata_line,out])
    return box_
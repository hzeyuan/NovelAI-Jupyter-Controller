import ipywidgets as widgets
from ipywidgets import Layout,Label, HBox, VBox,Button
import os
import subprocess

import Utils

chinese_name = {
    "stable-diffusion-webui-localization-zh_CN":"汉化插件",
    "sd_dreambooth_extension":"Dreambooth插件"
}

class Git_Item:
    def __init__(self,path,name,out):
        sd_dir = Utils.get_sd_dir()
        self.path2 = path
        self.path = sd_dir + path
        self.out = out
        
        self.refresh_button = Button(description = name + '(点我刷新)',layout=Layout(width='auto', height='auto'),button_style='info')
        self.refresh_button.on_click(self.refresh)
        
        self.now_time = Label(value="当前版本日期：请先刷新")
        self.newest_time = Label(value="最新版本日期：请先刷新")
        
        self.now_b_name = Label(value="当前版本分支：请先刷新")
        self.now_v_sha = Label(value="当前版本SHA：请先刷新")
        self.left_box = VBox([self.now_b_name, self.now_v_sha,self.now_time])

        self.bb = widgets.Dropdown(
            options=[('请先刷新', '请先刷新')],
            value='请先刷新',
            description='分支选择:',
        )
        self.sha = widgets.Text(
            value='',
            placeholder='不填默认更新为最新',
            description='自定义版本SHA值:',
            style={'description_width': 'initial'},
            layout=Layout(width='auto', height='auto'),
            disabled=False
        )
        self.right_box = VBox([self.bb, self.sha,self.newest_time])
        
        self.change_button = Button(description='设置插件版本',layout=Layout(width='150px', height='auto'),button_style='success')
        self.change_button.on_click(self.click)
        
        
        self.opengit_button = widgets.HTML(
            value="<a target='_blank' style='vertical-align: middle;padding:0 3px;background-color:#d7d7d7;word-wrap:break-word;display: table-cell; text-align:center; width:100px; height:95px; border:2px solid black' href=''>请先刷新</a>",
        )
        
        self.Box = HBox(children=[self.refresh_button,
                                  self.left_box,
                                  self.right_box,
                                  self.change_button,
                                  self.opengit_button
                                 ],
                        layout=Layout(border='solid 1px',width='100%'))
    def click(self,temp):
        self.update_dir()
        
        self.change_button.description = "正在更新..."
        self.change_button.button_style = "warning"
        
        self.out.clear_output()
        with self.out:
            Utils.change_b_and_v(self.path,self.bb.value,self.sha.value)
            self.refresh(self)
            print("更新成功！")
            self.change_button.description = "设置插件版本"
            self.change_button.button_style = "success"
        
    def get_box(self):
        return self.Box
    
    def refresh(self,temp):
        self.update_dir()
        
        old_des = self.refresh_button.description
        self.refresh_button.description = "正在检查..."
        self.refresh_button.button_style = "warning"
        
        self.out.clear_output()
        with self.out:
            b_now_name = Utils.get_nov_b_name(self.path)
            b_main_name = Utils.get_main_b_name(self.path)
            self.now_b_name.value = "当前版本分支：" + b_now_name
            self.now_v_sha.value = "当前版本SHA：" + Utils.get_now_v_sha(self.path)
            
            data = Utils.get_all_b_name(self.path)
            temp_arr = []
            for item in data:
                if b_main_name == item['branch_name']:
                    temp_arr.append((item['branch_name']+"(主分支)",item['branch_name']))
                else:
                    temp_arr.append((item['branch_name'],item['branch_name']))
            self.bb.options = temp_arr
            self.bb.value = b_now_name
            
            now_time = Utils.get_now_v_time(self.path)
            self.now_time.value = "当前版本日期：" + now_time
            newest_time = Utils.get_newest_v_time(self.path)
            self.newest_time.value = "最新版本日期："+ newest_time
            
            main_url = Utils.get_main_url(self.path)
            self.opengit_button.value = "<a target='_blank' style='vertical-align: middle;padding:0 3px;background-color:#d7d7d7;word-wrap:break-word;display: table-cell; text-align:center; width:100px; height:95px; border:2px solid black' href='" + main_url + "'>点我访问对应github官网</a>"
            
            self.refresh_button.description = old_des
            self.refresh_button.button_style = "info"
    
    def update_dir(self): # 更新sd目录，防止移动
        sd_dir = Utils.get_sd_dir()
        self.path = sd_dir + self.path2

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
    
    webui_Item = Git_Item('/','WebUi',out)
    
    # updata_webui_buttom = widgets.Button(
    #         description='更新WebUi(注意这是强制覆盖)',
    #         style={'description_width': 'initial'},
    #         layout=Layout(width='300px', height='auto'),
    #         button_style='success'
    # )
    
    updata_scan = widgets.Button(
            description='扫描可更新程序与插件(记得开学术加速)[设置版本前一定要先刷新！]',
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
                    cmd_run(head + "cd " + sd_dir + " && git fetch --all && git reset --hard origin && git pull" + tail)
    
    def updata_controller_buttom_(self):
        run_click(0)   
    
    # def updata_webui_buttom_(self):
    #     run_click(1)
    
    #绑定加速函数
    updata_controller_buttom.on_click(updata_controller_buttom_)
    # updata_webui_buttom.on_click(updata_webui_buttom_)

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
        extension_list = scan_extension_dir()
        button_list = [] # 创建一个空的button列表，用于存储按钮对象    
        for extension in extension_list: 
            
            if extension.get('chinese_name') != "":
                webui_Item_ = Git_Item('/extensions/' + extension['name'],extension['chinese_name'],out)
            else:
                webui_Item_ = Git_Item('/extensions/' + extension['name'],extension['name'],out)
            
            button_list.append(webui_Item_.get_box())# 将创建的按钮对象存储到button列表中  
            
#             # 判断当前插件是否需要更新  
#             if is_need_update(extension['path']): 
#                 # 如果需要更新，则创建一个黄色的按钮    
#                 if extension.get('chinese_name') != "":
#                     btn = widgets.Button(description = extension['chinese_name'], button_style='warning',layout=Layout(width='400px', height='auto')) 
#                 else:
#                     btn = widgets.Button(description = extension['name'], button_style='warning',layout=Layout(width='400px', height='auto')) 

#                 # 给按钮绑定一个事件处理函数，当点击该按钮时，调用update_extension函数进行更新    
#                 btn.on_click(lambda btn: update_extension(btn.description,btn))
#                 button_list.append(btn)# 将创建的按钮对象存储到button列表中
#             else: 
#                 # 否则创建一个绿色的按钮
#                 if extension.get('chinese_name') != "":
#                     btn = widgets.Button(description = extension['chinese_name'], button_style='success',layout=Layout(width='400px', height='auto'))
#                 else:
#                     btn = widgets.Button(description = extension['name'], button_style='success',layout=Layout(width='400px', height='auto'))
#                 btn.on_click(lambda btn: update_extension(btn.description,btn))
#                 button_list.append(btn)# 将创建的按钮对象存储到button列表中  
                
                
        # 显示button列表中的所有按钮
        box_.children = [updata_tip,updata_controller_buttom,webui_Item.get_box(),updata_scan,updata_line,VBox(button_list),out]
        self.description = "扫描可更新程序与插件(记得开学术加速)[设置版本前一定要先刷新！]"
        self.button_style = "info"
        
    updata_scan.on_click(scan_run)
    
    box_ = VBox([updata_tip,updata_controller_buttom,webui_Item.get_box(),updata_scan,updata_line,out])
    return box_
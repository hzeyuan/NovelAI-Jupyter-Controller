import ipywidgets as widgets
from ipywidgets import Layout,Label, HBox, VBox
import os

import Utils

def getUi(data,cmd_run):
    out = widgets.Output(layout={'border': '1px solid black'})
    
    line = widgets.HTML(
        value="<br>",
    )
    
    #===========
    
    tool_tip = widgets.HTML(
        value="<h1>官方常用帮助文档</h1><h3>1.<font color='#0fa3ff'><a target='_blank' href='https://www.autodl.com/docs/arc/'>压缩与解压</a></font></h3><h3>2.<font color='#0fa3ff'><a target='_blank' href='https://www.autodl.com/docs/netdisk/'>公网网盘上传下载</a></font></h3><h3>3.<font color='#0fa3ff'><a target='_blank' href='https://www.autodl.com/docs/migrate_instance/'>迁移实例</a></font></h3><h3>4.<font color='#0fa3ff'><a target='_blank' href='https://www.autodl.com/docs/ssh/'>SSH远程连接</a></font></h3><h3>5.<font color='#0fa3ff'><a target='_blank' href='https://www.autodl.com/docs/network_turbo/'>学术加速</a></font></h3>",
    )
    
    #===========
    
    extensions_tip = widgets.HTML(
        value="<h1>扩展安装工具</h1>",
    )
    
    extensions_input = widgets.Text(
        value='',
        placeholder='请输入扩展插件的git链接(例如：https://github.com/Akegarasu/sd-webui-model-converter.git)',
        style={'description_width': 'initial'},
        layout=Layout(width='1000px', height='auto'),
        description='扩展插件git链接(安装完毕后记得重启webui):',
        disabled=False
    )
    
    extensions_buttom = widgets.Button(
            description='点击安装',
            style={'description_width': 'initial'},
            layout=Layout(width='400px', height='auto'),
            button_style='success'
    )
    
    def extensions_buttom_click(self):
        out.clear_output()
        sd_dir = Utils.get_sd_dir()
        ext_dir = sd_dir + '/extensions'
        with out:
            cmd_run("echo 请稍等，正在安装! && cd " + ext_dir + " && git clone " + extensions_input.value + " && echo 插件已安装在" + ext_dir + " && echo 安装完成!")
    
    extensions_buttom.on_click(extensions_buttom_click)
    
    #===========
    
    del_tool_tip = widgets.HTML(
        value="<h1>文件删除工具</h1>",
    )
    
    file = open("/root/NovelAI-Jupyter-Controller/ui-script/删除.png", "rb")
    image = file.read()
    del_img = widgets.Image(
        value=image,
        format='png',
        width=300,
        height=300
    )
    
    del_input = widgets.Text(
        value='',
        placeholder='请直接粘贴，无需添加/root/',
        style={'description_width': 'initial'},
        layout=Layout(width='1000px', height='auto'),
        description='请输入复制好的文件路径(请直接粘贴，无需添加/root/):',
        disabled=False
    )
    
    del_buttom = widgets.Button(
            description='点击删除',
            style={'description_width': 'initial'},
            layout=Layout(width='400px', height='auto'),
            button_style='success'
    )
    
    clear_buttom = widgets.Button(
            description='点击清空路径',
            style={'description_width': 'initial'},
            layout=Layout(width='150px', height='auto'),
            button_style='danger'
    )
    
    def del_buttom_click(self):
        out.clear_output()
        with out:
            cmd_run("echo 请稍等，正在删除! && rm -rf /root/" + del_input.value + " && echo 删除完成!")
    
    def clear_buttom_click(self):
        del_input.value = ""
    
    del_buttom.on_click(del_buttom_click)
    clear_buttom.on_click(clear_buttom_click)
    
    del_tool_box = VBox([
        del_tool_tip,
        del_img,
        del_input,
        HBox([del_buttom,clear_buttom])
    ])
    
    #===========
    
    other_tool_tip = widgets.HTML(
        value="<h1>其它工具</h1>",
    )
    
    clear_buttom = widgets.Button(
            description='清理系统盘',
            style={'description_width': 'initial'},
            layout=Layout(width='300px', height='auto'),
            button_style='primary'
    )
    
    del_xformers_buttom = widgets.Button(
            description='删除xformers(非xformers报错请勿执行它!)',
            layout=Layout(width='300px', height='auto'),
            button_style='danger'
    )

    def clear_buttom_click(self):
        out.clear_output()
        with out:
            cmd_run("du -sh /root/miniconda3/pkgs/ && rm -rf /root/miniconda3/pkgs/*")
            cmd_run("du -sh /root/.local/share/Trash && rm -rf /root/.local/share/Trash")
            cmd_run("rm -rf ~/.cache/pip")
            cmd_run("echo 清理完成!")

    def del_xformers_buttom_click(self):
        out.clear_output()
        with out:
            cmd_run("rm -rf /root/xformers")
            cmd_run("echo 删除完成!")
    
    #绑定加速函数
    clear_buttom.on_click(clear_buttom_click)
    del_xformers_buttom.on_click(del_xformers_buttom_click)
    
    #===========
    
    return VBox([
        tool_tip,
        line,
        extensions_tip,extensions_input,extensions_buttom,
        line,
        del_tool_box,
        line,
        other_tool_tip,clear_buttom,del_xformers_buttom,
        out
    ])
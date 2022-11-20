import ipywidgets as widgets
from ipywidgets import Layout
import os

def show(data):
    out = widgets.Output(layout={'border': '1px solid black'})

    implement = widgets.Dropdown(
        options=[('芜湖区', 'http://192.168.0.91:12798'),
                 ('北京A区', 'http://100.72.64.19:12798'),
                 ('内蒙A区', 'http://192.168.1.174:12798'),
                 ('泉州A区', 'http://10.55.146.88:12798'),
                 ('南京新手区', 'http://172.181.217.43:12798'),
                 ('佛山区', 'http://192.168.126.12:12798')
                ],
        value='http://192.168.1.174:12798',
        style={'description_width': 'initial'},
        layout=Layout(width='100%', height='50px'),
        description='选择服务器所在区域:',
    )

    implement_buttom = widgets.Button(
            description='运行加速',
            button_style='success'
    )
    
    clear_implement_buttom = widgets.Button(
            description='清除加速',
            button_style='danger'
    )

    #加速函数
    def speed_click(self):
        out.clear_output()
        with out:
            os.environ['http_proxy']=implement.value
            os.environ['https_proxy']=implement.value
            print("加速成功！")
            data["is_speed"] = True
    
    #清除加速函数
    def clear_speed_click(self):
        out.clear_output()
        with out:
            os.unsetenv('http_proxy')
            os.unsetenv('https_proxy')
            print("已清除加速！")
            data["is_speed"] = False

    #绑定加速函数
    implement_buttom.on_click(speed_click)
    #绑定清除加速函数
    clear_implement_buttom.on_click(clear_speed_click)
    
    display(implement,implement_buttom,clear_implement_buttom)
    
    return out
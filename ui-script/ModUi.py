import ipywidgets as widgets
from ipywidgets import Layout,Label,HBox,VBox,GridBox
import os

import Utils

mod_list = [
{
    "name":"Stable Diffusion v1.5 (慢)",
    "url":["magnet:?xt=urn:btih:2daef5b5f63a16a9af9169a529b1a773fc452637&dn=v1-5-pruned-emaonly.ckpt&tr=udp%3a%2f%2ftracker.opentrackr.org%3a1337%2fannounce&tr=udp%3a%2f%2f9.rarbg.com%3a2810%2fannounce&tr=udp%3a%2f%2ftracker.openbittorrent.com%3a6969%2fannounce&tr=udp%3a%2f%2fopentracker.i2p.rocks%3a6969%2fannounce&tr=https%3a%2f%2fopentracker.i2p.rocks%3a443%2fannounce&tr=http%3a%2f%2ftracker.openbittorrent.com%3a80%2fannounce&tr=udp%3a%2f%2ftracker.torrent.eu.org%3a451%2fannounce&tr=udp%3a%2f%2fopen.stealth.si%3a80%2fannounce&tr=udp%3a%2f%2fvibe.sleepyinternetfun.xyz%3a1738%2fannounce&tr=udp%3a%2f%2ftracker2.dler.org%3a80%2fannounce&tr=udp%3a%2f%2ftracker1.bt.moack.co.kr%3a80%2fannounce&tr=udp%3a%2f%2ftracker.zemoj.com%3a6969%2fannounce&tr=udp%3a%2f%2ftracker.tiny-vps.com%3a6969%2fannounce&tr=udp%3a%2f%2ftracker.theoks.net%3a6969%2fannounce&tr=udp%3a%2f%2ftracker.publictracker.xyz%3a6969%2fannounce&tr=udp%3a%2f%2ftracker.monitorit4.me%3a6969%2fannounce&tr=udp%3a%2f%2ftracker.moeking.me%3a6969%2fannounce&tr=udp%3a%2f%2ftracker.lelux.fi%3a6969%2fannounce&tr=udp%3a%2f%2ftracker.dler.org%3a6969%2fannounce&tr=udp%3a%2f%2ftracker.army%3a6969%2fannounce"],
    "pos":3,
    "hash":'81761151'
},
{
    "name":"Anything v3.0 (极速)",
    "url":['https://huggingface.co/xiaolxl/Stable-diffusion-models/resolve/main/Anything-V3.0.ckpt',
           'https://huggingface.co/xiaolxl/Stable-diffusion-models/resolve/main/Anything-V3.0.vae.pt'],
    "pos":3,
    "hash":'1a7df6b8'
},
{
    "name":"momoko_e (极速)",
    "url":['https://huggingface.co/xiaolxl/Stable-diffusion-models/resolve/main/momoko-e.ckpt'],
    "pos":3,
    "hash":'a2a802b2'
},
{
    "name":"NovelAI-7G (极速)",
    "url":['https://huggingface.co/xiaolxl/Stable-diffusion-models/resolve/main/NovelAI-7G.ckpt'],
    "pos":3,
    "hash":'e6e8e1fc'
},
{
    "name":"MakotoNiitsu-1.1-xhc [新海诚画风] (极速)",
    "url":['https://huggingface.co/xiaolxl/Stable-diffusion-models/resolve/main/xhc.ckpt'],
    "pos":3,
    "hash":'33044c56'
},
{
    "name":"768-v-ema [SD2.0] [记得更新webui到最新版本在安装！！！] (极速)",
    "url":['https://huggingface.co/stabilityai/stable-diffusion-2/resolve/main/768-v-ema.ckpt',
          'https://huggingface.co/xiaolxl/Stable-diffusion-models/resolve/main/768-v-ema.yaml'],
    "pos":3,
    "hash":'2c02b20a'
},
{
    "name":"moDi-v1-pruned [迪士尼画风] 关键词:[modern disney style] (极速)",
    "url":['https://huggingface.co/nitrosocke/mo-di-diffusion/resolve/main/moDi-v1-pruned.ckpt'],
    "pos":3,
    "hash":'ccf3615f'
},
{
    "name":"redshift-diffusion-v1 [3D现实风格] 关键词:[redshift style] (极速)",
    "url":['https://huggingface.co/nitrosocke/redshift-diffusion/resolve/main/redshift-diffusion-v1.ckpt'],
    "pos":3,
    "hash":'74f4c61c'
}
]

def getUi(data,cmd_run):
    out = widgets.Output(layout={'border': '1px solid black'})
    
    mod_tip = widgets.HTML(
        value="<font size='2' color='red'>下载前记得安装下载器，安装前记得开启学术加速</font>",
    )
    
    install_download = None
    with out:
        if Utils.get_have_aria2() == False:
            install_download = widgets.Button(
                description='点我安装下载器',
                disabled=False,
                button_style='info', # 'success', 'info', 'warning', 'danger' or '',
                layout=Layout(width='auto', height='auto'),
                icon='download'
            )
        else:
            install_download = widgets.Button(
                description='已成功安装下载器',
                disabled=False,
                button_style='success', # 'success', 'info', 'warning', 'danger' or '',
                layout=Layout(width='auto', height='auto'),
                icon='check'
            )
    out.clear_output()

    def download(self):
        if Utils.get_have_aria2() == False:
            with out:
                cmd_run("cd /root/autodl-tmp/ && apt-get update && apt-get install aria2 -y && echo 安装完成")
                install_download.description='已成功安装下载器'
                install_download.button_style='success'
                install_download.icon='check'
            out.clear_output()
        
    install_download.on_click(download)
    
    # ====================
    
    url = widgets.Textarea(
        value='',
        placeholder='请输入下载直链或种子地址',
        description='',
        disabled=False,
        layout=Layout(width='400px', height='80px')
    )
    
    pos_list = widgets.Dropdown(
        options=[('embeddings目录(PT)', 1), ('hypernetworks目录(PT)', 2), ('大模型目录(CKPT)', 3), ('数据盘(autodl-tmp)', 4)],
        value=4,
        description='你需要安装到的位置:',
        style={'description_width': 'initial'},
        disabled=False,
    )
    
    download_buttom = widgets.Button(
        description='下载文件',
        button_style='success'
    )
    
    def run_click(self):
        out.clear_output()
        with out:
            cmd_run(Utils.get_download_command(url.value,pos_list.value))
    
    download_buttom.on_click(run_click)
    
    my_url = VBox([url,pos_list,download_buttom])
    
    # ====================
    
    items = []
    
    class ClickItem:
        def __init__(self, index):
            self.index = index
        def click(self,temp):
            out.clear_output()
            temp.description='正在安装...'
            temp.disabled=True
            temp.button_style='warning'
            with out:
                if len(mod_list[self.index]["url"]) == 1:
                    cmd_run(Utils.get_download_command(mod_list[self.index]["url"][0],mod_list[self.index]["pos"]))
                if len(mod_list[self.index]["url"]) > 1:
                    print("当前需要下载" + str(len(mod_list[self.index]["url"])) + "个文件，请稍等")
                    for j in range(len(mod_list[self.index]["url"])):
                        print("正在下载第" + str(j+1) + "个文件")
                        cmd_run(Utils.get_download_command(mod_list[self.index]["url"][j],mod_list[self.index]["pos"]))
                        print("第" + str(j+1) + "个文件下载完毕")
                    print("全部文件下载完毕!")
                temp.description='已安装'
                temp.disabled=True
                temp.button_style='success'
    
    class HashItem:
        def __init__(self):
            self.hash_item_list = [[],[],[]]
            self.hash_item_list[0] = Utils.scan_dir_hash(1)
            self.hash_item_list[1] = Utils.scan_dir_hash(2)
            self.hash_item_list[2] = Utils.scan_dir_hash(3)
        def find(self,style,hash_):
            if hash_ in self.hash_item_list[style-1]:
                return True
            else:
                return False
    hashItem = HashItem()
    
    for i in range(len(mod_list)):
        file_temp = widgets.HTML(
            value="下载 " + mod_list[i]["name"],
        )

        if hashItem.find(mod_list[i]["pos"],mod_list[i]["hash"]):
            file_temp_download_buttom = widgets.Button(
                description='已安装',
                disabled=False,
                button_style='success'
            )
        else:
            file_temp_download_buttom = widgets.Button(
                description='点击下载',
                button_style=''
            )
        
        clickItem = ClickItem(i)
        
        file_temp_download_buttom.on_click(clickItem.click)

        temp_box = HBox([file_temp, file_temp_download_buttom])
        items.append(temp_box)
        
    xformers_tip = widgets.HTML(
        value="<font size='2' color='red'>TIP:如果极速版下载慢，请打开学术加速</font>",
    )
        
    grid = GridBox(children=items,
        layout=Layout(
            width='100%',
            grid_template_columns='auto auto',
            grid_template_rows='auto auto',
            grid_gap='5px 10px')
       )
    
    other_url = VBox([xformers_tip,grid])
    
    # ====================
    
    accordion = widgets.Accordion(children=[my_url, other_url])
    accordion.set_title(0, '自定义链接下载')
    accordion.set_title(1, '内置模型下载')
    accordion.selected_index = None

    line1 = HBox([install_download])
    box = VBox([mod_tip,line1,accordion,out])

    return box
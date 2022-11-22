import ipywidgets as widgets
from ipywidgets import Layout,Label, HBox, VBox, GridBox
import os
import subprocess
import c_utils

mod_list = [
{
    "name":"Stable Diffusion v1.5 (慢)",
    "url":["magnet:?xt=urn:btih:2daef5b5f63a16a9af9169a529b1a773fc452637&dn=v1-5-pruned-emaonly.ckpt&tr=udp%3a%2f%2ftracker.opentrackr.org%3a1337%2fannounce&tr=udp%3a%2f%2f9.rarbg.com%3a2810%2fannounce&tr=udp%3a%2f%2ftracker.openbittorrent.com%3a6969%2fannounce&tr=udp%3a%2f%2fopentracker.i2p.rocks%3a6969%2fannounce&tr=https%3a%2f%2fopentracker.i2p.rocks%3a443%2fannounce&tr=http%3a%2f%2ftracker.openbittorrent.com%3a80%2fannounce&tr=udp%3a%2f%2ftracker.torrent.eu.org%3a451%2fannounce&tr=udp%3a%2f%2fopen.stealth.si%3a80%2fannounce&tr=udp%3a%2f%2fvibe.sleepyinternetfun.xyz%3a1738%2fannounce&tr=udp%3a%2f%2ftracker2.dler.org%3a80%2fannounce&tr=udp%3a%2f%2ftracker1.bt.moack.co.kr%3a80%2fannounce&tr=udp%3a%2f%2ftracker.zemoj.com%3a6969%2fannounce&tr=udp%3a%2f%2ftracker.tiny-vps.com%3a6969%2fannounce&tr=udp%3a%2f%2ftracker.theoks.net%3a6969%2fannounce&tr=udp%3a%2f%2ftracker.publictracker.xyz%3a6969%2fannounce&tr=udp%3a%2f%2ftracker.monitorit4.me%3a6969%2fannounce&tr=udp%3a%2f%2ftracker.moeking.me%3a6969%2fannounce&tr=udp%3a%2f%2ftracker.lelux.fi%3a6969%2fannounce&tr=udp%3a%2f%2ftracker.dler.org%3a6969%2fannounce&tr=udp%3a%2f%2ftracker.army%3a6969%2fannounce"],
    "pos":3
},
{
    "name":"Anything v3.0 (快)",
    "url":['https://cloud.whksoft.cn/api/v3/file/source/120/Anything-V3.0.ckpt?sign=wu_o0XNztESh29f0sjkaBvND7X5RoMDdtnH_s4AK5B4%3D%3A0',
           'https://cloud.whksoft.cn/api/v3/file/source/121/Anything-V3.0.vae.pt?sign=xXKmtZK9s3z5fPL2HmDsa012Ldda5Rq1K6DrA2HY_gM%3D%3A0'],
    "pos":3
},
{
    "name":"Anything v3.0 (极速)",
    "url":['https://huggingface.co/xiaolxl/Stable-diffusion-models/resolve/main/Anything-V3.0.ckpt',
           'https://huggingface.co/xiaolxl/Stable-diffusion-models/resolve/main/Anything-V3.0.vae.pt'],
    "pos":3
},
{
    "name":"momoko_e (极速)",
    "url":['https://huggingface.co/xiaolxl/Stable-diffusion-models/resolve/main/momoko-e.ckpt'],
    "pos":3
},
{
    "name":"NovelAI-7G (极速)",
    "url":['https://huggingface.co/xiaolxl/Stable-diffusion-models/resolve/main/NovelAI-7G.ckpt'],
    "pos":3
}
]

def show(cmd_):
    out = widgets.Output(layout={'border': '1px solid black'})
    
    items = []
    
    class ClickItem:
        def __init__(self, index):
            self.index = index
        def click(self,temp):
            out.clear_output()
            with out:
                if len(mod_list[self.index]["url"]) == 1:
                    cmd_(c_utils.get_download_command(mod_list[self.index]["url"][0],mod_list[self.index]["pos"]))
                if len(mod_list[self.index]["url"]) > 1:
                    print("当前需要下载" + str(len(mod_list[self.index]["url"])) + "个文件，请稍等")
                    for j in range(len(mod_list[self.index]["url"])):
                        print("正在下载第" + str(j+1) + "个文件")
                        cmd_(c_utils.get_download_command(mod_list[self.index]["url"][j],mod_list[self.index]["pos"]))
                        print("第" + str(j+1) + "个文件下载完毕")
                    print("全部文件下载完毕!")
    
    for i in range(len(mod_list)):
        file_temp = widgets.HTML(
            value="下载 " + mod_list[i]["name"],
        )

        file_temp_download_buttom = widgets.Button(
            description='点击下载',
            button_style='success'
        )
        
        clickItem = ClickItem(i)
        
        file_temp_download_buttom.on_click(clickItem.click)

        temp_box = HBox([file_temp, file_temp_download_buttom])
        items.append(temp_box)
        
    grid = GridBox(children=items,
        layout=Layout(
            width='100%',
            grid_template_columns='auto auto auto',
            grid_template_rows='auto auto auto',
            grid_gap='5px 10px')
       )
    
    display(grid)
    
    return out
        

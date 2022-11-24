import os

embeddings_dir_1 = "/embeddings"
hypernetworks_dir_2 = "/models/hypernetworks"
ckpt_dir_3 = "/models/Stable-diffusion"

def get_sd_dir():
    if os.path.exists("/root/stable-diffusion-webui"):
        return "/root/stable-diffusion-webui"
    elif os.path.exists("/root/autodl-tmp/stable-diffusion-webui"):
        return "/root/autodl-tmp/stable-diffusion-webui"
    else:
        return "-1"
    
def get_download_dir(style):
    sd_dir = get_sd_dir()
    mv_dir = "-1"
    if sd_dir != "-1":
        if style == 1:
            mv_dir = sd_dir + embeddings_dir_1
        if style == 2:
            mv_dir = sd_dir + hypernetworks_dir_2
        if style == 3:
            mv_dir = sd_dir + ckpt_dir_3
        if style == 4:
            mv_dir = "/root/autodl-tmp/"
        return mv_dir
    else:
        return "-1"
        
def get_download_command(url,style):
    download_dir = get_download_dir(style)
    if download_dir != "-1":
        command = "cd " + download_dir + " && aria2c -s 16 -x 8 --seed-time=0 '" + url + "' && echo 下载完毕!文件已保存到" + download_dir
        return command
    else:
        return "echo 未找到目录!无法下载!"
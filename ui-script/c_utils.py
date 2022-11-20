import os

def get_sd_dir():
    if os.path.exists("/root/stable-diffusion-webui"):
        return "/root/stable-diffusion-webui"
    elif os.path.exists("/root/autodl-tmp/stable-diffusion-webui"):
        return "/root/autodl-tmp/stable-diffusion-webui"
    else:
        return "-1"
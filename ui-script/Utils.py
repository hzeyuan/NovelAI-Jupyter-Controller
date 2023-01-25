import os
import random
import hashlib
import subprocess
import time

# ======================= 学术加速 =======================

ip_list = {
    '芜湖区':'192.168.0.91',
    '北京A区':'100.72.64.19',
    '内蒙A区':'192.168.1.174',
    '泉州A区':'10.55.146.88',
    '南京新手区':'172.181.217.43',
    '佛山区':'192.168.126.12',
    '北京C区':'172.31.1.127',
    '宿迁区':'10.0.0.7',
    '内蒙B区':'192.168.1.174',
}

# 获取加速IP
def get_speed_ip():
    for item in ip_list:
        if(os.system(f'ping -c 1 -w 1 {ip_list[item]}') == 0):
            return [item,ip_list[item]]
    return '-1'

# 判断是否已加速
def get_is_speed():
    return os.getenv("http_proxy") != None

# ======================= 下载 =======================

# 判断是否已安装下载器
def get_have_aria2():
    return os.system(f'aria2c -v') == 0

embeddings_dir_1 = "/embeddings"
hypernetworks_dir_2 = "/models/hypernetworks"
ckpt_dir_3 = "/models/Stable-diffusion"

# 获取SD目录
def get_sd_dir():
    if os.path.exists("/root/stable-diffusion-webui"):
        return "/root/stable-diffusion-webui"
    elif os.path.exists("/root/autodl-tmp/stable-diffusion-webui"):
        return "/root/autodl-tmp/stable-diffusion-webui"
    else:
        return "-1"

# 获取不用类型文件在SD目录的相对位置
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

# 获取文件下载命令(路径根据类型)
def get_download_command(url,style,file_name):
    download_dir = get_download_dir(style)
    if download_dir != "-1":
        command = "cd " + download_dir + " && aria2c -s 16 -x 8 --seed-time=0 '" + url + "' -o " + file_name + " && echo 下载完毕!文件已保存到" + download_dir
        return command
    else:
        return "echo 未找到目录!无法下载!"

# 获取文件下载命令(路径自定义)
def get_download_command_custom(url,file_path,file_name):
    command = "cd /root/" + file_path + " && aria2c -s 16 -x 8 --seed-time=0 '" + url + "' -o " + file_name + " && echo 下载完毕!文件已保存到" + "/root/" + file_path
    return command

def generate_random_str(randomlength = 8):
    random_str = ''
    base_str ='ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) -1
    for i in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str

def model_hash(filename):
    try:
        with open(filename, "rb") as file:
            import hashlib
            m = hashlib.sha256()

            file.seek(0x100000)
            m.update(file.read(0x10000))
            return m.hexdigest()[0:8]
    except FileNotFoundError:
        return 'NOFILE'
    
def get_style_mod_dir(style):
    sd_dir = get_sd_dir()
    mv_dir = "-1"
    
    if style == 1:
        mv_dir = sd_dir + embeddings_dir_1
    if style == 2:
        mv_dir = sd_dir + hypernetworks_dir_2
    if style == 3:
        mv_dir = sd_dir + ckpt_dir_3
    
    return mv_dir
    
def scan_dir_hash(style):
    mod_dir = get_style_mod_dir(style)
    hash_list = []
    if os.path.exists(mod_dir) == False:
        os.makedirs(mod_dir)
    for file_name in os.listdir(mod_dir):
        file_dir = mod_dir + "/" + file_name
        if os.path.isfile(file_dir):
            hash_list.append(model_hash(file_dir))
    return hash_list

# ======================= 系统 =======================

# 抛出错误
def exp(error):
    raise ValueError(error)

# ======================= UI =======================

def button_start(btn,tip):
    btn.description = tip
    btn.button_style = "warning"
    btn.icon = "spinner"

def button_yes_end(btn,tip):
    btn.description = tip
    btn.button_style = "success"
    btn.icon = "check"
    
def button_no_end(btn,tip):
    btn.description = tip
    btn.button_style = "danger"
    btn.icon = "close"

# ======================= git =======================

# 获取默认分支名字
def get_main_b_name(path):
    output = subprocess.check_output(
        ['git', 'ls-remote', '--symref', 'origin', 'HEAD'],
        cwd=path
    ).strip().decode('utf-8')

    # Get the branch name from the output
    return  output.split('/')[-1].split('\t')[0]

# 获取全部分支名字
def get_all_b_name(path):
    data = []
    output = subprocess.check_output(
        ['git', 'ls-remote', '--heads', 'origin'],
        cwd=path
    ).strip().decode('utf-8')

    main_b_name = get_main_b_name(path)
    
    for line in output.split('\n'):
        branch_name = line.split('/')[-1]
        
        if main_b_name == branch_name:
            item = {'branch_name':branch_name,'is_main':1}
        else:
            item = {'branch_name':branch_name,'is_main':0}
        
        data.append(item)
    
    return data

# 获取当前分支名字
def get_nov_b_name(path):
    return subprocess.check_output(
        ['git', 'rev-parse', '--abbrev-ref', 'HEAD@{upstream}'],
        cwd=path
    ).strip().decode('utf-8').split('/')[1]

# 获取当前分支SHA
def get_now_v_sha(path):
    output = subprocess.check_output(
        ['git', 'rev-parse', 'HEAD'],
        cwd=path
    ).strip()

    # Convert the output to a string
    output = output.decode('utf-8')

    # Remove the extra content
    full_sha = output.split('/')[0]
    
    return full_sha

# 切换分支与版本
def change_b_and_v(path,branch_name,full_sha):
    git_path = path

    if full_sha != "":
        # Fetch latest remote changes
        subprocess.run(
            ['git', 'fetch', '--all'],
            cwd=git_path
        )

        # Checkout the specified branch
        # subprocess.run(
        #     ['git', 'checkout','-b', branch_name],
        #     cwd=git_path
        # )

        # Update Branch
        subprocess.run(
            ['git', 'pull'],
            cwd=git_path
        )

        # Reset to the specified version
        subprocess.run(
            ['git', 'reset', '--hard', full_sha],
            cwd=git_path
        )
        
        # Update Branch
        # subprocess.run(
        #     ['git', 'pull'],
        #     cwd=git_path
        # )
    else:
        # Fetch latest remote changes
        subprocess.run(
            ['git', 'fetch', '--all'],
            cwd=git_path
        )
        
        # Checkout the specified branch
        subprocess.run(
            ['git', 'branch','--set-upstream-to=origin/' + branch_name, 'HEAD'],
            cwd=git_path
        )
        
        subprocess.run(
            ['git', 'reset', '--hard', 'origin/' + branch_name],
            cwd=git_path
        )
        subprocess.run(
            ['git', 'pull'],
            cwd=git_path
        )
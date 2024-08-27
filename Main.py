import subprocess
import re
import os
import shutil
import hashlib
from datetime import datetime

def clear_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
        print(f"已清空旧预下载音乐文件: {directory}")
    os.makedirs(directory)
    print(f"已创建新空目录: {directory}")

def check_and_prompt_for_new_game_files():
    new_game_files_path = os.path.join(os.getcwd(), 'New Game Files')
    music_file_path = os.path.join(new_game_files_path, 'Music0.pck')

    if not os.listdir(new_game_files_path):
        print(f"{new_game_files_path} 没有东西")
        return

    if os.path.exists(music_file_path):
        modification_time = os.path.getmtime(music_file_path)
        mod_time_str = datetime.fromtimestamp(modification_time).strftime('%Y-%m-%d %H:%M:%S')
        print(f"文件 Music0.pck 上次修改时间为: {mod_time_str}")
        
        user_input = input("是否删除旧的预下载文件？(y/n): ").lower()
        if user_input == 'y':
            clear_directory(new_game_files_path)
            print("旧预下载文件已删除。")
        else:
            print("保留旧的预下载文件。")
    else:
        print(f"未找到 Music0.pck 文件")

def find_genshin_path_with_reg_query():
    try:
        result = subprocess.run(
            ['reg', 'query', 'HKCU', '/f', '原神', '/t', 'REG_SZ', '/s'],
            capture_output=True, text=True
        )
        output = result.stdout
        match = re.search(r'([a-zA-Z]:\\[^\n]+Genshin Impact[^\n]+Update\.exe)', output)

        if match:
            genshin_update_path = match.group(1)
            genshin_install_path = genshin_update_path.rsplit('\\', 2)[0]  # 移除 updateProgram\Update.exe 的部分
            return genshin_install_path
        else:
            return None

    except Exception as e:
        print(f"出现错误: {e}")
        return None

def get_file_hash(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def files_are_identical(src_file, dst_file):
    if not os.path.exists(dst_file):
        return False
    return get_file_hash(src_file) == get_file_hash(dst_file)

def copy_music_files(genshin_path):
    music_src_path = os.path.join(genshin_path, 'Genshin Impact Game', 'YuanShen_Data', 'StreamingAssets', 'AudioAssets')
    music_dst_path = os.path.join(os.getcwd(), 'Original Game Files')

    if not os.path.exists(music_src_path):
        print(f"未找到音乐文件夹: {music_src_path}")
        return

    if not os.path.exists(music_dst_path):
        os.makedirs(music_dst_path)
    
    files_copied = False
    for file_name in os.listdir(music_src_path):
        if file_name.startswith("Music"):
            src_file = os.path.join(music_src_path, file_name)
            dst_file = os.path.join(music_dst_path, file_name)

            if not files_are_identical(src_file, dst_file):
                shutil.copy2(src_file, dst_file)
                print(f"已复制文件: {file_name} 到 {music_dst_path}")
                files_copied = True
            else:
                print(f"文件 {file_name} 已存在且一致，跳过复制")

    if files_copied:
        print("文件复制完成")
    else:
        print("所有文件已是最新，无需复制")

def run_download_script():
    download_script_path = os.path.join(os.getcwd(), 'Download.py')
    
    if os.path.exists(download_script_path):
        try:
            print("正在运行 Download.py 脚本...")
            subprocess.run(['python', 'Download.py'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"运行 Download.py 时出现错误: {e}")
    else:
        print("未找到 Download.py 脚本")

check_and_prompt_for_new_game_files()

genshin_install_path = find_genshin_path_with_reg_query()

if genshin_install_path:
    print(f"找到原神的安装路径为: {genshin_install_path}")
    copy_music_files(genshin_install_path)
else:
    print("未找到原神的安装路径，请手动复制音乐文件到Original Game Files文件夹，路径为\\Mihoyo\\Genshin Impact\\Genshin Impact Game\\YuanShen_Data\\StreamingAssets\\AudioAssets\\Music*.pck")

# 运行 Download.py 脚本
run_download_script()

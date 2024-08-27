import requests
import os
import subprocess
from pydantic import BaseModel
from typing import List, Optional

class GamePackage(BaseModel):
    pre_download: Optional["PreDownload"]

class PreDownload(BaseModel):
    major: "Major"

class Major(BaseModel):
    game_pkgs: List["GamePkg"]

class GamePkg(BaseModel):
    url: str

GamePackage.update_forward_refs()
PreDownload.update_forward_refs()
Major.update_forward_refs()

def get_genshin_predownload_resource_url():
    # Genshin Impact 的 game_id 为 '1Z8W5NHUQb'
    game_id = '1Z8W5NHUQb'
    
    # 调用 API 获取游戏资源包
    response = requests.get(f"https://hyp-api.mihoyo.com/hyp/hyp-connect/api/getGamePackages?game_ids[]={game_id}&launcher_id=jGHBHlcOq1")
    
    # 检查请求
    if response.status_code != 200:
        print("Failed to retrieve data.")
        return None
    
    # 解析 JSON 
    data = response.json()
    
    # 提取预下载资源包下载链接
    predownload_package_data = data["data"]["game_packages"][0]
    
    if predownload_package_data.get("pre_download") is not None:
        predownload_package = GamePackage(**predownload_package_data).pre_download

        url = predownload_package.major.game_pkgs[0].url
        
        if ".zip." in url:
            url = url.split("/YuanShen_")[0]
        
        return url
    else:
        print("No predownload packages available.")
        return None

def download_music_files(base_url, output_dir='./New Game Files'):
    index = 0
    print("开始下载...")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    while True:
        file_name = f"Music{index}.pck"
        file_path = os.path.join(output_dir, file_name)
        
        if os.path.exists(file_path):
            print(f"{file_name} 已存在，跳过下载.")
            index += 1
            continue
        
        url = f"{base_url}/ScatteredFiles/YuanShen_Data/StreamingAssets/AudioAssets/{file_name}"
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                file_size = response.headers.get('content-length')
                if file_size:
                    file_size = int(file_size)
                else:
                    file_size = "NONE"
                print(f"正在下载: {file_name}, 文件大小: {file_size}")

                with open(file_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=8192): 
                        if chunk: 
                            file.write(chunk)
                print(f"下载完成: {file_name}")
                index += 1
            else:
                print(f"下载失败: {url}")
                break
        except Exception as e:
            print(f"ERROR: {str(e)}")
            break
    print("所有文件下载完成")

def run_extract_compare_script():

    script_dir = os.path.dirname(os.path.abspath(__file__))
    extract_compare_script = os.path.join(script_dir, "Extract_Compare.py")
    
    if os.path.exists(extract_compare_script):
        print(f"运行 {extract_compare_script}...")
        try:
            subprocess.run(["python", extract_compare_script], check=True)
        except subprocess.CalledProcessError as e:
            print(f"运行 {extract_compare_script} 失败: {e}")
    else:
        print(f"找不到 {extract_compare_script}")

# 获取预下载资源包的基本URL
base_url = get_genshin_predownload_resource_url()

if base_url:
    print(f"Base URL: {base_url}")
    download_music_files(base_url)
    
    run_extract_compare_script()
else:
    print("无法获取预下载资源包的基本URL")

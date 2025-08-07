import requests
from prettytable import PrettyTable
from datetime import datetime

while True:
    table = PrettyTable()

    table.field_names = ["序号","歌名","歌手"]
    music_name = input("请输入音乐名称：")
    url = "https://163api.qijieya.cn/search?keywords=" + music_name
    response = requests.get(url)
    a=0

    if response.status_code == 200:
        data = response.json()
        for song in data["result"]["songs"]:
            a+=1
            table.add_row([a, song['name'], song['artists'][0]['name']])
        print(table)
        music_a=int(input("请输入您要播放的音乐编号："))
        music_id=data["result"]["songs"][music_a-1]["id"]
        if music_id:
            print(f"成功获取音乐ID:{music_id}")
            print("准备获取音乐链接")
            response=requests.get(f"https://api.sayqz.com/tunefree/ncmapi/song/url/v1?id={music_id}&level=exhigh")
            json_data = response.json()
            #$.data[0].time
            if json_data["data"][0]["time"] !=0 and json_data["data"][0]["time"] != None:
                if round(json_data["data"][0]["time"] // 10000) * 10000 == 30000:
                    a=input("此为VIP歌曲，是否下载？(y/n)")
                    if a == "y":
                        print("继续下载")
                    else:
                        print("已取消任务")
                        exit(0)


                else:
                    print("此为普通歌曲")
            else:
                print("无此歌曲，时间为0")

        #$.data[0].url
        music_url = json_data["data"][0]["url"]
        if music_url:
            print(f"成功获取音乐链接:{music_url}")
            # 下载音乐
            zuozhe=music_id=data["result"]["songs"][music_a-1]["artists"][0]["name"]
            music_computer_url=input("请输入音乐保存目录(留空为保存到当前目录)：")
            if music_computer_url == None:
                music_computer_url=f"{music_name}.mp3"
            from tqdm import tqdm
            response = requests.get(music_url, stream=True)
            time = datetime.now().strftime('%Y-%m-%d %H-%M-%S-%f')
            file_size = int(response.headers.get('content-length', 0))
            with open(f"{music_computer_url}{music_name} -{zuozhe} [{time}].mp3", "wb") as f:

                with tqdm(
                    desc="下载进度",
                    total=file_size,
                    unit='B',
                    unit_scale=True,
                    leave=False,
                    unit_divisor=1024,
                    bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]'
                ) as progress_bar:
                    for data in response.iter_content(chunk_size=1024):
                        size = f.write(data)
                        progress_bar.update(size)
            print("音乐下载完成")
            print(f"音乐已保存至：{music_computer_url}{music_name} -{zuozhe} [{time}].mp3")
            print("----------------------------------")

        else:
            print("音乐链接获取失败")
            print("您输入的编号有误")
    else:
        print("歌曲菜单拉取失败")





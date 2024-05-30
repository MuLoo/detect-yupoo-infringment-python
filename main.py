import aiohttp
import asyncio
import tkinter as tk
from tkinter import filedialog
from concurrent.futures import ThreadPoolExecutor
from termcolor import colored
import os

print(colored('开始执行程序', 'green'))

class ACbumChecker:
  def __init__(self, username, keyword):
    self.username = username
    self.keyword = keyword
    self.page = 1
    self.results = []
    self.password = None

  async def send_get_request(self, url):
    async with aiohttp.ClientSession() as session:
      async with session.get(url) as response:
        if response.status == 200:
          res = await response.json()
          return res
        else:
          print(colored(f'请求出现错误，Error: {response.status} {response.text}', 'red'))
          return None

  async def get_user_info (self) :
    url = f'https://x.yupoo.com/api/web/users/{self.username}'
    return await self.send_get_request(url)

  async def check_Album (self,id):
    try:
      url = f'https://x.yupoo.com/api/web/users/{id}/albums?page={self.page}&password={self.password}'
      res = await self.send_get_request(url)
      if res is None:
        return None
      else:
        data = res.get('data')
        list = data.get('list')
        if data is None or len(list) == 0:
          return None
        else:
          self.page += 1
          for item in list:
            name = item.get('name')
            description = item.get('description')
            if self.is_infrigement(item):
              self.results.append({
                "name": name,
                "link": f'https://{self.username}.x.yupoo.com/albums/{item["id"]}?uid=1',
                "backlink": f'https://x.yupoo.com/gallery/{item["id"]}'
              })
              print(colored(f'找到一个相册：{name}', 'yellow'))
      await self.check_Album(id)
    except Exception as e:
      print(colored(f'出现错误，退出程序: {e}', 'red'))
      os._exit(1)



  def is_infrigement(self,album):
    name = album.get('name')
    description = album.get('description')
    if self.keyword in name.lower() or self.keyword in description.lower():
      return True
    return False

  def write_to_file(self):
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", initialfile=f'{self.username}_results.csv',filetypes=[("CSV files", "*.csv")])
    if file_path:
      with open(file_path, 'w') as f:
        f.write('Album name, Album Link, Album Console Link\n')
        for item in self.results:
          f.write(f'{item["name"]}, {item["link"]}, {item["backlink"]}\n')
        print(colored(f'导出文件成功,文件位置:{file_path}', 'green'))

  async def main (self):
    userinfo = await self.get_user_info()
    if userinfo is not None:
      data = userinfo.get('data')
      id = data.get('id')
      if data.get('needPassWord') == True and data.get('passwordValid') != True:
        self.password = input(colored('该用户主页加密，请输入密码: ', 'blue'))

      print(colored(f'用户名: {self.username}, id 是 {id}， 开始查询相册...', 'blue'))
      await asyncio.gather(self.check_Album(id))
      print(colored(f'查询完毕，查到 {len(self.results)} 个相册', 'green'))
      if len(self.results) == 0:
        print(colored('未找到任何相册, 程序将退出', 'yellow'))
        os._exit(0)
      else:
        print(colored('开始写入文件...', 'green'))
    else:
      print(colored(f'未找到用户：{self.username}, 程序将推出', 'yellow'))
      os._exit(1)

  def run_async_main(self):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(self.main())
    loop.close()


username = input(colored("请输入用户名: ", 'blue'))
keyword = input(colored("请输入关键字: ", 'blue'))


if __name__ == "__main__":
  AC = ACbumChecker(username, keyword)
  AC.run_async_main()
  AC.write_to_file()
  os._exit(0)


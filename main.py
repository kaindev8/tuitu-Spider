import requests
from lxml import etree
import os


class TuiImgSpider:
    def __init__(self, page=100):
        self.page = page
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            "referer": "https://www.tuiimg.com/"
        }

    def get_title(self, src):
        res = requests.get(src)
        title_tree = etree.HTML(res.text)
        title = title_tree.xpath('//*[@id="main"]/h1/text()')
        if title:
            return title[0]
        else:
            return None

    def get_base_url(self, src):
        res = requests.get(src)
        url_tree = etree.HTML(res.text)
        img = url_tree.xpath('//*[@id="nowimg"]/@src')
        if img:
            x = img[0].split('/')
            return (x[0] + '/' + x[1] + '/' + x[2] + '/' + x[3] + '/' + x[4])
        else:
            return None

    def download(self, img_url, folder, i):
        print(f'正在下载第{i+1}张!')
        filename = os.path.basename(img_url)  # 生成文件名
        file_path = f"./{folder}/{filename}"
        if os.path.exists(file_path):  # 如果文件已存在则跳过
            print(file_path, "已存在，跳过下载!")
            return
        with open(file_path, "wb") as f:
            # 写入文件夹
            f.write(requests.get(img_url, headers=self.headers).content)

    def start(self, url):
        response = requests.get(url, headers=self.headers)
        tree = etree.HTML(response.text)
        li_list = tree.xpath('//div[@class="beauty"]/ul/li')
        for li in li_list:
            src = li.xpath('./a/@href')[0]
            res = requests.get(src)
            all_tree = etree.HTML(res.text)
            folder = self.get_title(src)  # 文件夹名字
            if not os.path.exists(folder):  # 如果文件夹不存在就创建
                os.makedirs(folder)

            base_url = self.get_base_url(src)  # 图片链接
            all_btn = all_tree.xpath('//*[@id="allbtn"]')
            for btn in all_btn:
                num = btn.text.split('/')[1].split(')')[0]  # 一套写真的张数
                print(f'{folder},共{num}张写真!')
                for i in range(int(num)):
                    img_url = '{}/{}.jpg'.format(base_url, i + 1)  # 图片链接
                    self.download(img_url, folder, i)

    def run(self):
        urls = ["https://www.tuiimg.com/meinv/list_{}.html".format(i)
                for i in range(1, self.page + 1)
                ]

        for url in urls:
            print("###开始下载")
            self.start(url)

        print("###下载结束!")


if __name__ == '__main__':
    spider = TuiImgSpider(page=100) # page = 爬取的页数
    spider.run()

def main():
    """
    爬取彼岸图网的缩略图
    """

    try:
        from typing import List
        from bs4 import BeautifulSoup as bs
        import requests as req
        from os import path, makedirs
        from time import sleep
        import shutil

        PGCNT = eval(input("页数区间（包含两边）："))
        ZONE = input('分区名(如"4kfengjing")：')
        TIMEOUT = int(input('每次重连间隔（秒）：'))
        DEFAULTRETRY = int(input('最大重连次数：'))
        OUTDIR = input('输出文件夹名（注意，该文件夹将被清除（如果存在））：')

        def catch(URL="https://pic.netbian.com/"+ZONE):
            URL = URL.replace("index_1.html", "")
            def getList(retryNum = DEFAULTRETRY):
                if retryNum <= 0:  return None
                try:
                    r = req.get(URL)
                    content = r.content
                    return content
                except:
                    sleep(TIMEOUT)
                    return getList(retryNum-1)
            
            r = getList()
            if r is None: 
                print("无法获取位于{}的图片列表，已经跳过。".format(URL))
            txt = str(r, encoding="GBK")
            bso = bs(txt, features="html.parser")

            results = set(bso.select(".clearfix"))
            results = results.intersection(set(bso.select("ul")))
            result = results.pop()
            results = list()

            ul = result.children
            for li in ul:
                bso = bs(str(li), features="html.parser")
                a = bso.a
                if a == None:
                    continue
                bso = bs(str(a), features="html.parser")
                img = bso.img
                src = img.attrs["src"]
                results.append("https://pic.netbian.com"+src)
            return results

        all_ = list()
        for i in range(PGCNT[0], PGCNT[1]+1):
            all_ += catch("https://pic.netbian.com/{}/index_{}.html".format(ZONE, i))
            print("\rGetting Image URLs. [{:.2f}%]".format(i/(PGCNT[1]-PGCNT[0]+1)*100), end='')
        print("\nGot {} URLs".format(len(all_)))

        if path.isdir(OUTDIR):  shutil.rmtree(OUTDIR)
        makedirs(OUTDIR)

        length = len(all_)
        def getImage(URL, retryNum=DEFAULTRETRY):
            try:
                r = req.get(URL)
                content = r.content
                return content
            except:
                sleep(TIMEOUT)
                return getImage(URL, retryNum-1)
        for i in range(1, length+1):
            print("\rGetting Image File {}. [{:.2f}%]".format(i, i/length*100), end='')
            content = getImage(all_[i-1])
            with open("{}/pic{}.jpg".format(OUTDIR, i), "wb") as f:
                f.write(content)
    except KeyboardInterrupt:
        print("操作由用户取消")


if __name__ == "__main__":
    main()
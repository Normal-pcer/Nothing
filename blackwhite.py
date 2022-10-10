def main():
    """
    把图片转为黑白（适用于扫描的文档等）
    """
    from typing import Tuple
    from PIL import Image
    from os import path, walk

    def 颜色差异度(颜色1: Tuple[int, int, int], 颜色2: Tuple[int, int, int]) -> int:
        """
        获得两个颜色的差异度。
        原理：计算(r1-r2)^2 + (g1-g2)^2 + (b1-b2)^2
        """
        r1, g1, b1 = 颜色1
        r2, g2, b2 = 颜色2

        return round(((r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2) / 100)

    文件名和路径 = input('文件路径: ')
    文件夹, 文件名 = path.split(文件名和路径)
    文件名, 扩展名 = path.splitext(文件名)

    文件指针 = open(文件名和路径, 'rb')
    图片 = Image.open(文件指针)
    宽度 = 图片.width
    高度 = 图片.height
    图片像素列表 = 图片.load()
    新的图片 = Image.new('RGB', (宽度, 高度), color=(255, 255, 255))

    for i in range(宽度):
        for j in range(高度):
            像素颜色: Tuple[int, int, int] = 图片像素列表[i, j]
            白色 = 颜色差异度((255, 255, 255), 像素颜色)
            黑色 = 颜色差异度((0, 0, 0), 像素颜色)
            if 白色 < 黑色:
                新的图片.putpixel((i, j), (255, 255, 255))
            else:
                新的图片.putpixel((i, j), (0, 0, 0))
        print('\r{}/{}'.format(i+1, 宽度), end='            ')

    文件指针.close()
    新的图片.save(path.join(文件夹, 文件名+'-bw.'+扩展名[1:]))


if __name__ == '__main__':
    main()

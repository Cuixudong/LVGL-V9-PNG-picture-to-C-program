#最好使用长宽一致且都为2的整数倍的jpg图片，尺寸不要太大，缩放到100左右就差不多了
from PIL import Image  
  
def rgb_to_rgb565(r, g, b):  
    """将RGB颜色转换为RGB565格式"""  
    return ((b >> 3) << 11) | ((g >> 2) << 5) | (r >> 3)  
  
def save_img_data(img_path, output_file):  
    """将图片的RGB565数据保存到文本文件中"""  
    img = Image.open(img_path)  
    pixels = img.load()  
    width, height = img.size  
    data = []
    with open(output_file, 'w') as f:
        #添加数组头
        f.write('static const EGL_ALIGN(4) uint32_t s_ptx_img_data[] = {')
        f.write('\n0x78657470, 0x00001100, ')
        fs_value = width*height*2 + 32
        f.write(f"0x{fs_value:08x}, ")
        f.write('0x01000201,')
        wh_value = width * 65536 + height;
        f.write(f"0x{wh_value:08x}, ")
        f.write('0x00000001, 0x00000000, 0x00000000, ')
        for y in range(height):  
            for x in range(0, width, 2):  # 强制组成u32的16进制，跟原格式一样 
                if x + 1 < width:
                    rgb565_1 = rgb_to_rgb565(*pixels[x + 1, y][:3])  
                    rgb565_2 = rgb_to_rgb565(*pixels[x, y][:3])  
                    data.append(f"0x{rgb565_1:04x}{rgb565_2:04x}")  
                else:  # 如果只剩下一个像素，则单独处理  
                    rgb565_1 = rgb_to_rgb565(*pixels[x, y][:3])  
                    data.append(f"0x{rgb565_1:04x}0000")  # 用0填充第二个像素的位置
        f.write(','.join(data))
        #添加数组尾
        f.write('};')
  
# 使用当前目录下的img.jpg图片作为输入，并将数据保存到img_data.txt文件中  
save_img_data('img.jpg', 'img_data.txt')

print("数据已写入img_data.txt文件")

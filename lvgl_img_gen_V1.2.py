from PIL import Image  
import os  

image_num = 0
# 遍历当前文件夹下的所有PNG文件  
for filename in os.listdir('.'):
    if filename.endswith('.png'): 
        # 设置输出文件  
        output_file = f'lv_img_{filename[:-4]}.c'  # 去掉.png后缀，添加lv_img_前缀和.c后缀

        # 获取文件名（不包括扩展名）  
        filename_without_ext = os.path.splitext(os.path.basename(filename))[0]  
          
        # 读取PNG图片，并转换为RGBA格式  
        img = Image.open(filename).convert('RGBA')  
          
        # 获取图片的宽度和高度  
        width, height = img.size  
          
        # 创建一个空列表用于保存像素数据  
        pixel_data = []  
          
        # 遍历图片的每个像素，并将像素值转换为LVGL所需的A8R8G8B8格式  
        for y in range(height):  
            for x in range(width):  
                r, g, b, a = img.getpixel((x, y))  
                # LVGL的LV_COLOR_FORMAT_RAW_ALPHA格式是A8R8G8B8  
                pixel_value = (r, g, b, a)
                pixel_data.append(pixel_value)  
          
        # 将像素数据转换为C数组格式  
        c_array_data = 'static const uint8_t image_data[] = {\n'  
        for i in range(0, len(pixel_data), 16):  # 每行16个元素  
            line_data = ', '.join("{}, {}, {}, {}".format(hex(d[2]), hex(d[1]), hex(d[0]), hex(d[3])) for d in pixel_data[i:i+16])  
            c_array_data += f'    {line_data},\n'  
        c_array_data += '};\n\n'  
          
        # 生成lv_img_dsc_t结构体初始化代码，并使用动态命名的变量  
        lv_img_dsc_name = f'img_{filename_without_ext}_dsc'  
        lv_img_dsc_code = f'''  
        const lv_img_dsc_t {lv_img_dsc_name} = {{  
            .header = {{
                .w = {width},  
                .h = {height},  
                .cf = LV_COLOR_FORMAT_ARGB8888,  // 设置颜色格式为LV_COLOR_FORMAT_ARGB8888 
            }},  
            .data_size = {len(pixel_data) * 4},  // 设置数据大小为字节数  
            .data = image_data,  // 指向图像数据的指针  
        }};  
        '''  
          
        # 输出到文件  
        with open(output_file, 'w', encoding='utf-8') as f:  
            f.write(f'/* Image: {filename}\n')  
            f.write(f' * Width: {width}, Height: {height}\n')  
            f.write(f' * LVGL Format: LV_COLOR_FORMAT_ARGB8888\n')  
            f.write(f' */\n\n')
            f.write(f'#include "lvgl/lvgl.h"\n\n')
            f.write(c_array_data)  
            f.write('\n')  
            f.write(lv_img_dsc_code)  
          
        print(f'Raw alpha image data and lv_img_dsc_t named {lv_img_dsc_name} has been written to {output_file}')
        image_num = image_num + 1

print(f'已处理完所有图片文件,共',image_num,'个\n\n')

# 打开test.c文件以写入内容  
with open('img_declare.c', 'w', encoding='utf-8') as f:  
    # 写入头文件
    f.write('#include "lvgl/lvgl.h"\n\n')  
      
    # 循环生成LV_IMAGE_DECLARE声明  
    for i in range(1, image_num + 1):  
        # 格式化字符串，将ID替换为当前序号  
        declaration = f'LV_IMAGE_DECLARE(img_picture_{i}_dsc);\n'  
        # 写入到文件中  
        f.write(declaration)

    # 写入数组声明  
    f.write('\n// 声明lv_img_dsc_t类型的数组my_img\n')  
    f.write('const lv_img_dsc_t * my_img[] = {\n')  
  
    # 循环生成数组元素  
    for i in range(1, image_num + 1):  
        # 假设每个结构体定义的名字是 img_picture_ID_dsc，其中ID是序号  
        struct_name = f'img_picture_{i}_dsc'  
        # 将结构体指针添加到数组中  
        f.write(f'    &{struct_name},\n')  
  
    # 结束数组声明  
    f.write('};\n')



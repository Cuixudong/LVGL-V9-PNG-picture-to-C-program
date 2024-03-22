import os  
import glob  
  
def rename_png_files(directory='.'):  
    # 获取当前路径下所有的.png文件  
    png_files = glob.glob(os.path.join(directory, '*.png'))  
      
    # 对文件进行排序，确保重命名时顺序正确  
    png_files.sort()  
      
    # 初始化序号  
    count = 1  
      
    # 遍历.png文件并重命名  
    for file in png_files:  
        # 构造新的文件名  
        new_name = os.path.join(directory, f'picture_{count}.png')  
          
        # 重命名文件  
        os.rename(file, new_name)  
        print(f'Renamed {file} to {new_name}')  
          
        # 更新序号  
        count += 1  
  
# 调用函数，默认处理当前路径下的.png文件  
rename_png_files()

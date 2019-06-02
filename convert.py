import os
import shutil
from decimal import Decimal

from chardet.universaldetector import UniversalDetector

from hant2zh import hant2zh

dir_path = r'D:\BaiduNetdiskDownload\字幕7000\女優不詳'

# 工作目录必须以'\'结尾，该符号不可省略
if dir_path[-1] != '\\':
    dir_path += '\\'

# 全局数据初始化
# 统计未包含数据
uncaniter = {}
# 统计非中文字符
except_chr = []
# 过滤字符集
unStatistics = {' ': -1, "·": -1, "\n": -1, chr(0): -1, chr(65279): -1}
# 过滤字符集包含ASCii码，以便屏蔽常见符号和英文
for i in range(32, 127):
    unStatistics[chr(i)] = -1
# 文本数据类型，需要转化的文本类型必须包含其中
text_type = {
    '.txt',
    '.srt',
    '.ass',
    '.vtt',
    '.py'
}


# 输入繁体，返回简体
def convert(line: str):
    new_line = ''
    # 对单个字符转化
    for char in line:
        # 字符包含在字典中，替换转化结果
        if char in hant2zh:
            new_line += hant2zh[char]
        # 字符不在字典中，统计
        else:
            # 统计过滤
            if char in unStatistics:  # 是否包含在过滤列表
                pass  # 跳过统计
            elif 13312 <= ord(char) <= 40869:  # 仅仅统计中文
                if char in uncaniter:
                    uncaniter[char] = uncaniter[char] + 1
                else:
                    uncaniter[char] = 1
            else:  # 非中文字符：直接吃掉
                except_chr.append(char)
                char = ""
            new_line += char
    return new_line


# 输入繁体文本内容（list[str]）,自动将转换结果写入为指定名称文件
def convert_file(new_filename, content: list):
    with open(new_filename, 'w', encoding='utf-8') as f:
        for line in content:
            line = convert(line)
            f.writelines(line)
    f.close()


# 输出log
def log(log_filename="log.txt"):
    with open(log_filename, 'w', encoding='utf-8') as f:
        f.write("{\n")
        for k, v in uncaniter.items():
            line = '"' + k + '"' + ": " + '"' + k + '"' + ",  # " + "code:" + str(ord(k)) + ' : ' + str(v)
            f.write("    " + line + ',\n')
        f.write("}")
    f.close()


# 创建目录
def creat_dir(dir_name: str):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


# 获取指定目录下文本文件绝对路径列表
def get_text_files(dir_name: str) -> list:
    return list(filter(lambda file: os.path.isfile(file) and os.path.splitext(file)[-1] in text_type,
                       [os.path.join(dir_name, x) for x in os.listdir(dir_name)]))


# 转换当前目录所有文本文件
# # 识别文本编码，识别失败的文本移动到err文件夹下
# # 转化后的文件不会替换当前文件，默认输出到simple文件夹下
def convert_in_dir(dir_name: str):
    creat_dir(os.path.join(dir_name, 'simple'))
    files = get_text_files(dir_name)
    for file in files:
        # 获取文件编码
        detector = UniversalDetector()
        with open(file, 'rb') as f:
            lines = f.readlines()
            line_number = len(lines)
            index = 0
            for line in lines:
                detector.feed(line)
                index += 1
                if detector.done:
                    break
            detector.close()
            encoding = detector.result.get('encoding')
            confidence = detector.result.get('confidence')
        f.close()
        print(
            " 编码:{},  \tfeed:{}%, \t可信度：{} :\t文件：{} ".format(encoding, round(
                Decimal(index) / Decimal(line_number) * Decimal(100), 2), round(Decimal(confidence), 2), file))
        try:
            with open(file, 'r', encoding=encoding) as f:
                lines = f.readlines()
                convert_file(os.path.join(dir_name, 'simple\\' + os.path.split(file)[-1]), lines)
            f.close()
        except UnicodeDecodeError:
            creat_dir(os.path.join(dir_name, 'err'))
            print('err:', file)
            shutil.move(file, os.path.join(dir_name, 'err'))


if __name__ == "__main__":
    print(dir_path)
    convert_in_dir(dir_path)
    log()

import os
import time
import re


# 计算更改的新名 整理番号名：字母大写
def new_filename(old_filename: str):
    arr = old_filename.split('.')
    sub = arr[-1]
    name = arr[0].replace('.', '-')
    infostr = ''
    for ni in arr[1:len(arr) - 1]:
        name += '.' + ni
    name = name.upper()
    prop = re.compile(r'([a-zA-Z]+-\d+)')
    info = re.compile(r'[a-zA-Z]+-\d+([^.]+)')
    m = info.search(name)
    if m:
        infostr = m.groups()[0]
        if re.fullmatch(r'^\d+$', infostr):
            infostr = ''
        else:
            infostr = infostr.replace('-C', '(高清中文字幕) ')
            infostr = infostr.replace('-', ' ')
            infostr = infostr.strip()
            infostr = infostr.replace('SUB', '中文字幕')
            infostr = infostr.replace('  ', ' ')
    m = prop.findall(name)

    if len(m) > 0:
        if infostr == '':
            old_filename = str(m[0]) + '.' + sub
        else:
            old_filename = str(m[0]) + ' ' + infostr + '.' + sub

    return old_filename


def file_new_name(fileName: str):
    prop = re.compile(r'([a-z]+)(\d+)([^.]+)?')
    m = prop.findall(fileName)
    if len(m) > 0 and len(m[0]) > 1:
        sub = fileName.split('.')[-1]
        print(m[0])
        fileName = ''
        fileName = m[0][0].upper() + '-' + m[0][1]
        if len(m[0]) > 2:
            ptr = 2
            while ptr < len(m[0]):
                fileName += ' ' + m[0][ptr]
                ptr += 1
        fileName += '.' + sub
        return fileName
    return fileName


def formattime(timestamp):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))


# print(file_new_name('abp023.HD.srt'))

path = 'D:\BaiduNetdiskDownload\字幕7000\简体化\简体'
new_file = new_filename


for file in [x for x in os.listdir(path)]:
    if os.path.isfile(os.path.join(path, file)):
        if str(file) != new_file(str(file)):
            print(str(file), ' new: ', new_file(str(file)))
            try:
                os.rename(os.path.join(path, file), os.path.join(path, new_file(str(file))))
            except FileExistsError:
                print('文件重名：',file)

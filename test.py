import os

text_type = {
    '.txt',
    '.srt',
    '.ass',
    '.vtt',
    '.py'
}

logs = []


def write_file(new_filename, content: list):
    with open(new_filename, 'w', encoding='utf-8') as f:
        for line in content:
            f.writelines(line)
    f.close()


def get_textfiles(dir_path: str) -> list:
    return list(filter(lambda file: os.path.isfile(file) and os.path.splitext(file)[-1] in text_type,
                       [os.path.join(dir_path, x) for x in os.listdir(dir_path)]))


dir = 'D:\BaiduNetdiskDownload\原始7000字幕\simple'
key = "圣水"
result = []
files = get_textfiles(dir)
for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        temp = []
        temp.clear()
        temp.append(file + "\n")
        lines = f.readlines()

        for index, line in enumerate(lines):
            if line.find(key) >= 0:
                temp.append("    " + str(index) + ":" + line)
        if len(temp) > 1:
            for t in temp:
                result.append(t)
    f.close()
write_file('00000.txt', result)

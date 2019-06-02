import re

prop = re.compile(r'([a-zA-Z]+-\d+)')
info = re.compile(r'[a-zA-Z]+-\d+([^.]+)')
strs = 'abp-111-info'
# m = prop.findall(strs)
# for item in m:
#     print(item)
m = info.search(strs)
if m:
    s = m.groups()[0]
    print(s)
    if re.fullmatch(r'^\d+$', s):
        s = ''
    print(s)

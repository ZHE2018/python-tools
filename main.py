from bs4 import BeautifulSoup
import requests


# domain: https://souka.co/ query_api: q/no=
def query_info(no: str, domain: str, query_api: str):
    wd = no.upper()
    html = requests.get(domain + query_api + wd).content  # 获取结果页面
    soup = BeautifulSoup(html, features="html.parser")  # 解析结果,soup 是一个DOM 树
    divs = soup.find_all('div', class_='el-card__body')  # 结果保存节点
    # 获得搜索结果
    url = ''
    if len(divs) > 0:
        div = divs[0]
        name = str(div.find_all('span', class_='sp_no')[0].contents)
        no = str(div.find_all('span', class_='sp_name')[0].contents)
        date = str(div.find_all('span', class_='sp_time')[0].contents)
        href = str(div.find_all('a', class_='a_name')[0]['href'])
        url = domain + href
        print(name, no, date, href, url)
    if url != '':
        html = requests.get(url).content
        soup = BeautifulSoup(html, features='html.parser')
        body = soup.find('body')
        with open(wd + '-body.html', 'w', encoding='utf-8') as f:
            f.write(str(body))
        divs = soup.find_all('form', class_='el-form js')
        if len(divs) > 0:
            divs = divs[0]
            divs_items = divs.find_all('div', class_='el-form-item')
            for item in divs_items:
                items = item.find_all('span')
                item_str = ''
                for span in items:
                    item_str += str(span.string) + '#@#'
                item_str = str(item_str)
                item_str = item_str.replace('\n', '').replace(' ', '')
                print(item_str)


def request_url(wd: str):
    wd = wd.upper()
    html = requests.get('https://souka.co/q/no=' + wd).content  # 获取结果页面
    soup = BeautifulSoup(html, features="html.parser")  # 解析结果,soup 是一个DOM 树
    # divs = soup.find_all('div', class_='result c-container')  # 获得 class='result c-container' 的容器,搜索结果保存在该容器中
    divs = soup.find_all('div', class_='el-card__body')
    with open(wd + '-results.html', 'w', encoding='utf-8') as f:
        for div in divs:
            f.write(str(div))
        if len(divs) > 0:
            div = divs[0]
            name = str(div.find_all('span', class_='sp_no')[0].contents)
            no = str(div.find_all('span', class_='sp_name')[0].contents)
            date = str(div.find_all('span', class_='sp_time')[0].contents)
            print(name, no, date)
        # for div in divs:  # 遍历结果集 获取每一条结果中的信息
        #     # 获取摘要
        #     abstract = div.find_all('div', class_="c-abstract")[0].contents
        #     i = 1  # 第一条摘要是搜索时间
        #     abstractstr = abstract[0].string
        #     # 循环获取全部摘要信息 保存为str类型
        #     while i < len(abstract):
        #         abstractstr += str(abstract[i])
        #         i = i + 1
        #     # 默认关键字被em标签包围,去除该包围 下同
        #     abstractstr = abstractstr.replace('<em>', '')
        #     abstractstr = abstractstr.replace('</em>', '')
        #     # 获取标签中的href 属性 结果为str
        #     href = div.h3.a['href']
        #     # 获取标题中的信息,将其转化为字符串
        #     content = div.h3.a.contents
        #     for con in content:  # 保存这些信息
        #         f.write(str(con).replace('<em>', '').replace('</em>', ''))
        #     f.write('\t')
        #     f.write(abstractstr)
        #     f.write('\t')
        #     f.write(href)
        #     f.write('\n')
    f.close()


query_info('CJOD-185', 'https://souka.co', '/q/no=')

# request_url('CJOD-185')

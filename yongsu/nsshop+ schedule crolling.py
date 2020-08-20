from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import datetime
import csv

#날짜별 블로그 게시글 링크 크롤링
def get_urls():
    # 크롬 창 없는 옵션 설정
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome('C:\\Users\\nex\\Desktop\\chromedriver_win32\\chromedriver.exe', chrome_options=options)

    list_href = []

    for i in range(1, 5):
        # ---- 페이지 접속 ----#
        url = 'https://blog.naver.com/PostView.nhn?blogId=livehomes&logNo=221932196744&categoryNo=34&parentCategoryNo=0&viewDate=&currentPage=1&postListTopCurrentPage=1&from=search&userTopListOpen=true&userTopListCount=30&userTopListManageOpen=false&userTopListCurrentPage=' + str(
            i) + '#'
        driver.get(url)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        hrefs = soup.find('div', id='toplistWrapper')

        for href in hrefs.find_all('a', class_='pcol2 _setTop _setTopListUrl'):
            list_href.append(href['href'])

    # 추가 3개 link 추가
    href_extra = [
                'https://blog.naver.com/PostView.nhn?blogId=livehomes&logNo=221758685785&categoryNo=34&parentCategoryNo=0&viewDate=&currentPage=5&postListTopCurrentPage=1&from=search',
                'https://blog.naver.com/PostView.nhn?blogId=livehomes&logNo=221757480012&categoryNo=34&parentCategoryNo=0&viewDate=&currentPage=5&postListTopCurrentPage=1&from=search',
                'https://blog.naver.com/PostView.nhn?blogId=livehomes&logNo=221756350321&categoryNo=34&parentCategoryNo=0&viewDate=&currentPage=5&postListTopCurrentPage=1&from=search'
    ]
    for link in href_extra:
        list_href.append(link)

    list_href.reverse()
    return list_href

#날짜별 방송 상품 정보 크롤링
def get_product_info(list_href):

    for url in list_href:
        req = requests.get(url)
        soup = BeautifulSoup(req.text, "html.parser")
        result = []

        contents = soup.find('div', class_='se_component_wrap sect_dsc __se_component_area')

        # 방송 날짜
        date_str = soup.find('span', class_='se_publishDate pcol2')
        date_list = date_str.get_text().replace(' ', '').split('.')
        date_str = datetime.datetime.strptime(date_list[0] + '-' + date_list[1] + '-' + date_list[2], '%Y-%m-%d')
        date_now = date_str.strftime('%Y-%m-%d')

        #시간별 상품명, 판매단가
        for content in contents.find_all('span'):
            text = content.get_text().replace(' ', '').replace('\n', '').replace('NS샵플러스', '').replace('[Shop+]','').replace('[eShop+]','').replace('상담신청','0원')
            if text == '':
                continue
            result.append(text)

        # 중복 상품 제거
        for i in range(0,4):
            del result[0]

        # 방송 정보 csv 파일 만들기
        make_csv(result,date_now)

    return None

#방송 정보 csv 파일 만들기
def make_csv(product_info, date_now):
    print(date_now)
    print(product_info)
    f = open('2020 nsshop+.csv','a',newline='',encoding='CP949')
    wr = csv.writer(f)

    for i in range(0,len(product_info),3):
        hour = product_info[i].split('~')
        name = product_info[i+1]
        price = int(product_info[i+2].replace('원','').replace(',',''))
        wr.writerow([date_now,hour[0],name,price])
    f.close()
    return None

def main():
    list_href = []

    # 날짜별 블로그 게시글 링크 크롤링
    list_href = get_urls()

    # 날짜별 방송 상품 정보 크롤링
    get_product_info(list_href)

if __name__ == '__main__' :
    main()

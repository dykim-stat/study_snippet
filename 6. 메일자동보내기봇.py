from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import time, pickle, datetime
import pandas as pd

my_id = ''
my_pw = ''



def initial_setting():
    """ 크롬드라이버 켜고 초기 세팅 진행 """

    global driver

    # 옵션 생성
    # options = webdriver.ChromeOptions()
    # # 창 숨기는 옵션 추가
    # options.add_argument("headless")
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_argument('--no-sandbox')
    # driver = Chrome('chromedriver.exe', option=options)
    
    driver = Chrome('chromedriver.exe')
    ## 로딩안되면 5초동안은 기다리기
    driver.implicitly_wait(5)

    driver.get('https://www.skku.edu/skku/index.do#')

    time.sleep(1)

    ## 로그인 버튼 클릭
    my_click('//*[@id="item_body"]/div[2]/div[1]/div/ul/li[4]/a')

    ## 아이디, 패스워드 입력
    driver.switch_to.window(driver.window_handles[1])
    my_input('//*[@id="userid"]', my_id)
    my_input('//*[@id="userpwd"]', my_pw)
    my_click('//*[@id="loginBtn"]')

    time.sleep(3)

    # 메일들어가기
    time.sleep(1)
    driver.get('https://mail3.skku.edu/portal.nsf/menulist_new?readform&comtype=&selnodecode=&count=1000&menu=MAIL&expand=&node=2&content=/mail_h/haedoji96.nsf/view?readform&viewtitle=&dhxr1630651509134#')
    print('크롬드라이버 구동 완료')

def read_gsheet():
    """ 구글 스프레드 링크로 불러오기 """
    sheet_id = '1OoH8lLDkNdNMQYCJOWjEWE1eI8N0sikyybh5ohPxMlk'
    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv'
    dat = pd.read_csv(url)
    return dat

def data_cleaning(df):
    """ 아웃풋 순서 (email, address, timestamp) """
    email = df.이메일
    address = df.주소
    timestamp = df.타임스탬프
    result = (email, address, timestamp)
    return result


def send_mail(email, address):
    """ 메일 보내는 부분 """

    title_text = '[응용통계연구소] 테스트용 메일입니다.'
    main_text = f'''안녕하세요, 응용통계연구소입니다.

테스트용 메일을 작성중입니다.

본 메일은 자동화 봇에 의해 발송되는 메일입니다.

{address} -> 해당 주소로 보내드릴 예정입니다.


감사합니다.
응용통계연구소 드림.
'''


    my_click('/html/body/form/div/div/div/div[1]/ul[1]/li/a')
    driver.switch_to.window(driver.window_handles[2])

    ## 받는 사람 입력
    my_input('//*[@id="inSendTo"]', email)

    ## 제목 입력
    my_input('//*[@id="DisSubject"]/input', title_text)

    ## 내용입력
    ## 본문 접근이 안되서 위에서 tab으로 접근
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="DisSubject"]/input').click()

    actions = ActionChains(driver)
    actions.key_down(Keys.TAB).pause(0.3).key_down(Keys.TAB).pause(0.3).key_down(Keys.TAB) \
    .pause(0.3).key_down(Keys.TAB).pause(0.3).send_keys(Keys.ENTER) \
    .pause(2).send_keys(main_text).perform()

    ## 보내기 버튼 클릭
    # my_click('//*[@id="GWpop"]/div[1]/div[1]/a[1]')

def my_click(xpath):
    """ xpath 입력 시 해당 부분 클릭 """
    driver.find_element_by_xpath(xpath).click()

def my_input(xpath, keyword):
    """ xpath랑 입력할 단어 """
    driver.find_element_by_xpath(xpath).send_keys(keyword)

def now():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def main():
    count = 0 # 발송한 메일 수
    initial_setting()

    while True:
        data = read_gsheet()
        new_count = len(data)


        wait = new_count - count
        if wait > 0:
            for i in range(wait):
                result = data_cleaning(data.iloc[count + i,:])
                send_mail(email=result[0], address=result[1])
                print(f'{result[2]}에 들어온 신청에 대해 {result[0]}님께 메일을 발송하였습니다.')
            count = new_count

        else:
            print(f'실시간 확인 중입니다. 새로운 신청이 없습니다. {now()}',end='\r')
        time.sleep(10)

if __name__ == "__main__":
    main()


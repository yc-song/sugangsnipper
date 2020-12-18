'''
제작: 송종현 (기항 17)
문의: hyeongoon11@snu.ac.kr
'''

import selenium
from selenium import webdriver
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
import smtplib
import threading
import time
from selenium.webdriver.chrome.options import Options


def main():
    snipping_list = [[[['M2794.001200', '001'], ['031.033', '001', '002', '003'], ['043.071', '003'], ['270.549', '001']],
             'hyeongoon11@snu.ac.kr', 7],[[['M2794.001200', '002']], 'hyeongoon@gmail.com', 12]]
    for jh in range(len(snipping_list)):
        ratio = []
        # 크롬 옵션 설정
        options = webdriver.ChromeOptions()
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome('./webdriver/chrome/chromedriver.exe',options=chrome_options)
        # driver = webdriver.Chrome('./webdriver/chrome/chromedriver.exe')

        # 접속. 수강편람
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        for t in range(len(snipping_list[jh][0])):
            driver.get('https://sugang.snu.ac.kr/sugang/cc/cc100.action')
            driver.find_element_by_xpath('//*[@id="srchSbjtCd"]').send_keys(snipping_list[jh][0][t][0])
            driver.find_element_by_xpath('//*[@id="cond00"]/a[4]').click()
            for j in range(1, snipping_list[jh][2]): # 유효한 정보가 있   는 셀을 받아옴 (학교 수신 사이트가 좀 구조가 이상함)
                try:
                    print(int(driver.find_element_by_xpath(
                        '//*[@id="content"]/div/div[3]/div[1]/div[2]/table/tbody/tr[{}]/td[16]'.format(j)).text.strip()[
                              0:3]), int(
                        driver.find_element_by_xpath(
                            '//*[@id="content"]/div/div[3]/div[1]/div[2]/table/tbody/tr[{}]/td[17]'.format(
                                j)).text.strip()))
                    ratio.append(j)
                except selenium.common.exceptions.NoSuchElementException:
                    pass
            for j in ratio:
                if int(driver.find_element_by_xpath(
                        '//*[@id="content"]/div/div[3]/div[1]/div[2]/table/tbody/tr[{}]/td[16]'.format(j)).text.strip()[
                       0:3]) > int(driver.find_element_by_xpath(
                        '//*[@id="content"]/div/div[3]/div[1]/div[2]/table/tbody/tr[{}]/td[17]'.format(
                                j)).text.strip()) : # 여석검증
                    for m in range(1,len(snipping_list[jh][0][t])):
                        if str(snipping_list[jh][0][t][m]) == str(driver.find_element_by_xpath(
                        '//*[@id="content"]/div/div[3]/div[1]/div[2]/table/tbody/tr[{}]/td[8]'.format(j)).text.strip()[0:3]):
                            print('조건문 진입')
                            smtp = smtplib.SMTP('smtp.gmail.com', 587)
                            smtp.ehlo()
                            smtp.starttls()
                            smtp.login('발송 이메일 아이디', '비번')
                            msg = MIMEText('https://sugang.snu.ac.kr/\n\n{} ({}) 수업의 여석이 발생하였습니다.\n\n현재 수강생은 {}명, 정원은{}명입니다.\n상기 링크에 접속하여 줍줍에 성공하시기 바랍니다.'.format(snipping_list[jh][0][t][0],snipping_list[jh][0][t][m],int(
                        driver.find_element_by_xpath(
                            '//*[@id="content"]/div/div[3]/div[1]/div[2]/table/tbody/tr[{}]/td[17]'.format(
                                j)).text.strip()),int(driver.find_element_by_xpath(
                        '//*[@id="content"]/div/div[3]/div[1]/div[2]/table/tbody/tr[{}]/td[16]'.format(j)).text.strip()[
                              0:3])))
                            msg['Subject'] = '[긴급] {} ({}) 수업 여석 발생'.format(snipping_list[jh][0][t][0],snipping_list[jh][0][t][m])
                            msg['To'] = snipping_list[jh][1]
                            smtp.sendmail('수신  메일 주소', snipping_list[jh][1], msg.as_string())

                            smtp.quit()
            ratio = []
    threading.Timer(60,thread_run).start()
    
if __name__ == "__main__":
    main()


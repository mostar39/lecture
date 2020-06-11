import pymysql
from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import datetime

conn = pymysql.connect(host="localhost",port=3306, user="dbuser", passwd ="blabla", db="real_term_project")
cur = conn.cursor()


#test

'''
제천 고암동 : https://weather.naver.com/rgn/townWetr.nhn?naverRgnCd=16150115
서울 중구 장충동 2가 : https://weather.naver.com/rgn/townWetr.nhn?naverRgnCd=09140144
대구 중구 동성로 1가 : https://weather.naver.com/rgn/townWetr.nhn?naverRgnCd=06110148
대전 대덕구 송촌동 : https://weather.naver.com/rgn/townWetr.nhn?naverRgnCd=07230107
부산 중구 남포동 : https://weather.naver.com/rgn/townWetr.nhn?naverRgnCd=08110580
'''

area_number = ['09140144','16150115','07230107','06110148','08110580']
#서울, 제천, 대전, 대구, 부산 순서

root = 'https://weather.naver.com/rgn/townWetr.nhn?naverRgnCd='
area_list = ["Seoul","Jechon","Daejeon","Daeju","Busan"]

#비 -> rain
#흐림 -> cloud
#맑음 -> sunny

for i in range(0,5) :

    date_ = datetime.today().strftime("%Y%m%d")
    print(type(date_))

    print(i)
    req=root+area_number[i]
    html = urlopen(req)
    soup = BeautifulSoup(html, 'html.parser')
    
    div_area = soup.find('div',{'class':'fl'})

    today_area = div_area.find('em')
    today = today_area.text #온도+날씨
    today = today.strip()
    temp = today[:2] #온도만
    temp = int(temp)
    print(type(temp))
    print(temp)
    
    # 초반에는 날씨 형식이 어떻게 나올지 잘 몰라서 한글 날씨정보를 보고, 직접 영어로 입
    weather_area = today_area.find('strong')
    weather= weather_area.text #날씨

    dust_ar = div_area.find('p')
    dust_area = dust_ar.find('a')
    dust_oz = dust_area.find_all('em')

    du_oz=[]

    
    for duoz in dust_oz :
        du_oz.append(duoz.get('class'))

    dust = du_oz[0][0] #미세먼지정도
    ozone = du_oz[1][0] #오존정도


    print(dust)
    print(ozone)
    area = area_list[i] # 지역

    #순서 : 지역, 날짜, 현재 날씨, 현재 온도, 미세먼지 정도, 오존 정도
    sql = "INSERT INTO weather Values(%s,%s,%s,%s,%s,%s)"
    print(type(temp))
    cur.execute(sql,(area, date_,weather, temp, dust, ozone))

#데이터 커밋
conn.commit()  
    

sql = "select * from weather"
cur.execute(sql)

#안에 있는 데이터 출력해 주는 것
result = cur.fetchall()
print(result)


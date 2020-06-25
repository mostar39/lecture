import pymysql
from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import datetime

conn = pymysql.connect(host="localhost",port=3306, user="dbuser", passwd ="blabla", db="real_term_project")
cur = conn.cursor()

area_number = ['09140144','16150115','07230107','06110148','08110580']
#서울, 제천, 대전, 대구, 부산 순서

root = 'https://weather.naver.com/rgn/townWetr.nhn?naverRgnCd='
area_list = ["서울","제천","대전","대구","부산"]

for i in range(0,5) :
    area = area_list[i] # 지역
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
    
   
    weather_area = today_area.find('strong')
    weather= weather_area.text #날씨

    dust_ar = div_area.find('p')
    dust_area = dust_ar.find('a')
    dust_oz = dust_area.find_all('em')

    du_oz=[]

    for duoz in dust_oz :
        du_oz.append(duoz.text)
        print(duoz.text)
        

    try:
        ozone = du_oz[1] #오존정도
    except:
        ozone = "보통"
        print(".")
        
    dust = du_oz[0] #미세먼지정도


    print(dust)
    print(ozone)

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


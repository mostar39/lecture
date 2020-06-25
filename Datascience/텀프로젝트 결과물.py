import pymysql
from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

conn = pymysql.connect(host="localhost",port=3306, user="dbuser", passwd ="blabla", db="real_term_project")
cur = conn.cursor()

sql = "select * from weather"
cur.execute(sql)
result = cur.fetchall()
result = pd.DataFrame(result,columns=['지역','날짜','날씨','온도','미세먼지','오존'])
result['지역']=result['지역'].astype('str')
result['날짜']=result['날짜'].astype('str')

country = ['서울','제천','대전','대구','부산']

date =[]
for i in range(20200614,int(datetime.today().strftime("%Y%m%d"))+1) :
    date.append(i)

print("안녕하세요! 지역별 날씨정보를 제공하기 위한 시스템입니다.")
print("해당 프로그램은 서울, 제천, 대전, 대구, 부산 총 5개의 지역의 날씨, 온도, 미세먼지 정도, 오존 정도 정보를 가지고 있습니다.")

while(True) :
    print("\n1 > 원하는 지역, 날짜를 입력하고 정보 알기"+
      "\n2 > 원하는 지역, 날짜, 날씨 정보를 입력하고 정보 알기"+
      "\n3 > 전체 지역의 시계열 현재온도 그래프 보기"+
      "\n4 > 원하는 지역을 입력하고 해당 지역의 현재온도 시계열 그래프 보기"+
      "\n5 > 날짜 별, 현재 온도가 가장 높은 지역과 온도 알기" +
      "\n6 > 과거부터 현재까지 미세먼지/오존 정도가 가장 나쁜지역 알기"+
      "\n7 > 전체 지역의 지금까지 평균 온도 구하기"+
      "\n8 > 프로그램 종료하기")
    choice = int(input("\n원하는 것을 선택하세요 > "))

    if choice == 1 :
        wherewant = input("\n원하는 지역을 선택하세요(서울, 제천, 대전, 대구, 부산) > ")
        whenwant = input("원하는 날짜를 입력하세요(20200622 형식) > ")
        while(wherewant!="서울" and wherewant!="대전" and wherewant!="제천" and wherewant!="대구" and wherewant!="부산" ):
              wherewant = input("지역을 잘못입력하였습니다! 다시 입력하세요 > (서울, 제천, 대전, 대구, 부산) > ")
        result_1_1=result.set_index('지역')
        result_1=result_1_1.loc[wherewant]
        result_1=result_1.set_index('날짜')
        try :
            result_2 = result_1.loc[whenwant]
            print("\n%s 지역의 %s에 날씨는 %s였으며 기온은 %d, 미세먼지는 %s, 오존은 %s 였습니다."%(wherewant,whenwant,result_2['날씨'],result_2['온도'],result_2['미세먼지'],result_2['오존']))
        except :
            print("날짜 형식이 잘못되었거나, 해당 날짜에 대한 데이터가 없습니다.")
            
    elif choice == 2 :
        wherewant = input("\n원하는 지역을 선택하세요(서울, 제천, 대전, 대구, 부산) > ")
        whenwant = input("원하는 날짜를 입력하세요(20200622 형식) > ")
        while(wherewant!="서울" and wherewant!="대전" and wherewant!="제천" and wherewant!="대구" and wherewant!="부산" ):
              wherewant = input("지역을 잘못입력하였습니다! 다시 입력하세요 > (서울, 제천, 대전, 대구, 부산) > ")
        whatwant = input("원하는 날씨 정보를 입력하세요! > (날씨, 온도, 미세먼지, 오존)")
        while(whatwant!="날씨" and whatwant!="온도" and whatwant!="미세먼지" and whatwant!="오존"):
            whatwant = input("날씨정보를 잘못입력하였습니다! 다시 입력하세요 > (날씨, 온도, 미세먼지, 오존) > ")

        result_2_3=result.set_index('지역')
        result_2=result_2_3.loc[wherewant]
        try :
            result_2=result_2.set_index('날짜')
            result_2_1 = result_2.loc[whenwant]
            print("\n%s 지역의 %s에 %s는 %s 입니다." %(wherewant, whenwant, whatwant, result_2_1[whatwant]))
        except :
            print("\n해당 데이터가 없습니다!")

    elif choice==3 :
        #전체 지역의 시계열 현재온도 그래프 보기
        result_3 = pd.DataFrame({"지역":result["지역"], "날짜":result["날짜"], "온도":result["온도"]})
        result_3=result_3.set_index('지역')
        result_3_1 = result_3.loc['서울']
        result_3_2 = result_3.loc['제천']
        result_3_3 = result_3.loc['대전']
        result_3_4 = result_3.loc['대구']
        result_3_5 = result_3.loc['부산']
        plt.rc("font", family="gulim")
        plt.plot(result_3_1['날짜'], result_3_1['온도'],"ro-",result_3_2['날짜'], result_3_2['온도'],"yx-",result_3_3['날짜'], result_3_3['온도'],"gd-",result_3_4['날짜'], result_3_4['온도'],"bs-",result_3_5['날짜'], result_3_5['온도'],"kp-")
        plt.title("현재온도 시계열 그래프")
        plt.xlabel('날짜')
        plt.ylabel("온도")
        plt.legend(["서울","제천","대전","대구","부산"])
        plt.show()

    elif choice == 4:
        #원하는 지역을 입력하고 해당지역의 현재온도 시계열 그래프
        result_4 = pd.DataFrame({"지역":result["지역"], "날짜":result["날짜"], "온도":result["온도"]})
        result_4=result_4.set_index('지역')
        wherewant = input("\n원하는 지역을 입력하세요 > ")
        result_4 = result_4.loc[wherewant]
        plt.rc("font", family="gulim")
        plt.plot(result_4['날짜'], result_4['온도'],"ro--",)
        plt.title("현재온도 시계열 그래프")
        plt.xlabel('날짜')
        plt.ylabel("온도")
        plt.legend([wherewant])
        plt.show()

    elif choice==5:
        #날짜 별, 현재 온도가 가장 높은 지역과 온도 알기
        result_5_2 = pd.DataFrame({"지역":result["지역"], "날짜":result["날짜"], "온도":result["온도"]})
        result_5_2 = result_5_2.set_index(['날짜'])
        result_5 = result.groupby(['날짜'])['온도'].max()
        
        for i in range (0,len(result_5)):
            result_5 = result.groupby(['날짜'])['온도'].max()
            result_5_1 = result.set_index('날짜')
            result_5_1 = result_5_1.loc[result_5.index[i]]
            result_5_2 = result_5_1.set_index('온도')
            result_5_2 = result_5_2.loc[result_5[i]]
            result_5_3 = result_5_2.reset_index()
            try:
                con=result_5_3[result_5[i]][0]
            except:
                c=0
            result_5 = result_5.reset_index()
            try:

                print("%d에 %s 지역이 %s 도씨로 가장 높았습니다."%(date[i],con,result_5['온도'][i]))
            except:
                for j in range(0,len(result_5_3['지역'])):
                    print("%d에 %s 지역이 %s 도씨로 가장 높았습니다."%(date[i],result_5_3['지역'][j],result_5['온도'][i]))



        
    elif choice == 6 :
        #과거부터 현재까지 미세먼지/오존 정도가 가장 나쁜지역 알기
        result_6 = result
        dust_list=[]
        for dust in result_6['미세먼지'] :
            if dust=="좋음" :
                dust_list.append(3)
            elif dust=="보통" :
                dust_list.append(2)
            elif dust=="나쁨" :
                dust_list.append(1)

        result_6['미세먼지 점수']=dust_list

        oz_list=[]
        for oz in result_6['오존'] :
            if oz=="좋음" :
                oz_list.append(3)
            elif oz=="보통" :
                oz_list.append(2)
            elif oz=="나쁨" :
                oz_list.append(1)

        result_6['오존 점수']=oz_list

        result_6_1 = result_6.groupby(['지역'])['미세먼지 점수'].mean()
        result_6_2 = result_6.groupby(['지역'])['오존 점수'].mean()


        result_6_1=result_6_1.reset_index()
        result_6_2=result_6_2.reset_index()

        min_du = 1000.0
        min_oz=1000.0
        for i in range(0,5) :
            if min_du>result_6_1['미세먼지 점수'][i] :
                min_du = result_6_1['미세먼지 점수'][i]
            if min_du>result_6_2['오존 점수'][i] :
                min_oz = result_6_2['오존 점수'][i]
        print()
        for i in range(0,5) :
            if result_6_1['미세먼지 점수'][i]==min_du :
                print("최악의 미세먼지 지역은 평균 %f점으로 %s 입니다."%(min_du,result_6_1['지역'][i]))
        for i in range(0,5):
            if result_6_2['오존 점수'][i]==min_oz :
                print("최악의 오존 지역은 평균 %f점으로 %s 입니다."%(min_oz,result_6_2['지역'][i]))
        

    elif choice == 7 :
        result_7 = pd.DataFrame({"지역":result["지역"], "온도":result["온도"]})
        result_7_1 = result_7.groupby('지역').mean()
        result_7_2 = result_7_1.reset_index()
        print()
        for i in range(0,5) :
            print("%s지역의 지금까지 평균 기온은 %d도씨입니다."%(result_7_2['지역'][i],result_7_2['온도'][i]))

    
    elif choice ==8 :
        break

    else :
        print("잘못입력하였습니다. 다시 입력하세요")

print("\n감사합니다!")

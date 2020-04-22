
import csv

csvfile = input("오픈하고 싶은 csv파일 이름을 쓰세요!(automoblog_news.csv) >> ")
with open(csvfile, mode = "r",encoding='UTF8') as f:
    automotive = list(csv.reader(f))

for i in range (0,len(automotive)):
    print(automotive[i][0]+" "+automotive[i][1])


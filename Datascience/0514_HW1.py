import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

covid = pd.read_csv("covid19a.csv")
covid.fillna(0)
covid_date=covid.groupby("date").sum()
print(covid_date)

gragh=covid_date.plot(kind='bar',title='deaths/cases',legend=True)
plt.show()


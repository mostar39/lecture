import numpy as np
import pandas as pd

covid = pd.read_csv('covid19a.csv')
covid.fillna(0)
population = pd.read_csv('population.csv')
population.set_index('country')
covid_country = covid.groupby('country').sum()
print(covid_country)

covid_population = pd.merge(covid_country.reset_index(), population.reset_index()).set_index("country")
print(covid_population.head(20))


covid_population['crade'] = covid_population.cases*1000000 / covid_population.population
covid_population['drade'] = covid_population.deaths*1000000 / covid_population.population
new_covid_population = covid_population.astype({'crade':int,'drade':int})

print(new_covid_population)
print(new_covid_population.sort_values(by = 'crade', ascending=False))

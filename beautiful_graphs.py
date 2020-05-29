import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.ticker as ticker
import matplotlib

"""
Reference: https://towardsdatascience.com/visualizing-covid-19-data-beautifully-in-python-in-5-minutes-or-less-affc361b2c6a
"""

df = pd.read_csv("https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv", parse_dates=["Date"])
"""parse_dates=["Date"] reads the "Date" column values as datetime objects """

# Getting an overview of the dataset

# Numbered list of column names
print('Columns:')
for i in range(len(df.columns)):
    print(str(i+1)+". "+df.columns[i])

print('Number of countries: {}'.format(df['Country'].unique().shape[0]))
print('Number of dates: {}'.format(df['Date'].unique().shape[0]))
print('Total number of rows: {}'.format(df['Date'].shape[0]))
print(df['Country'].unique().shape[0] * df['Date'].unique().shape[0] == \
    df['Date'].shape[0])
print('===================================')
"""The dataset contains Confirmed, Recovered, and Death cases for 187
countries for 110 days. Country specific counts are given for each date.
Therefore, there are 187*110=20570 rows. Day count is as on May 12, and it
keeps increasing as a new date is added everyday.
""" 

countries = ['Canada', 'China', 'France', 'Germany', 'US', 'United Kingdom']
df = df[df['Country'].isin(countries)]
df['Cases'] = df[['Confirmed', 'Recovered', 'Deaths']].sum(axis='columns')

df = df.pivot(index='Date', columns='Country', values='Cases')
covid = df.copy(deep=True)
covid.columns = countries

#Calculating rates per 100,000
populations = {'Canada':37664517,\
    'Germany':83721496, \
    'United Kingdom':67802690,\
    'US':330548815,\
    'France':65239883,\
    'China':1438027228}

percapita = covid.copy(deep=True)
for country in list(percapita.columns):
    percapita[country] = (percapita[country]/populations[country])*100000

#Generating colors and styles
colors = {'Canada':'#045275', 'China':'#089099', 'France':'#7CCBA2', \
'Germany':'#FCDE9C', 'US':'#DC3977', 'United Kingdom':'#7C1D6F'}

plt.style.use('fivethirtyeight')
matplotlib.rcParams['font.sans-serif'] = 'Liberation Sans'
matplotlib.rcParams['font.family'] = 'sans-serif'

#Creating the visualisation
fig = plt.figure(figsize=(12, 8))
ax = fig.subplots(nrows=1, ncols=1)
covid.plot(color=colors.values(), ax=ax, linewidth=5)
ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
ax.grid(color='#d4d4d4')
ax.set(xlabel='Date', ylabel='# of Cases')
ax.legend().set_visible(False)

# Adding country names
for country in colors.keys():
    ax.text(x=covid.index[-1], y=covid[country].max(), color=colors[country], s=country, weight='bold')

# Adding header text
ax.text(x=covid.index[1], y=(covid.max().max() + (0.15 * covid.max().max())), \
s='COVID-19 Cases by Country', fontsize=23, weight='bold', alpha=0.75)
ax.text(x=covid.index[1], y=(covid.max().max() + (0.05*covid.max().max())), \
    s='For the USA, China, Germany, France, United Kingdom, and \
Canada\nIncludes Current Cases, Recoveries, and Deaths', fontsize=16, \
    alpha=0.75)

# Adding reference
ax.text(x=percapita.index[1], y=-70000, \
    s='Source: https://github.com/datasets/covid-19/blob/master/data/countries-aggregated.csv', \
    fontsize=10, alpha=0.4)

fig.savefig('covid_total_cases.png', transparent=False, dpi=300, bbox_inches='tight')

fig1 = plt.figure(figsize=(12, 8))
ax1 = fig1.subplots(nrows=1, ncols=1)
percapita.plot(color=list(colors.values()), linewidth=5, ax=ax1)
ax1.grid(color='#d4d4d4')
ax1.set(xlabel='Date', ylabel='# Cases per 100,000 people')
ax1.legend().set_visible(False)

for country in list(colors.keys()):
    ax1.text(x=percapita.index[-1], y=percapita[country].max(), \
    color=colors[country], s=country, weight='bold')

ax1.text(x=percapita.index[1], y=(percapita.max().max() + (0.15*percapita.max().max())), s="Per Capita COVID-19 \
cases by country", fontsize=23, weight='bold', alpha=0.75)
ax1.text(x=percapita.index[1], y=(percapita.max().max() + (0.05 * percapita.max().max())), s="For the USA, China,\
 Germany, France, United Kingdom, and Canada\nIncludes current cases, recoveries,\
 and deaths", fontsize=16, alpha=0.75)
ax1.text(x=percapita.index[1], y=-25,\
s='Source: https://github.com/datasets/covid-19/blob/master/data/countries-aggregated.csv',
fontsize=10, alpha=0.4)

fig1.savefig('covid_percapita.png', transparent=False, dpi=300, bbox_inches='tight')

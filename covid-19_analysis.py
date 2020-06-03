from datetime import datetime
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.pyplot import cm
import matplotlib.ticker as ticker
import matplotlib
from scipy.optimize import curve_fit
from scipy.signal import savgol_filter
from scipy.stats import gamma
import seaborn as sns

sns.set()
sns.set_context(context="notebook", font_scale=1.8)
plt.close('all')

plt.style.use('fivethirtyeight')
matplotlib.rcParams['font.sans-serif'] = 'Liberation Sans'
matplotlib.rcParams['font.family'] = 'sans-serif'

now = datetime(2020, 6, 1) # Creating a datetime object
date = now.strftime("%Y-%m-%d") 
url = "http://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-"
url = url+date+".xlsx"
url

df = pd.read_excel(url)
#print(df.info())
country = 'Sweden'
df_filtered = df[df['countriesAndTerritories'] == country]
timeSpan = 7*9 # 8 weeks
dates = np.array(df_filtered['dateRep'][0:timeSpan], dtype='datetime64[D]')
newCases = np.array(df_filtered['cases'][0:timeSpan])
dates = dates[::-1] #Reverse the order
newCases = newCases[::-1]
allCases = np.cumsum(newCases)+1e-10 #Add small bias to avoid zeroes in the data
xTicks = np.arange(np.size(newCases))

def fit_expo(x, y):
    logParams = np.polyfit(x=x, y=np.log(y), deg=1, w=np.sqrt(y), full=False)
    initParams = (np.exp(logParams[1]), logParams[0])
    params = curve_fit(lambda t, a, b: a * np.exp(b * t), x, y, p0 = initParams)
    return params[0], params[1], initParams

params, *_ = fit_expo(x=xTicks, y=allCases)

fig1 = plt.figure(figsize=(12,8))
ax1 = fig1.subplots(nrows=1, ncols=1)
ax1.grid(color='#d4d4d4')
ax1.plot(xTicks, params[0]*np.exp(params[1]*xTicks), 'r--', linewidth=4, label='whole time span')
ax1.bar(xTicks, allCases, color='gray', align='center', alpha=1.00)
ax1.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
ax1.set_xticklabels(dates[::7], rotation=30)
ax1.tick_params(axis='both', which='major', labelsize=12)
ax1.grid(True)
ax1.text(xTicks[1], allCases.max() + (0.15 * allCases.max()), s=country, 
         fontsize=25, weight='bold', alpha=1.00)
ax1.text(xTicks[1], allCases.max() + (0.05 * allCases.max()), s='Dashed Line: \
Model\nBars: Actual cases', fontsize=16, alpha=0.45)
fig1.savefig('exponential_model.png', transparent=False, dpi=300, bbox_inches='tight')

#sliding fit
fittedDays = 5
n = timeSpan - fittedDays + 1 #samples for sliding fit

colorMap = cm.rainbow(np.linspace(1, 0, n)) #e.g. rainbow, magma
color = iter(colorMap)
doublingVec = np.zeros((n,))

fig2 = plt.figure(figsize=(12,8))
ax2 = fig2.subplots(nrows=1, ncols=1)

for d in range(n):
    c = next(color)
    y = allCases[d:d+fittedDays]
    x = xTicks[d:d+fittedDays]
    params,_, _ = fit_expo(x,y)
    yFit = params[0]*np.exp(params[1]*xTicks)
    ax2.bar(xTicks, allCases, color='gray', alpha=1, align='center') 
    ax2.plot(xTicks[d::], yFit[d::], c=c, lw=3) 
    doublingVec[d] = np.log(2)/params[1]
    
ax2.set(ylim=[0, allCases[-1]*1.4], xlim=[-1, timeSpan])
ax2.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
ax2.tick_params(axis='both', which='major', labelsize=12)
ax2.text(xTicks[1], yFit.max() + (0.5 * yFit.max()), s=country, fontsize=25, 
         weight='bold', alpha=1)
ax2.text(xTicks[1], yFit.max() + (0.43 * yFit.max()), s='Epidemic model for Sweden', fontsize=16, 
         weight='bold', alpha=0.75)
ax2.set_xticklabels(dates[::7], rotation=30)
fig2.savefig('to_be_figured_out.png', transparent=False, dpi=300, bbox_inches='tight')

#Doubling Interval
fig3 = plt.figure(figsize=(12, 8))
ax3 = fig3.subplots(nrows=1, ncols=1)
ax3.grid(color='#d4d4d4')
ax3.plot(xTicks[fittedDays-1::], doublingVec, linewidth=3)
ax3.set_xticklabels(dates[fittedDays-1::7], rotation=30)
ax3.set(ylim=[0, doublingVec[-1]*2])
ax3.text(xTicks[3], doublingVec.max() + (0.5 * doublingVec.max()), s=country, 
         fontsize=25, weight='bold', alpha=1.00)
ax3.text(xTicks[3], doublingVec.max() + (0.42 * doublingVec.max()), s='Doubling Interval (days)', 
         fontsize=16, alpha=1.00)
fig3.savefig('doubling_interval.png', transparent=False, dpi=300, bbox_inches='tight')


#Relative Growth
relGrowth =100*(allCases[1::]-allCases[:-1:])/allCases[:-1:]
target = 10
fig4 = plt.figure(figsize=(12, 8))
ax4 = fig4.subplots(nrows=1, ncols=1)
ax3.grid(color='#d4d4d4')
ax4.bar(xTicks[1::],relGrowth,color = 'k', alpha=1  , align = 'center')   
ax4.set_xticklabels(dates[1::9], rotation=30)
ax4.axhline(target, 0, 1, c='r', label='Austrian target')
ax4.text(xTicks[1], relGrowth.max() + (0.1 * relGrowth.max()), s=country, 
         fontsize=25, weight='bold', alpha=1.00)
ax4.text(xTicks[1], relGrowth.max() + (0.05 * relGrowth.max()), s='Relative Growth (%)',      
         fontsize=16, alpha=1.00)
ax4.text(xTicks[-10], target+3, s='Austrian Target', fontsize=16, alpha=0.75)
fig4.savefig('relative_growth.png', transparent=False, dpi=300, bbox_inches='tight')

#God only knwos the purpose of this graph
fig5 = plt.figure(figsize=(12, 8))
ax5 = fig5.subplots(nrows=1, ncols=1)
ax3.grid(color='#d4d4d4')
xVal = savgol_filter(allCases, 5, 3)   #filter length, filter order
yVal = savgol_filter(newCases, 5, 3)
ax5.loglog(xVal,yVal)
ax5.set(xlim=[100,max(xVal)*1.1], ylim=[10, 10**np.ceil(np.log10(np.max(yVal)))])
ax5.set_xlabel('All Cases', fontsize=22)
ax5.set_ylabel('New Cases', fontsize=22)
fig5.savefig('GOK.png', transparent=False, dpi=300, bbox_inches='tight')

### effective re-production
tau     = 5#13    #tau equals number of fitted days
a       = 1
b       = 5

n       = timeSpan-tau + 1  #samples for fit
repVec  = np.zeros((n,))

for d in np.arange(1,n):   
    ii  = np.arange(d,d+tau)
    y   = newCases[ii]

    num         = a+ np.sum(y)
 
    s           = np.arange(0,d+tau)
    ws          = gamma.pdf(s,a=3,loc=0,scale=1)  # gamma parameters to play around
    ws          = ws/np.sum(ws)

    
    sum_di      = 0 
    for i in ii:
        w       = np.reshape(ws[:i:],(-1,1))
        w       = w[::-1]
        ys      = np.reshape(newCases[:i:],(1,-1))
        sum_di  += ys@w
        
        
        #unifrom dist.
        #sum_di  += np.mean(ys)
                        
    den         = 1/b +  sum_di

    repVec[d]   = num/den                
                           
plt.figure(5)
plt.plot(xTicks[tau::], repVec[1::], linewidth = '2')
plt.xticks(xTicks[tau::3], dates[fittedDays::3], rotation=30)
plt.ylabel('effective re-production', fontsize = 22)
plt.axhline(1, 0, 1,c='r', label='pandemic stop')
plt.title(country.replace('_',' '), fontsize = 26)
plt.grid(True)
plt.ylim([0, 5])
#plt.show()
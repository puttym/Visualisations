import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

# Set defaults 
label_size = 16
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = 'Liberation Sans' 
matplotlib.rcParams['ytick.labelsize'] = label_size
matplotlib.rcParams['xtick.labelsize'] = label_size

# Data
data = {
    'Player':['J C Butler', 'S O Hetmyer', 'S D Russel', 'L S Livingstone', 
              'K D Karthik', 'S A Yadav', 'S Dube', 'S V Samson', 'R V Uthappa',
             'R A Tripathi'],
    'Sixes':[23, 17, 16, 16, 15, 13, 13, 12, 12, 11]
}

df = pd.DataFrame(data)

fig = plt.figure(figsize=(12, 8))
ax = fig.subplots(nrows=1, ncols=1)

plt.style.use('fivethirtyeight')

df.plot(x='Player', y='Sixes', kind='bar', width=0.5, edgecolor='black', 
        ax=ax, rot=90)

# Remove legend, axis labels, and grid lines
ax.legend().set_visible(False)
ax.set(xlabel=None)
ax.set(ylabel=None)
ax.grid(False)

# Set axis limits and ticks
ax.set_ylim([-2, 30])
ax.set_yticks([0, 5, 10, 15, 20])

# Graph title
ax.text(x=-0.2, y=df['Sixes'].max() + (0.2*df['Sixes'].max()), 
        s='Top-10 six hitters in IPL 2022',
       fontsize=23, weight='bold', alpha=0.75)

ax.text(x=-0.2, y=df['Sixes'].max() + (0.12*df['Sixes'].max()),
       s='As on April 21, 2022', fontsize=18, alpha=0.65)

# Reference
ax.text(x=-0.2, y=-1.5,
       s='Source: https://stats.espncricinfo.com/ci/engine/records/batting/most_sixes_career.html?id=14452;type=tournament',
       fontsize=10, alpha=0.4)

# Print the number of sixes above the bars
ax.text(x=-0.07, y=df['Sixes'][0]+0.5, s=df['Sixes'][0], fontsize=14, 
        weight='bold', alpha=0.75)

#ax.text(x=0.92, y=df['Sixes'][1]+0.5, s=df['Sixes'][1], fontsize=14,
#       weight='bold', alpha=0.75)

for i in range(1, len(df['Sixes'])):
    ax.text(x=(i-1)+0.92, y=df['Sixes'][i]+0.5, s=df['Sixes'][i], fontsize=14,
       weight='bold', alpha=0.75)

# Save the plot
fig.savefig('top10_six_hitters.png', transparent=False, dpi=300, 
         bbox_inches='tight')
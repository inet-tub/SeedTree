import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data=[['A','0.16',0.74],['B','0.16', 0.87],['C','0.16',0.95],
['A','0.25',0.77],['B','0.25',0.87],['C','0.25',0.95],
['A','0.33',0.77],['B','0.33',0.87],['C','0.33',0.95],
['A','0.5',0.76],['B','0.5',0.87],['C','0.5',0.95],
['A','0.66',0.76],['B','0.66',0.87],['C','0.66',0.95],
['A','0.75',0.81],['B','0.75',0.87],['C','0.75',0.94],
['A','0.83',0.77],['B','0.83',0.86],['C','0.83',0.95]
]

df=pd.DataFrame(data,columns=['name','fractions','cost'])

print(df)

# plot with seaborn and use the hue parameter
plt.figure(figsize=(10, 6))
fs = 15
sns.lineplot(x='fractions', y='cost', data=df, hue='name')
plt.legend(bbox_to_anchor=(0.8, 0.9), loc='upper left', fontsize=fs)
plt.ylabel('adjusted cost', fontsize=fs)
plt.xlabel('fractions', fontsize=fs)
plt.tick_params(axis='both', which='major', labelsize=fs)
plt.savefig("fb_lines_fractions_c12.pdf",bbox_inches='tight')
plt.show()
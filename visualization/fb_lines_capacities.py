import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


data=[['A','2',0.89],['B','2', 0.91],['C','2',0.97],
['A','4',0.84],['B','4',0.9],['C','4',0.96],
['A','6',0.8],['B','6',0.89],['C','6',0.96],
['A','8',0.81],['B','8',0.88],['C','8',0.95],
['A','10',0.78],['B','10',0.87],['C','10',0.95],
['A','12',0.76],['B','12',0.87],['C','12',0.94],
['A','14',0.73],['B','14',0.86],['C','14',0.95],
['A','16',0.75],['B','16',0.86],['C','16',0.95]
]

df=pd.DataFrame(data,columns=['name','capacities','cost'])

print(df)

# plot with seaborn and use the hue parameter
plt.figure(figsize=(10, 6))
fs = 22
sns.lineplot(x='capacities', y='cost', data=df, hue='name')
plt.legend(bbox_to_anchor=(0.8, 0.5), loc='upper left', fontsize=fs)
plt.ylabel('adjusted cost', fontsize=fs)
plt.xlabel('capacities', fontsize=fs)
plt.tick_params(axis='both', which='major', labelsize=fs)
plt.savefig("fb_lines_capacities_f0.5.pdf",bbox_inches='tight')
plt.show()
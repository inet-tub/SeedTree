import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

raw = pd.read_excel('../results/Results_f_c12_sns.xlsx',
                 dtype={'temp-p':float,'f':float,'cost_div':float}
                )
                
print(raw.head())

sns_data=raw.pivot(columns='temp-p', index='f', values='cost_div')

fs = 13
sns.heatmap(sns_data, annot=True, cbar=False, fmt='.2f', cmap = 'RdYlGn_r', annot_kws={"size":fs})

plt.xlabel('temp-p', fontsize = fs) # x-axis label with fontsize 15
plt.ylabel('f', fontsize = fs) # y-axis label with fontsize 15
plt.xticks(size=fs)
plt.yticks(size=fs)

plt.savefig("heatmap_f_c12.pdf",bbox_inches='tight')
plt.show()
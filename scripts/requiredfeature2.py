import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
penalty = pd.read_csv('penalty_data_set_2.csv', index_col=False)

#Chart for offence codes
def code_count(penalty):
    return penalty['OFFENCE_CODE'].value_counts().sort_values(ascending=0)[:10].plot.bar(figsize=(15, 10)), plt.xlabel('Offence Code'), plt.ylabel('Count')


code_count(penalty)
plt.show()
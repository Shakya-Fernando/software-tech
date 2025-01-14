import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
penalty = pd.read_csv('penalty_data_set_2.csv', index_col=False)

#regex to find camera and radar in description

def desc_penalty(penalty):
     return penalty[penalty.OFFENCE_DESC.str.contains('Camera|Radar', na=False)][['OFFENCE_MONTH', 'OFFENCE_CODE', 'OFFENCE_DESC']][0:200]

print(desc_penalty(penalty))
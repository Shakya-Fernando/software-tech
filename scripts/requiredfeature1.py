import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
penalty = pd.read_csv('penalty_data_set_2.csv', index_col=False)
penalty['OFFENCE_MONTH'] = pd.to_datetime(penalty['OFFENCE_MONTH'], format='%d/%m/%Y')

#user-selected period, report the information for all penalty cases
def date_penalty(penalty):
    return penalty.loc[(penalty['OFFENCE_MONTH'] >= '2016-01-01') & (penalty['OFFENCE_MONTH'] < '2016-02-01')]

print(date_penalty(penalty))
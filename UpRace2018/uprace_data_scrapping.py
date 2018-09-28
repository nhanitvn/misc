# import libraries
from bs4 import BeautifulSoup
import pandas as pd

def to_pandas(html_data):
    soup = BeautifulSoup(html_data, 'html.parser')
    # Get all rows
    table_rows = soup.find_all('div', 'tr')
    
    if len(table_rows) == 0:
        print("""No data""")
        return None
    # header
    header = [x.get_text() for x in table_rows[0].find_all('div', 'th')]
    print(header)
    rows = []
    for table_row in table_rows[1:]:
        tds = [x.get_text() for x in table_row.find_all('div', 'td')]
        print(tds)
        rows.append(tds)
        
    data = pd.DataFrame.from_records(rows, columns=header)
    for idx, col in enumerate(data.columns):
        data[col] = data[col].str.strip()
        if idx >=2:
            data[col] = data[col].str.replace(',', '').astype('float')
    
    import re
    cols = [re.sub(r'\s', '', col) for col in  data.columns]
    cols = [re.sub(r'\(km\)', '', col) for col in  cols]
    data.columns = cols
    return data



data_2408_2808_1 = to_pandas(html_2408_2808_1)
data_2408_2808_2 = to_pandas(html_2408_2808_2)
data_2408_2808_3 = to_pandas(html_2408_2808_3)
data_2408_2908 = pd.concat((data_2408_2808_1, data_2408_2808_2, data_2408_2808_3))

data_2908_0209_1 = to_pandas(html_2908_0209_1)
data_2908_0209_2 = to_pandas(html_2908_0209_2)
data_2908_0209_3 = to_pandas(html_2908_0209_3)
data_2908_0209 = pd.concat((data_2908_0209_1, data_2908_0209_2, data_2908_0209_3))


data_0309_0709_1 = to_pandas(html_0309_0709_1)
data_0309_0709_2 = to_pandas(html_0309_0709_2)
data_0309_0709_3 = to_pandas(html_0309_0709_3)
data_0309_0709 = pd.concat((data_0309_0709_1, data_0309_0709_2, data_0309_0709_3))

data_0809_1209_1 = to_pandas(html_0809_1209_1)
data_0809_1209_2 = to_pandas(html_0809_1209_2)
data_0809_1209_3 = to_pandas(html_0809_1209_3)
data_0809_1209 = pd.concat((data_0809_1209_1, data_0809_1209_2, data_0809_1209_3))

data_1309_1709_1 = to_pandas(html_1309_1709_1)
data_1309_1709_2 = to_pandas(html_1309_1709_2)
data_1309_1709_3 = to_pandas(html_1309_1709_3)
data_1309_1709 = pd.concat((data_1309_1709_1, data_1309_1709_2, data_1309_1709_3))

data_1409_1809_1 = to_pandas(html_1409_1809_1)
data_1409_1809_2 = to_pandas(html_1409_1809_2)
data_1409_1809_3 = to_pandas(html_1409_1809_3)
data_1409_1809 = pd.concat((data_1409_1809_1, data_1409_1809_2, data_1409_1809_3))

data_1909_2309_1 = to_pandas(html_1909_2309_1)
data_1909_2309_2 = to_pandas(html_1909_2309_2)
data_1909_2309_3 = to_pandas(html_1909_2309_3)
data_1909_2309 = pd.concat((data_1909_2309_1, data_1909_2309_2, data_1909_2309_3))


from functools import reduce
dfs = [data_2408_2908, data_2908_0209, data_0309_0709, data_0809_1209, data_1309_1709, data_1409_1809, data_1909_2309]
df_final = reduce(lambda left,right: pd.merge(left,right,on='Name', suffixes=('_x', '')), dfs)
df_final.drop([col for col in df_final.columns if '_y' in col or '_x' in col], axis=1, inplace=True)
df_final = df_final[['Rank'] + [col for col in df_final.columns if col != 'Rank' and col != 'Total'] + ['Total']]
df_final.sort_values('Total', ascending=False, inplace=True)
df_final['Avg'] = df_final['Total'].sum() * 1.0 / len(df_final)
df_final['Rank'] = range(1, len(df_final)+1)
df_final.to_excel('pmhr_data.xls', index=None)
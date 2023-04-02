#!/usr/bin/env python
# coding: utf-8
import os
import pandas as pd
import streamlit as st
from util.dat_edit import dat_edit
from util.preprocess_dat import preprocess_dat

# config
version = 'v0.2'
about = f""" Developed by [Ala-Alsanea](https://github.com/Ala-Alsanea) - {version}"""
pd.options.display.max_columns = 999
st.set_page_config(layout='wide',
                   menu_items={'About': about})

st.header('parsing .dat file')

#  load .dat file and parse it
fileDat = st.file_uploader('pick (.dat) file', type=[
                           'dat'], accept_multiple_files=True)

first_lines = []
if fileDat == None or fileDat == []:
    st.caption(about)
    exit()

for i, item in enumerate(fileDat):
    first_lines.append(dat_edit(item))

first_lines_df = pd.DataFrame()
st.write('#### Metadata')
for i, item in enumerate(zip(first_lines, fileDat)):
    first_lines_df[item[1].name] = str(item[0]).split(',')


st.table(first_lines_df)

tableDat_dict = {}
year = []
month = []


for i, item in enumerate(fileDat):
    # ? load from DataEdited
    tableDat_dict.update({item.name: preprocess_dat(item)})

for key, item in tableDat_dict.items():
    # st.write(item)
    # exit()
    # ? change type of all col except TIMESTAMP and index
    for col in item.columns:
        if col != 'TIMESTAMP' or col != 'index':
            item[col] = pd.to_numeric(
                item[col], errors='ignore')

# ? change type of TIMESTAMP
    item['TIMESTAMP'] = pd.to_datetime(
        item['TIMESTAMP'])


# ? separate year and month from Timestamp
    item['year'] = [item.TIMESTAMP.iloc[j -
                                        1].year for j in item.index.tolist()]
    item['month'] = [item.TIMESTAMP.iloc[j -
                                         1].month for j in item.index.tolist()]

# ? show data
    if st.checkbox(f'show all data for __{key}__'):
        st.write(f'#### {key}')
        st.dataframe(item)

    year.append(item.year.unique())
    month.append(item.month.unique())

# ? split the arrays inside year and month into one array for each
year = [j for i in year for j in i]
year = set(year)

month = [j for i in month for j in i]
month = set(month)

st.write(
    """
----
### Query by date
"""
)


selectYear = ''
selectMonth = ''
if st.checkbox('enable year selection', key=100, value=True):
    selectYear = st.selectbox('select year', year)

    if st.checkbox('enable month selection', key=101):
        selectMonth = st.selectbox('select month', month)

st.write(
    """
----
#### Query : ({} - {})
""".format(selectMonth, selectYear)
)

query_dict = {}
for key, item in tableDat_dict.items():

    st.write(f'#### {key}')

    query = item[(item['year'] == selectYear)]

    query = query[query['month'] == selectMonth] if (
        selectMonth in item['month'].values) else query

    query_dict.update({key: query})
    st.write(query)
    # st.write(query_dict)


# ? extract columns
cols = []
for item in tableDat_dict.values():
    cols.append(item.columns)

cols = [j for i in cols for j in i]
cols = set(cols)


st.write(
    """
----
### Selected columns
"""
)

selectedCols = []
reset = False


st.sidebar.header(f'column No. {len(cols)}')
for i, value in enumerate(sorted(cols)):
    with st.sidebar:
        if st.checkbox(value, key=200+i, value=reset):
            selectedCols.append(value)

st.table(selectedCols)


# ? get results
result = pd.DataFrame(selectedCols, columns=['columns'])

for key, item in query_dict.items():

    if len(selectedCols) != 0:
        for i in selectedCols:
            # st.write(f'{i} - __{key}__')
            # st.write({'Avg': item[i].mean(), 'Sum': item[i].sum()})
            # result[key] = {'Avg': item[i].mean(), 'Sum': item[i].sum()}
            result[key + " \n __Avg__"] = item[i].mean()
            result[key + ' \n __Sum__'] = item[i].sum()


st.write(
    """
    #### Result :
        """
)
st.table(result)
# st.line_chart(result)

exit()

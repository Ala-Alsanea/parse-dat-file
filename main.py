#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import streamlit as st

version = 'v0.1'
about = f""" Developed by [Ala-Alsanea](https://github.com/Ala-Alsanea) - {version}"""
# config
pd.options.display.max_columns = 999
st.set_page_config(layout='wide',
                   menu_items={'About': about})

st.header('parsing .dat file')

#  load .dat file and parse it
fileDat = st.file_uploader('pick (.dat) file', type=['dat'])

if fileDat == None:
    st.caption(about)
    exit()

lines = fileDat.readlines()
lines.pop(0)

with open("DatEdited/"+fileDat.name, "w") as f:
    for line in lines:
        # st.write(line)
        # if line.strip("\n") != delLine:
        f.write(line.decode('utf-8'))
fileDat.close()

# ? show data from DataEdited
tableDat = pd.read_csv("DatEdited/"+fileDat.name)
tableDat.drop(0, inplace=True)
tableDat.drop(1, inplace=True)

# set index
tableDat['index'] = range(1, len(tableDat)+1)
tableDat.set_index('index', inplace=True)

# replace missing vlans with 0
tableDat = tableDat.replace('NAN', 0)

for col in tableDat.columns:
    if col != 'TIMESTAMP' or col != 'index':
        tableDat[col] = pd.to_numeric(tableDat[col], errors='ignore')


tableDat['TIMESTAMP'] = pd.to_datetime(tableDat['TIMESTAMP'])

headShow = st.number_input('Head show', value=5)
st.write(
    """
----
### first {1} rows of  ({0})
""".format(fileDat.name, headShow)
)

st.dataframe(tableDat.head(int(headShow)))


st.write(
    """
----
### Query by date
"""
)

# ? separate year and month from Timestamp
tableDat['year'] = [tableDat.TIMESTAMP.iloc[i -
                                            1].year for i in tableDat.index.tolist()]
tableDat['month'] = [tableDat.TIMESTAMP.iloc[i -
                                             1].month for i in tableDat.index.tolist()]
# tableDat['year'] = pd.to_datetime(tableDat['year'])

selectYear = ''
year = tableDat.year.unique()
if st.checkbox('enable year selection', key=100):
    selectYear = st.selectbox('select year', year)

selectMonth = ''
month = tableDat.month.unique()
if st.checkbox('enable month selection', key=101):
    selectMonth = st.selectbox('select month', month)

st.write(
    """
----
#### Query : ({} - {})
""".format(selectMonth, selectYear)
)

query = tableDat[(tableDat['year'] == selectYear)] if (
    selectYear in tableDat['year'].values) else tableDat

query = query[query['month'] == selectMonth] if (
    selectMonth in query['month'].values) else query

st.write(query)

# ? avg and sum
st.write(
    """
----
### Selected columns
"""
)

selectedCols = []
reset = False
# st.button('reset', on_click=)
# st.write(reset)
# col1, col2, col3 = st.columns(3)

# for i in zip(query.columns, range(1, len(query.columns))):
#     if i[1] < int(len(query.columns)/3):
#         with col1:
#             if st.sidebar.checkbox(i[0], key=200+i[1], value=reset):
#                 selectedCols.append(i[0])

#     if (i[1] <= int(len(query.columns)/3)+int(len(query.columns)/3)
#         and
#             i[1] >= int(len(query.columns)/3)):
#         with col2:
#             if st.sidebar.checkbox(i[0], key=200+i[1], value=reset):
#                 selectedCols.append(i[0])

#     if i[1] > int(len(query.columns)/3)+int(len(query.columns)/3):
#         with col3:
#             if st.sidebar.checkbox(i[0], key=200+i[1], value=reset):
#                 selectedCols.append(i[0])


for i in zip(query.columns, range(1, len(query.columns))):
    with st.sidebar:
        if st.checkbox(i[0], key=200+i[1], value=reset):
            selectedCols.append(i[0])


# st.table(selectedCols)
# st.write(query['ETo_24Hrs'])
result = pd.DataFrame(selectedCols, columns=['columns'])


if len(selectedCols) != 0:
    dict1 = {'Avg': [], 'Sum': []}
    for i in selectedCols:
        # dict1['Avg'].append({i: query[i].mean()})
        dict1['Avg'].append(query[i].mean())
        dict1['Sum'].append(query[i].sum())

    result['Avg'] = dict1['Avg']
    result['Sum'] = dict1['Sum']

    st.write(
        """
        #### Result :
            """
    )
    st.table(result)
    # st.line_chart(result)

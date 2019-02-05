# importing required modules
import PyPDF2
import numpy as np
import re
import pandas as pd
import datetime

# creating a pdf file object
pdfFileObj = open('RD-Mortality-Report_2015-18-180531.pdf', 'rb')

# creating a pdf reader object
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

# saving the number of pages in pdf file
num_pages = pdfReader.numPages
page_data = []


def dataWrangling(i):
    test = []
    # creating a page object
    pageObj = pdfReader.getPage(i)

    # extracting text from page
    page = pageObj.extractText()
    page = page.encode('utf-8')
    page = page.replace("6/4/2018\n", "")
    page = page.replace("JAN", "01")
    page = page.replace("FEB", "02")
    page = page.replace("MAR", "03")
    page = page.replace("APR", "04")
    page = page.replace("MAY", "05")
    page = page.replace("JUN", "06")
    page = page.replace("JUL", "07")
    page = page.replace("AGO", "08")
    page = page.replace("SEP", "09")
    page = page.replace("OCT", "10")
    page = page.replace("NOV", "11")
    page = page.replace("DEC", "12")
    page = re.sub("\D", " ", page)
    page = re.sub("                                                                                          ", "", page)
    page = page.split()

    page_data.append(page)


    for j in range(5, len(page), 5):
        test.append(page[(j-5):j])
        if (int(page[j]) >= 2000):
            break

    test = np.array(test)
    df = pd.DataFrame(test, columns=['month', '2015', '2016', '2017', '2018'])
    df['day'] = df.index
    cols = ['month', 'day', '2015', '2016', '2017', '2018']
    df = df[cols]
    #print(df)
    #select_rows = df.iloc[1:, 0]
    df['day'] = df.index
    month = int(df.iloc[0:1, 0])
    df['month'] = month
    df = df.drop(df.index[0])
    #print(df)

    k = 0
    if month == 2:
        k = int(df.iloc[28, [2]])
        df.iloc[28, 2:6] = 0
        df.iloc[28, 3] = k
    return df

x = []
for i in range(num_pages):
    x.append(dataWrangling(i))
    #print(x[i])

df_of = pd.concat([x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9], x[10], x[11]])
#print(df_of)

df_off = pd.melt(df_of, id_vars=['month', 'day'], var_name='year', value_name='deaths')
#print(df_off)
#print(df_off.index)

date_ymd = []

for i in range(len(list(df_off.index))):
    if (int(df_off.iloc[i, [0]]) == 2 and int(df_off.iloc[i, [1]]) == 29 and (int(df_off.iloc[i, [2]]) == 2015 or int(df_off.iloc[i, [2]]) == 2017 or int(df_off.iloc[i, [2]]) == 2018)):
            date_ymd.append(0)
            continue
    date_ymd.append(datetime.date(int(df_off.iloc[i, [2]]), int(df_off.iloc[i, [0]]), int(df_off.iloc[i, [1]])))

df_off['date'] = date_ymd
df_official = df_off.drop(['month', 'year', 'day'], axis = 1)
cols = ['date', 'deaths']
df_official = df_official[cols]

print(df_official)




# closing the pdf file object
pdfFileObj.close()

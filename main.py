# Certificate in Data Analytics - UCD
# Selina Bayly March 2021

# Imports
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import urllib.request

##################################################
# Import Datasets
##################################################

##################################################
# Import Book Order from URL
##################################################

# Take in Website
Reading_Order_Source = urllib.request.urlopen('https://www.bookseriesinorder.com/discworld/')

# Make readable
Reading_Order_All = BeautifulSoup(Reading_Order_Source,'lxml')

# Take the first table, which is
# Publication Order of Discworld Books
Reading_Order = Reading_Order_All.find('table')

# Loop through Table to extract title and year

build_table = []
counter = 0
for tr in Reading_Order.find_all('tr'):
    counter = counter + 1
    book_id = counter
    title_elem = tr.find('td', class_='booktitle').text
    year_elem = tr.find('td',class_ = 'bookyear').text
    build_table.append((book_id,title_elem,year_elem))

# Create table and then remove brackets from year
cols = ['Book_Id','Book_Title','Book_Year']
DW_Publication_Order = pd.DataFrame(build_table, columns=cols)

DW_Publication_Order['Book_Year'] = DW_Publication_Order['Book_Year'].str.replace('(','')
DW_Publication_Order['Book_Year'] = DW_Publication_Order['Book_Year'].str.replace(')','')

print(DW_Publication_Order.head())

##################################################
# Import Character Order from XLSX
##################################################

DW_Character_Order = pd.read_excel(r'DW_Public_Genre_Order.xlsx')

##################################################
# Do data checks between two DW dataframes
# Year, Title
##################################################

# Check number of columns in the two tables = 41
print(DW_Publication_Order.shape)
print(DW_Publication_Order.columns)
print(DW_Character_Order.shape)
print(DW_Character_Order.columns)

# Merge the tables and compare columns
DW_Orders_Merge = pd.merge(DW_Publication_Order,DW_Character_Order,how='inner',left_on = 'Book_Id',right_on = 'DW_ID')
print(DW_Orders_Merge.shape)
print(DW_Orders_Merge.columns)
print(DW_Orders_Merge.dtypes) # find out year / publication_date

# Check title names
for i in DW_Orders_Merge.itertuples():
    if i[2] != i[5]:
        print('Title ',i[0],' (',i[2],') not equal (',i[5],')')

# Check publication year
for i in DW_Orders_Merge.itertuples():
    if str(i[3]) != str(i[10]):
        print('Year ',i[0],' (',i[3],') not equal (',i[10],')')

# Result:
# Titles matching, but one publication year is incorrect:
# Year  36  ( 2007 ) not equal ( 2009 )
# Having checked online, 2009 is correct, so need to replace date on Merge and Publication Order
#DW_Publication_Order('Book_Year')[36] = '2009'
DW_Orders_Merge.at[36,'Book_Year'] = '2009'
DW_Publication_Order.loc[36,'Book_Year'] = '2009'

# Check publication year
print('Recheck whether years match')

for i in DW_Orders_Merge.itertuples():
    if str(i[3]) != str(i[10]):
        print('Year ',i[0],' (',i[3],') not equal (',i[10],')')

##################################################
# Plot a timeline of the books being published
##################################################
plt.plot(DW_Orders_Merge['Short_Title'],DW_Orders_Merge['Book_Year'], marker="*", linestyle="-", color="r")
plt.title("Timeline of Publication")
plt.xticks(rotation=45)
plt.xlabel("Publication Title")
plt.ylabel("Book Year")

plt.show()



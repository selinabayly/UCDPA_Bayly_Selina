
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
Reading_Order_All = BeautifulSoup(Reading_Order_Source, 'lxml')

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
    year_elem = tr.find('td', class_='bookyear').text
    build_table.append((book_id, title_elem, year_elem))

# Create table and then remove brackets from year
cols = ['Book_Id', 'Book_Title', 'Book_Year']
DW_Publication_Order = pd.DataFrame(build_table, columns=cols)

DW_Publication_Order['Book_Year'] = DW_Publication_Order['Book_Year'].str.replace('(', '')
DW_Publication_Order['Book_Year'] = DW_Publication_Order['Book_Year'].str.replace(')', '')

##################################################
# Import Character Order from XLSX
# For transportability of code, changing to CSV
##################################################

DW_Character_Order = pd.read_csv(r'DW_Public_Genre_Order.csv')

##################################################
# Do data checks between two DW dataframes
# Year, Title
##################################################

# Check number of columns in the two tables = 41
# Showing shape, columns and data types
print('DW_Publication_Order shape: ', DW_Publication_Order.shape)
print('DW_Publication_Order dtypes: ', DW_Publication_Order.dtypes)
print('DW_Character_Order shape: ', DW_Character_Order.shape)
print('DW_Character_Order dtypes: ', DW_Character_Order.dtypes)

# Convert Book Year to numeric to make it easier for comparison and making bins on graphs
DW_Publication_Order['Book_Year'] = DW_Publication_Order.Book_Year.astype('int64')
print('DW_Character_Order dtypes: ', DW_Publication_Order.dtypes)

# Merge the tables and compare columns
DW_Orders_Merge = pd.merge(DW_Publication_Order,
                           DW_Character_Order,
                           how='inner',
                           left_on='Book_Id',
                           right_on='DW_ID')
print('DW_Orders_Merge shape:', DW_Orders_Merge.shape)
print('DW_Orders_Merge dtypes:', DW_Orders_Merge.dtypes)

# Check title names
for i in DW_Orders_Merge.itertuples():
    if i[2] != i[5]:
        print('Title ', i[0], ' (', i[2], ') not equal (', i[5], ')')

# Check publication year
for i in DW_Orders_Merge.itertuples():
    if i[3] != i[10]:
        print('Year ', i[0], ' (', i[3], ') not equal (', i[10], ')')

# Result:
# Titles matching, but one publication year is incorrect:
# Year  36  ( 2007 ) not equal ( 2009 )
# Having checked online, 2009 is correct, so need to replace date on Merge and Publication Order
# DW_Publication_Order('Book_Year')[36] = '2009'

DW_Orders_Merge.at[36, 'Book_Year'] = 2009
DW_Publication_Order.loc[36, 'Book_Year'] = 2009

# Check publication year
print('Recheck whether years match')

for i in DW_Orders_Merge.itertuples():
    if i[3] != i[10]:
        print('Year ', i[0], ' (', i[3], ') not equal (', i[10], ')')

##################################################
# Plot a timeline of all the books being published
##################################################
x1 = DW_Orders_Merge['Book_Year']
y1 = DW_Orders_Merge['Display_Title']

# Plot the line graph
plt.figure('Timeline of Publication', figsize=(12, 10))
plt.plot(x1, y1, marker="o", linestyle="-", color="b")
plt.title('Timeline of Publication of Full Series')
plt.xticks(rotation=45)
plt.xticks(np.arange(min(x1), max(x1)+1, 1.0))
plt.tight_layout()
plt.xlabel("Publication Year")
plt.ylabel("Book Title")

#plt.show()

################################################################
# Plot a timeline of all the books being published by character
################################################################

# Find out how many Characters (Genres) there are
print('All the Genres')

# Print out the Characters so that we can extract each to its own dataframe
print(pd.value_counts(DW_Orders_Merge.Genre))

# Create the dataframes
DW_Orders_Merge_CW = DW_Orders_Merge[DW_Orders_Merge['Genre'] == 'The City Watch']
DW_Orders_Merge_Wd = DW_Orders_Merge[DW_Orders_Merge['Genre'] == 'The Wizards/Rincewind']
DW_Orders_Merge_Wh = DW_Orders_Merge[DW_Orders_Merge['Genre'] == 'The Witches']
DW_Orders_Merge_Se = DW_Orders_Merge[DW_Orders_Merge['Genre'] == 'Standalone']
DW_Orders_Merge_Dh = DW_Orders_Merge[DW_Orders_Merge['Genre'] == 'Death']
DW_Orders_Merge_TA = DW_Orders_Merge[DW_Orders_Merge['Genre'] == 'Tiffany Aching & the Nac Mac Feegles']
DW_Orders_Merge_ML = DW_Orders_Merge[DW_Orders_Merge['Genre'] == 'Moist Van Lipwig']

# Get all the x-axes
x2_CW = DW_Orders_Merge_CW['Book_Year']
x2_Wd = DW_Orders_Merge_Wd['Book_Year']
x2_Wh = DW_Orders_Merge_Wh['Book_Year']
x2_Se = DW_Orders_Merge_Se['Book_Year']
x2_Dh = DW_Orders_Merge_Dh['Book_Year']
x2_TA = DW_Orders_Merge_TA['Book_Year']
x2_ML = DW_Orders_Merge_ML['Book_Year']

# Get all the y-axes
y2_CW = DW_Orders_Merge_CW['Display_Title']
y2_Wd = DW_Orders_Merge_Wd['Display_Title']
y2_Wh = DW_Orders_Merge_Wh['Display_Title']
y2_Se = DW_Orders_Merge_Se['Display_Title']
y2_Dh = DW_Orders_Merge_Dh['Display_Title']
y2_TA = DW_Orders_Merge_TA['Display_Title']
y2_ML = DW_Orders_Merge_ML['Display_Title']

# Plot the line graph
plt.figure('Timeline of Publication for Characters', figsize=(12, 10))

plt.plot(x2_CW, y2_CW, marker="o", linestyle="-", color="b", label='City Watch')
plt.plot(x2_Wd, y2_Wd, marker="o", linestyle="-", color="r", label='Wizards')
plt.plot(x2_Wh, y2_Wh, marker="o", linestyle="-", color="g", label='Witches')
plt.plot(x2_Se, y2_Se, marker="o", linestyle="-", color="c", label='Standalone')
plt.plot(x2_Dh, y2_Dh, marker="o", linestyle="-", color="m", label='Death')
plt.plot(x2_TA, y2_TA, marker="o", linestyle="-", color="y", label='Tiffany Aching')
plt.plot(x2_ML, y2_ML, marker="o", linestyle="-", color="brown", label='Moist Van Lipwig')

plt.title('Timeline of Publication for Characters')
plt.xticks(rotation=45)
plt.xticks(np.arange(min(x1), max(x1)+1, 1.0))
plt.tight_layout()
plt.xlabel("Publication Year", fontsize=16)
plt.ylabel("Book Title", fontsize=16)
plt.legend()

plt.show()

################################################################
# Plot a timeline of all the books being published by character
# Adding full series to try and she character/genre crossover
################################################################

# Plot the line graph
plt.figure('Timeline of Publication for Characters including Full Series', figsize=(12, 10))

plt.plot(x1, y1, marker="o", linestyle="-", color="k",label='Full Series')
plt.plot(x2_CW, y2_CW, marker="o", linestyle="-", color="b", label='City Watch')
plt.plot(x2_Wd, y2_Wd, marker="o", linestyle="-", color="r", label='Wizards')
plt.plot(x2_Wh, y2_Wh, marker="o", linestyle="-", color="g", label='Witches')
plt.plot(x2_Se, y2_Se, marker="o", linestyle="-", color="c", label='Standalone')
plt.plot(x2_Dh, y2_Dh, marker="o", linestyle="-", color="m", label='Death')
plt.plot(x2_TA, y2_TA, marker="o", linestyle="-", color="y", label='Tiffany Aching')
plt.plot(x2_ML, y2_ML, marker="o", linestyle="-", color="brown", label='Moist Van Lipwig')

plt.title('Timeline of Publication for Characters including Full Series')
plt.xticks(rotation=45)
plt.xticks(np.arange(min(x1), max(x1)+1, 1.0))
plt.tight_layout()
plt.xlabel("Publication Year", fontsize=16)
plt.ylabel("Book Title", fontsize=16)
plt.legend()

plt.show()

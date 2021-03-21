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

DW_Character_Order = pd.read_csv(r'DW_Public_Character_Order.csv')

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
plt.xticks(np.arange(min(x1), max(x1) + 1, 1.0))
plt.tight_layout()
plt.xlabel("Publication Year")
plt.ylabel("Book Title")

################################################################
# Plot a timeline of all the books being published by character
################################################################

# Find out how many Characters there are
print('All the Characters')

# Print out the Characters so that we can extract each to its own dataframe
print(pd.value_counts(DW_Orders_Merge.Character))

# Save Characters, Colour and Label to list]
DW_Character_List = DW_Orders_Merge[['Character', 'Colour', 'Label']].value_counts().index[:].tolist()
print(DW_Character_List)

# Create function to create dataframes for Character
def create_dw_orders_merge(l_character):
    return_dataframe = DW_Orders_Merge[DW_Orders_Merge['Character'] == l_character]
    return return_dataframe


# Create the dataframes - subset to character and store in array
DW_Orders_Merge_Characters = {}
DW_Orders_Merge_Characters_x = {}
DW_Orders_Merge_Characters_y = {}

# Set up the subsets of data and the x and y axes
for i in range(len(DW_Character_List)):
    DW_Orders_Merge_Characters[i] = create_dw_orders_merge(DW_Character_List[i][0])
    DW_Orders_Merge_Characters_x[i] = DW_Orders_Merge_Characters[i]['Book_Year']
    DW_Orders_Merge_Characters_y[i] = DW_Orders_Merge_Characters[i]['Display_Title']

# Plot the line graph
plt.figure('Timeline of Publication for Characters', figsize=(12, 10))

for i in range(len(DW_Character_List)):
    plt.plot(DW_Orders_Merge_Characters_x[i], DW_Orders_Merge_Characters_y[i],
             marker="o", linestyle="-", color=DW_Character_List[i][1],
             label=DW_Character_List[i][2])

plt.title('Timeline of Publication for Characters')
plt.xticks(rotation=45)
plt.xticks(np.arange(min(x1), max(x1) + 1, 1.0))
plt.tight_layout()
plt.xlabel("Publication Year", fontsize=16)
plt.ylabel("Book Title", fontsize=16)
plt.legend()

################################################################
# Plot a timeline of all the books being published by character
# Adding full series to try and see character crossover
################################################################

# Plot the line graph
plt.figure('Timeline of Publication for Characters including Full Series', figsize=(12, 10))

plt.plot(x1, y1, marker="o", linestyle="-", color="grey", label='Full Series')

for i in range(len(DW_Character_List)):
    plt.plot(DW_Orders_Merge_Characters_x[i], DW_Orders_Merge_Characters_y[i],
             marker="o", linestyle="-", color=DW_Character_List[i][1],
             label=DW_Character_List[i][2])

plt.title('Timeline of Publication for Characters including Full Series')
plt.xticks(rotation=45)
plt.xticks(np.arange(min(x1), max(x1) + 1, 1.0))
plt.tight_layout()
plt.xlabel("Publication Year", fontsize=16)
plt.ylabel("Book Title", fontsize=16)
plt.legend()

################################################################
# Create the previous graph as a scatter instead of linear
################################################################
plt.figure('Timeline of Publication for Characters including Full Series - Scatter', figsize=(12, 10))

plt.scatter(x1, y1, color='grey', marker='o', alpha=0.5, label='Full Series')
for i in range(len(DW_Character_List)):
    plt.scatter(DW_Orders_Merge_Characters_x[i], DW_Orders_Merge_Characters_y[i],
                alpha=0.5,
                color=DW_Character_List[i][1],
                label=DW_Character_List[i][2])

plt.title('Timeline of Publication for Characters including Full Series')
plt.xticks(rotation=45)
plt.xticks(np.arange(min(x1), max(x1) + 1, 1.0))
plt.tight_layout()
plt.xlabel("Publication Year", fontsize=16)
plt.ylabel("Book Title", fontsize=16)
plt.legend()

plt.show()

################################################################
# Plot a timeline of all the books being published by character
# Adding full series to try and she character crossover
################################################################

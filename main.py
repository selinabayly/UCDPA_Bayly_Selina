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

# Loop through Table to extract title and year+

build_table = []
for tr in Reading_Order.find_all('tr'):
    title_elem = tr.find('td', class_='booktitle').text
    year_elem = tr.find('td',class_ = 'bookyear').text
    build_table.append((title_elem,year_elem))

# Create table and then remove brackets from year
cols = ['Book_Title','Book_Year']
DW_Publication_Order = pd.DataFrame(build_table, columns=cols)

DW_Publication_Order['Book_Year'] = DW_Publication_Order['Book_Year'].str.replace('(','')
DW_Publication_Order['Book_Year'] = DW_Publication_Order['Book_Year'].str.replace(')','')

print(DW_Publication_Order.head())



##################################################
# Plot a timeline of the books being published
##################################################
plt.plot(DW_Publication_Order['Book_Year'],DW_Publication_Order['Book_Title'], marker="*", linestyle="-", color="r")
plt.title("Timeline of Publication")
plt.xticks(rotation=90)
plt.xlabel("Book Year")
plt.ylabel("Publication Title")
plt.show()


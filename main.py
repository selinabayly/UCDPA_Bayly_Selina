# Certificate in Data Analytics - UCD
# Selina Bayly March 2021

# Imports
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import urllib.request
import math
import seaborn as sns

# pd.options.display.max_columns = 6
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
print('DW_Publication_Order shape:')
print(DW_Publication_Order.shape)
print('DW_Character_Order shape:')
print(DW_Character_Order.shape)

# Convert Book Year to numeric to make it easier for comparison and making bins on graphs
DW_Publication_Order['Book_Year'] = DW_Publication_Order.Book_Year.astype('int64')

# Merge the tables and compare columns
DW_Orders_Merge = pd.merge(DW_Publication_Order,
                           DW_Character_Order,
                           how='inner',
                           left_on='Book_Id',
                           right_on='DW_ID')
print('DW_Orders_Merge shape:')
print(DW_Orders_Merge.shape)

# We now know we have 41 books to work from.  Any merges / joins with book databases
# should return 41 joins.
# Check title names
print('DW_Orders_Merge - Title and Year check')
for i in DW_Orders_Merge.itertuples():
    if i[2] != i[5]:
        print('Title ', i[0], ' (', i[2], ') not equal (', i[5], ')')

# Check publication year
for i in DW_Orders_Merge.itertuples():
    if i[3] != i[11]:
        print('Year ', i[0], ' (', i[3], ') not equal (', i[11], ')')

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
    if i[3] != i[11]:
        print('Year ', i[0], ' (', i[3], ') not equal (', i[11], ')')

##################################################
# Set common plt arguments and save figure
##################################################


def line_public_timeline(title_name):
    plt.figure(title_name, figsize=(12, 8), linewidth=5, edgecolor='navy')
    plt.title(title_name)
    plt.xticks(rotation=45)
    plt.xticks(np.arange(min(x1), max(x1) + 1, 1.0))
    plt.xlabel("Publication Year", fontsize=12)
    plt.ylabel("Book Title", fontsize=12)
    return title_name


def save_image(title_name):
    plt.get_current_fig_manager().window.showMaximized()
    plt.savefig(title_name + '.png')


##################################################
# Plot a timeline of all the books being published
##################################################
x1 = DW_Orders_Merge['Book_Year']
y1 = DW_Orders_Merge['Display_Title']

# Plot the line graph
save_name = line_public_timeline('Timeline of publication of Discworld series')
plt.plot(x1, y1, marker="o", linestyle="-", color="navy")
save_image(save_name)

################################################################
# Plot a timeline of all the books being published by character
################################################################

# Find out how many Characters there are
print('All the Characters and the number of books per character')
print('Unsorted and then sorted')

# Print out the Characters so that we can extract each to its own dataframe
print(pd.value_counts(DW_Orders_Merge.Character))

# Save Characters, Colour and Label to list and sort
DW_Character_List = DW_Orders_Merge[['Character', 'Colour', 'Label']].value_counts().index[:].tolist()
print(DW_Character_List)
DW_Character_List.sort()
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

# Plot the line graph - as one of the character subsets is standalone, a line
# graph doesn't fit; a scatter will work better.  Only the series of characters
# should have lines.
save_name = line_public_timeline('Timeline of publication for Discworld characters')
print('****', DW_Character_List)
for i in range(len(DW_Character_List)):
    if i == 2:
        plt.scatter(DW_Orders_Merge_Characters_x[i], DW_Orders_Merge_Characters_y[i],
                    alpha=1,
                    color=DW_Character_List[i][1],
                    label=DW_Character_List[i][2])
    else:
        plt.plot(DW_Orders_Merge_Characters_x[i], DW_Orders_Merge_Characters_y[i],
                 marker="o", linestyle="-", color=DW_Character_List[i][1],
                 label=DW_Character_List[i][2])
plt.legend()
save_image(save_name)

################################################################
# Plot a timeline of all the books being published by character
# Adding full series to try and see character crossover
################################################################

# Plot the line graph
save_name = line_public_timeline('Timeline of publication for Discworld characters including full Series')

plt.plot(x1, y1, marker="o", linestyle="-", color="grey", label='Full Series')

for i in range(len(DW_Character_List)):
    plt.plot(DW_Orders_Merge_Characters_x[i], DW_Orders_Merge_Characters_y[i],
             marker="o", linestyle="-",
             color=DW_Character_List[i][1],
             label=DW_Character_List[i][2])
plt.legend()
save_image(save_name)

################################################################
# Create the previous graph as a scatter instead of linear
################################################################
save_name = line_public_timeline('Timeline of publication for Discworld characters including full Series - Scatter')

plt.scatter(x1, y1, color='grey', marker='o', alpha=0.5, label='Full Series')

for i in range(len(DW_Character_List)):
    plt.scatter(DW_Orders_Merge_Characters_x[i], DW_Orders_Merge_Characters_y[i],
                alpha=0.95,
                color=DW_Character_List[i][1],
                label=DW_Character_List[i][2])
plt.legend()
save_image(save_name)

###################################################################
# Review other files to see which ones will give the best results.
###################################################################

###################################################################
# Review book_data_kaggle_subset
###################################################################

print('######################################')
print('# book_data_kaggle_subset')
print('######################################')

book_data_kaggle = pd.read_csv(r'book_data_kaggle_subset.csv')
print('book_data_kaggle - dtypes and shape')
# print(book_data_kaggle.dtypes)
print(book_data_kaggle.shape)

# Print subset of book_data_kaggle and see what type of structure it is

print(type(book_data_kaggle.iloc[:, [0, 9]]))
print(book_data_kaggle.iloc[:5, [0, 9]])

# print(type(DW_Orders_Merge.iloc[:, [1, 5]]))
# print(DW_Orders_Merge.iloc[:5, [1, 5]])

# Merge Kaggle dataset with characters dataset to see if the dataset
# all the books on it.
book_data_kaggle_join = pd.merge(DW_Orders_Merge, book_data_kaggle,
                                 how='inner', left_on=('Book_Title', 'Author'),
                                 right_on=('book_title', 'book_authors'))
# Check index etc.
print('book_data_kaggle_join - dtypes, shape, head, index')
# print(book_data_kaggle_join.dtypes)
print(book_data_kaggle_join.shape)
print(book_data_kaggle_join.head())
print('')
print(book_data_kaggle_join.iloc[:5, [1, 4, 5, 15, 24]])

# Set index to author and extract based on Terry Pratchett
# Don't need to set index anymore because merging on author
# and only author on DW_Orders_Merge is Terry Pratchett
# book_data_kaggle_join.set_index('Author', inplace=True)
# book_data_kaggle_TP = book_data_kaggle_join.loc[['Terry Pratchett']]

# Check for missing data
print('kaggle missing data?')
print(book_data_kaggle_join.isnull().sum())

# Only NaN's on dataframe re book_edition and book_isbn, which are not required.
# Can now check data for only columns that are of interest.  Not doing this anymore
# as gave problems with remove duplicates process.  Will use iloc later on when
# analysing data.

# book_data_kaggle_TP_subset = book_data_kaggle_TP.iloc[:, [7, 1, 9, 11, 12, 13, 19, 20, 21, 22]]
# print('After i-loc on kaggle_TP')
# print(book_data_kaggle_TP_subset.shape)

# Index on Book_ID so that we can drop duplicates
# Don't need to set the other index because didn't set index in the first place.
# book_data_kaggle_TP_subset.set_index('Book_ID', inplace=True)

# Drop Duplicates from dataset
print('kaggle join')
print(book_data_kaggle_join.iloc[:, [1]])
print('Drop Duplicates')
book_data_kaggle_join.drop_duplicates(subset='Book_Title', keep=False, inplace=True)
print(book_data_kaggle_join.shape)
print(book_data_kaggle_join.head())

# Not using file - insufficient data

###################################################################
# Second File books.csv
###################################################################

print('######################################')
print('# books')
print('######################################')

books = pd.read_csv(r'books.csv')

# Note: 4 rows had an additional comma in the file.  Was saved as CSV
# from XLSX because of other xls issues.  Choosing to delete 4 records
# as they are not required anyway.
print('')
print('books - dtypes and shape')
# print(books.dtypes)
print(books.shape)

# Print subset of books and see what type of structure it is

print(books.iloc[:5, [1, 2]])

# print(DW_Orders_Merge.iloc[:5, [1, 5]])

# Merge books dataset with characters dataset to see if the dataset
# all the books on it.
books_join = pd.merge(DW_Orders_Merge, books,
                      how='inner', left_on=('Book_Title', 'Author'),
                      right_on=('title', 'authors'))

# Results are zero.  The Book_Title is made up of the following:
# Witches Abroad (Discworld  #12; Witches #3)                       Terry Pratchett
# Witches Abroad (Discworld  #12)                                   Terry Pratchett
# Small Gods (Discworld  #13)                                       Terry Pratchett
# Wintersmith (Discworld  #35; Tiffany Aching  #3)                  Terry Pratchett
# The Color of Magic (Discworld  #1; Rincewind  #1)	                Terry Pratchett
# The Truth (Discworld  #25; Industrial Revolution  #2)	            Terry Pratchett
# A Hat Full of Sky (Discworld  #32; Tiffany Aching  #2)            Terry Pratchett
# The Last Hero (Discworld #27; Rincewind #7)	                    Terry Pratchett/Paul Kidby
# Wyrd Sisters (Discworld  #6; Witches #2)	                        Terry Pratchett
# The Light Fantastic (Discworld  #2; Rincewind #2)	                Terry Pratchett
# Equal Rites (Discworld  #3; Witches  #1)	                        Terry Pratchett
# Moving Pictures (Discworld  #10; Industrial Revolution  #1)   	Terry Pratchett
# Darwin's Watch (The Science of Discworld  #3)	                    Terry Pratchett/Ian Stewart/Jack Cohen
# Reaper Man (Discworld  #11; Death  #2)	                        Terry Pratchett
# Where's My Cow? (Discworld  #34.5)	                            Terry Pratchett/Melvyn Grant
# Lords and Ladies (Discworld  #14; Witches #4)	                    Terry Pratchett
# Guards! Guards! (Discworld  #8)	                                Terry Pratchett
# Hogfather (Discworld  #20; Death  #4)	                            Terry Pratchett
# The Amazing Maurice and His Educated Rodents (Discworld  #28)	    Terry Pratchett
# Going Postal (Discworld  #33)	                                    Terry Pratchett
# The Last Hero: A Discworld Fable (Discworld  #27)	                Terry Pratchett/Paul Kidby
# Carpe Jugulum (Discworld #23; Witches #6)	                        Terry Pratchett

# Decision made not to use this file.  There are only 22 results and 41 are expected, so
# data is incomplete.
# I could use ISIN function, but there is no point as the data is incomplete
# Will move onto next file.

###################################################################
# Third file Goodreads_TP_DW.csv
###################################################################

print('######################################')
print('# Goodreads_TP_DW')
print('######################################')

Goodreads_TP_DW = pd.read_csv(r'Goodreads_TP_DW.csv')
print('')
print('Goodreads_TP_DW - dtypes and shape')
# print(Goodreads_TP_DW.dtypes)
print(Goodreads_TP_DW.shape)

# Print subset of Goodreads_TP_DW and see what type of structure it is

print(type(Goodreads_TP_DW.iloc[:, [2, 3]]))
print(Goodreads_TP_DW.iloc[:5, [0, 9]])

# print(type(DW_Orders_Merge.iloc[:, [1, 5]]))
# print(DW_Orders_Merge.iloc[:5, [1, 5]])

# Merge Goodreads_TP_DW dataset with characters dataset to see if the dataset
# all the books on it.
Goodreads_TP_DW_join = pd.merge(DW_Orders_Merge, Goodreads_TP_DW,
                                how='inner', left_on=('Book_Title', 'Author'),
                                right_on=('Title', 'Author'))
print(Goodreads_TP_DW_join)

# There are only two results out of 41 because of the Title structure.
# Not using file. Moving onto the next!

###################################################################
# Review second books.csv file - from Archive.zip, so renaming
# archive_books.csv
###################################################################

print('######################################')
print('# archive_books')
print('######################################')

print('archive_books - dtypes and shape')

archive_books = pd.read_csv(r'archive - books.csv')
print(archive_books.dtypes)
# print(archive_books.shape)

# Print subset of datasets to be merged
# print(archive_books.iloc[:5, [7, 9]])

# print(DW_Orders_Merge.iloc[:5, [1, 5]])

# Merge archive_books dataset with characters dataset to see if the dataset
# all the books on it.
archive_books_join = pd.merge(DW_Orders_Merge, archive_books,
                              how='inner', left_on=('Book_Title', 'Author'),
                              right_on=('original_title', 'authors'))

print('Missing Data? - DW_Orders_Merge:', len(DW_Orders_Merge),
      'archive_books_join:', len(archive_books_join),
      'Missing:', len(DW_Orders_Merge)-len(archive_books_join))

# Find out which books are missing by doing outer join between merged file
# (missing 2) and DW_Orders_Merge
check_for_missing_books = pd.merge(DW_Orders_Merge, archive_books_join,
                                   how='outer', on=('Book_Title', 'Author'))
NaN_columns = check_for_missing_books.columns[check_for_missing_books.isna().any()].to_list()
# print('Columns missing data',NaN_columns)

# Find the missing books based on the title and author - the keys used for the merge
missing_books = check_for_missing_books[check_for_missing_books['original_title'].isna()]
print('Missing books are:')
print(missing_books.iloc[:, [1, 5]])

# Try and find these books on archive_books - checked in CSV file for confirmation
books_found = archive_books.isin([missing_books.iloc[0, 5], missing_books.iloc[1, 5]])
print('archive')
print(archive_books.iloc[[4564, 5098], [7, 9]])
print('found')
print(books_found.iloc[[4564, 5098], [7, 9]])

# The Last Hero matched, but is joint authorship so didn't show up.  Amazing Maurice has a
# space at the end, so it didn't show up.  If I add the space, it will.
books_found = archive_books.isin(['The Last Hero', 'The Amazing Maurice and His Educated Rodents '])
print('archive')
print(archive_books.iloc[[4564, 5098], [7, 9]])
print('found')
print(books_found.iloc[[4564, 5098], [7, 9]])

# As I couldn't find both and need to add them, I chose to use a different option for finding the
# missing records.
match1 = archive_books.loc[archive_books.original_title.str.contains('The Last Hero', na=False)]
match2 = archive_books.loc[archive_books.original_title.str.contains('Amazing Maurice', na=False)]
print('match1')
print(match1.iloc[:, [0, 1, 7, 9]], match1.index)
print('match2')
print(match2.iloc[:, [0, 1, 7, 9]], match2.index)
print('')

# As both missing records are to be found, they need to be updated so that they'll match
#                          #authors                                 original_title
# 4564              Terry Pratchett  The Amazing Maurice and His Educated Rodents  - update original title
# 5098  Terry Pratchett, Paul Kidby                                  The Last Hero - update author

# Update 4564 authors with Author from DW_Orders_Merge
archive_books.at[match2.iloc[0, 0]-1, 'original_title'] = missing_books.iloc[1, 1]

# Update 5098 original_title with Book_Title from DW_Orders_Merge
archive_books.at[match1.iloc[0, 0]-1, 'authors'] = missing_books.iloc[0, 5]

# Merge the files again and check how many rows.  Should now be 41

archive_books_join = pd.merge(DW_Orders_Merge, archive_books,
                              how='inner', left_on=('Book_Title', 'Author'),
                              right_on=('original_title', 'authors'))

print('Missing Data? - DW_Orders_Merge:', len(DW_Orders_Merge),
      'archive_books_join:', len(archive_books_join),
      'Missing:', len(DW_Orders_Merge)-len(archive_books_join))

#############################################################################
# Analyse Data in archive_books_join
#############################################################################

print('########################################')
print('# Data Analysis of archive_books_join')
print('# Using archive_books join and possibly ')
print('# DW_Orders_Merge for crosschecking')
print('########################################')

# Extract required columns only and sort by character and then publication order
archive_books_join_subset = archive_books_join[['Book_Id', 'Book_Title', 'Book_Year',   # 1 2 3
                                                'Short_Title', 'Display_Title',         # 4 5
                                                'Character', 'Short_Character',         # 6 7
                                                'Order', 'Label', 'Colour',             # 8 9 10 | 11, 12, 13, 14, 15
                                                'ratings_1', 'ratings_2', 'ratings_3', 'ratings_4', 'ratings_5']]
archive_books_join_sort = archive_books_join_subset.sort_values(by=['Character', 'Order'], ignore_index=True)
# Add column for ratings - will assign int64
archive_books_join_sort['Total_Reviews'] = 0

# Loop through dataframe and calculate:
# Total Ratings   -> sum of all 5 ratings
# Average Ratings -> sum (percentage of each rating of the total * the rating)
j = -1
for i in archive_books_join_sort.itertuples():
    j = j + 1
# Total number of ratings
    stars = [i[11], i[12], i[13], i[14], i[15]]
    stars_tot = sum(stars)
    archive_books_join_sort.at[j, 'Total_Reviews'] = stars_tot

# Average Rating
    stars_pc = []
    for k in range(5):
        stars_rate = stars[k] / stars_tot * (k+1)
        stars_pc.insert(k, stars_rate)

    stars_pc_tot = sum(stars_pc)
# Only allocating column here as it was being allocated int64 and need float64
    archive_books_join_sort.at[j, 'Average_Rating'] = round(stars_pc_tot, 2)

#############################################################################
# Get Mean for Ratings and Reviews
#############################################################################

archive_books_character_averages = archive_books_join_sort.groupby(['Character']).mean()
# Rounding to whole number, but gave .0, so using floor function to remove.
Discworld_Average_Reviews = math.floor(round(archive_books_join_sort['Total_Reviews'].mean(), 0))
Discworld_Average_Rating = round(archive_books_join_sort['Average_Rating'].mean(), 2)

#############################################################################
# Basic set up for bar graphs and create a list of colours for the bar graph
#############################################################################


def bar_books(title_name):
    plt.figure(title_name, figsize=(12, 8), linewidth=5, edgecolor='navy')
    plt.title(title_name)
    plt.suptitle(title_name)
    return title_name


def extract_colours(colour_details):
    colour_details.sort()
    temp_colour = []
    for z in range(len(colour_details)):
        temp_colour.insert(z, colour_details[z][1])
    return temp_colour


#############################################################################
#                       At Character Level
# Create a bar graph of the average ratings per book - 2 side by side graphs
# Grouping by Label, which is a shortened version of Character
#############################################################################
save_name = bar_books('Ratings & Reviews of the Discworld Series')

character_rating = archive_books_join_sort.groupby('Label').agg(np.mean)['Average_Rating']

colour_list = extract_colours(archive_books_join_sort[['Label', 'Colour']].value_counts().index[:].tolist())
plt.subplot(211)
plt.xlabel("Discworld Character sub-series", fontsize=12)
plt.ylabel("Average Rating per Book", fontsize=12)
for y in range(len(character_rating)):
    print(character_rating.index)
    print(y, character_rating.index[y])
    plt.text(y, 1, round(character_rating[y], 2), ha='center', color='grey')
plt.yticks(np.arange(0, 5, 0.25))
plt.plot([0, 7], [4.15, 4.15], color='grey', label='Average Rating')
plt.bar(x=character_rating.index, height=character_rating, color=colour_list)
plt.legend()

character_reviews = archive_books_join_sort.groupby('Label').agg(np.mean)['Total_Reviews']
plt.subplot(212)
plt.xlabel("Discworld Character sub-series", fontsize=12)
plt.ylabel("Number of Reviews", fontsize=12)
for y in range(len(character_rating)):
    print(character_reviews.index)
    print(y, character_reviews.index[y])
    plt.text(y, 1000, round(character_reviews[y], 2), ha='center', color='grey')
plt.yticks(np.arange(0, 80000, 5000))
plt.plot([0, 7], [59162, 59162], color='grey', label='Average Reviews')
plt.bar(x=character_reviews.index, height=character_reviews, color=colour_list)
plt.legend()
save_image(save_name)

#############################################################################
#                       At Book Level
# Create a bar graph of the average ratings per book - 2 side by side graphs
# Grouping by Label, which is a shortened version of Character
#############################################################################

save_name = bar_books('Ratings & Reviews of the Discworld Books')

character_rating = archive_books_join_sort.groupby('Label').agg(np.mean)['Average_Rating']

colour_list = extract_colours(archive_books_join_sort[['Label', 'Colour']].value_counts().index[:].tolist())
plt.subplot(211)
plt.xlabel("Discworld Character sub-series", fontsize=12)
plt.ylabel("Average Rating per Book", fontsize=12)
for y in range(len(character_rating)):
    print(character_rating.index)
    print(y, character_rating.index[y])
    plt.text(y, 1, round(character_rating[y], 2), ha='center', color='white')
plt.yticks(np.arange(0, 5, 0.25))
plt.plot([0, 7], [4.15, 4.15], color='grey', label='Average Rating')
plt.bar(x=character_rating.index, height=character_rating, color=colour_list)
plt.legend()

character_reviews = archive_books_join_sort.groupby('Label').agg(np.mean)['Total_Reviews']
plt.subplot(212)
plt.xlabel("Discworld Character sub-series", fontsize=12)
plt.ylabel("Number of Reviews", fontsize=12)
for y in range(len(character_rating)):
    print(character_reviews.index)
    print(y, character_reviews.index[y])
    plt.text(y, 1000, round(character_reviews[y], 2), ha='center', color='white')
plt.yticks(np.arange(0, 80000, 5000))
plt.plot([0, 7], [59162, 59162], color='grey', label='Average Reviews')
plt.bar(x=character_reviews.index, height=character_reviews, color=colour_list)
plt.legend()
save_image(save_name)

#############################################################################
# Seaborn Scatterplot to see whether there is a relationship
# between number of reviews per book and average rating - None
# Put an average line marker on x and y axis to denote how much is above
# or below the average
#############################################################################
save_name = 'Seaborn Scatterplot - Relationship between Number of Reviews and Average Rating'
plt.figure(save_name,
           figsize=(12, 8), linewidth=5, edgecolor='navy')
plt.title(save_name)
plt.xticks(rotation=45)
plt.xticks(np.arange(10000, 230000, 20000))
plt.yticks(np.arange(3, 5, 0.2))
plt.xlabel("Number of Reviews", fontsize=12)
plt.ylabel("Average Rate per Book", fontsize=12)
plt.plot([10000, 230000], [4.15, 4.15], color='green', label='Average Rating')
plt.plot([59162, 59162], [3, 5], color='red', label='Average Reviews')
Seaborn_Scatter = sns.scatterplot(x='Total_Reviews', y='Average_Rating', data=archive_books_join_sort, color='navy')
plt.legend()
save_image(save_name)

################################################################
# Get information on the Book Series
################################################################

print('---------------------------------------')
print('|                                     |')
print('|  First Book                : ', DW_Orders_Merge['Book_Year'].min(), ' |')
print('|  Last Book                 : ', DW_Orders_Merge['Book_Year'].max(), ' |')
print('|  Period of Discworld       :   ', DW_Orders_Merge['Book_Year'].max() - DW_Orders_Merge['Book_Year'].min(),
      ' |')
print('|  Number of books           :   ', len(DW_Orders_Merge), ' |')
print('|  Average Books per Year    : ',
      round(len(DW_Orders_Merge) / (DW_Orders_Merge['Book_Year'].max() - DW_Orders_Merge['Book_Year'].min()), 2),
      ' |')
print('|  Discworld_Average_Reviews :', Discworld_Average_Reviews, ' |')
print('|  Discworld_Average_Rating  : ', Discworld_Average_Rating, ' |')
print('|                                     |')
print('---------------------------------------')

#############################################################################
# Render all the graphs
#############################################################################
plt.show()
# end

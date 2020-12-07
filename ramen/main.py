import pandas as pd
import pyreadstat  # need this line for SPSS data otherwise get errors
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# step 1 import data
ramen = pd.read_csv('ramen-ratings.csv')

# step 2 check the data
pd.set_option('max_columns', None) # displaying maximum columns

print(ramen.info()) # check data types start should be a numerical variable

print(ramen.head(3)) # check the first 3 rows

print(ramen.describe(include='all')) # check all describe data

# step 3 displaying a side-by-side boxplot as 1 numerical and 1 categorical variable

ramen['Stars'] = pd.to_numeric(ramen['Stars'], errors='coerce') # stars contains 'NaN', so must have errors='coerce':If ‘coerce’, then invalid parsing will be set as NaN.

print(ramen.groupby(by='Country')['Stars'].median().sort_values(ascending=False)) # displaying median of Stars for the boxplot with ascending orders

bp = sns.boxplot(x=ramen['Country'], y=ramen['Stars']) # set X(categorical) and Y(Numerical)
bp.set_xticklabels(bp.get_xticklabels(), rotation=90) # rotate the labels, must have bp.get_xticklabels() for a lable

plt.show()

# step 4 counting brands each country pareto chart
brands = ramen.groupby(['Country','Brand']).agg({'Review #':'count'}) # agg is aggregation and {'Review #': 'count'} is Different aggregations per column and count (aggregation)
brands = brands.reset_index() # When we reset the index, the old index is added as a column, and a new sequential index is used -> brands is index now
brands = brands.sort_values('Review #', ascending = False)

# Count brand from each country that got review
coun = brands.groupby('Country').agg({'Brand':'count'}).reset_index() # count brands grouped by Country
coun = coun.rename(columns = {'Brand':'Total brand'}) # rename of columns
coun = coun.sort_values(['Total brand', 'Country'], ascending = [False, True]) # sort by an scending order

print(coun.head(10))

plt.bar('Country', 'Total brand', data=coun, color='#77FDA2')
plt.xticks(rotation=90)

# visualization with seaborn
bc = sns.barplot(x='Country', y='Total brand', data=coun, palette='tab10')
bc.set_xticklabels(bc.get_xticklabels(), rotation=90)
plt.show()

# step 5 counting variety each country
variety = ramen.groupby(['Country']).agg({'Variety': 'count'}) # grouped by Country and aggregated with Variety as counting variety of each country
variety = variety.reset_index()
variety = variety.sort_values(['Variety', 'Country'], ascending = [False, True]) #ascending false -> Variety, True -> Country
variety = variety.rename(columns={'Variety': 'Total Variety'}) # this is for the plot

print(variety.head(10)) # check the values with numbers

plotstyle = sns.barplot(x='Country', y='Total Variety', data=variety, palette='hls')
plotstyle.set_xticklabels(plotstyle.get_xticklabels(), rotation=90)
plt.show()


# step 6 counting styles each country with bar and stacked bar

style = ramen.groupby(['Country', 'Style']).agg({'Variety': 'count'})
style = style.reset_index()
style = style.sort_values('Variety', ascending = False)

print(style.head(10))

sType = sorted(style['Style'].unique()) # finding unique styles from all style
print(sType) # check the styles

# count each style by country
'''    
Japan         Bar       0
              Bowl      0
              Box       0
              Can       0
              Cup       0
              ...
United States Box       0
'''
#   DataFrame(data={'name' : set 266(indices imply 266) rows with 0 value}, index= MultipleIndex create multiple index in the dataframe, names are optional)
pattern = pd.DataFrame({'temp' : [0]*266}, index = pd.MultiIndex.from_product([coun['Country'], sType], names=['Country', 'Style']))
print(pattern)

# merge(tables, tables, how(inner join is default), on must be found in both DataFrames) -> merge is similar to SQL joint tables
style = pd.merge(style, pattern, how='outer', on=['Country', 'Style'])

style = style[['Country', 'Style', 'Variety']].fillna(0) #fillna is if there is a missing value in the table, fill as an arbitrary value, in this case is 0 as can't add the value into the temp dataframe

style = pd.merge(style, variety, how = 'left', on = 'Country') # left-join style and variety on country
style = style.sort_values(['Total Variety','Country', 'Style'], ascending = [False,True, True]) # sorting

print(style.head(3))

# create a bar plot based on the above data
bottom_bar = [0]*38 # freq  7(Country)    38 (Style)
bar_color = ['chocolate', 'yellowgreen', 'orange', 'forestgreen', 'peru', 'gold', 'saddlebrown']

# Use for loop for plot bar chart and stack the amount of ramen in each ramen style: creating each bar and overlapping
for i in range(len(sType)):
    plt.bar('Country', 'Variety', data=style[style['Style'] == sType[i]], bottom=bottom_bar, color=bar_color[i]) #not seaborn as legened is mono with seaborn
    # change the bottom_bar to the the amount of current style for the next loop ex) Bar -> Bowl
    bottom_bar = list(np.add(bottom_bar, style[style['Style'] == sType[i]]['Variety']))

plt.title( 'The amount of ramen style in each country', fontsize=14)
plt.ylabel('Number of ramen')
plt.xticks(rotation = 90)
plt.legend(sType) #legend is inner box and describe the bar details
plt.show()

# create a stacked bar based on the data

stacked = style[style['Total Variety'] >= 50].reset_index() # select the total variety is over 50
print(stacked.head(3))
stacked['Percentage'] = stacked['Variety'] * 100 / stacked['Total Variety'] # stacked bar chart needs percentage

print(stacked.describe(include='all'))
#freq  NaN   7(country)    12(style)
bottom_bar = [0]*12
for i in range(len(sType)):
    plt.bar('Country', 'Percentage', data = stacked[stacked['Style'] == sType[i]], bottom = bottom_bar, color = bar_color[i])

    bottom_bar = list(np.add(bottom_bar, stacked[stacked['Style'] == sType[i]]['Percentage']))

plt.title('The percentage of ramen style in countries which have more than or equal to 50 products reviewed', fontsize=14)
plt.ylabel('Per cent')
plt.xticks(rotation = 90)
plt.legend(sType,bbox_to_anchor=(1.1, 1))    # move legend box to the right of the graph
plt.show()
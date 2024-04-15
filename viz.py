import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import geopandas as gpd

df = pd.read_csv('Origin_usa.csv')

# Extract the year portion from the 'Year' column
df['year'] = df['year'].str.split('/').str[0]

df = df.dropna(subset=['year'])

# Convert the 'Year' column to integer type
df['year'] = df['year'].astype(int)

# Filter the DataFrame based on the year condition
filtered_df = df[df['year'].between(2007, 2022)]

grouped_df = filtered_df.groupby('year')['students'].sum()

# Plot the bar graph
grouped_df.plot(kind='bar', figsize=(10, 6))

# Add labels and title
st.title('Number of Students Over Time')
st.bar_chart(grouped_df, y = 'students')



# Student Academic Type over the years
filtered_df = filtered_df.drop(columns=['Unnamed: 5']).reset_index(drop=True)

groupData = filtered_df.groupby(['year','academic_type']).sum().unstack(fill_value=0).reset_index()

# Streamlit app
st.title('Number of Students by Academic Type over Years')

# Plotting
fig, ax = plt.subplots(figsize=(10, 6))
groupData.plot(kind='bar', stacked=True, x='year', ax=ax)

# Add labels and title
plt.xlabel('Year')
plt.ylabel('Number of Students')
plt.title('Number of Students by Academic Type over Years')
plt.legend(title='Academic Type')

# Display plot in Streamlit
st.pyplot(fig)

import geopandas as gpd
origin_df = filtered_df.groupby('origin')['students'].sum().reset_index()

# Load a world shapefile or any other suitable geographical dataset
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Merge the origin DataFrame with the world dataset based on country names
world = world.merge(origin_df, left_on='name', right_on='origin', how='left')

# Fill NaN values with 0
world['students'] = world['students'].fillna(0)

# Plotting
fig, ax = plt.subplots(figsize=(15, 10))

# Plot the world map
world.boundary.plot(ax=ax)

# Plot countries with color representing the number of students
world.plot(column='students', cmap='Blues', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)

# Add title and legend
plt.title('Number of Students by Origin')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.legend(title='Number of Students', loc='lower right')

# Display plot in Streamlit
st.pyplot(fig)
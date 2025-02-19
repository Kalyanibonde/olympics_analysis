import numpy as np
import pandas as pd

def fetch_medal_tally(df, year, country):
    # Drop duplicate medals entries
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    # Filtering based on year and country
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    elif year == 'Overall' and country != 'Overall':
        temp_df = medal_df[medal_df['region'] == country]
    elif year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    else:
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    # Ensure Gold, Silver, Bronze columns exist
    if 'Gold' not in temp_df.columns:
        temp_df['Gold'] = (temp_df['Medal'] == 'Gold').astype(int)
    if 'Silver' not in temp_df.columns:
        temp_df['Silver'] = (temp_df['Medal'] == 'Silver').astype(int)
    if 'Bronze' not in temp_df.columns:
        temp_df['Bronze'] = (temp_df['Medal'] == 'Bronze').astype(int)

    # Aggregate medal counts
    if country != 'Overall':
        x = temp_df.groupby('Year', as_index=False)[['Gold', 'Silver', 'Bronze']].sum().sort_values('Year')
    else:
        x = temp_df.groupby('region', as_index=False)[['Gold', 'Silver', 'Bronze']].sum().sort_values('Gold', ascending=False)

    x['total'] = x[['Gold', 'Silver', 'Bronze']].sum(axis=1)

    return x


def country_year_list(df):
    years = sorted(df['Year'].unique().tolist())
    years.insert(0, 'Overall')

    country = sorted(np.unique(df['region'].dropna().values).tolist())
    country.insert(0, 'Overall')

    return years, country


def data_over_time(df, col):
    nations_over_time = (
        df.drop_duplicates(['Year', col])['Year']
        .value_counts()
        .reset_index()
        .rename(columns={'index': 'Edition', 'Year': col})
        .sort_values('Edition')
    )
    return nations_over_time


def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = temp_df['Name'].value_counts().reset_index(name='Medals').head(15)
    x = x.merge(df[['Name', 'Sport', 'region']], on='Name', how='left').drop_duplicates('Name')

    return x[['Name', 'Medals', 'Sport', 'region']]


def yearwise_medal_tally(df, country):
    temp_df = df.dropna(subset=['Medal']).drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year', as_index=False)['Medal'].count()

    return final_df


def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal']).drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    new_df = temp_df[temp_df['region'] == country]

    heatmap_df = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)

    if heatmap_df.empty:
        return None  # Prevents errors when passing to heatmap visualization

    return heatmap_df


def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Name'].value_counts().reset_index(name='Medals')
    x = x.head(10).merge(df[['Name', 'Sport']], on='Name', how='left').drop_duplicates('Name')

    return x[['Name', 'Medals', 'Sport']]


def weight_v_height(df, sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region']).copy()
    athlete_df['Medal'].fillna('No Medal', inplace=True)

    if sport != 'Overall':
        return athlete_df[athlete_df['Sport'] == sport]
    return athlete_df


def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year', as_index=False)['Name'].count()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year', as_index=False)['Name'].count()

    final = men.merge(women, on='Year', how='left').fillna(0)
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    return final

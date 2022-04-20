#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 21:11:42 2022

@author: Kat
"""

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt


# page setup
st.set_page_config(
    layout="wide"
)

# load dataset and change emissions to numeric
link = 'https://raw.githubusercontent.com/KatHusar/CSE-5544-Final/main/EmissionsSubset.csv'
df_data = pd.read_csv(link)


col = df_data.columns
col =col.rename(None)

#change object type
df_data[col[1:]] = df_data[col[1:]].apply(pd.to_numeric,  errors='coerce')
df_data.sort_values(by=['Country'], inplace=True)

st.title("CSE 5544: Final Project")

# interface


countries = df_data['Country'].tolist()



location = st.multiselect("Select up to 5 countries to explore", (countries), ("United States"))


if len(location) > 5:
     st.warning("You have to select at most 5 countries")
elif len(location)>0:
        url = 'https://raw.githubusercontent.com/carli-werner/cse5544FinalProject/main/cse5544FinalData.csv'
        data_df = pd.read_csv(url,index_col=0, parse_dates=True)
        
        data = data_df.loc[data_df['Country'].isin(location)]
        
        
        
            
        topPanel = st.container()
        with topPanel:
            x = st.slider("Select a year" , 2010, 2019)
            
            data_sub = data.loc[data['Year']==x]
            
            # slider = alt.binding_range(min=2010, max=2019, step=1)
            # select_year = alt.selection_single(name='Year', fields=['Year'],
            #                    bind=slider, init={'Year': 2019})
            title0 = 'Emissions and Population in ' + str(x)
            base = alt.Chart(data_sub, title = title0)
            left = base.encode(
            y=alt.Y('Country:N', axis=None),
            x=alt.X('Emissions:Q',
                    title='Emissions',
                    scale=alt.Scale(domain=(0, 7000000)),
                    sort=alt.SortOrder('descending')), 
            color = 'Country').mark_bar().properties(title='Emissions')
        
            middle = base.encode(
            y=alt.Y('Country:N', axis=None),
            text=alt.Text('Country:N'),).mark_text().properties(width=80)
        
            right = base.encode(
            y=alt.Y('Country:O', axis=None),
            x=alt.X('Population:Q', title='Population',scale=alt.Scale(domain=(0, 400000000))),  color = 'Country').mark_bar().properties(title='Population')


            plot2 = alt.concat(left, middle, right, spacing=5)

            st.altair_chart(plot2, use_container_width = True)
            
            
        midPanel = st.container()
        with midPanel:
            columns = st.columns([4, 0.4])
            with columns[0]:
            
                years = list(data['Year'])
                country = list(data['Country'])
                population = data['Population']
                category = list(np.repeat('Emissions', len(years)))
                
                category.extend(list(np.repeat('Population', len(years))))
                years.extend(years)
                country.extend(country)
                
                values = list(data['Emissions']) + list(data['Population'])
                
                emissions = list(data['Emissions'])
                emissions.extend(emissions)
                populations = list(data['Population'])
                populations.extend(populations)
    
                    
                long_data = pd.DataFrame({'Country': country, 'Year': years, 'Values':values, 'Category':category})
                
                title1 = 'Changes in Emission and Populations Over the Years'
                base = alt.Chart(data).mark_line().encode(
                alt.X('Year:O', axis=alt.Axis(title='Year'))
                ).properties(
                    height = 300
                )
                
                line1 = base.mark_line().encode(
                    alt.Y('Emissions:Q',
                          axis=alt.Axis(title='Emissions')), color='Country:N')
                line2 = base.mark_line(strokeDash=[5,3]).encode(
                   alt.Y('Population:Q',
                         axis=alt.Axis(title='Population')), color='Country:N',
                   )
                lineplot= alt.layer(line1, line2).resolve_scale(
                    y = 'independent'
                )
               
                st.altair_chart(lineplot, use_container_width = True)
            with columns[1]:
                #workaround altair not letting customize legend
                a = 0
                b = 0
                fig, ax = plt.subplots()
                fig.set_size_inches(1, 1, forward=True)
                ax.axis("off")
                ax.plot(a, b, 'k', label='Emissions')
                ax.plot(a, b, 'k--', label='Population')
                fig.legend(loc=[0,0.2], fontsize='x-large', frameon=False)
                st.pyplot(fig)
                            
        sliderPanel = st.container()
        with sliderPanel:
            
            columns = st.columns([4, 0.2, 4])
            with columns[0]:
                values = st.slider('Select years you want to compare', 2010, 2019, (2010, 2019))
            
        bottomPanel = st.container()
        
        with bottomPanel:
            #values = st.slider('Select years you want to compare', 2010, 2019, (2010, 2019))
            columns = st.columns([4, 0.2, 5])
            
            
            with columns[0]:
                
                
                
                year1 = values[0]
                year2 = values[1]
                years2 = [year1, year2]
                data_filtered = data[data['Year'].isin(years2)]
                
                temp1 = data_filtered[data_filtered['Year'] == year1]
                temp2 = data_filtered[data_filtered['Year'] == year2]
                l2 = list(temp2['Emissions'])
                l1 = list(temp1['Emissions'])
                changes = list()
                for i in range(len(l1)):
                    changes.append((l2[i] - l1[i])/l1[i]*100)

                countries = temp1['Country']
                emission_changes = pd.DataFrame({'Country': countries, 'Change': changes})
                
                title = 'Percent Change in Emissions From Year ' + str(year1) + ' to ' + str(year2)
                plot3 = alt.Chart(emission_changes, title = title).mark_bar().encode(
                    x='Country',
                    y='Change',
                    color = alt.condition(
                        alt.datum.Change> 0,
                        alt.value("red"),  # The positive color
                        alt.value("green")  # The negative color
                       )).properties(height=300).configure_title(fontSize=15)
                

                st.altair_chart(plot3, use_container_width = True)
            with columns[2]:
                
                l3= list(temp2['Population'])
                l4 = list(temp1['Population'])
                changesp = list()
                for i in range(len(l3)):
                    changesp.append((l4[i] - l3[i])/l3[i]*100)

                countries = temp1['Country']
                population_changes = pd.DataFrame({'Country': countries, 'Change': changesp})
                
                title = 'Percent Change in Population From Year ' + str(year1) + ' to ' + str(year2)
                plot4 = alt.Chart(population_changes, title = title).mark_bar().encode(
                    x='Country',
                    y='Change',
                    color = alt.condition(
                        alt.datum.Change> 0,
                        alt.value("red"),  # The positive color
                        alt.value("green")  # The negative color
                       )).properties(height=300).configure_title(fontSize=15)
                

                st.altair_chart(plot4, use_container_width = True)
                
            
        
       
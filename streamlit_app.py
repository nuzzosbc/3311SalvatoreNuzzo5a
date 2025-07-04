
# Salvatore Nuzzo
# CSCI 3311 File 5A Discussion 6-7 Streamlit-enhanced version
# June 2, 2025

# Discussion 6-7 Inside Airbnb Dashboard

import altair
import pandas
import streamlit

def cleaning(df2):
    df2_clean = df2.dropna(subset = ['price', 'bathrooms', 'bedrooms', 'minimum_nights', 'number_of_reviews_ltm', 'estimated_revenue_l365d', 'review_scores_rating'])
    df2_clean['price'] = df2_clean['price'].apply(lambda row: row.replace("$", ""))
    df2_clean['price'] = df2_clean['price'].apply(lambda row: row.replace(",", ""))
    df2_clean['price'] = df2_clean['price'].apply(pandas.to_numeric)
    return df2_clean

def parts1and2(df2_clean):
    brush = altair.selection_interval(encodings = ['x'])
    #conditional_1 = altair.when(brush).then(altair.value(1.0)).otherwise(altair.value(0.4))
    histogram = altair.Chart(df2_clean).mark_bar().encode(
        altair.X('price:Q', bin = altair.BinParams(maxbins = 50), title = 'Prices'),
        altair.Y('count()', title = 'Counts'),
        #opacity = conditional_1
    ).add_params(
        brush
    )
    
    zoom = altair.selection_interval(bind = 'scales')
    conditional_2 = altair.condition(brush, altair.value(0.8), altair.value(0.05))
    scatterplot = altair.Chart(df2_clean).mark_point().encode(
        altair.X('bedrooms:Q', title = 'Bedrooms'),
        altair.Y('price:Q', title = 'Price'),
        opacity = conditional_2
    ).add_params(
        zoom
    )
    
    return altair.vconcat(histogram, scatterplot)

def part3(df2_clean):
    zoom = altair.selection_interval(bind = 'scales')
    chart = altair.Chart(df2_clean).mark_point().encode(
        altair.X('price:Q', title = 'Price'),
        altair.Y('estimated_revenue_l365d:Q', title = 'Estimated Revenue, last 365 days'),
        altair.Color('bedrooms:Q', title = 'Bedrooms').scale(scheme = 'blues')
    ).add_params(
        zoom
    )
    return chart

def part4(df2_clean):
    zoom = altair.selection_interval(bind = 'scales')
    chart = altair.Chart(df2_clean).mark_point().encode(
        altair.X('number_of_reviews_ltm:Q', title = 'Number of Reviews LTM'),
        altair.Y('review_scores_rating:Q', title = 'Review Scores Rating'),
        altair.Color('price:Q', title = 'Price').scale(scheme = 'blues')
    ).add_params(
        zoom
    )
    return chart

streamlit.set_page_config(page_title = "Discussion 6.7 Inside Airbnb Dashboard")

streamlit.title("Discussion 6.7 Inside Airbnb Dashboard")

streamlit.write("Salvatore Nuzzo")
streamlit.write("CSCI 3311 - June 2, 2025")

df = pandas.read_csv('listings.csv')
df_clean = cleaning(df)

streamlit.write("For all charts, interactive zooming and panning is available. Please select the price range for all the charts below.")
price_range = streamlit.slider("Select Price Range", 25, 2006, (25, 2050))

filtered_df_clean = df_clean[df_clean['price'].between(*price_range)]

streamlit.write("**Charts 1 and 2: Comparing Prices with Bedrooms**")
streamlit.write("For these charts, you can select on the histogram the price range you would like to view, and the data points on the price / bedroom plot below will be updated.")
streamlit.altair_chart(parts1and2(filtered_df_clean), use_container_width = True)

streamlit.write("**Chart 3: Estimated Revenue by Price**")
streamlit.altair_chart(part3(filtered_df_clean), use_container_width = True)

streamlit.write("**Chart 4: Review Scores Ratings vs Number of Reviews**")
streamlit.altair_chart(part4(filtered_df_clean), use_container_width = True)


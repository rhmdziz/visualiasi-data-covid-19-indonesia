# import import
import streamlit as st
import pandas as pd


# set website
st.set_page_config(page_title='Time Series: Covid 19 Indonesia', page_icon='🦠', layout='wide')
st.title('Visualisasi Data Covid 19 Indonesia')
st.markdown('Source [datasets](http://www.kaggle.com/datasets/hendratno/covid19-indonesia) or you can see [here](https://docs.google.com/spreadsheets/d/1D7fxcSRPQgFDKPp-UdZbLUDKjhkWjzvTigo6SkCTBxY/edit#gid=0) | source [code]()')

# datasets
datasets = 'https://docs.google.com/spreadsheets/d/1D7fxcSRPQgFDKPp-UdZbLUDKjhkWjzvTigo6SkCTBxY/edit#gid=0'.replace('/edit#gid=', '/export?format=csv&gid=')
df = pd.read_csv(datasets)


# date to index
df['Date'] = pd.to_datetime(df['Date'],format='%m/%d/%Y')
df['Date'] = df['Date'].dt.date
df.set_index('Date', inplace=True)


df_country = df.loc[df['Location ISO Code'] == 'IDN']
df_province = df.loc[df['Location ISO Code'] != 'IDN']

df_province['Aceh'] = df_province.loc[df_province['Location'] == 'Aceh', 'New Cases']
df_province['DKI Jakarta'] = df_province.loc[df_province['Location'] == 'DKI Jakarta', 'New Cases']


locations = ["Aceh", "Bali", "Banten", "Bengkulu", "Daerah Istimewa Yogyakarta", "DKI Jakarta", "Gorontalo", "Jambi", "Jawa Barat", "Jawa Tengah", "Jawa Timur", "Kalimantan Barat", "Kalimantan Selatan", "Kalimantan Tengah", "Kalimantan Timur", "Kalimantan Utara", "Kepulauan Bangka Belitung", "Kepulauan Riau", "Lampung", "Maluku", "Maluku Utara", "Nusa Tenggara Barat", "Nusa Tenggara Timur", "Papua", "Papua Barat", "Riau", "Sulawesi Barat", "Sulawesi Selatan", "Sulawesi Tengah", "Sulawesi Tenggara", "Sulawesi Utara", "Sumatera Barat", "Sumatera Selatan", "Sumatera Utara"]

for loc in locations:
    df_province[loc+' New Cases'] = df_province.loc[df_province['Location'] == loc, 'New Cases']
    df_province[loc+' New Deaths'] = df_province.loc[df_province['Location'] == loc, 'New Deaths']
    df_province[loc+' New Recovered'] = df_province.loc[df_province['Location'] == loc, 'New Recovered']





tab_indonesia, tab_provinces, tab_dataframe = st.tabs(['Indonesia', 'Provinces','Dataframe'])


with tab_indonesia:
    st.write('### Pertumbuhan kasus baru, kematian, sembuh di Indonesia')

    start_date, end_date = st.slider(
        "Select a range of dates:",
        value=(df_country.index.min(), df_country.index.max()),
        format="DD-MM-YYYY"
    )

    case = st.multiselect('Choose case', ['New Cases', 'New Deaths', 'New Recovered'], ['New Cases', 'New Deaths', 'New Recovered'])

    df_range = df_country[case].loc[start_date:end_date]

    col1, col2 = st.columns([5,1])

    with col1:
        st.line_chart(df_range, use_container_width=True)

    with col2:
        df_selected = df_country.loc[start_date:end_date]

        total_cases = '{:,.0f}'.format(df_selected['New Cases'].sum()).replace(',','.')

        total_deaths = '{:,.0f}'.format(df_selected['New Deaths'].sum()).replace(',','.')

        total_recovered = '{:,.0f}'.format(df_selected['New Recovered'].sum()).replace(',','.')

        if 'New Cases' in case:
            st.metric("Total Case", total_cases)
        if 'New Deaths' in case:
            st.metric("Total Deaths", total_deaths)
        if 'New Recovered' in case:
            st.metric("Total Recovered", total_recovered)

with tab_provinces:
    st.write('### Pertumbuhan kasus baru, kematian, dan sembuh tiap provinsi di Indonesia')

    start_date_province, end_date_province = st.slider(
        "Select a range of dates of province:",
        value=(df_country.index.min(), df_country.index.max()),
        format="DD-MM-YYYY"
    )

    location = st.multiselect('Choose provinces', locations, ['DKI Jakarta', 'Banten'], max_selections=10)

    df_range_province_new_cases = df_province[(i+' New Cases' for i in location)].loc[start_date_province:end_date_province]
    st.line_chart(df_range_province_new_cases, use_container_width=True)

    df_range_province_new_deaths = df_province[(i+' New Deaths' for i in location)].loc[start_date_province:end_date_province]
    st.line_chart(df_range_province_new_deaths, use_container_width=True)

    df_range_province_new_recovered = df_province[(i+' New Recovered' for i in location)].loc[start_date_province:end_date_province]
    st.line_chart(df_range_province_new_recovered, use_container_width=True)


# with tab_map:
    #     pass

    # st.write('### Map of COVID-19 Cases in Indonesia')
    # # buat objek peta
    # m = folium.Map(location=[-789.275, 113.921327], zoom_start=5)

    # # tambahkan marker untuk setiap provinsi dengan jumlah kasus sebagai teks popup
    
    # for lat, lon, loc, cases in zip(df_province['Latitude'], df_province['Longitude'], df_province['Location'], df_province['New Cases']):
    #     folium.Marker(
    #         location=[lat, lon],
    #         popup=f'{loc}: {cases} cases'
    #     ).add_to(m)

    # # tampilkan peta menggunakan folium_static
    # folium_static(m)



with tab_dataframe:
    st.dataframe(df)
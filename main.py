import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

dataBike = pd.read_csv('./Bike-sharing-dataset/day.csv')
dataBikeHour = pd.read_csv('./Bike-sharing-dataset/hour.csv')

dataBike['dteday'] = pd.to_datetime(dataBike['dteday']) # mengubah dteday menjadi datetime
dataBike['bulan'] = dataBike['dteday'].dt.to_period('M') # menambahkan kolom bulan
dataBike['Hari'] = dataBike['dteday'].dt.day_name() # menambah kolom hari dengan nama harinya
dataBike['Tipe Hari'] = dataBike['Hari'].apply(lambda x : 'Weekend' if x in ['Saturday', 'Sunday'] else 'Weekday') # menambah kolom tipe hari weekday / weekend
dataBikeHour['jam'] = dataBikeHour['hr'].apply(lambda x : f"{x:02d}:00") # menambah kolom jam 
dataBike['tahun']= dataBike['dteday'].dt.year # menambah kolom tahun
dataBike['musim'] = dataBike['season'].map({1: 'Musim Semi', 2: 'Musim Panas', 3: 'Musim Gugur', 4: 'Musim Dingin'})

dataPerbulanMusim = dataBike.groupby(['bulan', 'musim'])['cnt'].mean()
dataPerbulanMusim = dataPerbulanMusim.ffill()

dataPerbulanCuaca = dataBike.groupby(['bulan', 'weathersit'])['cnt'].mean()
dataPerbulanCuaca = dataPerbulanCuaca.ffill()

dataPertahun = dataBike.groupby('tahun')['cnt'].sum()

dataHour = dataBikeHour.groupby('jam')['cnt'].mean()

dataMusim = dataBike.groupby('musim')['cnt'].mean().sort_values()

dataMusimSemi = dataBike[dataBike['musim'] == 'Musim Semi']
jumlahCuacaMusimSemi = dataMusimSemi.groupby('weathersit')['cnt'].mean()



dataMusimDingin = dataBike[dataBike['musim'] == 'Musim Dingin']
jumlahCuacaMusimDingin = dataMusimDingin.groupby('weathersit')['cnt'].mean()

dataMusimPanas = dataBike[dataBike['musim'] == 'Musim Panas']
jumlahCuacaMusimPanas = dataMusimPanas.groupby('weathersit')['cnt'].mean()

dataMusimGugur = dataBike[dataBike['musim'] == 'Musim Gugur']
jumlahCuacaMusimGugur = dataMusimGugur.groupby('weathersit')['cnt'].mean()

for i in range(1,5):
    if i not in jumlahCuacaMusimSemi.index:
        jumlahCuacaMusimSemi[i] = 0
    if i not in jumlahCuacaMusimDingin.index:
        jumlahCuacaMusimDingin[i] = 0
    if i not in jumlahCuacaMusimPanas.index:
        jumlahCuacaMusimPanas[i] = 0
    if i not in jumlahCuacaMusimGugur.index:
        jumlahCuacaMusimGugur[i] = 0
        
dataPerHari = dataBike.groupby('Hari')['cnt'].mean()

dataTipeHari = dataBike.groupby('Tipe Hari')['cnt'].mean()





tab1, tab2 = st.tabs(["Tab 1", "Tab 2"])
with tab1:
    st.header("Tab 1")
    
    # Plot data
    fig, ax = plt.subplots()

    st.write("## Perbandingan rata-rata Jumlah Penyewa Sepeda per Musim")
    dataMusim.plot(kind='bar', x='Musim', y='Jumlah Penyewa', color=['pink', 'blue', 'red', 'orange'], ax=ax)
    plt.xlabel('Musim' , color="white")
    plt.ylabel('Jumlah Pengguna' , color="white")
    plt.xticks(rotation=0)
    # Set warna garis sumbu x dan y menjadi putih
    st.pyplot(fig)


    cuaca_index = st.radio(
    label="Pilih Cuaca: ",
    options=(1, 2, 3, 4),
    horizontal=True
    )



    labelCuaca = {1: 'Cerah, Sedikit awan, Berawan sebagian, Berawan sebagian',
                2: 'Kabut + Berawan, Kabut + Awan pecah, Kabut + Sedikit awan, Kabut',
                3: 'Salju Ringan, Hujan Ringan + Badai Petir + Awan Tersebar, Hujan Ringan + Awan Tersebar',
                4: 'Hujan Lebat + Palet Es + Badai Petir + Kabut, Salju + Kabut'}

    colors = ['blue', 'green', 'orange', 'red']


    fig, ax = plt.subplots(figsize=(10, 6))
    st.write(f'### Perbandingan jumlah penyewa untuk cuaca: {labelCuaca[cuaca_index]}')

    bar_width = 0.2
    bar_positions = [1, 2, 3, 4]

    for i, (musim, jumlah) in enumerate(zip([jumlahCuacaMusimSemi, jumlahCuacaMusimDingin, jumlahCuacaMusimGugur, jumlahCuacaMusimPanas], ['Musim Semi', 'Musim Dingin', 'Musim Gugur', 'Musim Panas'])):
        ax.bar(bar_positions[i], musim[cuaca_index], color=colors[i], width=bar_width, label=jumlah)

    ax.set_xticks([x + bar_width for x in bar_positions])
    ax.set_xticklabels(['Musim Semi', 'Musim Dingin', 'Musim Gugur', 'Musim Panas'])
    ax.set_ylabel('Jumlah Penyewa')

    ax.legend(title='Musim', loc='upper left', title_fontsize='large')
    plt.tight_layout()
    st.pyplot(fig)

    fig, ax = plt.subplots()
    ax.pie(dataPerHari, labels=dataPerHari.index ,   autopct='%1.1f%%', startangle=140)
    st.write("## diagram penyewa tiap Hari")
    st.pyplot(fig)



    fig, ax = plt.subplots()
    plt.bar(dataTipeHari.index, dataTipeHari, color=['red','blue'])
    st.write('## Perbandingan rata-rata penyewa weekday dan weekend')
    plt.xlabel('tipe hari')
    plt.ylabel('jumlah penyewa')

    for i , value in enumerate(dataTipeHari):
        plt.text(i,value/2, int(value), ha='center',va='center', color="white", fontweight='bold')

    st.pyplot(fig)

    fig, ax = plt.subplots()
    plt.plot(dataHour.index, dataHour , marker='o', linestyle='-', color='blue')
    plt.xticks(rotation=90)
    st.write('## diagram rata-rata penyewa tiap jam')
    plt.xlabel('jam')
    plt.ylabel('jumlah penyewa')
    st.pyplot(fig)


    fig, ax = plt.subplots()
    plt.bar(dataPertahun.index.astype(str), dataPertahun, color=['red','blue'])
    st.write('## perbandingan jumlah penyewa tiap tahun')
    plt.xlabel('tahun')
    plt.ylabel('jumlah penyewa')

    for i , value in enumerate(dataPertahun):
        plt.text(i,value/2, str(value), ha='center',va='center', color="white", fontweight='bold')

    st.pyplot(fig)
    st.write(f'### dari 2011 ke 2012 mengalami kenaikan sebesar {int(((dataPertahun[2012]- dataPertahun[2011])/dataPertahun[2011])*100)}%')



    colors = {'Musim Dingin': 'blue', 'Musim Semi': 'green', 'Musim Panas': 'red', 'Musim Gugur': 'orange'}
    bulan = [i[0] for i in dataPerbulanMusim.index]
    pengguna = [i for i in dataPerbulanMusim]

    fig, ax = plt.subplots()
    plt.bar([str(i[0]) for i in dataPerbulanMusim.index], [i for i in dataPerbulanMusim], color=[colors[i[1]] for i in dataPerbulanMusim.index],  label=[i[1] for i in dataPerbulanMusim.index] )
    st.write('## data rata-rata penyewa tiap bulan (Musim)')
    plt.xticks(rotation = 90)
    plt.xlabel('bulan')
    plt.ylabel('jumlah penyewa')

    legend_labels = ['Musim Dingin', 'Musim Semi', 'Musim Panas', 'Musim Gugur']
    legend_colors = ['blue', 'green', 'red', 'orange']
    legend_patches = [mpatches.Patch(color=color, label=label) for color, label in zip(legend_colors, legend_labels)]
    plt.legend(handles=legend_patches,  title='Musim', bbox_to_anchor=(1, 1))

    st.pyplot(fig)



    colors = {1: 'orange', 2: 'gray', 3: 'lightblue', 4: 'blue'}
    bulan = [i[0] for i in dataPerbulanCuaca.index]
    pengguna = [i for i in dataPerbulanCuaca]

    fig, ax = plt.subplots()
    plt.bar([str(i[0]) for i in dataPerbulanCuaca.index], [i for i in dataPerbulanCuaca], color=[colors[i[1]] for i in dataPerbulanCuaca.index],  label=[i[1] for i in dataPerbulanCuaca.index] )
    st.write('## data rata-rata penyewa tiap bulan (Cuaca)')
    plt.xticks(rotation = 90)
    plt.xlabel('bulan')
    plt.ylabel('jumlah penyewa')

    legend_labels = ['Cerah, Sedikit awan, Berawan sebagian, Berawan sebagian',  'Kabut + Berawan, Kabut + Awan pecah, Kabut + Sedikit awan, Kabut', 'Salju Ringan, Hujan Ringan + Badai Petir + Awan Tersebar, Hujan Ringan + Awan Tersebar', 'Hujan Lebat + Palet Es + Badai Petir + Kabut, Salju + Kabut']
    legend_colors = ['orange', 'gray', 'lightblue', 'blue']
    legend_patches = [mpatches.Patch(color=color, label=label) for color, label in zip(legend_colors, legend_labels)]


    st.pyplot(fig)
    st.image('./img/legend1.png')
   
with tab2:
    st.header("Tab 2")
    st.write("# percobaan")



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


data = {
    'Musim': ['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin'],
    'Jumlah Penyewa': [100, 150, 120, 80]
}


# Plot data
fig, ax = plt.subplots()
dataMusim.plot(kind='bar', x='Musim', y='Jumlah Penyewa', color=['pink', 'blue', 'red', 'orange'], ax=ax)
plt.title('Perbandingan rata-rata Jumlah Penyewa Sepeda per Musim')
plt.xlabel('Musim')
plt.ylabel('Jumlah Pengguna')
plt.xticks(rotation=0)

# Tampilkan plot menggunakan Streamlit
st.pyplot(fig)



st.write("""
         # My first app
         Hello, para calon praktisi data masa depan!
         """)

labelCuaca = jumlahCuacaMusimSemi.index.map({1: 'Cerah, Sedikit awan, Berawan sebagian, Berawan sebagian', 2: 'Kabut + Berawan, Kabut + Awan pecah, Kabut + Sedikit awan, Kabut', 3: 'Salju Ringan, Hujan Ringan + Badai Petir + Awan Tersebar, Hujan Ringan + Awan Tersebar', 4: 'Hujan Lebat + Palet Es + Badai Petir + Kabut, Salju + Kabut'}).tolist()

fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(14, 6))
fig.suptitle('Perbandingan jumlah penyewa percuaca tiap Musim ')

axes[0 , 0].bar(jumlahCuacaMusimSemi.index.astype(str), jumlahCuacaMusimSemi, color=['blue', 'green', 'orange', 'red'] ,label=labelCuaca)
axes[0 , 0].set_title('Musim Semi')
axes[0 , 0].set_xlabel('Musim')
axes[0 , 0].set_ylabel('Jumlah Penyewa')
axes[0 , 0].set_ylim([0, 7000])  
axes[0 , 0].set_xticks([])

axes[0, 1].bar(jumlahCuacaMusimDingin.index.astype(str), jumlahCuacaMusimDingin, color=['blue', 'green', 'orange', 'red'])
axes[0, 1].set_title('Musim Dingin')
axes[0, 1].set_xlabel('Musim')
axes[0, 1].set_ylabel('Jumlah Penyewa')
axes[0, 1].set_ylim([0, 7000])
axes[0, 1].set_xticks([])

axes[1, 0].bar(jumlahCuacaMusimGugur.index.astype(str), jumlahCuacaMusimGugur, color=['blue', 'green', 'orange', 'red'])
axes[1, 0].set_title('Musim Gugur')
axes[1, 0].set_xlabel('Musim')
axes[1, 0].set_ylabel('Jumlah Penyewa')
axes[1, 0].set_ylim([0, 7000]) 
axes[1, 0].set_xticks([])

axes[1, 1].bar(jumlahCuacaMusimPanas.index.astype(str), jumlahCuacaMusimPanas, color=['blue', 'green', 'orange', 'red'])
axes[1, 1].set_title('Musim Panas')
axes[1, 1].set_xlabel('Musim')
axes[1, 1].set_ylabel('Jumlah Penyewa')
axes[1, 1].set_ylim([0, 7000])
axes[1, 1].set_xticks([])

fig.legend(loc='center left', bbox_to_anchor=(1, 0.5), title='Legenda')
plt.subplots_adjust(right=0.85)
plt.tight_layout()
st.pyplot(fig)
import pandas as pd
import os
from sklearn.preprocessing import MinMaxScaler

# Load dataset
file_path = r"D:\Reza\kuliah\Semester 10\VisDat\Tugas\Mg-4\avenged_songs.csv"
df = pd.read_csv(file_path)

# Cek nama kolom
print("Kolom dalam dataset:", df.columns)

# Pilih kolom yang relevan untuk analisis dan mengabaikan fitur lainnya
selected_columns = [
    "name", "album", "popularity", "danceability", "energy", 
    "loudness", "speechiness", "acousticness", "instrumentalness", 
    "liveness", "valence", "tempo"
]

# Pastikan semua kolom ada dalam dataset
missing_columns = [col for col in selected_columns if col not in df.columns]
if missing_columns:
    print("Kolom yang hilang:", missing_columns)
else:
    df_selected = df[selected_columns].copy()  # Hindari SettingWithCopyWarning

    # Tampilkan jumlah data sebelum preprocessing
    print(f"Jumlah data sebelum preprocessing: {df_selected.shape[0]} baris, {df_selected.shape[1]} kolom")

    # Menghapus data dengan missing values
    df_cleaned = df_selected.dropna()

    # Identifikasi kolom numerik untuk normalisasi
    numeric_columns = df_cleaned.select_dtypes(include=['number']).columns

    # Menghapus outlier menggunakan IQR
    Q1 = df_cleaned[numeric_columns].quantile(0.25)
    Q3 = df_cleaned[numeric_columns].quantile(0.75)
    IQR = Q3 - Q1

    df_cleaned = df_cleaned[~((df_cleaned[numeric_columns] < (Q1 - 1.5 * IQR)) |
                              (df_cleaned[numeric_columns] > (Q3 + 1.5 * IQR))).any(axis=1)].copy()

    # Tampilkan jumlah data setelah preprocessing
    print(f"Jumlah data setelah preprocessing: {df_cleaned.shape[0]} baris, {df_cleaned.shape[1]} kolom")

    # Path untuk menyimpan file
    output_folder = r"D:\Reza\kuliah\Semester 10\VisDat\Tugas\Mg-4\dataset"
    output_file = os.path.join(output_folder, "avenged_preprocessed-3.xlsx")

    # Pastikan folder `dataset` ada
    os.makedirs(output_folder, exist_ok=True)

    # Simpan hasil ke file Excel
    df_cleaned.to_excel(output_file, index=False)

    print(f"Preprocessing selesai. File disimpan di: {output_file}")

import matplotlib.pyplot as plt
import seaborn as sns

# Pilih dua variabel numerik untuk scatter plot
x_var = "danceability"
y_var = "energy"

# Plot scatter plot
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df_cleaned, x=x_var, y=y_var, hue="popularity", size="popularity", sizes=(20, 200), palette="coolwarm")

# Tambahkan label dan judul
plt.xlabel(x_var.capitalize())
plt.ylabel(y_var.capitalize())
plt.title(f'Scatter Plot {x_var.capitalize()} vs {y_var.capitalize()}')
plt.legend(title="Popularity", loc="upper right")

# Tampilkan plot
plt.show()

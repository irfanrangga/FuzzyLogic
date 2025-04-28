import pandas as pd

#a adalah batas bawah, b adalah batas tengah, c adalah batas atas
# Fungsi segitiga fuzzy untuk menghitung derajat keanggotaan
def segitiga_fuzzy(x, a, b, c):
    if a <= x <= b:
        return (x - a) / (b - a)
    elif b < x <= c:
        return (c - x) / (c - b)
    else:
        return 0

# Fungsi untuk menghitung derajat keanggotaan untuk setiap kategori dengan segitiga fuzzy    
def member_output(x):
    return {
        'Sangat Rendah': segitiga_fuzzy(x, 0, 20, 40),
        'Rendah': segitiga_fuzzy(x, 20, 40, 60),
        'Sedang': segitiga_fuzzy(x, 40, 60, 80),
        'Tinggi': segitiga_fuzzy(x, 60, 80, 100),
        'Sangat Tinggi': segitiga_fuzzy(x, 80, 100, 100)
    }

# Harga
def fuzzy_harga(x):
    if x <= 20000:
        return "Sangat Murah"
    elif 20000 < x <= 35000:
        return "Murah"
    elif 35000 < x <= 50000:
        return "Sedang"
    elif 50000 < x <= 65000:
        return "Mahal"
    else:
        return "Sangat Mahal"

# Pelayanan
def fuzzy_pelayanan(x):
    if x <= 20:
        return "Sangat Buruk"
    elif 20 < x <= 40:
        return "Buruk"
    elif 40 < x <= 60:
        return "Cukup"
    elif 60 < x <= 80:
        return "Baik"
    else:
        return "Sangat Baik"

# Inferensi Mamdani manual berdasarkan kombinasi harga dan pelayanan
def inferensi(kategori_harga, nilai_pelayanan):
    if kategori_harga == "Sangat Murah":
        if nilai_pelayanan == "Sangat Baik":
            return "Sangat Tinggi"
        elif nilai_pelayanan in ["Baik", "Cukup"]:
            return "Tinggi"
        else:
            return "Sedang"
    elif kategori_harga == "Murah":
        if nilai_pelayanan == "Sangat Baik":
            return "Sangat Tinggi"
        elif nilai_pelayanan == "Baik":
            return "Tinggi"
        elif nilai_pelayanan == "Cukup":
            return "Sedang"
        else:
            return "Rendah"
    elif kategori_harga == "Sedang":
        if nilai_pelayanan == "Sangat Baik":
            return "Tinggi"
        elif nilai_pelayanan == "Baik":
            return "Tinggi"
        elif nilai_pelayanan == "Cukup":
            return "Sedang"
        else:
            return "Rendah"
    elif kategori_harga == "Mahal":
        if nilai_pelayanan == "Sangat Baik":
            return "Tinggi"
        elif nilai_pelayanan == "Baik":
            return "Sedang"
        else:
            return "Rendah"
    elif kategori_harga == "Sangat Mahal":
        if nilai_pelayanan == "Sangat Baik":
            return "Sedang"
        elif nilai_pelayanan == "Baik":
            return "Sedang"
        else:
            return "Sangat Rendah"

# Defuzzifikasi menggunakan metode centroid
def defuzzifikasi(kategori):
    x_start = 0
    x_end = 100
    step = 0.1  # Semakin kecil semakin akurat
    x = x_start
    numerator = 0.0
    denominator = 0.0
    
    while x <= x_end:
        membership = member_output(x)[kategori]
        numerator += x * membership
        denominator += membership
        x += step
    
    if denominator == 0:
        return 0.0
    return numerator / denominator

# Proses semua data
data = pd.read_excel('restoran.xlsx')
hasil = []
for index, row in data.iterrows():
    harga_value = row['harga']
    pelayanan_value = row['Pelayanan']
    
    harga_fuzzy = fuzzy_harga(harga_value)
    pelayanan_fuzzy = fuzzy_pelayanan(pelayanan_value)
    
    hasil_inferensi = inferensi(harga_fuzzy, pelayanan_fuzzy)
    rekomendasi_nilai = defuzzifikasi(hasil_inferensi)
    
    hasil.append({
        'ID Restoran': row['id Pelanggan'],
        'Kualitas Servis': pelayanan_value,
        'Harga': harga_value,
        'Nilai Rekomendasi': rekomendasi_nilai
    })

# Masukkan ke dataframe
hasil_df = pd.DataFrame(hasil)

# Sortir berdasarkan Nilai Rekomendasi (Descending)
hasil_df = hasil_df.sort_values(by='Nilai Rekomendasi', ascending=False)

# Ambil 5 data terbaik
top5 = hasil_df.head(5)

# Simpan ke Excel
output_path = 'rekomen_semua_restoran.xlsx'
hasil_df.to_excel(output_path, index=False)

if __name__ == "__main__":
    print("Proses selesai. Hasil disimpan di:", output_path)
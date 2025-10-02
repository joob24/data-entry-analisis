import pandas as pd
import matplotlib.pyplot as plt  # Opsional, untuk visualisasi
import seaborn as sns

# Load data dan hapus kolom Unnamed yang tidak berisi data
df = pd.read_csv('data.csv')
df = df.drop(columns=['Unnamed: 3', 'Unnamed: 5', 'Unnamed: 7', 'Unnamed: 9', 'date.1'], errors='ignore')

# Ubah kolom date ke tipe datetime
df['date'] = pd.to_datetime(df['date'])

# Buat kolom tahun dan bulan untuk grouping
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.to_period('M')

# 1. Vendor paling banyak melakukan pembelian berdasarkan total per bulan
vendor_monthly_total = df.groupby(['vendor', 'month'])['total'].sum().reset_index()
vendor_top_monthly = vendor_monthly_total.loc[vendor_monthly_total.groupby('month')['total'].idxmax()]
# Format kolom 'total' menjadi string dengan simbol $ (karena sudah USD)
def format_currency(value):
    return f"${value:,.2f}"  # Contoh: $1,234.56 (comma untuk ribuan, 2 desimal)
vendor_top_monthly['total'] = vendor_top_monthly['total'].apply(format_currency)

# 2. Vendor paling banyak melakukan pembelian berdasarkan total per tahun
vendor_yearly_total = df.groupby(['vendor', 'year'])['total'].sum().reset_index()
vendor_top_yearly = vendor_yearly_total.loc[vendor_yearly_total.groupby('year')['total'].idxmax()]
# Format kolom 'total' menjadi string dengan simbol $ (karena sudah USD)
def format_currency(value):
    return f"${value:,.2f}"
vendor_top_yearly['total']=vendor_top_yearly['total'].apply(format_currency)

# 3. Description paling banyak terjual berdasarkan unit per bulan
desc_monthly_unit = df.groupby(['description', 'month'])['unit'].sum().reset_index()
desc_top_monthly = desc_monthly_unit.loc[desc_monthly_unit.groupby('month')['unit'].idxmax()]

# 4. Description paling banyak terjual berdasarkan unit per tahun
desc_yearly_unit = df.groupby(['description', 'year'])['unit'].sum().reset_index()
desc_top_yearly = desc_yearly_unit.loc[desc_yearly_unit.groupby('year')['unit'].idxmax()]

# 5. Description paling banyak dibeli oleh vendor berdasarkan jumlah unit per bulan
vendor_desc_monthly = df.groupby(['vendor', 'description', 'month'])['unit'].sum().reset_index()
idx = vendor_desc_monthly.groupby(['vendor', 'month'])['unit'].idxmax()
vendor_desc_top_monthly = vendor_desc_monthly.loc[idx]

# 6. Description paling banyak dibeli oleh vendor berdasarkan jumlah unit per tahun
vendor_desc_yearly = df.groupby(['vendor', 'description', 'year'])['unit'].sum().reset_index()
idx_year = vendor_desc_yearly.groupby(['vendor', 'year'])['unit'].idxmax()
vendor_desc_top_yearly = vendor_desc_yearly.loc[idx_year]

# Menampilkan hasil
print("Vendor dengan Total Pembelian Terbesar per Bulan (dalam USD):")
print(vendor_top_monthly[['vendor', 'month', 'total']])

print("\nThe vendor that makes the most purchases based on the years:")
print(vendor_top_yearly[['vendor','year','total']])

print("\nDescription that makes the most purchases based on the monthly:")
print(desc_top_monthly)

print("\nDescription that makes the most purchases based on the years:")
print(desc_top_yearly)

print("\nDescription most purchased by the vendor based on the number of units per month:")
print(vendor_desc_top_monthly)

print("\nDescription most purchased by the vendor based on the number of units per years:")
print(vendor_desc_top_yearly)

# Buat kolom label untuk x-axis (misalnya 'Vendor - Year')
vendor_desc_top_yearly['vendor_year'] = vendor_desc_top_yearly['vendor'] + ' (' + vendor_desc_top_yearly['year'].astype(str) + ')'

# --- OPSI 1: Grafik Sederhana dengan Matplotlib (Bar Chart Horizontal untuk readability) ---
# Filter top N baris jika data banyak (misalnya top 15 untuk hindari ramai)
top_data = vendor_desc_top_yearly.nlargest(15, 'unit')  # Ambil top 15 terbesar
top_data = top_data.sort_values('unit', ascending=True)  # Ascending untuk horizontal bar dari bawah
# Buat label y yang lebih pendek: Vendor-Year + Description dipotong
def shorten_label(row):
    desc_short = row['description'][:25] + '...' if len(row['description']) > 25 else row['description']  # Potong description
    return f"{row['vendor']} ({row['year']}): {desc_short}"
top_data['short_label'] = top_data.apply(shorten_label, axis=1)
plt.figure(figsize=(14, 10))  # Ukuran lebih besar: lebar 14, tinggi 10
y_pos = range(len(top_data))
bars = plt.barh(y_pos, top_data['unit'], color='lightblue')
plt.yticks(y_pos, top_data['short_label'], fontsize=9)  # Font lebih kecil untuk muat
plt.xlabel('Jumlah Unit', fontsize=12)
plt.title('Top Description that makes the most purchases based on the years', fontsize=14)
plt.gca().invert_yaxis()  # Balik agar terbesar di atas
# Tambah label nilai di bar (posisi lebih aman)
max_unit = top_data['unit'].max()
for i, (bar, v) in enumerate(zip(bars, top_data['unit'])):
    plt.text(v + (max_unit * 0.01), bar.get_y() + bar.get_height()/2, f"{v:,}", 
             va='center', fontsize=9, color='black')  # Format ribuan, posisi tengah bar
# Manual adjust margins untuk hindari warning tight_layout
plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
# Coba tight_layout lagi (sekarang seharusnya berhasil)
plt.tight_layout()
# TAMBAHAN: Simpan grafik ke file PNG (sebelum show)
plt.savefig('top_description_yearly.png', dpi=300, bbox_inches='tight', facecolor='white')
print("Grafik berhasil disimpan ke 'top_description_yearly.png' di folder script Anda!")
plt.show()

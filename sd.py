import csv
import os

# File utama dan laporan
FILE_TRANSAKSI = 'keuangan.csv'
FILE_LAPORAN_BULANAN = 'laporan_bulanan.csv'
FILE_LAPORAN_TAHUNAN = 'laporan_tahunan.csv'

# Tambah data transaksi
def tambah_data():
    tanggal = input("Masukkan tanggal (YYYY-MM-DD): ")
    jenis = input("Jenis (Pemasukan/Pengeluaran): ")
    kategori = input("Kategori: ")
    deskripsi = input("Deskripsi: ")
    try:
        jumlah = int(input("Jumlah: "))
    except ValueError:
        print("Jumlah harus berupa angka!")
        return
    with open(FILE_TRANSAKSI, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([tanggal, jenis, kategori, deskripsi, jumlah])
    print("✅ Data berhasil ditambahkan ke keuangan.csv")

# Lihat semua data
def lihat_data():
    with open(FILE_TRANSAKSI, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)
        print("📋 Data Keuangan:")
        for i, row in enumerate(reader, start=1):
            print(f"{i}. {row}")

# Edit data
def edit_data():
    lihat_data()
    try:
        index = int(input("Pilih nomor data yang ingin diedit: "))
    except ValueError:
        print("❌ Input harus berupa angka!")
        return

    # Baca semua data
    with open(FILE_TRANSAKSI, mode='r') as file:
        reader = list(csv.reader(file))
    
    if len(reader) == 0:
        print("❌ File kosong!")
        return

    header = reader[0]  # Baris header
    data = reader[1:]   # Data transaksi

    # Validasi index
    if 0 < index <= len(data):
        new_data = []
        print("\nEdit data (biarkan kosong jika tidak ingin mengubah):")
        for col_name, current_value in zip(header, data[index-1]):
            new_value = input(f"{col_name} [{current_value}]: ").strip()
            new_data.append(new_value if new_value else current_value)
        
        # Update data
        data[index-1] = new_data

        # Tulis ulang seluruh data ke file (mode 'w')
        with open(FILE_TRANSAKSI, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)  # Tulis header
            writer.writerows(data)   # Tulis semua data
        print("✅ Data berhasil diperbarui.")
    else:
        print("❌ Index tidak valid.")

# Hapus data
def hapus_data():
    lihat_data()
    index = int(input("Pilih nomor data yang ingin dihapus: "))
    with open(FILE_TRANSAKSI, mode='r') as file:
        reader = list(csv.reader(file))

    header = reader[0]
    data = reader[1:]

    if 0 < index <= len(data):
        data.pop(index - 1)
        with open(FILE_TRANSAKSI, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(data)
        print("🗑️ Data berhasil dihapus.")
    else:
        print("❌ Index tidak valid.")

# Laporan Bulanan
def laporan_bulanan():
    bulan = input("Masukkan bulan (01-12): ")
    tahun = input("Masukkan tahun (YYYY): ")
    total_masuk, total_keluar = 0, 0

    with open(FILE_TRANSAKSI, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                tanggal = row['Tanggal']
                if tanggal[0:7] == f"{tahun}-{bulan}":
                    jenis = row['Jenis'].lower()
                    jumlah = int(row['Jumlah'])
                    if jenis == 'pemasukan':
                        total_masuk += jumlah
                    elif jenis == 'pengeluaran':
                        total_keluar += jumlah
            except:
                continue
    if total_masuk != 0 or total_keluar != 0:
        with open(FILE_LAPORAN_BULANAN, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([tahun, bulan, total_masuk, total_keluar])
        print(f"📁 Disimpan ke: {FILE_LAPORAN_BULANAN}")
    else:
        print("⚠️ Tidak ada data, laporan tidak disimpan.")

# Laporan Tahunan
def laporan_tahunan():
    tahun = input("Masukkan tahun (YYYY): ")
    total_masuk, total_keluar = 0, 0

    with open(FILE_TRANSAKSI, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                tanggal = row['Tanggal']
                if tanggal[0:4] == tahun:
                    jenis = row['Jenis'].lower()
                    jumlah = int(row['Jumlah'])
                    if jenis == 'pemasukan':
                        total_masuk += jumlah
                    elif jenis == 'pengeluaran':
                        total_keluar += jumlah
            except:
                continue
    if total_masuk != 0 or total_keluar != 0:
        with open(FILE_LAPORAN_TAHUNAN, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([tahun, total_masuk, total_keluar])
        print(f"📁 Disimpan ke: {FILE_LAPORAN_TAHUNAN}")
    else:
        print("⚠️ Tidak ada data, laporan tidak disimpan.")

# Menu utama
def menu():
    while True:
        print("=== Menu Manajemen Keuangan ===")
        print("1. Tambah Data")
        print("2. Lihat Semua Data")
        print("3. Edit Data")
        print("4. Hapus Data")
        print("5. Laporan Bulanan")
        print("6. Laporan Tahunan")
        print("7. Keluar")

        pilihan = input("Pilih menu (1-7): ")

        if pilihan == '1':
            tambah_data()
        elif pilihan == '2':
            lihat_data()
        elif pilihan == '3':
            edit_data()
        elif pilihan == '4':
            hapus_data()
        elif pilihan == '5':
            laporan_bulanan()
        elif pilihan == '6':
            laporan_tahunan()
        elif pilihan == '7':
            print("👋 Terima kasih, nanti kembali lagi ya....")
            break
        else:
            print("❌ Pilihan tidak valid.")

if __name__ == "__main__":
    menu()
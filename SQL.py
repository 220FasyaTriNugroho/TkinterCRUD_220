import sqlite3 
import tkinter as tk  
import tkinter.messagebox as msg  
from tkinter import ttk  


def koneksi():
    koneksi = sqlite3.connect("prediksi_prodi.db")  # Membuat/membuka file database
    return koneksi

def create_table():
    con = koneksi()  # Buka koneksi database
    cur = con.cursor()  # Buat cursor untuk eksekusi query
    
    # Query SQL untuk membuat tabel
    cur.execute("""
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT NOT NULL,
            biologi INTEGER NOT NULL,
            fisika INTEGER NOT NULL,
            inggris INTEGER NOT NULL,
            prediksi_fakultas TEXT NOT NULL
        )
    """)
    
    con.commit()  # Simpan perubahan ke database
    con.close()  # Tutup koneksi database


def insert_nilai(nama: str, biologi: int, fisika: int, inggris: int, prediksi: str):
    con = koneksi()  # Buka koneksi database
    cur = con.cursor()  # Buat cursor

    # Query INSERT untuk menyimpan data
    cur.execute("""
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas) 
        VALUES (?, ?, ?, ?, ?)
    """, (nama, biologi, fisika, inggris, prediksi))
    
    con.commit()  # Simpan perubahan
    rowid = cur.lastrowid  # Ambil ID data yang baru disimpan
    con.close()  # Tutup koneksi
    return rowid


def read_nilai():
    con = koneksi()  # Buka koneksi database
    cur = con.cursor()  # Buat cursor
    
    # Query SELECT untuk mengambil semua data, diurutkan berdasarkan ID
    cur.execute("SELECT id, nama_siswa, biologi, fisika, inggris, prediksi_fakultas FROM nilai_siswa ORDER BY id")
    rows = cur.fetchall()  # Ambil semua hasil query
    con.close()  # Tutup koneksi
    return rows


create_table()



class PrediksiProdi(tk.Tk):
    
    def __init__(self):

        super().__init__()  # Panggil constructor parent class (tk.Tk)
        
        # ====================================================================
        # PENGATURAN WINDOW UTAMA
        # ====================================================================
        self.title("Aplikasi Prediksi Prodi Pilihan")  # Judul window
        self.geometry("700x600")  # Ukuran window (lebar x tinggi)
        self.configure(bg="#e3f2fd")  # Warna background window (biru muda)

        # ====================================================================
        # JUDUL APLIKASI
        # ====================================================================
        judul = tk.Label(
            self, 
            text="Aplikasi Prediksi Prodi Pilihan", 
            font=("Arial", 16, "bold"),  # Font: Arial, ukuran 16, tebal
            bg="#e3f2fd",  # Background warna biru muda
            fg="#1565c0"   # Foreground (warna teks) biru tua
        )
        judul.pack(pady=15)  # Tampilkan dengan padding atas-bawah 15px

        # ====================================================================
        # FRAME UNTUK INPUT - KOTAK PUTIH UNTUK FORM
        # ====================================================================
        frm = tk.Frame(
            self, 
            bg="#ffffff",  # Background putih
            padx=20,  # Padding kiri-kanan 20px
            pady=20   # Padding atas-bawah 20px
        )
        frm.pack(padx=20, pady=10, fill="x")  # Tampilkan dengan padding dan fill horizontal

        # ====================================================================
        # KONFIGURASI GRID
        # ====================================================================
        # Konfigurasi frame agar konten berada di tengah horizontal
        frm.grid_columnconfigure(0, weight=1)  # Kolom 0 (label) dapat meregang
        frm.grid_columnconfigure(1, weight=1)  # Kolom 1 (entry) dapat meregang

        # ====================================================================
        # INPUT 1: NAMA SISWA
        # ====================================================================
        # Label "Nama Siswa:"
        tk.Label(
            frm, 
            text="Nama Siswa:", 
            bg="#ffffff", 
            font=("Arial", 10)
        ).grid(row=0, column=0, sticky="e", pady=8, padx=(0, 10))  # sticky="e" = rata kanan
        
        # Entry (kotak input) untuk nama siswa
        self.ent_nama = tk.Entry(frm, width=35, font=("Arial", 10))
        self.ent_nama.grid(row=0, column=1, sticky="w", pady=8)  # sticky="w" = rata kiri

        # ====================================================================
        # INPUT 2: NILAI BIOLOGI
        # ====================================================================
        # Label "Nilai Biologi:"
        tk.Label(
            frm, 
            text="Nilai Biologi:", 
            bg="#ffffff", 
            font=("Arial", 10)
        ).grid(row=1, column=0, sticky="e", pady=8, padx=(0, 10))  # sticky="e" = rata kanan
        
        # Entry untuk nilai biologi
        self.ent_biologi = tk.Entry(frm, width=35, font=("Arial", 10))
        self.ent_biologi.grid(row=1, column=1, sticky="w", pady=8)

        # ====================================================================
        # INPUT 3: NILAI FISIKA
        # ====================================================================
        # Label "Nilai Fisika:"
        tk.Label(
            frm, 
            text="Nilai Fisika:", 
            bg="#ffffff", 
            font=("Arial", 10)
        ).grid(row=2, column=0, sticky="e", pady=8, padx=(0, 10))  # sticky="e" = rata kanan
        
        # Entry untuk nilai fisika
        self.ent_fisika = tk.Entry(frm, width=35, font=("Arial", 10))
        self.ent_fisika.grid(row=2, column=1, sticky="w", pady=8)

        # ====================================================================
        # INPUT 4: NILAI INGGRIS
        # ====================================================================
        # Label "Nilai Inggris:"
        tk.Label(
            frm, 
            text="Nilai Inggris:", 
            bg="#ffffff", 
            font=("Arial", 10)
        ).grid(row=3, column=0, sticky="e", pady=8, padx=(0, 10))  # sticky="e" = rata kanan
        
        # Entry untuk nilai inggris
        self.ent_inggris = tk.Entry(frm, width=35, font=("Arial", 10))
        self.ent_inggris.grid(row=3, column=1, sticky="w", pady=8)

        # ====================================================================
        # FRAME UNTUK TOMBOL
        # ====================================================================
        btn_frame = tk.Frame(frm, bg="#ffffff")  # Frame khusus untuk tombol
        btn_frame.grid(row=4, column=0, columnspan=2, pady=15)  # Span 2 kolom, padding atas-bawah 15px

        # ====================================================================
        # TOMBOL 1: SUBMIT NILAI
        # ====================================================================
        self.btn_submit = tk.Button(
            btn_frame, 
            text="Submit Nilai",  # Text yang tampil di tombol
            width=12,  # Lebar tombol
            command=self.submit_nilai,  # Fungsi yang dipanggil saat tombol diklik
            bg="#1976d2",  # Background biru
            fg="white",  # Foreground (teks) putih
            font=("Arial", 10, "bold")
        )
        self.btn_submit.pack(side="left", padx=5)  # Tampilkan di sisi kiri dengan padding 5px

        # ====================================================================
        # TOMBOL 2: REFRESH DATA
        # ====================================================================
        self.btn_refresh = tk.Button(
            btn_frame, 
            text="Refresh",  # Text yang tampil di tombol
            width=12, 
            command=self.read_data,  # Fungsi yang dipanggil saat tombol diklik
            bg="#43a047",  # Background hijau
            fg="white", 
            font=("Arial", 10, "bold")
        )
        self.btn_refresh.pack(side="left", padx=5)  # Tampilkan di sisi kiri dengan padding 5px

        # ====================================================================
        # TREEVIEW - TABEL UNTUK MENAMPILKAN DATA
        # ====================================================================
        # Definisikan kolom-kolom yang akan ditampilkan
        cols = ("id", "nama", "biologi", "fisika", "inggris", "prediksi")
        
        # Buat Treeview (widget tabel)
        self.tree = ttk.Treeview(
            self, 
            columns=cols,  # Kolom yang akan ditampilkan
            show="headings",  # Tampilkan hanya heading (tanpa kolom default)
            height=10  # Tinggi tabel (jumlah baris yang terlihat)
        )
        
        # Konfigurasi kolom ID
        self.tree.heading("id", text="ID")  # Heading dengan text "ID"
        self.tree.column("id", width=50, anchor="center")  # Lebar 50px, text di tengah
        
        # Konfigurasi kolom Nama Siswa
        self.tree.heading("nama", text="Nama Siswa")
        self.tree.column("nama", width=180)  # Lebar 180px, text di kiri (default)
        
        # Konfigurasi kolom Biologi
        self.tree.heading("biologi", text="Biologi")
        self.tree.column("biologi", width=80, anchor="center")  # Lebar 80px, text di tengah
        
        # Konfigurasi kolom Fisika
        self.tree.heading("fisika", text="Fisika")
        self.tree.column("fisika", width=80, anchor="center")
        
        # Konfigurasi kolom Inggris
        self.tree.heading("inggris", text="Inggris")
        self.tree.column("inggris", width=80, anchor="center")
        
        # Konfigurasi kolom Prediksi Fakultas
        self.tree.heading("prediksi", text="Prediksi Fakultas")
        self.tree.column("prediksi", width=150, anchor="center")
        
        # Tampilkan treeview dengan padding dan fill
        self.tree.pack(padx=20, pady=(0, 20), fill="both", expand=True)

        # ====================================================================
        # LOAD DATA AWAL SAAT APLIKASI PERTAMA KALI DIBUKA
        # ====================================================================
        self.read_data()  # Panggil fungsi untuk membaca dan menampilkan data dari database

    # ========================================================================
    # METHOD 1: CLEAR INPUTS - MENGOSONGKAN SEMUA KOTAK INPUT
    # ========================================================================
    def clear_inputs(self):
        self.ent_nama.delete(0, tk.END)  # Hapus dari index 0 sampai END (semua text)
        self.ent_biologi.delete(0, tk.END)
        self.ent_fisika.delete(0, tk.END)
        self.ent_inggris.delete(0, tk.END)

    # ========================================================================
    # METHOD 2: VALIDATE INPUTS - VALIDASI INPUT DARI USER
    # ========================================================================
    def validate_inputs(self):
        # Ambil nilai dari entry dan hapus spasi di awal/akhir
        nama = self.ent_nama.get().strip()
        bio_str = self.ent_biologi.get().strip()
        fis_str = self.ent_fisika.get().strip()
        ing_str = self.ent_inggris.get().strip()

        # Cek apakah ada field yang kosong
        if not nama or not bio_str or not fis_str or not ing_str:
            msg.showwarning("Peringatan", "Semua field harus diisi!")
            return None  # Return None jika ada yang kosong

        try:
            # Konversi string ke integer
            biologi = int(bio_str)
            fisika = int(fis_str)
            inggris = int(ing_str)

            # Cek apakah nilai berada di range 0-100
            if biologi < 0 or biologi > 100 or fisika < 0 or fisika > 100 or inggris < 0 or inggris > 100:
                raise ValueError("Nilai harus antara 0-100")

        except ValueError as e:
            # Jika konversi gagal atau nilai di luar range, tampilkan error
            msg.showerror("Error", f"Nilai harus berupa angka 0-100!\n{str(e)}")
            return None

        # Return tuple berisi semua nilai jika valid
        return nama, biologi, fisika, inggris

    # ========================================================================
    # METHOD 3: PREDIKSI FAKULTAS - LOGIKA UTAMA PREDIKSI
    # ========================================================================
    def prediksi_fakultas(self, biologi, fisika, inggris):
        # Cari nilai maksimum dari ketiga nilai
        nilai_max = max(biologi, fisika, inggris)
        
        # Cek nilai mana yang tertinggi
        if nilai_max == biologi:
            return "Kedokteran"  # Biologi tertinggi
        elif nilai_max == fisika:
            return "Teknik"  # Fisika tertinggi
        else:
            return "Bahasa"  # Inggris tertinggi

    # ========================================================================
    # METHOD 4: SUBMIT NILAI - PROSES SAAT TOMBOL SUBMIT DIKLIK
    # ========================================================================
    def submit_nilai(self):
        # STEP 1: Validasi input
        val = self.validate_inputs()
        if not val:
            return  # Jika validasi gagal, stop eksekusi
        
        # STEP 2: Ambil nilai dari hasil validasi
        nama, biologi, fisika, inggris = val
        
        # STEP 3: Prediksi fakultas berdasarkan nilai tertinggi
        prediksi = self.prediksi_fakultas(biologi, fisika, inggris)
        
        try:
            # STEP 4: Simpan data ke database
            new_id = insert_nilai(nama, biologi, fisika, inggris, prediksi)
            
            # STEP 5: Tampilkan popup sukses dengan detail hasil
            msg.showinfo("Hasil Prediksi", 
                        f"Data berhasil disimpan!\n\n"
                        f"Nama: {nama}\n"
                        f"Biologi: {biologi}\n"
                        f"Fisika: {fisika}\n"
                        f"Inggris: {inggris}\n\n"
                        f"Prediksi Fakultas: {prediksi}")
            
            # STEP 6: Refresh tabel untuk menampilkan data baru
            self.read_data()
            
            # STEP 7: Kosongkan semua input
            self.clear_inputs()
            
        except Exception as e:
            # Jika terjadi error saat menyimpan ke database
            msg.showerror("Database Error", str(e))

    # ========================================================================
    # METHOD 5: READ DATA - MEMBACA DAN MENAMPILKAN DATA DARI DATABASE
    # ========================================================================
    def read_data(self):
        # STEP 1: Hapus semua data yang ada di treeview
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        try:
            # STEP 2: Baca semua data dari database
            rows = read_nilai()
            
            # STEP 3: Insert setiap row ke dalam treeview
            for r in rows:
                # r adalah tuple: (id, nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
                self.tree.insert("", tk.END, values=r)
                
        except Exception as e:
            # Jika terjadi error saat membaca database
            msg.showerror("Database Error", str(e))


# ============================================================================
# MAIN PROGRAM - MENJALANKAN APLIKASI
# ============================================================================
if __name__ == "__main__":
    app = PrediksiProdi()  # Buat instance/objek dari class PrediksiProdi
    app.mainloop()  # Jalankan event loop GUI (aplikasi akan terus berjalan)
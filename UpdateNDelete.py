import sqlite3
import tkinter as tk
import tkinter.messagebox as msg
from tkinter import ttk

def koneksi():
    koneksi = sqlite3.connect("prediksi_prodi.db")
    return koneksi

def create_table():
    con = koneksi()
    cur = con.cursor()
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
    con.commit()
    con.close()

def insert_nilai(nama, biologi, fisika, inggris, prediksi):
    con = koneksi()
    cur = con.cursor()
    cur.execute("""
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas) 
        VALUES (?, ?, ?, ?, ?)
    """, (nama, biologi, fisika, inggris, prediksi))
    con.commit()
    con.close()

# FUNGSI BARU: UPDATE DATA
def update_nilai(id_siswa, nama, biologi, fisika, inggris, prediksi):
    con = koneksi()
    cur = con.cursor()
    cur.execute("""
        UPDATE nilai_siswa 
        SET nama_siswa=?, biologi=?, fisika=?, inggris=?, prediksi_fakultas=?
        WHERE id=?
    """, (nama, biologi, fisika, inggris, prediksi, id_siswa))
    con.commit()
    con.close()

# FUNGSI BARU: DELETE DATA
def delete_nilai(id_siswa):
    con = koneksi()
    cur = con.cursor()
    cur.execute("DELETE FROM nilai_siswa WHERE id=?", (id_siswa,))
    con.commit()
    con.close()

def read_nilai():
    con = koneksi()
    cur = con.cursor()
    cur.execute("SELECT id, nama_siswa, biologi, fisika, inggris, prediksi_fakultas FROM nilai_siswa ORDER BY id DESC")
    rows = cur.fetchall()
    con.close()
    return rows

# Inisialisasi Tabel
create_table()


# ============================================================================
# BAGIAN GUI (INTERFACE)
# ============================================================================

class PrediksiProdi(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title("Aplikasi Prediksi Prodi Pilihan")
        self.geometry("750x650")
        self.configure(bg="#e3f2fd")
        
        # Variabel untuk menyimpan ID record yang sedang dipilih (untuk update/delete)
        self.selected_record_id = None

        # --- JUDUL ---
        judul = tk.Label(self, text="Aplikasi Prediksi Prodi Pilihan", font=("Arial", 18, "bold"), bg="#e3f2fd", fg="#1565c0")
        judul.pack(pady=20)

        # --- FRAME INPUT ---
        frm = tk.Frame(self, bg="#ffffff", padx=20, pady=20)
        frm.pack(padx=20, pady=10, fill="x")

        # Input Nama
        tk.Label(frm, text="Nama Siswa:", bg="#ffffff", font=("Arial", 10)).grid(row=0, column=0, sticky="e", pady=5, padx=10)
        self.ent_nama = tk.Entry(frm, width=40, font=("Arial", 10))
        self.ent_nama.grid(row=0, column=1, sticky="w", pady=5)

        # Input Biologi
        tk.Label(frm, text="Nilai Biologi:", bg="#ffffff", font=("Arial", 10)).grid(row=1, column=0, sticky="e", pady=5, padx=10)
        self.ent_biologi = tk.Entry(frm, width=40, font=("Arial", 10))
        self.ent_biologi.grid(row=1, column=1, sticky="w", pady=5)

        # Input Fisika
        tk.Label(frm, text="Nilai Fisika:", bg="#ffffff", font=("Arial", 10)).grid(row=2, column=0, sticky="e", pady=5, padx=10)
        self.ent_fisika = tk.Entry(frm, width=40, font=("Arial", 10))
        self.ent_fisika.grid(row=2, column=1, sticky="w", pady=5)

        # Input Inggris
        tk.Label(frm, text="Nilai Inggris:", bg="#ffffff", font=("Arial", 10)).grid(row=3, column=0, sticky="e", pady=5, padx=10)
        self.ent_inggris = tk.Entry(frm, width=40, font=("Arial", 10))
        self.ent_inggris.grid(row=3, column=1, sticky="w", pady=5)

        # --- FRAME TOMBOL ---
        btn_frame = tk.Frame(frm, bg="#ffffff")
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)

        # Tombol Submit (Add)
        self.btn_submit = tk.Button(btn_frame, text="Submit Nilai", width=10, bg="#1976d2", fg="white", font=("Arial", 10, "bold"), command=self.submit_nilai)
        self.btn_submit.pack(side="left", padx=5)

        # Tombol Update (Baru)
        self.btn_update = tk.Button(btn_frame, text="Update", width=10, bg="#2faa02", fg="white", font=("Arial", 10, "bold"), command=self.update_data)
        self.btn_update.pack(side="left", padx=5)

        # Tombol Delete (Baru)
        self.btn_delete = tk.Button(btn_frame, text="Delete", width=10, bg="#d32f2f", fg="white", font=("Arial", 10, "bold"), command=self.delete_data)
        self.btn_delete.pack(side="left", padx=5)

        # --- TABEL TREEVIEW ---
        cols = ("id", "nama", "biologi", "fisika", "inggris", "prediksi")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=10)
        
        self.tree.heading("id", text="ID")
        self.tree.column("id", width=40, anchor="center")
        self.tree.heading("nama", text="Nama Siswa")
        self.tree.column("nama", width=180)
        self.tree.heading("biologi", text="Biologi")
        self.tree.column("biologi", width=70, anchor="center")
        self.tree.heading("fisika", text="Fisika")
        self.tree.column("fisika", width=70, anchor="center")
        self.tree.heading("inggris", text="Inggris")
        self.tree.column("inggris", width=70, anchor="center")
        self.tree.heading("prediksi", text="Prodi Pilihan")
        self.tree.column("prediksi", width=150, anchor="center")
        
        self.tree.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Event Listener: Saat baris di tabel diklik
        self.tree.bind("<<TreeviewSelect>>", self.on_select_record)

        # Load data awal
        self.read_data()

    # --- LOGIKA APLIKASI ---

    def reset_form(self):
        """Mengosongkan form dan mereset ID pilihan"""
        self.ent_nama.delete(0, tk.END)
        self.ent_biologi.delete(0, tk.END)
        self.ent_fisika.delete(0, tk.END)
        self.ent_inggris.delete(0, tk.END)
        self.selected_record_id = None
        self.btn_submit.config(state="normal") # Aktifkan tombol add kembali

    def on_select_record(self, event):
        """Mengisi form input saat baris tabel diklik"""
        try:
            selected_item = self.tree.selection()[0] # Ambil item yang dipilih
            values = self.tree.item(selected_item, 'values') # Ambil datanya
            
            # Simpan ID record untuk keperluan update/delete
            self.selected_record_id = values[0]
            
            # Isi form input
            self.ent_nama.delete(0, tk.END)
            self.ent_nama.insert(0, values[1])
            
            self.ent_biologi.delete(0, tk.END)
            self.ent_biologi.insert(0, values[2])
            
            self.ent_fisika.delete(0, tk.END)
            self.ent_fisika.insert(0, values[3])
            
            self.ent_inggris.delete(0, tk.END)
            self.ent_inggris.insert(0, values[4])
            
        except IndexError:
            pass

    def validate_inputs(self):
        nama = self.ent_nama.get().strip()
        if not nama:
            msg.showwarning("Peringatan", "Nama tidak boleh kosong!")
            return None
            
        try:
            bio = int(self.ent_biologi.get())
            fis = int(self.ent_fisika.get())
            ing = int(self.ent_inggris.get())
            
            if not (0 <= bio <= 100 and 0 <= fis <= 100 and 0 <= ing <= 100):
                 raise ValueError("Range 0-100")
                 
            return nama, bio, fis, ing
        except ValueError:
            msg.showerror("Error", "Nilai harus berupa angka 0 - 100!")
            return None

    def tentukan_prediksi(self, bio, fis, ing):
        """
        Logika Penentuan Prodi:
        - Biologi Tertinggi -> Kedokteran
        - Fisika Tertinggi -> Teknik
        - Inggris Tertinggi -> Bahasa
        """
        if bio > fis and bio > ing:
            return "Kedokteran"
        elif fis > bio and fis > ing:
            return "Teknik"
        elif ing > bio and ing > fis:
            return "Bahasa"
        else:
            # Jika ada nilai yang sama tinggi (misal Bio == Fisika)
            # Kita buat prioritas default atau tampilkan kondisi lain
            # Disini kita pakai prioritas urutan: Kedokteran > Teknik > Bahasa
            if bio == max(bio, fis, ing):
                return "Kedokteran"
            elif fis == max(bio, fis, ing):
                return "Teknik"
            else:
                return "Bahasa"

    def submit_nilai(self):
        data = self.validate_inputs()
        if not data: return
        
        nama, bio, fis, ing = data
        prediksi = self.tentukan_prediksi(bio, fis, ing)
        
        insert_nilai(nama, bio, fis, ing, prediksi)
        self.read_data()
        self.reset_form()
        msg.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi: {prediksi}")

    def update_data(self):
        if not self.selected_record_id:
            msg.showwarning("Peringatan", "Pilih data dari tabel terlebih dahulu untuk di-update!")
            return
            
        data = self.validate_inputs()
        if not data: return
        
        nama, bio, fis, ing = data
        prediksi = self.tentukan_prediksi(bio, fis, ing)
        
        # Panggil fungsi database update
        update_nilai(self.selected_record_id, nama, bio, fis, ing, prediksi)
        
        self.read_data()
        self.reset_form()
        msg.showinfo("Sukses", f"Data berhasil diperbarui!\nPrediksi Baru: {prediksi}")

    def delete_data(self):
        if not self.selected_record_id:
            msg.showwarning("Peringatan", "Pilih data dari tabel terlebih dahulu untuk dihapus!")
            return

        confirm = msg.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus data ini?")
        if confirm:
            delete_nilai(self.selected_record_id)
            self.read_data()
            self.reset_form()
            msg.showinfo("Sukses", "Data berhasil dihapus!")

    def read_data(self):
        # Bersihkan tabel lama
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # Ambil data baru
        rows = read_nilai()
        for row in rows:
            self.tree.insert("", tk.END, values=row)

if __name__ == "__main__":
    app = PrediksiProdi()
    app.mainloop()
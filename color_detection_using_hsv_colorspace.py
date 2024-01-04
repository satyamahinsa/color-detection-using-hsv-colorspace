import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, IntVar, ttk
from PIL import Image, ImageTk


class ColorDetectionApp:
    def __init__(self, root):
        # Inisialisasi objek aplikasi dengan parameter root
        self.root = root
        self.root.title("Color Detection App")

        # Mengatur ukuran awal aplikasi
        self.root.geometry("1000x500")

        # Mengatur style untuk bagian tombol
        style = ttk.Style()
        style.configure('TButton', font=('tahoma', 14, 'bold'), borderwidth='4')

        # Inisialisasi path gambar terakhir yang dipilih
        self.last_image_path = None

        # Definisikan rentang warna yang ingin dideteksi berdasarkan pilihan pengguna
        # Warna hsv dengan rentang nilai minimum dan maksimum
        self.color_ranges = {
            'Merah': ([0, 50, 50], [6, 255, 255]),
            'Merah Muda': ([150, 50, 50], [170, 255, 255]),
            'Jingga': ([8,150,150], [20,255,255]),
            'Coklat': ([8,130,55], [12,255,135]),
            'Kuning': ([20, 50, 50], [40, 255, 255]),
            'Hijau': ([40, 50, 50], [80, 255, 255]),
            'Biru': ([85, 0, 0], [130, 255, 255]),
            'Ungu': ([130, 50, 50], [160, 255, 255]),
            'Putih': ([0, 0, 85], [180, 65, 255]),
            'Hitam': ([0, 0, 0], [180, 255, 50]),
            'Abu-Abu': ([0, 0, 80], [180, 20, 200])
        }

        # Inisialisasi main_frame sebagai frame utama untuk aplikasi
        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Inisialisasi button_open sebagai tombol untuk membuka dialog pemilihan file gambar
        button_open = ttk.Button(main_frame, text="Pilih Gambar", command=self.open_file_dialog)
        button_open.pack(pady=10)
        
        # Inisialisasi color_frame sebagai frame untuk kumpulan checkbox warna
        color_frame = ttk.Frame(main_frame)
        color_frame.pack(pady=5)

        # Inisialisasi variabel selected_colors sebagai status untuk setiap warna
        # Merepresentasikan status checkbox terkait dengan setiap warna yang dipilih oleh user
        self.selected_colors = {color: IntVar() for color in self.color_ranges}

        # Inisialisasi beberapa checkbox untuk setiap warna yang telah didefinisikan
        for color in self.selected_colors:
            checkbox = ttk.Checkbutton(color_frame, text=color, variable=self.selected_colors[color])
            checkbox.pack(side=tk.LEFT, padx=5)

        # Inisialisasi button_change_color sebagai tombol untuk mengubah gambar sesuai pilihan warna
        button_change_color = ttk.Button(main_frame, text="Deteksi Warna", command=self.change_color_selection)
        button_change_color.pack(pady=10)

        # Inisialisasi image_frame_container sebagai frame untuk menampilkan gambar asli dan hasil deteksi warna
        image_frame_container = ttk.Frame(main_frame)
        image_frame_container.pack(pady=10)

        # Inisialisasi original_image_frame sebagai frame untuk menampilkan gambar asli di sebelah kiri
        original_image_frame = ttk.Frame(image_frame_container)
        original_image_frame.pack(side=tk.LEFT)
        
        # Inisialisasi result_image_frame sebagai frame untuk menampilkan hasil deteksi warna di sebelah kanan
        result_image_frame = ttk.Frame(image_frame_container)
        result_image_frame.pack(side=tk.RIGHT)

        # Inisialisasi original_label sebagai label untuk menampilkan header Gambar Asli
        self.original_label = ttk.Label(original_image_frame, text="Gambar Asli", font=('tahoma', 20, 'bold'))
        # Inisialisasi original_image sebagai label untuk menampilkan gambar asli
        self.original_image = ttk.Label(original_image_frame, background="", anchor="center")
        

        # Inisialisasi result_label sebagai label untuk menampilkan header Hasil Deteksi Warna
        self.result_label = ttk.Label(result_image_frame, text="Hasil Deteksi Warna", font=('tahoma', 20, 'bold'))
        # Inisialisasi result_image sebagai label untuk menampilkan gambar hasil deteksi warna
        self.result_image = ttk.Label(result_image_frame, background="", anchor="center")
        

    def detect_color(self, image_path):
        # Melakukan reset atau hapus gambar sebelumnya
        self.original_image.config(image=None)
        self.result_image.config(image=None)
        
        # Memberhentikan fungsi ketika path gambar tidak valid
        if not image_path:
            return  

        # Inisialisasi original_image sebagai gambar dari path yang telah dimasukkan
        original_image = cv2.imread(image_path)
        # Melakukan resize terhadap original_image dengan ukuran 400x300
        original_image = cv2.resize(original_image, (400, 300))
        # Mengubah format warna menjadi RGB agar bisa ditampilkan sebagai gambar asli
        image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

        # Mengubah format warna menjadi HSV agar bisa diolah
        hsv_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)

        # Inisialisasi combined_mask sebagai mask kosong yang akan digunakan untuk menentukan area di gambar yang sesuai dengan warna-warna yang dipilih
        combined_mask = np.zeros_like(hsv_image[:, :, 0])

        # Perulangan untuk menggabungkan setiap warna yang dipilih menjadi gambar hasil deteksi warna
        for color in self.color_ranges:
            if self.selected_colors[color].get():
                lower, upper = self.color_ranges[color]
                color_mask = cv2.inRange(hsv_image, np.array(lower), np.array(upper))
                combined_mask = cv2.bitwise_or(combined_mask, color_mask)

        # Inisialisasi result_image sebagai hasil penggabungan hasil mask dan gambar asli
        result_image = cv2.bitwise_and(original_image, original_image, mask=combined_mask)

        # Konversi array yang menyimpan gambar ke objek Image
        original_image = Image.fromarray(image)
        # Konversi original_image menjadi objek ImageTk untuk penggunaan dalam aplikasi
        original_image = ImageTk.PhotoImage(original_image)
        self.original_label.pack(side=tk.TOP)
        self.original_image.config(image=original_image)
        self.original_image.image = original_image
        self.original_image.pack(side=tk.LEFT, padx=10)

        # Mengubah format warna menjadi RGB agar bisa ditampilkan pada aplikasi
        result_image = cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB)
        # Konversi array yang menyimpan gambar ke objek Image
        result_image = Image.fromarray(result_image)
        # Konversi result_image menjadi objek ImageTk untuk penggunaan dalam aplikasi
        result_image = ImageTk.PhotoImage(result_image)
        self.result_label.pack(side=tk.TOP)
        self.result_image.config(image=result_image)
        self.result_image.image = result_image
        self.result_image.pack(side=tk.RIGHT, padx=10)

    def open_file_dialog(self):
        # Membuka dialog pemilihan file gambar dan menyimpan path file yang dipilih
        file_path = filedialog.askopenfilename(title="Pilih file gambar")
        
        if file_path:
            # Menyimpan path file gambar terakhir yang dipilih
            self.last_image_path = file_path
            # Memanggil fungsi detect_color untuk melakukan deteksi warna pada gambar yang dipilih
            self.detect_color(file_path)

    def change_color_selection(self):
        if self.last_image_path:
            # Memanggil fungsi detect_color untuk melakukan deteksi warna pada gambar terakhir yang dipilih
            self.detect_color(self.last_image_path)

if __name__ == "__main__":
    # Membuat objek Tkinter Tk sebagai jendela utama
    root = tk.Tk()
    # Membuat objek ColorDetectionApp dengan menggunakan root
    app = ColorDetectionApp(root)
    # Memulai loop utama aplikasi untuk menampilkan antarmuka grafis dan menanggapi peristiwa user
    root.mainloop()

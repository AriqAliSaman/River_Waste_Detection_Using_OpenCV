import os
import cv2
import time
import threading
import numpy as np
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import filedialog
from get_background import get_background

# Membuat window utama
app = tk.Tk()
app.title("DETEKSI SAMPAH PADA ALIRAN SUNGAI DI JAKARTA")

# Mengatur tinggi dan lebar window
window_width = 800
window_height = 500

# Mendapatkan dimensi layar
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

# Menghitung posisi tengah layar
center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)

# Mengatur posisi window
app.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

# Membuat frame utama
main_frame = tk.Frame(app)
main_frame.pack(fill=tk.BOTH, expand=True)

# Membuat sidebar
sidebar_frame = tk.Frame(main_frame, width=200, bg="#433F3F")
sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

# Membuat logo
logo_image = Image.open("icon.png")
logo_image = logo_image.resize((60, 60))
logo_photo = ImageTk.PhotoImage(logo_image)

#! Fungsi untuk berpindah halaman
def open_page(page_name, text_to_set):
    card_frame.select(page_name)
    set_page_text(page_name, text_to_set)

def set_page_text(page_name, text_to_set):
    if page_name == halaman_utama:
        halaman_utama_label.config(text=text_to_set)
    elif page_name == tahap_1:
        tahap_1_label.config(text=text_to_set)
    elif page_name == tahap_2:
        tahap_2_label.config(text=text_to_set)
    elif page_name == tahap_3:
        tahap_3_label.config(text=text_to_set)
    elif page_name == tahap_4:
        tahap_4_label.config(text=text_to_set)
    elif page_name == tahap_5:
        tahap_5_label.config(text=text_to_set)
    elif page_name == tahap_6:
        tahap_6_label.config(text=text_to_set)
    elif page_name == tahap_7:
        tahap_7_label.config(text=text_to_set)
    elif page_name == tahap_8:
        tahap_8_label.config(text=text_to_set)
#! Fungsi untuk berpindah halaman

video_file = None

#! +++ Pilih Video +++
def browse_file():
    global video_file
    video_file = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mkv *.mov")])
    if video_file:
        file_label.config(text=f"File yang dipilih: {video_file}")
    else: 
        video_file = None
        file_label.config(text="File yang dipilih: ")
#! +++ Pilih Video +++

#! +++ Putar Video Original +++
def start_play_original_video():
    if video_file is None:
        messagebox.showwarning("Peringatan", "Silakan kembali ke tahap 1 untuk memilih video terlebih dahulu.")
        return
    else:
        loading_label = ttk.Label(tahap_2, text="Processing Video, Please Wait...", font=("Helvetica", 10))
        loading_label.pack(pady=15)
        
        # Menampilkan label loading
        app.update_idletasks()  
        
        # Jalankan perintah
        play_original_video()  
        
        # Hapus label loading setelah selesai
        loading_label.destroy() 
        
def play_original_video():
    cap = cv2.VideoCapture(video_file)
    frame_rate = 30  # Ganti dengan frame rate yang diinginkan
    delay = 1 / frame_rate
    while cap.isOpened():
        read, frame = cap.read()
        if read == True:
            cv2.imshow('Video Original', frame)
            time.sleep(delay)  # Mengatur kecepatan frame
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        else:
            break

    cap.release()
    cv2.destroyAllWindows()
#! +++ Putar Video Original +++

#! +++ Proses Background Modelling +++
def start_process_background_modelling():
    if video_file is None:
        messagebox.showwarning("Peringatan", "Silakan kembali ke tahap 1 untuk memilih video terlebih dahulu.")
        return
    else:
        loading_label = ttk.Label(tahap_3, text="Processing Background Modelling, Please Wait...", font=("Helvetica", 10))
        loading_label.pack(pady=15)
        
        # Menampilkan label loading
        app.update_idletasks()  
        
        # Jalankan perintah
        process_background_modelling()  
        
        # Hapus label loading setelah selesai
        loading_label.destroy() 

def process_background_modelling():
    cap = cv2.VideoCapture(video_file)
        
    # Dapatkan model background
    background = get_background(video_file)
        
    # Mengonversi model background ke format skala abu-abu
    background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
        
    while cap.isOpened():
        read, frame = cap.read()
        if read == True:
            #! Mengubah citra menjadi skala abu-abu
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow('Proses Background Modelling', background)
            
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break

        else:
            break        
            
    cap.release()
    cv2.destroyAllWindows()
#! +++ Proses Background Modelling +++

#! +++ Proses Grayscale +++
def start_process_grayscale():
    if video_file is None:
        messagebox.showwarning("Peringatan", "Silakan kembali ke tahap 1 untuk memilih video terlebih dahulu.")
        return
    else:
        loading_label = ttk.Label(tahap_4, text="Processing Grayscale, Please Wait...", font=("Helvetica", 10))
        loading_label.pack(pady=15)
    
        # Menampilkan label loading
        app.update_idletasks()  
    
        # Jalankan perintah
        process_grayscale()
    
        # Hapus label loading setelah selesai
        loading_label.destroy()
    
def process_grayscale():
    cap = cv2.VideoCapture(video_file)
    frame_rate = 30  # Ganti dengan frame rate yang diinginkan
    delay = 1 / frame_rate
    while cap.isOpened():
        read, frame = cap.read()
        if read == True:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow('Proses Grayscale', gray_frame)
            time.sleep(delay)  # Mengatur kecepatan frame
        
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
        else:
            break
         
    cap.release()
    cv2.destroyAllWindows()
#! +++ Proses Grayscale +++

#! +++ Proses Frame Differencing +++
def start_process_frame_differencing():
    if video_file is None:
        messagebox.showwarning("Peringatan", "Silakan kembali ke tahap 1 untuk memilih video terlebih dahulu.")
        return
    else:
        loading_label = ttk.Label(tahap_5, text="Processing Frame Differencing, Please Wait...", font=("Helvetica", 10))
        loading_label.pack(pady=15)
        
        # Menampilkan label loading
        app.update_idletasks()  
        
        # Jalankan perintah
        process_frame_differencing()  
        
        # Hapus label loading setelah selesai
        loading_label.destroy() 

def process_frame_differencing():
    cap = cv2.VideoCapture(video_file)
        
    # Dapatkan model background
    background = get_background(video_file)
        
    # Mengonversi model background ke format skala abu-abu
    background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
        
    # Mengatur kecepatan frame
    cap.set(cv2.CAP_PROP_FPS, 60)
        
    while cap.isOpened():
        read, frame = cap.read()
        if read == True:
            #! Mengubah citra menjadi skala abu-abu
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            #! Dilakukan penghitungan perbedaan antara bingkai saat ini (gray) dan bingkai latar belakang 
            #! (background) dengan menggunakan fungsi cv2.absdiff(). Hasil dari operasi ini adalah citra 
            #! perbedaan (Frame Differencing).
            frame_diff = cv2.absdiff(gray, background)
            cv2.imshow('Proses Frame Differencing', frame_diff)
        
            if cv2.waitKey(1000 // 60) & 0xFF == ord('q'):
                break
            
        else:
            break
        
    cap.release()
    cv2.destroyAllWindows()        
#! +++ Proses Frame Differencing +++

#! +++ Proses Background Subtraction +++
def start_process_background_subtraction():
    if video_file is None:
        messagebox.showwarning("Peringatan", "Silakan kembali ke tahap 1 untuk memilih video terlebih dahulu.")
        return
    else:
        loading_label = ttk.Label(tahap_6, text="Processing Background Subtraction, Please Wait...", font=("Helvetica", 10))
        loading_label.pack(pady=15)
        
        # Menampilkan label loading
        app.update_idletasks()  
        
        # Jalankan perintah
        process_background_subtraction()  
        
        # Hapus label loading setelah selesai
        loading_label.destroy() 
    
def process_background_subtraction():
    cap = cv2.VideoCapture(video_file)

    # Dapatkan model background
    background = get_background(video_file)

    # Mengonversi model background ke format skala abu-abu
    background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)

    # Mengatur kecepatan frame
    cap.set(cv2.CAP_PROP_FPS, 60)

    while cap.isOpened():
        read, frame = cap.read()
        if read == True:
            #! Mengubah citra menjadi skala abu-abu
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            #! Dilakukan penghitungan perbedaan antara bingkai saat ini (gray) dan bingkai latar belakang 
            #! (background) dengan menggunakan fungsi cv2.absdiff(). Hasil dari operasi ini adalah citra 
            #! perbedaan (Frame Differencing).
            frame_diff = cv2.absdiff(gray, background)

            #! Jika terdapat pixel dengan intensitas di atas 70, maka akan menjadi putih (nilai maks 255)
            #! Sedangkan terdapat pixel dengan intensitas di bawah 70, maka akan menjadi hitam (nilai min 0)
            read, thres = cv2.threshold(frame_diff, 70, 255, cv2.THRESH_BINARY)

            #! Melebarkan sedikit frame untuk mendapatkan lebih banyak area putih agar pendeteksian kontur sedikit lebih mudah
            dilate_frame = cv2.dilate(thres, None, iterations=2)
            cv2.imshow('Proses Background Subtraction', dilate_frame)
            
            if cv2.waitKey(1000 // 60) & 0xFF == ord('q'):
                break
            
        else:
            break

    cap.release()
    cv2.destroyAllWindows()
#! +++ Proses Background Subtraction +++

#! +++ Proses Object Detection +++
def start_process_object_detection():
    if video_file is None:
        messagebox.showwarning("Peringatan", "Silakan kembali ke tahap 1 untuk memilih video terlebih dahulu.")
        return
    else:
        loading_label = ttk.Label(tahap_7, text="Processing Object Detection, Please Wait...", font=("Helvetica", 10))
        loading_label.pack(pady=15)
        
        # Menampilkan label loading
        app.update_idletasks()  
        
        # Jalankan perintah
        process_object_detection()  
        
        # Hapus label loading setelah selesai
        loading_label.destroy()
        
def process_object_detection():
    cap = cv2.VideoCapture(video_file)

    # Dapatkan model background
    background = get_background(video_file)

    # Mengonversi model background ke format skala abu-abu
    background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)

    # Mengatur kecepatan frame
    cap.set(cv2.CAP_PROP_FPS, 60)

    # Inisialisasi variabel
    frame_count = 0
    consecutive_frame = 40

    while cap.isOpened():
        read, frame = cap.read()
        if read == True:
            frame_count += 1

            #! Mengubah citra menjadi skala abu-abu
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            #! Jika 'frame_count' adalah kelipatan dari "consecutive_frame" atau pada frame pertama, maka array akan dikosongkan kembali
            if frame_count % consecutive_frame == 0 or frame_count == 1:
                frame_diff_list = []    

            #! Dilakukan penghitungan perbedaan antara bingkai saat ini (gray) dan bingkai latar belakang 
            #! (background) dengan menggunakan fungsi cv2.absdiff(). Hasil dari operasi ini adalah citra 
            #! perbedaan (Frame Differencing).
            frame_diff = cv2.absdiff(gray, background)

            #! Jika terdapat pixel dengan intensitas di atas 70, maka akan menjadi putih (nilai maks 255)
            #! Sedangkan terdapat pixel dengan intensitas di bawah 70, maka akan menjadi hitam (nilai min 0)
            read, thres = cv2.threshold(frame_diff, 70, 255, cv2.THRESH_BINARY)

            #! Melebarkan sedikit frame untuk mendapatkan lebih banyak area putih agar pendeteksian kontur sedikit lebih mudah
            dilate_frame = cv2.dilate(thres, None, iterations=2)

            #! Menambahkan frame hasil dilasi ke dalam `frame_diff_list` untuk memiliki informasi tentang perubahan dalam beberapa frame sebelumnya
            frame_diff_list.append(dilate_frame)
            
            # print(frame_diff_list)

            #! Jika panjang 'frame_diff_list' sama dengan 'consecutive_frame' maka akan lanjut ke proses selanjutnya
            if len(frame_diff_list) == consecutive_frame:
                    
                # Jumlahkan semua frame di `frame_diff_list`
                sum_frames = sum(frame_diff_list)
                
                # Menemukan kontur menggunakan fungsi cv2.findContours
                contours, hierarchy = cv2.findContours(np.uint8(sum_frames), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                print(contours)
                
            #     for contour in contours:
                    
            #         #! Kontur yang memiliki luas kurang dari 500 piksel diabaikan atau dilewati
            #         if cv2.contourArea(contour) < 500:
            #             continue
                    
            #         #! Mendapatkan koordinat dan dimensi dari kotak pembatas (bounding box) yang melingkupi kontur tersebut.
            #         #! Fungsi cv2.boundingRect mengembalikan koordinat sudut kiri atas (x, y), lebar (w), dan tinggi (h) dari kotak pembatas
            #         (x, y, w, h) = cv2.boundingRect(contour)
                    
            #         #! Membuat kotak pembatas pada frame menggunakan fungsi cv2.rectangle# membuat kotak pembatas
            #         cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            #     cv2.imshow('Proses Object Detection', frame)
                
            #     if cv2.waitKey(1000 // 60) & 0xFF == ord('q'):
            #         break
                
        else:
            break
            
    cap.release()
    cv2.destroyAllWindows() 
#! +++ Proses Object Detection +++

#! +++ Proses Final Detection +++
def start_final_detection():
    if video_file is None:
        messagebox.showwarning("Peringatan", "Silakan kembali ke tahap 1 untuk memilih video terlebih dahulu.")
        return
    else:
        loading_label = ttk.Label(tahap_8, text="Processing Final Detection, Please Wait...", font=("Helvetica", 10))
        loading_label.pack(pady=15)
        
        # Menampilkan label loading
        app.update_idletasks()  
        
        # Jalankan perintah
        final_detection()  
        
        # Hapus label loading setelah selesai
        loading_label.destroy() 

def final_detection():
    cap = cv2.VideoCapture(video_file)
        
    # Dapatkan model background
    background = get_background(video_file)
        
    # Mengonversi model background ke format skala abu-abu
    background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
        
    # Mengatur kecepatan frame
    cap.set(cv2.CAP_PROP_FPS, 60)
        
    # Inisialisasi variabel
    frame_count = 0
    total_detected_frames = 0
    total_detected_objects = 0
    start_time = time.time()
    consecutive_frame = 40
    
    while cap.isOpened():
        read, frame = cap.read() #! "read" berfungsi untuk membaca setiap frame pada video
        if read == True: #! Selama video belum berakhir maka "read" akan bernilai true, jika sudah mencapai akhir video maka "read" akan menjadi false
            detected_objects = 0  
            frame_count += 1
           
            #! Mengubah citra menjadi skala abu-abu
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
           
            #! Jika 'frame_count' adalah kelipatan dari "consecutive_frame" atau pada frame pertama, maka array akan dikosongkan kembali
            if frame_count % consecutive_frame == 0 or frame_count == 1:
                frame_diff_list = []     
                
            #! Dilakukan penghitungan perbedaan antara bingkai saat ini (gray) dan bingkai latar belakang
            frame_diff = cv2.absdiff(gray, background)
                
            #! Jika terdapat pixel dengan intensitas di atas 70, maka akan menjadi putih (nilai maks 255)
            #! Sedangkan terdapat pixel dengan intensitas di bawah 70, maka akan menjadi hitam (nilai min 0)
            read, thres = cv2.threshold(frame_diff, 70, 255, cv2.THRESH_BINARY)
                
            #! Melebarkan sedikit frame untuk mendapatkan lebih banyak area putih agar pendeteksian kontur sedikit lebih mudah
            dilate_frame = cv2.dilate(thres, None, iterations=2)
                
            #! Menambahkan frame hasil dilasi ke dalam `frame_diff_list` untuk memiliki informasi tentang perubahan dalam beberapa frame sebelumnya
            frame_diff_list.append(dilate_frame)
            #! Jika panjang isi 'frame_diff_list' sama dengan 'consecutive_frame' maka akan lanjut ke proses deteksi
            #! Isi 'frame_diff_list' didapat dari kondisi if diatas, isi 'frame_diff_list' saat ini adalah kelipatan 40 {40,80,120,...}
            #! Nantinya di panjang array yang ke-40 akan terhitung/terdeteksi, setelah itu akan dijumlahkan
            if len(frame_diff_list) == consecutive_frame:
                    
                #! Jumlahkan semua frame di `frame_diff_list`
                sum_frames = sum(frame_diff_list)
                    
                #! Menemukan kontur menggunakan fungsi cv2.findContours
                contours, hierarchy = cv2.findContours(sum_frames, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    
                #! setiap elemen (kontur) dalam daftar contours
                for contour in contours:
                    
                    #! Kontur yang memiliki luas kurang dari 500 piksel diabaikan atau dilewati
                    if cv2.contourArea(contour) < 500:
                        continue
                        
                    #! Mendapatkan koordinat dan dimensi dari kotak pembatas (bounding box) yang melingkupi kontur tersebut.
                    #! Fungsi cv2.boundingRect mengembalikan koordinat sudut kiri atas (x, y), lebar (w), dan tinggi (h) dari kotak pembatas
                    (x, y, w, h) = cv2.boundingRect(contour)

                    #! Membuat kotak pembatas pada frame menggunakan fungsi cv2.rectangle    
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    detected_objects += 1
                    total_detected_objects += 1
                    
                if detected_objects > 0:
                    total_detected_frames += 1
                    
                #! Menampilkan nomor frame dan jumlah objek yang terdeteksi
                print(f"Frame ke-{(frame_count // consecutive_frame) * consecutive_frame}, "f"Jumlah objek terdeteksi: {detected_objects}")
                
                #! Dapatkan direktori tempat berkas video berada
                video_directory = os.path.dirname(video_file)
                            
                #! Simpan setiap frame yang berisi objek terdeteksi
                capture_folder = os.path.join(video_directory, "captures")
                os.makedirs(capture_folder, exist_ok=True)
                capture_filename = f"{capture_folder}/S_Baru_Barat_{(frame_count // consecutive_frame) * consecutive_frame}.png"
                cv2.imwrite(capture_filename, frame)
                print(f"Capture saved: {capture_filename}")
                
                #! Menampilkan jumlah objek yang terdeteksi di jendela video
                cv2.putText(frame, f"Objek Terdeteksi: {detected_objects}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                cv2.imshow('Final Detection', frame)
                    
                if cv2.waitKey(1000 // 60) & 0xFF == ord('q'):
                    break
                    
        else:
            break
        
    # Menambahkan informasi tentang durasi proses deteksi
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Durasi proses deteksi: {elapsed_time:.2f} detik") # Menampilkan total durasi proses deteksi berlangsung 
    print(f"Jumlah frame yang menangkap objek: {total_detected_frames}, Total jumlah objek terdeteksi: {total_detected_objects}") # Menampilkan jumlah frame yang menangkap objek dan jumlah objeknya
    print(f"Proses Selesai")
        
    cap.release()
    cv2.destroyAllWindows()
#! +++ Proses Final Detection +++

# Membuat tombol di sidebar
button_halaman_utama = tk.Button(sidebar_frame, border=0, image=logo_photo, bg="#433F3F",activebackground="#373737", command=lambda: open_page(halaman_utama, halaman_utama_paragraph))
button_tahap_1 = tk.Button(sidebar_frame, border=0, text="Tahap 1", font=("tahoma", 10, "bold"), bg="#433F3F", fg="#43BF24", activebackground="#373737", activeforeground="yellow", width=10, command=lambda: open_page(tahap_1, tahap_1_paragraph))
button_tahap_2 = tk.Button(sidebar_frame, border=0, text="Tahap 2", font=("tahoma", 10, "bold"), bg="#433F3F", fg="#43BF24", activebackground="#373737", activeforeground="yellow", width=10, command=lambda: open_page(tahap_2, tahap_2_paragraph))
button_tahap_3 = tk.Button(sidebar_frame, border=0, text="Tahap 3", font=("tahoma", 10, "bold"), bg="#433F3F", fg="#43BF24", activebackground="#373737", activeforeground="yellow", width=10, command=lambda: open_page(tahap_3, tahap_3_paragraph))
button_tahap_4 = tk.Button(sidebar_frame, border=0, text="Tahap 4", font=("tahoma", 10, "bold"), bg="#433F3F", fg="#43BF24", activebackground="#373737", activeforeground="yellow", width=10, command=lambda: open_page(tahap_4, tahap_4_paragraph))
button_tahap_5 = tk.Button(sidebar_frame, border=0, text="Tahap 5", font=("tahoma", 10, "bold"), bg="#433F3F", fg="#43BF24", activebackground="#373737", activeforeground="yellow", width=10, command=lambda: open_page(tahap_5, tahap_5_paragraph))
button_tahap_6 = tk.Button(sidebar_frame, border=0, text="Tahap 6", font=("tahoma", 10, "bold"), bg="#433F3F", fg="#43BF24", activebackground="#373737", activeforeground="yellow", width=10, command=lambda: open_page(tahap_6, tahap_6_paragraph))
button_tahap_7 = tk.Button(sidebar_frame, border=0, text="Tahap 7", font=("tahoma", 10, "bold"), bg="#433F3F", fg="#43BF24", activebackground="#373737", activeforeground="yellow", width=10, command=lambda: open_page(tahap_7, tahap_7_paragraph))
button_tahap_8 = tk.Button(sidebar_frame, border=0, text="Tahap 8", font=("tahoma", 10, "bold"), bg="#433F3F", fg="#43BF24", activebackground="#373737", activeforeground="yellow", width=10, command=lambda: open_page(tahap_8, tahap_8_paragraph))
button_halaman_utama.pack(pady=15, padx=10)
button_tahap_1.pack(pady=5, padx=10)
button_tahap_2.pack(pady=5, padx=10)
button_tahap_3.pack(pady=5, padx=10)
button_tahap_4.pack(pady=5, padx=10)
button_tahap_5.pack(pady=5, padx=10)
button_tahap_6.pack(pady=5, padx=10)
button_tahap_7.pack(pady=5, padx=10)
button_tahap_8.pack(pady=5, padx=10)

# Membuat headbar
headbar = tk.Frame(main_frame, height=20, bg="darkgreen")
headbar.pack(fill=tk.X)

# Membuat label di headbar
headbar_label = tk.Label(headbar, text="DETEKSI SAMPAH PADA ALIRAN SUNGAI DI JAKARTA", fg="yellow", bg="darkgreen", font=("Helvetica", 14, "bold"))
headbar_label.pack(pady=10)

strip = tk.Frame(main_frame, height=20, bg="yellow")
strip.pack(fill=tk.X)

strip_label = tk.Label(strip, bg="yellow", width=700)
strip_label.pack()

# Membuat card frame
card_frame = ttk.Notebook(main_frame)
card_frame.pack(fill=tk.BOTH, expand=True)


# Membuat Halaman Utama
halaman_utama = tk.Frame(card_frame)
card_frame.add(halaman_utama, text="")
# Membuat Isi di Halaman Utama
halaman_utama_paragraph = "ARIQ ALI SAMAN - 2011500739 \n\n"
halaman_utama_paragraph += "Aplikasi ini dibuat untuk melakukan pendeteksian sampah pada aliran sungai yang ada di Jakarta \n"
halaman_utama_paragraph += "Sekian Terimakasih"
halaman_utama_label = tk.Label(halaman_utama, text=halaman_utama_paragraph, font=("tahoma", 10, "bold"), padx=20, pady=10, justify='center')
halaman_utama_label.pack(fill='both')


# Membuat Halaman Tahap Pertama
tahap_1 = tk.Frame(card_frame)
card_frame.add(tahap_1, text="")
# Membuat Isi di Halaman Tahap Pertama
tahap_1_paragraph = "Tahap 1 (Pilih Video) \n\n"
tahap_1_paragraph += "Pada tahap yang pertama ini, diharuskan memilih file video yang akan dilakukan pendeteksian. "
tahap_1_paragraph += "Klik tombol di bawah ini untuk memilih video."
tahap_1_label = tk.Label(tahap_1, text=tahap_1_paragraph, font=("tahoma", 10, "bold"), padx=20, pady=10, justify='left', wraplength=666)
tahap_1_label.pack(fill='both')

browse_button = tk.Button(tahap_1, text="Pilih", command=browse_file, font=("tahoma", 10, "bold"), bg="darkgreen", fg="yellow", activebackground="yellow", activeforeground="darkgreen", width=10)
browse_button.pack(pady=15)

# Label untuk menampilkan nama file yang dipilih
file_label = tk.Label(tahap_1, font=("tahoma", 10), padx=20, pady=10, text="File yang dipilih: ", wraplength=666)
file_label.pack()


# Membuat Halaman Tahap Kedua
tahap_2 = tk.Frame(card_frame)
card_frame.add(tahap_2, text="")
# Membuat Isi di Halaman Tahap Kedua
tahap_2_paragraph = "Tahap 2 (Putar Video Original) \n\n"
tahap_2_paragraph += "Tahap kedua digunakan untuk memutar video yang telah dipilih sebelumnya. "
tahap_2_paragraph += "Klik tombol di bawah ini untuk memutar video yang telah dipilih."
tahap_2_label = tk.Label(tahap_2, text=tahap_2_paragraph, font=("tahoma", 10, "bold"), padx=20, pady=10, justify='left', wraplength=666)
tahap_2_label.pack(fill='both')

play_video_button = tk.Button(tahap_2, text="Jalankan", command=start_play_original_video, font=("tahoma", 10, "bold"), bg="darkgreen", fg="yellow", activebackground="yellow", activeforeground="darkgreen", width=10)
play_video_button.pack(pady=15)


# Membuat Halaman Tahap Ketiga
tahap_3 = tk.Frame(card_frame)
card_frame.add(tahap_3, text="")
# Membuat Isi di Halaman Tahap Ketiga
tahap_3_paragraph = "Tahap 3 (Proses Background Modelling) \n\n"
tahap_3_paragraph += "Tahap ketiga digunakan untuk menghilangkan objek dan hanya menyisakan background. "
tahap_3_paragraph += "Klik tombol di bawah ini untuk menjalankan proses background modelling."
tahap_3_label = tk.Label(tahap_3, text=tahap_3_paragraph, font=("tahoma", 10, "bold"), padx=20, pady=10, justify='left', wraplength=666)
tahap_3_label.pack(fill='both')

play_video_button = tk.Button(tahap_3, text="Jalankan", command=start_process_background_modelling, font=("tahoma", 10, "bold"), bg="darkgreen", fg="yellow", activebackground="yellow", activeforeground="darkgreen", width=10)
play_video_button.pack(pady=15)


# Membuat Halaman Tahap Keempat
tahap_4 = tk.Frame(card_frame)
card_frame.add(tahap_4, text="")
# Membuat Isi di Halaman Tahap Keempat
tahap_4_paragraph = "Tahap 4 (Proses Grayscale) \n\n"
tahap_4_paragraph += "Di tahap yang keempat ini video yang telah dipilih akan diubah menjadi grayscale. "
tahap_4_paragraph += "Grayscale hanya memiliki warna abu-abu dan tidak berwarna. Dengan menghilangkan warna, "
tahap_4_paragraph += "grayscale dapat memudahkan untuk lebih fokus pada bentuk dan tekstur objek dalam citra. Ini bisa menemukan detail yang mungkin tersembunyi "
tahap_4_paragraph += "dalam citra berwarna. "
tahap_4_paragraph += "Klik tombol di bawah ini untuk memulai proses grayscale."
tahap_4_label = tk.Label(tahap_4, text=tahap_4_paragraph, font=("tahoma", 10, "bold"), padx=20, pady=10, justify='left', wraplength=666)
tahap_4_label.pack(fill='both')

grayscale_button = tk.Button(tahap_4, text="Jalankan", command=start_process_grayscale, font=("tahoma", 10, "bold"), bg="darkgreen", fg="yellow", activebackground="yellow", activeforeground="darkgreen", width=10)
grayscale_button.pack(pady=15)


# Membuat Halaman Tahap Kelima
tahap_5 = tk.Frame(card_frame)
card_frame.add(tahap_5, text="")
# Membuat Isi di Halaman Tahap Kelima
tahap_5_paragraph = "Tahap 5 (Proses Frame Differencing) \n\n"
tahap_5_paragraph += "Tahap kelima ini digunakan untuk memulai proses frame differencing. Frame Differencing merupakan suatu metode untuk membedakan frame "
tahap_5_paragraph += "dengan menghitung selisih antara frame saat ini dengan model background untuk menemukan objek pada suatu citra. "
tahap_5_paragraph += "Frame Differencing juga berguna untuk mengecek apakah ada perbedaan antara dua buah frame yang sedang dibandingkan. Apabila terdapat "
tahap_5_paragraph += "perbedaan, berarti ada pergerakan objek dalam citra frame tersebut. "
tahap_5_paragraph += "Klik tombol di bawah ini untuk memulai proses frame differencing."
tahap_5_label = tk.Label(tahap_5, text=tahap_5_paragraph, font=("tahoma", 10, "bold"), padx=20, pady=10, justify='left', wraplength=666)
tahap_5_label.pack(fill='both')

frame_differencing_button = tk.Button(tahap_5, text="Jalankan", command=start_process_frame_differencing, font=("tahoma", 10, "bold"), bg="darkgreen", fg="yellow", activebackground="yellow", activeforeground="darkgreen", width=10)
frame_differencing_button.pack(pady=15)


# Membuat Halaman Tahap Keenam
tahap_6 = tk.Frame(card_frame)
card_frame.add(tahap_6, text="")
# Membuat Isi di Halaman Tahap Keenam
tahap_6_paragraph = "Tahap 6 (Proses Background Subtraction) \n\n"
tahap_6_paragraph += "Pada tahap yang keenam ini akan dilakukan proses background subtraction. "
tahap_6_paragraph += "Proses ini bertujuan untuk memperbesar atau menonjolkan fitur dalam video, seperti "
tahap_6_paragraph += "meningkatkan ketebalan garis tepi objek atau mengubah tampilan objek dalam video dengan cara tertentu. "
tahap_6_paragraph += "Klik tombol di bawah ini untuk memulai proses background subtraction."
tahap_6_label = tk.Label(tahap_6, text=tahap_6_paragraph, font=("tahoma", 10, "bold"), padx=20, pady=10, justify='left', wraplength=666)
tahap_6_label.pack(fill='both')

dilate_frame_button = tk.Button(tahap_6, text="Jalankan", command=start_process_background_subtraction, font=("tahoma", 10, "bold"), bg="darkgreen", fg="yellow", activebackground="yellow", activeforeground="darkgreen", width=10)
dilate_frame_button.pack(pady=15)


# Membuat Halaman Tahap Ketujuh
tahap_7 = tk.Frame(card_frame)
card_frame.add(tahap_7, text="")
# Membuat Isi di Halaman Tahap Ketujuh
tahap_7_paragraph = "Tahap 7 (Proses Object Detection) \n\n"
tahap_7_paragraph += "Pada tahap yang ketujuh ini adalah pendeteksian objek. "
tahap_7_paragraph += "Klik tombol di bawah ini untuk memulai proses object detection."
tahap_7_label = tk.Label(tahap_7, text=tahap_7_paragraph, font=("tahoma", 10, "bold"), padx=20, pady=10, justify='left', wraplength=666)
tahap_7_label.pack(fill='both')

result_detection_button = tk.Button(tahap_7, text="Jalankan", command=start_process_object_detection, font=("tahoma", 10, "bold"), bg="darkgreen", fg="yellow", activebackground="yellow", activeforeground="darkgreen", width=10)
result_detection_button.pack(pady=15)


# Membuat Halaman Tahap Terakhir
tahap_8 = tk.Frame(card_frame)
card_frame.add(tahap_8, text="")
# Membuat Isi di Halaman Tahap Terakhir
tahap_8_paragraph = "Tahap 8 (Final Detection) \n\n"
tahap_8_paragraph += "Pada tahap yang terakhir ini akan dilakukan perhitungan dari objek yang terdeteksi. "
tahap_8_paragraph += "Klik tombol di bawah ini untuk memulai pendeteksian akhir"
tahap_8_label = tk.Label(tahap_8, text=tahap_8_paragraph, font=("tahoma", 10, "bold"), padx=20, pady=10, justify='left', wraplength=666)
tahap_8_label.pack(fill='both')

result_detection_button = tk.Button(tahap_8, text="Jalankan", command=start_final_detection, font=("tahoma", 10, "bold"), bg="darkgreen", fg="yellow", activebackground="yellow", activeforeground="darkgreen", width=10)
result_detection_button.pack(pady=15)


strip_down = tk.Frame(main_frame, height=20, bg="yellow")
strip_down.pack(fill=tk.X)

strip_down_label = tk.Label(strip_down, bg="yellow", width=700)
strip_down_label.pack()

# Membuat footer
footer = tk.Frame(main_frame, height=20, bg="darkgreen")
footer.pack(fill='both')

# Membuat label di footer
footer_label = tk.Label(footer, text="@copyright Ariq Ali Saman - 2011500739", fg="yellow", bg="darkgreen", font=("Tahoma", 10))
footer_label.pack()

app.mainloop()
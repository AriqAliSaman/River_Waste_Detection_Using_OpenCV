import numpy as np
import cv2

def get_background(file_path):
    cap = cv2.VideoCapture(file_path)
    
    #! cv2.CAP_PROP_FRAME_COUNT digunakan untuk mendapatkan jumlah total frame dalam video
    #! Memilih frame secara acak untuk menghitung nilai median
    frame_indices = cap.get(cv2.CAP_PROP_FRAME_COUNT) * np.random.uniform(size=10)
    
    #! Membuat array kosong (frames) untuk menyimpan frame-frame yang akan dipilih
    frames = []
    #! Dilakukan iterasi untuk setiap indeks (idx) dalam array frame_indices
    #! Setiap nilai idx merepresentasikan indeks dari frame di dalam video yang akan dipilih
    for idx in frame_indices:
    
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx) #! Mengatur posisi frame yang akan dibaca
        read, frame = cap.read() #! Membaca setiap frame
        frames.append(frame) #! Menambahkan frame ke dalam array frames
    
    #! Menghitung nilai median dari semua frame yang telah dipilih
    #! Hasilnya adalah frame median yang kemudian diubah tipe datanya menjadi unsigned 8-bit integer (np.uint8)
    median_frame = np.median(frames, axis=0).astype(np.uint8)
    return median_frame
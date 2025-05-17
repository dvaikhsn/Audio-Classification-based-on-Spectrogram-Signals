
---
# 🎧 Klasifikasi Gerak Pukulan Bulu Tangkis berbasis Sinyal Spektrogram dengan Metode CNN

Penelitian ini merupakan tugas akhir D3 Teknik Telekomunikasi yang berfokus pada bidang olahraga dengan pendekatan audio dan deep learning. Tujuan utama dari penelitian ini adalah untuk mengklasifikasikan jenis pukulan dalam 
olahraga bulu tangkis, khususnya antara pukulan smash dan dropshot berdasarkan sinyal audio yang direpresentasikan menjadi spektrogram sebagai input model Convolutional Neural Network (CNN).

---

## 🧠 Metodologi

1. **Pengumpulan Data**  
   Data audio diperoleh dari rekaman pertandingan profesional bulu tangkis yang berfokus pada pukulan*smash* dan *dropshot* dengan total 1240 Dataset.

2. **Preprocessing**  
   - File audio `.wav` dikonversi menjadi citra spektrogram menggunakan Mel-spectrogram.

3. **Pelatihan Model**  
   - CNN dirancang menggunakan TensorFlow/Keras.
   - Input berupa representasi spektrogram dan output berupa label klasifikasi.

4. **Evaluasi Model**  
   - Evaluasi dilakukan menggunakan metrik akurasi, confusion matrix, dan visualisasi training history.

---

## 🔍 Contoh Spektrogram

Berikut adalah contoh spektrogram yang digunakan sebagai input model:

![Screenshot 2025-05-02 052408](https://github.com/user-attachments/assets/326162b8-69ec-42cd-8154-b2efc2ace4dd)


---

## 📊 Hasil dan Evaluasi

- **Akurasi Pelatihan (Training Accuracy)**: 96%
- **Akurasi Validasi (Validation Accuracy)**: 90%
- **Akurasi Pengujian (Testing Accuracy)**: 91%

Model menunjukkan performa yang stabil antara data pelatihan, validasi, dan pengujian, menandakan bahwa model tidak mengalami overfitting dan memiliki kemampuan generalisasi yang baik terhadap data baru.

### 📉 Confusion Matrix & Grafik Pelatihan
Visualisasi confusion matrix dan grafik akurasi/loss dapat ditemukan di folder `notebook/`, yang memberikan gambaran lebih lanjut mengenai distribusi prediksi dan proses pelatihan model.


---

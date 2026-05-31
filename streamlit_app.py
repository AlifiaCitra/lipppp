import streamlit as st
import pandas as pd

# 1. Konfigurasi Halaman (Wajib Paling Atas)
st.set_page_config(page_title="ChemGrid - Visual Lab", page_icon="🗂️", layout="wide")

# =========================
# CUSTOM CSS (Untuk membuat tampilan seperti aplikasi di foto)
# =========================
st.markdown("""
<style>
/* Background Web */
[data-testid="stAppViewContainer"] {
    background-color: #f0f4f8;
}

/* Modifikasi Tombol di Grid agar terlihat seperti kotak elemen */
div[data-testid="stButton"] button {
    width: 100%;
    height: 80px;
    border-radius: 12px;
    background: white;
    border: 2px solid #e2e8f0;
    color: #1e293b;
    font-weight: 800;
    font-size: 16px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    transition: all 0.3s ease-in-out;
}

/* Efek saat kotak di-hover (disentuh mouse) */
div[data-testid="stButton"] button:hover {
    border-color: #3b82f6;
    background: #eff6ff;
    transform: translateY(-3px);
    box-shadow: 0 8px 15px rgba(59, 130, 246, 0.2);
}

/* Kartu Detail di bagian bawah */
.detail-card {
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    padding: 30px;
    border-radius: 20px;
    border-left: 8px solid #3b82f6;
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# 2. Database Senyawa / Uji (Bisa diganti sesuai topik yang kamu mau)
data_uji = [
    {"ID": "AL", "Nama": "Uji Tollens", "Gugus": "Aldehida", "Visual": "🪞 Cermin Perak", "Reagen": "AgNO3 + NH4OH", "Sifat": "Oksidasi ringan membentuk endapan logam perak."},
    {"ID": "FE", "Nama": "Uji Fehling", "Gugus": "Aldehida", "Visual": "🔴 Merah Bata", "Reagen": "CuSO4 + Tartrat", "Sifat": "Mereduksi ion Cu2+ menjadi endapan Cu2O pada suhu tinggi."},
    {"ID": "FN", "Nama": "Uji FeCl3", "Gugus": "Fenol", "Visual": "🟣 Ungu Pekat", "Reagen": "Besi(III) Klorida 1%", "Sifat": "Pembentukan kompleks besi-fenolat yang pekat."},
    {"ID": "LC", "Nama": "Uji Lucas", "Gugus": "Alkohol", "Visual": "⚪ Kekeruhan", "Reagen": "HCl pekat + ZnCl2", "Sifat": "Substitusi gugus -OH menjadi alkil klorida yang tak larut."},
    {"ID": "BY", "Nama": "Uji Baeyer", "Gugus": "Alkena", "Visual": "🟤 Endapan Coklat", "Reagen": "KMnO4 1%", "Sifat": "Oksidasi ikatan rangkap, warna ungu KMnO4 memudar."},
    {"ID": "BD", "Nama": "Uji Benedict", "Gugus": "Gula Pereduksi", "Visual": "🟠 Merah Bata", "Reagen": "Tembaga(II) Sitrat", "Sifat": "Oksidasi gula membentuk endapan Cu2O."},
    {"ID": "NB", "Nama": "Uji NaHCO3", "Gugus": "Asam Karboksilat", "Visual": "🫧 Gelembung Gas", "Reagen": "Natrium Bikarbonat 5%", "Sifat": "Reaksi asam basa menghasilkan gas Karbon Dioksida."},
    {"ID": "SF", "Nama": "Uji Schiff", "Gugus": "Aldehida", "Visual": "💗 Magenta", "Reagen": "Fuchsin + SO2", "Sifat": "Mengembalikan warna pink/magenta dari zat warna fuchsin."}
]

# 3. Memory Streamlit (Session State)
# Berfungsi untuk mengingat kotak mana yang sedang diklik user
if "terpilih" not in st.session_state:
    st.session_state.terpilih = data_uji[0] # Default yang tampil pertama kali

# 4. TAMPILAN HEADER
st.title("🗂️ Grid Visual: Uji Kualitatif Organik")
st.write("Klik salah satu kotak uji di bawah ini untuk melihat detail lengkapnya!")
st.divider()

# 5. MEMBUAT GRID KOTAK-KOTAK (Seperti Tabel Periodik di foto)
# Kita buat 4 kolom per baris
kolom_per_baris = 4
for i in range(0, len(data_uji), kolom_per_baris):
    cols = st.columns(kolom_per_baris)
    for j in range(kolom_per_baris):
        if i + j < len(data_uji):
            item = data_uji[i + j]
            # Jika tombol diklik, simpan datanya ke memory "terpilih"
            if cols[j].button(f"{item['ID']}\n\n{item['Nama']}", key=f"btn_{item['ID']}"):
                st.session_state.terpilih = item

st.divider()

# 6. KARTU DETAIL (Muncul di bawah, sesuai kotak yang diklik)
terpilih = st.session_state.terpilih

st.markdown(f"""
<div class="detail-card">
    <h1 style="color: #0f172a; margin-bottom: 0px;">{terpilih['Visual']} {terpilih['Nama']}</h1>
    <p style="color: #64748b; font-size: 18px; margin-top: 0px;">Target Analisis: <b>{terpilih['Gugus']}</b></p>
    <hr style="border: 1px solid #e2e8f0;">
    
    <div style="display: flex; justify-content: space-between; margin-top: 20px;">
        <div style="width: 48%;">
            <h4 style="color: #3b82f6;">🧪 Reagen yang Digunakan</h4>
            <p style="font-size: 16px; background: #e0f2fe; padding: 10px; border-radius: 8px;">{terpilih['Reagen']}</p>
        </div>
        <div style="width: 48%;">
            <h4 style="color: #3b82f6;">⚙️ Sifat & Mekanisme Kimia</h4>
            <p style="font-size: 16px; background: #e0f2fe; padding: 10px; border-radius: 8px;">{terpilih['Sifat']}</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

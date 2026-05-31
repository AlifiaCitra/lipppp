import streamlit as st
import time

# 1. Konfigurasi Halaman
st.set_page_config(page_title="ChemSim - Simulator Tabung", page_icon="🧪", layout="wide")

# Custom CSS untuk mempercantik UI & Tombol Samping
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background-color: #f8fafc; }
    .stSlider { background: white; padding: 15px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
    .equation-box {
        background-color: #1e293b; color: #38bdf8; font-family: 'Courier New', monospace;
        padding: 15px; border-radius: 12px; text-align: center; font-size: 18px;
        font-weight: bold; box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🧪 Virtual Beaker Simulator Game")
st.write("Campurkan zat kimia, atur suhunya, dan lihat perubahan visualnya secara langsung!")
st.divider()

# 2. SELEKSI BAHAN (Dibuat mirip menu kategori di game)
col_input, col_visual = st.columns([1, 1.2])

with col_input:
    st.subheader("📋 Panel Kontrol Laboratorium")
    
    # Pilih Sampel Organik
    sampel = st.selectbox("1. Pilih Sampel Utama:", ["-- Kosong --", "Formaldehida (Aldehida)", "Fenol", "Minyak Goreng (Ester)"])
    
    # Pilih Pereaksi
    reagen = st.selectbox("2. Tambahkan Pereaksi (Reagen):", ["-- Tanpa Reagen --", "Pereaksi Tollens", "Larutan FeCl3", "NaOH + Pemanasan"])
    
    # Slider Suhu (Mirip indikator termometer di game)
    suhu = st.slider("3. Atur Suhu Sistem (°C):", min_value=25, max_value=100, value=25, step=5)
    
    st.write("")
    jalankan = st.button("🧪 REAKSIKAN SEKARANG", use_container_width=True)

# 3. LOGIKA SIMULATOR (Menentukan Perubahan Warna & Rumus)
warna_cairan = "#e2e8f0"  # Default: Bening/Abu-abu kosong
tinggi_cairan = "30%"    # Kosong isi dikit
status_reaksi = "Belum ada zat yang dicampur."
rumus_kimia = "Menunggu Reaksi..."
efek_asap = ""

if sampel != "-- Kosong --":
    warna_cairan = "#f1f5f9" # Ada sampel = cairan bening jernih
    tinggi_cairan = "50%"
    status_reaksi = f"Sampel {sampel} telah dimasukkan ke dalam gelas kimia."
    
    if reagen != "-- Tanpa Reagen --":
        tinggi_cairan = "75%"
        
        # KONDISI 1: UJI TOLLENS (Harus Aldehida + Tollens + Panas)
        if "Aldehida" in sampel and reagen == "Pereaksi Tollens":
            if suhu >= 70:
                warna_cairan = "linear-gradient(to right, #94a3b8, #cbd5e1, #94a3b8)" # Efek Cermin Perak mengkilap
                status_reaksi = "💥 REAKSI POSITIF! Terbentuk lapisan cermin perak di dinding gelas kimia!"
                rumus_kimia = "R-CHO + 2[Ag(NH3)2]+ + 3OH- -> R-COO- + 2Ag(s) + 4NH3 + 2H2O"
                if suhu >= 90:
                    efek_asap = "💨"
            else:
                warna_cairan = "#cbd5e1" # Keruh biasa kalau belum panas
                status_reaksi = "Campuran Tollens dingin. Butuh suhu tinggi (≥70°C) untuk mereduksi ion perak!"
                rumus_kimia = "R-CHO + 2[Ag(NH3)2]+"
                
        # KONDISI 2: UJI FENOL + FeCl3 (Instan berubah warna tanpa pemanasan)
        elif "Fenol" in sampel and reagen == "Larutan FeCl3":
            warna_cairan = "#4c1d95" # Ungu pekat kompleks besi
            status_reaksi = "💥 REAKSI POSITIF! Terbentuk senyawa kompleks besi(III) fenolat berwarna ungu pekat!"
            rumus_kimia = "6Ar-OH + Fe3+ -> [Fe(OAr)6]3- + 6H+"
            if suhu >= 80:
                efek_asap = "💨"
                
        # KONDISI 3: SAPONIFIKASI ESTER (Ester + NaOH + Panas)
        elif "Ester" in sampel and reagen == "NaOH + Pemanasan":
            if suhu >= 60:
                warna_cairan = "#fef08a" # Kuning keruh sabun/emulsi
                status_reaksi = "💥 REAKSI POSITIF! Hidrolisis ester (saponifikasi) berhasil membentuk sabun dan gliserol!"
                rumus_kimia = "R-COOR' + NaOH -> R-COONa + R'-OH"
                efek_asap = "🧼"
            else:
                warna_cairan = "#fef9c3" # Minyak mengapung biasa
                status_reaksi = "Campuran belum menyatu sempurna. Naikkan suhu untuk mempercepat hidrolisis!"
                rumus_kimia = "R-COOR' + NaOH"
        
        # KONDISI NEGATIF (Zat tidak cocok)
        else:
            warna_cairan = "#fca5a5" # Berubah warna merah/oranye tanda tidak bereaksi
            status_reaksi = "❌ REAKSI NEGATIF! Reagen tidak cocok dengan gugus fungsi sampel tersebut."
            rumus_kimia = "Tidak terjadi reaksi (No Reaction)"

# 4. TAMPILAN VISUAL GELAS KIMIA (Di sebelah kanan)
with col_visual:
    st.subheader("🖥️ Monitor Beaker Virtual")
    
    # Kotak Rumus Kimia Atas (Persis seperti di game HP kamu)
    st.markdown(f'<div class="equation-box">REACTION: {rumus_kimia}</div>', unsafe_allow_html=True)
    
    # Animasi Proses Sebentar saat tombol ditekan
    if jalankan:
        with st.spinner("Mereaksikan zat..."):
            time.sleep(1)
            
    # Grafis Gelas Kimia pakai HTML asli bawaan Streamlit
    st.markdown(f"""
    <div style="text-align: center; margin-top: 20px; position: relative;">
        <div style="font-size: 40px; height: 50px; margin-bottom: -10px; animation: pulse 1s infinite;">
            {efek_asap if suhu >= 60 else ""}
        </div>
        
        <div style="border: 5px solid #94a3b8; border-top: none; border-radius: 0 0 30px 30px; 
                    width: 240px; height: 280px; margin: 0 auto; position: relative; background: #ffffff50;
                    box-shadow: 0 10px 20px rgba(0,0,0,0.05);">
            
            <div style="position: absolute; top: 0; left: -15px; width: 0; height: 0; 
                        border-right: 15px solid #94a3b8; border-bottom: 15px solid transparent;"></div>
            
            <div style="background: {warna_cairan}; width: 100%; height: {tinggi_cairan}; 
                        position: absolute; bottom: 0; border-radius: 0 0 25px 25px; 
                        transition: all 0.8s ease-in-out; display: flex; align-items: center; justify-content: center;">
                <span style="color: #1e293b; font-size: 12px; font-weight: bold; opacity: 0.4;">
                    {f"{suhu}°C" if sampel != "-- Kosong--" else ""}
                </span>
            </div>
            
            <div style="position: absolute; right: 15px; top: 50px; border-top: 3px solid #cbd5e1; width: 25px;"></div>
            <div style="position: absolute; right: 15px; top: 110px; border-top: 3px solid #cbd5e1; width: 15px;"></div>
            <div style="position: absolute; right: 15px; top: 170px; border-top: 3px solid #cbd5e1; width: 25px;"></div>
            <div style="position: absolute; right: 15px; top: 230px; border-top: 3px solid #cbd5e1; width: 15px;"></div>
        </div>
        <p style="font-weight: bold; color: #64748b; margin-top: 15px;">Beaker Glass 250 mL</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Keterangan Status Hasil di Bawah Gelas
    st.write("")
    if "POSITIF" in status_reaksi:
        st.success(status_reaksi)
    elif "❌" in status_reaksi:
        st.error(status_reaksi)
    else:
        st.info(status_reaksi)

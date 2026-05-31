import streamlit as st

# 1. Konfigurasi Dasar Halaman
st.set_page_config(
    page_title="ChemSim - Game Simulator Lab", 
    page_icon="🧪", 
    layout="wide"
)

st.title("🧪 Virtual Beaker Simulator Game")
st.write("Pilih sampel dan reagen di kiri, amati reaksi visual gelas kimia di kanan!")
st.divider()

# 2. PANEL INPUT (Kiri)
col_input, col_visual = st.columns([1, 1.1])

with col_input:
    st.subheader("📋 Panel Kontrol Laboratorium")
    
    sampel = st.selectbox(
        "1. Pilih Sampel Utama:", 
        ["-- Kosong --", "Formaldehida (Aldehida)", "Fenol", "Minyak Goreng (Ester)"]
    )
    
    reagen = st.selectbox(
        "2. Tambahkan Pereaksi (Reagen):", 
        ["-- Tanpa Reagen --", "Pereaksi Tollens", "Larutan FeCl3", "NaOH + Pemanasan"]
    )
    
    suhu = st.slider(
        "3. Atur Suhu Sistem (°C):", 
        min_value=25, max_value=100, value=25, step=5
    )

# 3. LOGIKA PENENTUAN WARNA & RUMUS KIMIA
warna_cairan = "#e2e8f0"  # Default: kosong (abu-abu)
tinggi_cairan = "80px"    # Sedikit isi
rumus_kimia = "Menunggu Reaksi..."
status_teks = "Silakan masukkan sampel dan reagen untuk memulai simulasi."
status_tipe = "info"       # Gaya kotak pesan (info, success, error)
efek_asap = "opacity: 0;"  # Default tidak berasap

if sampel != "-- Kosong --":
    warna_cairan = "#e2e8f0"  # Bening transparan awal
    tinggi_cairan = "140px"
    rumus_kimia = f"Sampel dimasukkan: {sampel}"
    status_teks = "Sampel berhasil dituangkan ke dalam gelas kimia. Tambahkan reagen pembantu!"
    
    if reagen != "-- Tanpa Reagen --":
        tinggi_cairan = "200px"  # Volume bertambah karena dicampur
        
        # Skenario A: Uji Tollens (Aldehida + Tollens)
        if "Aldehida" in sampel and reagen == "Pereaksi Tollens":
            if suhu >= 70:
                # Efek Cermin Perak Gradasi Mengkilap
                warna_cairan = "linear-gradient(135deg, #94a3b8 0%, #f1f5f9 50%, #64748b 100%)"
                rumus_kimia = "R-CHO + 2[Ag(NH3)2]+ + 3OH- -> R-COO- + 2Ag(s) + 4NH3 + 2H2O"
                status_teks = "💥 REAKSI POSITIF! Terbentuk lapisan cermin perak (Ag murni) mengkilap pada dinding dalam gelas!"
                status_tipe = "success"
                efek_asap = "opacity: 1;"
            else:
                warna_cairan = "#cbd5e1"  # Keruh dingin
                rumus_kimia = "R-CHO + 2[Ag(NH3)2]+"
                status_teks = "Campuran Tollens masih dingin. Naikkan suhu slider ke >= 70°C untuk mereduksi perak!"
                status_tipe = "warning"
                
        # Skenario B: Uji Fenol (Fenol + FeCl3)
        elif "Fenol" in sampel and reagen == "Larutan FeCl3":
            warna_cairan = "#4c1d95"  # Ungu pekat instan
            rumus_kimia = "6Ar-OH + Fe3+ -> [Fe(OAr)6]3- + 6H+"
            status_teks = "💥 REAKSI POSITIF! Terbentuk kompleks besi(III) fenolat berwarna ungu pekat secara instan!"
            status_tipe = "success"
            if suhu >= 75:
                efek_asap = "opacity: 1;"
                
        # Skenario C: Saponifikasi (Ester + NaOH)
        elif "Ester" in sampel and reagen == "NaOH + Pemanasan":
            if suhu >= 60:
                warna_cairan = "#fef08a"  # Kuning keruh emulsi sabun
                rumus_kimia = "R-COOR' + NaOH -> R-COONa + R'-OH"
                status_teks = "💥 REAKSI POSITIF! Hidrolisis basa (saponifikasi) berhasil memecah ester membentuk sabun!"
                status_tipe = "success"
                efek_asap = "opacity: 1;"
            else:
                warna_cairan = "#fef9c3"  # Lapisan minyak terpisah
                rumus_kimia = "R-COOR' + NaOH"
                status_teks = "Reaksi lambat. Naikkan suhu pemanas ke >= 60°C agar reaksi hidrolisis berjalan sempurna!"
                status_tipe = "warning"
                
        # Skenario D: Tidak Bereaksi / Salah Reagen
        else:
            warna_cairan = "#fca5a5"  # Warna pink kemerahan (tanda eror/negatif)
            rumus_kimia = "Tidak Terjadi Reaksi (No Reaction)"
            status_teks = "❌ REAKSI NEGATIF! Reagen pereaksi tidak cocok dengan jenis gugus fungsi sampel ini."
            status_tipe = "error"

# 4. MONITOR VISUALISASI JALANNYA GAME (Kanan)
with col_visual:
    st.subheader("🖥️ Monitor Beaker Virtual")
    
    # Box Persamaan Reaksi Atas (Gaya Game HP)
    st.markdown(
        f'<div class="equation-box">REACTION: {rumus_kimia}</div>', 
        unsafe_allow_html=True
    )
    
    # HTML KHUSUS: Mengunci kode gambar di dalam Sandbox agar tidak tumpah jadi teks
    html_gelas = f"""
    <div style="font-family: Arial, sans-serif; text-align: center; background-color: #f8fafc; padding: 10px;">
        <div style="font-size: 35px; height: 45px; transition: all 0.5s; {efek_asap}">💨</div>
        
        <div style="border: 6px solid #64748b; border-top: none; border-radius: 0 0 25px 25px; 
                    width: 200px; height: 240px; margin: 0 auto; position: relative; 
                    background: rgba(255,255,255,0.7); box-shadow: 0 10px 15px rgba(0,0,0,0.05);">
            
            <div style="position: absolute; top: 0; left: -16px; width: 0; height: 0; 
                        border-right: 16px solid #64748b; border-bottom: 16px solid transparent;"></div>
            
            <div style="background: {warna_cairan}; width: 100%; height: {tinggi_cairan}; 
                        position: absolute; bottom: 0; border-radius: 0 0 20px 20px; 
                        transition: all 0.6s ease-in-out; display: flex; align-items: center; justify-content: center;">
                <b style="color: #1e293b; font-size: 16px; opacity: 0.6;">{suhu}°C</b>
            </div>
            
            <div style="position: absolute; right: 12px; top: 40px; border-top: 3px solid #94a3b8; width: 20px;"></div>
            <div style="position: absolute; right: 12px; top: 90px; border-top: 3px solid #94a3b8; width: 12px;"></div>
            <div style="position: absolute; right: 12px; top: 140px; border-top: 3px solid #94a3b8; width: 20px;"></div>
            <div style="position: absolute; right: 12px; top: 190px; border-top: 3px solid #94a3b8; width: 12px;"></div>
        </div>
        <p style="margin-top: 12px; font-weight: bold; color: #64748b;">Beaker Glass 250 mL</p>
    </div>
    """
    
    # PERINTAH SAKTI: Ini yang merender HTML menjadi grafis gambar utuh!
    st.components.v1.html(html_gelas, height=350)
    
    # Cetak kotak status informasi di paling bawah
    if status_tipe == "success":
        st.success(status_teks)
    elif status_tipe == "warning":
        st.warning(status_teks)
    elif status_tipe == "error":
        st.error(status_teks)
    else:
        st.info(status_teks)

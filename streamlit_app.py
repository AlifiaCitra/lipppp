import streamlit as st

# 1. Konfigurasi Halaman & Tema Neon Laboratorium
st.set_page_config(
    page_title="ChemSim - Virtual Test Tube", 
    page_icon="🧪", 
    layout="wide"
)

# CSS untuk memperbaiki warna tulisan agar terbaca jelas dan background super estetik
st.markdown("""
<style>
    /* Background Laboratorium Digital */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #311042 100%) !important;
    }
    
    /* Panel Kontrol di Kiri (Teks Hitam Tegas di atas Kotak Putih) */
    .stSelectbox, .stSlider {
        background-color: #ffffff !important;
        padding: 18px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
        margin-bottom: 15px;
        border: 2px solid #a855f7;
    }
    
    /* Memaksa label dropdown & slider berwarna putih agar terbaca */
    label, .stMarkdown p, h1, h2, h3 {
        color: #f8fafc !important;
        font-weight: bold !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
    }
    
    /* Kotak Persamaan Reaksi di Kanan */
    .equation-box {
        background: #020617;
        color: #22d3ee;
        font-family: 'Courier New', monospace;
        padding: 18px;
        border-radius: 20px;
        text-align: center;
        font-size: 18px;
        font-weight: bold;
        border: 2px solid #22d3ee;
        box-shadow: 0 0 20px rgba(34, 211, 238, 0.3);
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🧪 Virtual Test Tube Simulator Game v4.0")
st.write("Campurkan zat organik, atur suhu, dan lihat efek visual unik sesuai hasil reaksi kimianya!")
st.divider()

# 2. PANEL INPUT (Kiri)
col_input, col_visual = st.columns([1, 1.1])

with col_input:
    st.markdown("### 📋 Panel Kontrol Laboratorium")
    
    sampel = st.selectbox(
        "Pilih Sampel Utama:", 
        [
            "-- Kosong --", 
            "Formaldehida (Aldehida)", 
            "Aseton (Keton)",
            "Glukosa (Gula Pereduksi)",
            "Fenol", 
            "Asam Asetat (Asam Karboksilat)",
            "Minyak Goreng (Ester)"
        ]
    )
    
    reagen = st.selectbox(
        "Tambahkan Pereaksi (Reagen):", 
        [
            "-- Tanpa Reagen --", 
            "Pereaksi Tollens", 
            "Pereaksi Fehling",
            "Larutan FeCl3", 
            "Larutan NaHCO3 5%",
            "NaOH + Pemanasan"
        ]
    )
    
    suhu = st.slider(
        "Atur Suhu Pemanas (°C):", 
        min_value=25, max_value=100, value=25, step=5
    )

# 3. LOGIKA KOKTAIL REAKSI & EFEK VISUAL ANIMASI
warna_cairan = "rgba(255, 255, 255, 0.15)"
tinggi_cairan = "30px"
rumus_kimia = "Menunggu Reaksi..."
status_teks = "Silakan tuangkan sampel dan reagen pada panel kontrol di kiri."
status_tipe = "info"

# Variabel Efek Animasi HTML
efek_asap = "0"
efek_gelembung = "none"
efek_endapan = "none"

if sampel != "-- Kosong --":
    warna_cairan = "rgba(226, 232, 240, 0.4)" # Cairan bening sampel awal
    tinggi_cairan = "90px"
    rumus_kimia = f"Sampel dimasukkan: {sampel}"
    status_teks = "Sampel berada di dalam tabung reaksi. Tambahkan senyawa reagen pereaksi!"
    
    if reagen != "-- Tanpa Reagen --":
        tinggi_cairan = "180px" # Volume bertambah semenjak dicampur
        
        # [EFEK 1] ALDEHIDA + TOLLENS (Cermin Perak + Uap Gas)
        if "Aldehida" in sampel and reagen == "Pereaksi Tollens":
            if suhu >= 70:
                warna_cairan = "linear-gradient(135deg, #cbd5e1 0%, #94a3b8 50%, #334155 100%)"
                rumus_kimia = "R-CHO + 2[Ag(NH3)2]+ + 3OH- -> R-COO- + 2Ag(s) + 4NH3 + 2H2O"
                status_teks = "💥 REAKSI POSITIF! Reduksi ion perak berhasil memicu pengendapan Cermin Perak mengkilap pada dinding dalam tabung!"
                status_tipe = "success"
                efek_asap = "1"
                efek_gelembung = "block"
            else:
                warna_cairan = "rgba(203, 213, 225, 0.7)"
                rumus_kimia = "R-CHO + Reagen Tollens (Dingin)"
                status_teks = "Larutan Tollens masih dingin. Naikkan suhu pemanas ke >= 70°C untuk memicu cermin perak!"
                status_tipe = "warning"
                
        # [EFEK 2] ALDEHIDA / GLUKOSA + FEHLING (Endapan Merah Bata di Dasar)
        elif ("Aldehida" in sampel or "Glukosa" in sampel) and reagen == "Pereaksi Fehling":
            if suhu >= 60:
                warna_cairan = "linear-gradient(to bottom, #f87171, #ef4444)"
                rumus_kimia = "R-CHO + 2Cu2+ + 5OH- -> R-COO- + Cu2O(s) + 3H2O"
                status_teks = "💥 REAKSI POSITIF! Gugus gula pereduksi menghasilkan endapan Merah Bata Cu2O yang mengumpul di dasar tabung!"
                status_tipe = "success"
                efek_endapan = "block"
                efek_asap = "0.7"
            else:
                warna_cairan = "#1d4ed8" # Biru pekat Fehling asli
                rumus_kimia = "R-CHO + Kompleks Cu2+"
                status_teks = "Larutan berwarna biru khas Fehling. Reaksi reduksi membutuhkan panas, naikkan suhu ke >= 60°C!"
                status_tipe = "warning"

        # [EFEK 3] KETON + REAGEN (Pembatas Negatif)
        elif "Keton" in sampel and reagen in ["Pereaksi Tollens", "Pereaksi Fehling"]:
            warna_cairan = "rgba(252, 165, 165, 0.6)" if reagen == "Pereaksi Tollens" else "#1d4ed8"
            rumus_kimia = "R-CO-R + Reagen -> Tidak Bereaksi"
            status_teks = "❌ REAKSI NEGATIF! Keton menolak reaksi oksidasi lemah karena tidak memiliki atom hidrogen yang terikat pada karbon karbonil."
            status_tipe = "error"
                
        # [EFEK 4] FENOL + FeCl3 (Perubahan Warna Ungu Pekat Eksotis)
        elif "Fenol" in sampel and reagen == "Larutan FeCl3":
            warna_cairan = "linear-gradient(to bottom, #6b21a8, #3b0764)"
            rumus_kimia = "6Ar-OH + Fe3+ -> [Fe(OAr)6]3- + 6H+"
            status_teks = "💥 REAKSI POSITIF! Substitusi ligan menghasilkan pembentukan senyawa kompleks besi(III) fenolat berwarna ungu gelap pekat!"
            status_tipe = "success"
            if suhu >= 75:
                efek_asap = "1"

        # [EFEK 5] ASAM KARBOKSILAT + NaHCO3 (Efek Busa Mendidih / Gelembung Gas CO2 Berlimpah)
        elif "Asam Karboksilat" in sampel and reagen == "Larutan NaHCO3 5%":
            warna_cairan = "rgba(241, 245, 249, 0.7)"
            rumus_kimia = "R-COOH + NaHCO3 -> R-COONa + H2O + CO2(g) ↑"
            status_teks = "💥 REAKSI POSITIF! Reaksi pelepasan gugus asam organik menghasilkan gelembung gas CO2 (effervescent) aktif!"
            status_tipe = "success"
            efek_gelembung = "block"
            efek_asap = "0.5"

        # [EFEK 6] ESTER + NaOH (Saponifikasi Emulsi Sabun)
        elif "Ester" in sampel and reagen == "NaOH + Pemanasan":
            if suhu >= 60:
                warna_cairan = "linear-gradient(to bottom, #fef08a, #ca8a04)"
                rumus_kimia = "R-COOR' + NaOH -> R-COONa (Sabun) + R'-OH"
                status_teks = "💥 REAKSI POSITIF! Hidrolisis dalam suasana basa (Saponifikasi) memecah ikatan ester membentuk emulsi sabun kental!"
                status_tipe = "success"
                efek_asap = "1"
            else:
                warna_cairan = "rgba(254, 249, 195, 0.8)"
                rumus_kimia = "R-COOR' + NaOH"
                status_teks = "Minyak dan larutan basa masih terpisah (heterogen). Panaskan tabung reaksi hingga >= 60°C!"
                status_tipe = "warning"
        else:
            warna_cairan = "rgba(225, 29, 72, 0.5)"
            rumus_kimia = "No Reaction"
            status_teks = "❌ REAKSI NEGATIF! Uji gugus fungsi gagal karena karakteristik sampel tidak cocok dengan fungsi reagen."
            status_tipe = "error"

# 4. MONITOR VISUALISASI JALANNYA SIMULASI (Kanan)
with col_visual:
    st.markdown("### 🖥️ Monitor Tabung Reaksi Virtual")
    
    # Render Box Rumus Kimia Atas
    st.markdown(f'<div class="equation-box">REACTION FORMULA: {rumus_kimia}</div>', unsafe_allow_html=True)
    
    # HTML Grafis Intuitif: Tabung Reaksi + Rak + Animasi Partikel/Gelembung Kimia
    html_game = f"""
    <div style="text-align: center; padding-top: 10px;">
        <div style="font-size: 38px; height: 45px; margin-bottom: 5px; opacity: {efek_asap}; transition: opacity 0.4s; filter: drop-shadow(0 0 8px #fff);">💨</div>
        
        <div style="border: 5px solid #e2e8f0; border-top: none; 
                    border-radius: 0 0 50px 50px; 
                    width: 95px; height: 270px; margin: 0 auto; position: relative; 
                    background: rgba(255, 255, 255, 0.15); box-shadow: 0 0 25px rgba(255,255,255,0.1);
                    z-index: 2; overflow: hidden;">
            
            <div style="position: absolute; top: 0; left: -10px; width: 105px; height: 8px; 
                        background-color: #e2e8f0; border-radius: 4px; z-index: 5;"></div>
            
            <div style="background: {warna_cairan}; width: 100%; height: {tinggi_cairan}; 
                        position: absolute; bottom: 0; border-radius: 0 0 45px 45px; 
                        transition: height 0.6s ease, background 0.6s ease; 
                        display: flex; align-items: center; justify-content: center; overflow: hidden;">
                
                <b style="color: #ffffff; font-size: 14px; text-shadow: 1px 1px 4px #000; z-index: 4;">
                    {f"{suhu}°C" if sampel != "-- Kosong --" else ""}
                </b>

                <div style="display: {efek_gelembung}; position: absolute; width: 100%; height: 100%; bottom: 0; left: 0;">
                    <div style="position: absolute; bottom: 10px; left: 20px; width: 8px; height: 8px; background: rgba(255,255,255,0.6); border-radius: 50%; animation: naik 1.5s infinite;"></div>
                    <div style="position: absolute; bottom: 30px; left: 50px; width: 6px; height: 6px; background: rgba(255,255,255,0.6); border-radius: 50%; animation: naik 1.2s infinite 0.3s;"></div>
                    <div style="position: absolute; bottom: 50px; left: 35px; width: 10px; height: 10px; background: rgba(255,255,255,0.6); border-radius: 50%; animation: naik 1.8s infinite 0.5s;"></div>
                </div>

                <div style="display: {efek_endapan}; position: absolute; bottom: 0; left: 0; width: 100%; height: 35px; 
                            background: #7f1d1d; border-radius: 0 0 45px 45px; border-top: 3px dashed #b91c1c;">
                </div>
            </div>
        </div>
        
        <div style="width: 180px; height: 18px; background-color: #b45309; margin: -25px auto 0 auto; border-radius: 6px; position: relative; z-index: 1; box-shadow: 0 4px 10px rgba(0,0,0,0.5);"></div>
        <div style="width: 140px; height: 45px; border-left: 12px solid #d97706; border-right: 12px solid #d97706; margin: 0 auto; position: relative; z-index: 1;"></div>
        <div style="width: 200px; height: 15px; background-color: #b45309; margin: 0 auto; border-radius: 4px; position: relative; z-index: 1; box-shadow: 0 4px 10px rgba(0,0,0,0.5);"></div>
        
        <style>
            @keyframes naik {
                0% { transform: translateY(0px) scale(0.8); opacity: 0; }
                50% { opacity: 0.8; }
                100% { transform: translateY(-120px) scale(1.2); opacity: 0; }
            }
        </style>
        
        <p style="margin-top: 15px; font-weight: bold; color: #cbd5e1; font-size: 14px;">Test Tube Real-time Visualizer</p>
    </div>
    """
    
    st.components.v1.html(html_game, height=430)
    
    # Kotak Status Informasi Hasil di Paling Bawah
    st.write("")
    if status_tipe == "success":
        st.success(status_teks)
    elif status_tipe == "warning":
        st.warning(status_teks)
    elif status_tipe == "error":
        st.error(status_teks)
    else:
        st.info(status_teks)

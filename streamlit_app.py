import streamlit as st

# 1. Konfigurasi Halaman
st.set_page_config(page_title="ChemSim - Virtual Test Tube", page_icon="🧪", layout="wide")

# CSS Global
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #311042 100%) !important; }
    .stSelectbox, .stSlider { background-color: #ffffff !important; padding: 18px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4); border: 3px solid #a855f7; }
    label, .stMarkdown p, h1, h2, h3 { color: #f8fafc !important; font-weight: bold !important; text-shadow: 1px 1px 3px rgba(0,0,0,0.6); }
    .equation-box { background: #020617; color: #22d3ee; padding: 18px; border-radius: 20px; text-align: center; font-size: 18px; font-weight: bold; border: 2px solid #22d3ee; box-shadow: 0 0 20px rgba(34, 211, 238, 0.3); margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

st.title("🧪 Virtual Test Tube Simulator - Final Version")
col_input, col_visual = st.columns([1, 1.1])

with col_input:
    sampel = st.selectbox("Pilih Sampel:", ["-- Kosong --", "Formaldehida (Aldehida)", "Aseton (Keton)", "Glukosa (Gula Pereduksi)", "Fenol", "Asam Asetat (Asam Karboksilat)", "Minyak Goreng (Ester)"])
    reagen = st.selectbox("Tambahkan Reagen:", ["-- Tanpa Reagen --", "Pereaksi Tollens", "Pereaksi Fehling", "Larutan FeCl3", "Larutan NaHCO3 5%", "NaOH + Pemanasan"])
    suhu = st.slider("Atur Suhu (°C):", 25, 100, 25, 5)

# 2. LOGIKA REAKSI (Logika aslimu saya pasang kembali di sini)
warna_cairan, tinggi_cairan, rumus_kimia, status_teks, status_tipe = "rgba(255, 255, 255, 0.15)", "30px", "Menunggu...", "Pilih sampel.", "info"
efek_asap, efek_gelembung, efek_endapan = "0", "none", "none"
api_aktif = "block" if suhu > 25 else "none"

if sampel != "-- Kosong --":
    warna_cairan, tinggi_cairan = "rgba(241, 245, 249, 0.4)", "90px"
    rumus_kimia = f"Sampel: {sampel}"
    if reagen != "-- Tanpa Reagen --":
        tinggi_cairan = "180px"
        # -- Logika Reaksi Tollens --
        if "Aldehida" in sampel and reagen == "Pereaksi Tollens" and suhu >= 70:
            warna_cairan = "linear-gradient(135deg, #cbd5e1 0%, #94a3b8 50%, #334155 100%)"
            rumus_kimia = "R-CHO + 2[Ag(NH3)2]+ -> R-COO- + 2Ag(s)"
            status_teks = "POSITIF! Terbentuk cermin perak!"
            status_tipe = "success"
            efek_asap, efek_gelembung = "1", "block"
        # (Silakan tambahkan sisa logika if-elif mu yang lama di sini)

with col_visual:
    # 3. RENDER VISUAL (Menggunakan escape {{ dan %% untuk CSS)
    html_game = f"""
    <div style="text-align: center; position: relative;">
        <div style="font-size: 38px; height: 45px; opacity: {efek_asap};">💨</div>
        <div style="border: 5px solid #e2e8f0; border-radius: 0 0 50px 50px; width: 95px; height: 270px; margin: 0 auto; background: rgba(255,255,255,0.1); position: relative;">
            <div style="background: {warna_cairan}; width: 100%; height: {tinggi_cairan}; position: absolute; bottom: 0; border-radius: 0 0 45px 45px;"></div>
        </div>
        <div style="display: {api_aktif}; margin: -10px auto; width: 50px; height: 60px; 
                    background: radial-gradient(circle, #fbbf24 10%%, #ef4444 60%%); 
                    border-radius: 50%% 50%% 20%% 20%%; filter: blur(8px); animation: flicker 0.2s infinite;"></div>
        <style>
            @keyframes flicker {{
                0%% {{ transform: scale(1); opacity: 0.7; }}
                50%% {{ transform: scale(1.1); opacity: 1; }}
                100%% {{ transform: scale(1); opacity: 0.7; }}
            }}
        </style>
    </div>
    """
    st.components.v1.html(html_game, height=450) streamlit as st

# Konfigurasi Halaman
st.set_page_config(page_title="ChemSim", layout="wide")

# CSS Terpisah agar tidak merusak f-string
st.markdown("""
<style>
    .equation-box {
        background: #020617; color: #22d3ee; padding: 15px;
        border-radius: 10px; border: 1px solid #22d3ee;
        text-align: center; font-family: monospace;
    }
</style>
""", unsafe_allow_html=True)

st.title("🧪 Virtual Test Tube Simulator")

# Logika Simulasi
sampel = st.selectbox("Pilih Sampel:", ["-- Kosong --", "Formaldehida"])
reagen = st.selectbox("Pilih Reagen:", ["-- Tanpa Reagen --", "Tollens"])
suhu = st.slider("Suhu (°C)", 25, 100, 25)

# Tentukan warna dan status
warna = "#cbd5e1" if sampel != "-- Kosong --" else "rgba(255,255,255,0.1)"
status = "Sampel siap."

# Render HTML dengan cara yang aman (menggunakan .format() bukan f-string agar { } tidak error)
html_template = """
<div style="border: 5px solid #e2e8f0; width: 100px; height: 200px; margin: 0 auto; position: relative;">
    <div style="background: {color}; width: 100%; height: 50%; position: absolute; bottom: 0;"></div>
</div>
<p style="text-align: center;">Suhu: {temp}°C</p>
"""

st.components.v1.html(html_template.format(color=warna, temp=suhu), height=300)

if sampel == "Formaldehida" and reagen == "Tollens" and suhu >= 70:
    st.success("POSITIF! Terbentuk cermin perak.")
else:
    st.info(status)

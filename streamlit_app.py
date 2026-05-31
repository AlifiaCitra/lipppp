import streamlit as st
import pandas as pd

# 1. Konfigurasi Halaman (Harus ditaruh paling atas)
st.set_page_config(
    page_title="ChemQual - Katalog Organik", 
    page_icon="🧪", 
    layout="wide"
)

# =========================
# CUSTOM CSS UNTUK BACKGROUND GAMBAR
# =========================
st.markdown("""
<style>
/* 1. Background utama menggunakan gambar Lab Kimia */
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1532094349884-543bc11b234d?q=80&w=2070&auto=format&fit=crop");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* 2. Bikin header Streamlit (garis atas) transparan */
[data-testid="stHeader"] {
    background-color: transparent;
}

/* 3. Container utama dibuat seperti kaca (Glassmorphism) agar tulisan tetap terbaca */
.block-container {
    background: rgba(255, 255, 255, 0.90); /* Putih transparan */
    backdrop-filter: blur(10px); /* Efek blur kaca */
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
    border-radius: 20px;
    max-width: 1200px;
    margin-top: 2rem;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
}

/* Judul */
h1, h2, h3 {
    color: #12355b;
    font-weight: 700;
}

/* Expander/card */
[data-testid="stExpander"] {
    border-radius: 15px;
    border: 1px solid #d6e4f0;
    background: rgba(255,255,255,0.95);
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    margin-bottom: 10px;
}

/* Input box */
.stTextInput input,
.stSelectbox div[data-baseweb="select"] {
    border-radius: 12px;
    border: 1px solid #cbd5e1;
}

/* Divider */
hr {
    border: none;
    height: 2px;
    background: linear-gradient(to right, transparent, #93c5fd, transparent);
}

/* Dataframe */
[data-testid="stDataFrame"] {
    background: white;
    border-radius: 15px;
    overflow: hidden;
}
</style>
""", unsafe_allow_html=True)

# 2. Database Uji Kualitatif Organik
data_uji = [
    {
        "Nama Uji": "Uji Lucas",
        "Gugus Fungsi": "Alkohol (Substitusi)",
        "Reagen": "HCl pekat + ZnCl2 (Reagen Lucas)",
        "Prosedur Singkat": "Campurkan sampel dengan reagen Lucas pada suhu kamar, amati kecepatan terbentuknya kekeruhan/fasa cair terpisah.",
        "Hasil Positif": "Tersier: Instan (<1 menit)\nSekunder: 5-10 menit\nPrimer: Tidak bereaksi pada suhu kamar",
        "Warna/Visual": "⚪ Kekeruhan / Terbentuk 2 Lapisan",
        "Reaksi Kimia": "R-OH + HCl --(ZnCl2)--> R-Cl + H2O"
    },
    {
        "Nama Uji": "Uji Tollens",
        "Gugus Fungsi": "Aldehida",
        "Reagen": "AgNO3 + NaOH + NH4OH (Reagen Tollens)",
        "Prosedur Singkat": "Tambahkan sampel ke dalam reagen Tollens, lalu panaskan di penangas air selama beberapa menit.",
        "Hasil Positif": "Terbentuk lapisan perak mengkilap di dinding tabung reaksi.",
        "Warna/Visual": "🪞 Cermin Perak (Silver Mirror)",
        "Reaksi Kimia": "R-CHO + 2[Ag(NH3)2]+ + 3OH- --> R-COO- + 2Ag (s) + 4NH3 + 2H2O"
    },
    {
        "Nama Uji": "Uji Fehling",
        "Gugus Fungsi": "Aldehida",
        "Reagen": "Fehling A (CuSO4) + Fehling B (K-Na-tartrat + NaOH)",
        "Prosedur Singkat": "Campurkan Fehling A dan B (1:1), tambahkan sampel, lalu panaskan di penangas air.",
        "Hasil Positif": "Warna biru tua reagen akan berubah menjadi endapan merah bata.",
        "Warna/Visual": "🔴 Endapan Merah Bata",
        "Reaksi Kimia": "R-CHO + 2Cu2+ + 5OH- --> R-COO- + Cu2O (s) + 3H2O"
    },
    {
        "Nama Uji": "Uji Ferri Klorida",
        "Gugus Fungsi": "Fenol",
        "Reagen": "Larutan FeCl3 1% atau 5%",
        "Prosedur Singkat": "Larutkan sampel dalam air/etanol, lalu teteskan beberapa tetes larutan FeCl3.",
        "Hasil Positif": "Terbentuk warna ungu, hijau, atau biru kompleks yang pekat.",
        "Warna/Visual": "🟣 Warna Ungu / Biru / Hijau Pekat",
        "Reaksi Kimia": "6Ar-OH + Fe3+ --> [Fe(OAr)6]3- (kompleks berwarna) + 6H+"
    },
    {
        "Nama Uji": "Uji Natrium Bikarbonat",
        "Gugus Fungsi": "Asam Karboksilat",
        "Reagen": "Larutan NaHCO3 5%",
        "Prosedur Singkat": "Tambahkan sampel organik ke dalam larutan NaHCO3 jenuh.",
        "Hasil Positif": "Terbentuk gelembung gas dengan cepat (efervesen).",
        "Warna/Visual": "🫧 Gelembung Gas (CO2)",
        "Reaksi Kimia": "R-COOH + NaHCO3 --> R-COONa + H2O + CO2 (g)"
    },
    {
        "Nama Uji": "Uji Baeyer",
        "Gugus Fungsi": "Alkena / Alkuna (Ikatan Rangkap)",
        "Reagen": "Larutan KMnO4 1% (Basa/Netral)",
        "Prosedur Singkat": "Teteskan larutan KMnO4 ke dalam sampel sambil dikocok.",
        "Hasil Positif": "Warna ungu dari KMnO4 hilang dan terbentuk endapan coklat.",
        "Warna/Visual": "🟤 Warna Ungu Hilang & Endapan Coklat",
        "Reaksi Kimia": "3R-CH=CH-R + 2KMnO4 + 4H2O --> 3R-CH(OH)-CH(OH)-R + 2MnO2 (s) + 2KOH"
    },
    {
        "Nama Uji": "Uji Benedict",
        "Gugus Fungsi": "Gula Pereduksi / Aldehida",
        "Reagen": "Larutan Benedict",
        "Prosedur Singkat": "Tambahkan pereaksi Benedict ke sampel lalu panaskan beberapa menit.",
        "Hasil Positif": "Larutan berubah dari biru menjadi hijau, kuning, jingga, hingga merah bata.",
        "Warna/Visual": "🟠 Endapan Merah Bata",
        "Reaksi Kimia": "R-CHO + Cu2+ + OH- --> R-COO- + Cu2O (s)"
    },
    {
        "Nama Uji": "Uji Schiff",
        "Gugus Fungsi": "Aldehida",
        "Reagen": "Reagen Schiff",
        "Prosedur Singkat": "Tambahkan reagen Schiff ke sampel.",
        "Hasil Positif": "Muncul warna merah muda atau magenta.",
        "Warna/Visual": "💗 Merah Muda / Magenta",
        "Reaksi Kimia": "Aldehida + reagen Schiff --> kompleks berwarna"
    },
    {
        "Nama Uji": "Uji Molisch",
        "Gugus Fungsi": "Karbohidrat",
        "Reagen": "α-naftol + H2SO4 pekat",
        "Prosedur Singkat": "Tambahkan pereaksi Molisch lalu alirkan H2SO4 perlahan.",
        "Hasil Positif": "Terbentuk cincin ungu pada batas larutan.",
        "Warna/Visual": "🟣 Cincin Ungu",
        "Reaksi Kimia": "Karbohidrat --> furfural --> kompleks ungu"
    },
    {
        "Nama Uji": "Uji Saponifikasi",
        "Gugus Fungsi": "Ester / Lemak",
        "Reagen": "NaOH atau KOH",
        "Prosedur Singkat": "Panaskan sampel dengan basa kuat.",
        "Hasil Positif": "Terbentuk sabun atau emulsi.",
        "Warna/Visual": "🫧 Emulsi / Sabun",
        "Reaksi Kimia": "Ester + NaOH --> Alkohol + Garam Asam"
    }
]

df = pd.DataFrame(data_uji)

# 3. Tampilan Header Aplikasi
st.title("🧪 ChemQual v1.0")
st.subheader("Katalog Uji Kualitatif Senyawa Organik")
st.write("Aplikasi saku untuk membantu mahasiswa/siswa mengidentifikasi gugus fungsi organik di laboratorium.")

st.divider()

# 4. Membuat Menu Navigasi dengan Tabs
tab1, tab2 = st.tabs(["🔍 Pencarian & Filter", "📚 Semua Daftar Uji"])
with tab1:
    st.markdown("### Cari Berdasarkan Parameter")
    
    search_gugus = "Semua Gugus"
    search_name = ""
    
    col1, col2 = st.columns(2)
    
    with col1:
        search_gugus = st.selectbox(
            "Pilih Gugus Fungsi yang mau dicari:",
            ["Semua Gugus"] + list(df["Gugus Fungsi"].unique())
        )
    
    with col2:
        search_name = st.text_input("Atau ketik nama uji / reagen (contoh: Tollens, FeCl3):")

    filtered_df = df.copy()
    
    if search_gugus != "Semua Gugus":
        filtered_df = filtered_df[filtered_df["Gugus Fungsi"] == search_gugus]
        
    if search_name:
        filtered_df = filtered_df[
            filtered_df["Nama Uji"].str.contains(search_name, case=False) | 
            filtered_df["Reagen"].str.contains(search_name, case=False)
        ]

    if filtered_df.empty:
        st.warning("Uji kualitatif tidak ditemukan. Coba kata kunci lain!")
    else:
        for index, row in filtered_df.iterrows():
            with st.expander(f"🔹 {row['Nama Uji']} — Target: {row['Gugus Fungsi']}", expanded=True):
                c1, c2 = st.

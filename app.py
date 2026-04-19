import streamlit as st
import pandas as pd
import re
import plotly.express as px
import joblib
import os
import base64
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# --- 
# FUNGSI MEMBACA FOTO LOKAL (ADZKIA.JPG) ---
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Inisialisasi string foto
bin_str = ""
if os.path.exists("adzkia.png"):
    bin_str = get_base64("adzkia.png")

# --- 1. KONFIGURASI HALAMAN & UI ---
st.set_page_config(page_title="PRODI INFORMATIKA UNVERSITAS ADZKIA", layout="wide")

st.markdown(f"""
    <style>
    /* BAGIAN BARU: Menambahkan Foto Background ke CSS kamu */
    .stApp {{
        background: {f'linear-gradient(rgba(0, 20, 39, 0.8), rgba(0, 20, 39, 0.8)), url("data:image/jpg;base64,{bin_str}")' if bin_str else '#001427'} !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }}

    
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    html, body, [class*="css"]
            {{ font-family: 'Poppins', sans-serif;
            color: #2c3e50; }}
    
    .role-card {{
        background-color: #01161e; 
        padding: 20px; border-radius: 10px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08); text-align: center;
        border: 2px solid #598392; margin-bottom: 10px;
    }}

    [data-testid="stSidebar"] {{ 
            background-color: #3e5c76; 
            color: #284b63; 
            }}
    
    .stRadio label, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h3 
    {{ 
        color: white !important; 
    }}

    [data-testid="stMetric"] {{
        background-color: #ffffff; padding: 20px; border-radius: 15px;
        box-shadow: 0 8px 15px rgba(0,0,0,0.05); border-left: 10px solid #a8dadc;
    }}
    [data-testid="stMetricValue"] {{ color: #01161e !important; font-weight: 600 !important; }}
    [data-testid="stMetricLabel"] {{ color: #555555 !important; }}

    /* Menargetkan container tombol agar bisa digeser ke tengah */
    [data-testid="column"] .stButton {{
        display: flex;
        justify-content: center; /* Memindahkan tombol ke tengah kolom */
        width: 100%;
        margin-top: 10px; /* Jarak antara kartu dan tombol */
    }}

    /* Mengatur lebar tombol agar pas (tidak kepanjangan) */
    [data-testid="column"] .stButton button {{
        width: 200px !important; /* Sesuaikan lebar tombol sesuai keinginanmu */
    }}
    .stButton>button {{
        width: 100%; border-radius: 25px;
        background: linear-gradient(135deg, #124559 0%, #598392 100%);
        color: white !important; border: none; font-weight: 600;
    }}

    div[data-baseweb="input"] > div, 
    div[data-baseweb="textarea"] > div {{
        background-color: #ffffff !important;
        border-radius: 10px !important;
    }}

    .stTextInput input, .stTextArea textarea {{
        color: #01161e !important;
        -webkit-text-fill-color: #01161e !important;
        background-color: #ffffff !important;
    }}

    div[data-baseweb="input"] > div:focus-within, 
    div[data-baseweb="textarea"] > div:focus-within {{
        border: 1px solid #598392 !important;
        box-shadow: none !important;
    }}

    div.stButton > button {{
        background: linear-gradient(135deg, #b0c4b1 0%, #598392 100%) !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
        transition: 0.3s !important;
    }}

    div.stButton > button:hover {{
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(18, 69, 89, 0.4);
        color: #aec3b0 !important;
    }}
            
    div[data-baseweb="select"] > div {{
        background-color: #598392 !important; 
        border: 1px solid #aec3b0 !important;
        border-radius: 10px !important;
    }}

    div[data-baseweb="select"] span, div[data-baseweb="select"] div {{
        color: white !important;
    }}

    svg[title="open"] {{
        fill: white !important;
    }}

    ul[role="listbox"] {{
        background-color: #598392 !important; 
    }}

    ul[role="listbox"] li {{
        color: white !important;
    }}

    ul[role="listbox"] li:hover {{
        background-color: #598392 !important;
        color: #aec3b0 !important;
    }}
    
    .stTabs [data-baseweb="tab"] p {{
        color: #ade8f4 !important; 
        font-weight: 400 !important;
        transition: 0.3s;
    }}

    .stTabs [aria-selected="true"] p {{
        color: #ffffff !important; 
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }}

    .stTabs [data-baseweb="tab-highlight"] {{
        background-color: #ffffff !important; 
    }}

    .stTabs [data-baseweb="tab"]:hover p {{
        color: #ffffff !important;
        text-shadow: 0 0 10px rgba(168, 218, 220, 0.8); 
    }}
    



   /* Menghilangkan label standar */
    [data-testid="stSidebarNav"] {{display: none;}}
    
    /* Container Menu Navigasi */
    div[role="radiogroup"] {{
        display: flex;
        flex-direction: column;
        gap: 0px; 
        /* Trik margin negatif agar garis menempel ke pinggir sidebar */
        margin-left: -1rem !important;
        margin-right: -1rem !important;
        margin-top: 10px;
        width: calc(100% + 2rem) !important;
    }}

    /* Styling per item menu */
    div[role="radiogroup"] label {{
        background-color: transparent;
        /* Garis pembatas bawah yang sejajar/full lebar sidebar */
        border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important; 
        padding: 18px 25px !important; 
        border-radius: 0px !important;
        transition: 0.3s all ease;
        width: 100% !important;
        margin: 0 !important;
    }}

    /* Efek Hover (Saat kursor di atas menu) */
    div[role="radiogroup"] label:hover {{
        background-color: rgba(255, 255, 255, 0.05) !important;
        /* Garis penanda di kiri saat disentuh */
        border-left: 5px solid #598392 !important;
        padding-left: 30px !important;
    }}

    /* Styling saat menu dipilih (Aktif) */
    div[role="radiogroup"] label[data-selected="true"] {{
        background-color: rgba(89, 131, 146, 0.2) !important;
        border-left: 5px solid #ffffff !important;
        font-weight: bold;
    }}

    /* Sembunyikan bulatan radio button-nya */
    div[role="radiogroup"] [data-testid="stWidgetLabel"] div div {{
        display: none;
    }}

    /* --- CSS NAVIGASI FULL WIDTH --- */
    div[role="radiogroup"] {{
        display: flex;
        flex-direction: column;
        gap: 0px; 
        margin-left: -1rem !important; /* Menarik garis ke kiri sidebar */
        margin-right: -1rem !important; /* Menarik garis ke kanan sidebar */
        margin-top: 10px;
        width: calc(100% + 2rem) !important;
    }}

    div[role="radiogroup"] label {{
        background-color: transparent;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important; 
        padding: 18px 25px !important; 
        border-radius: 0px !important;
        transition: 0.3s all ease;
        width: 100% !important;
        margin: 0 !important;
    }}

    /* Efek Hover Navigasi */
    div[role="radiogroup"] label:hover {{
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-left: 5px solid #598392 !important;
        padding-left: 30px !important;
    }}

    /* --- CSS TOMBOL LOGOUT MERAH CORAL --- */
    /* Kita menargetkan tombol logout agar selalu di bawah */
    .stButton > button {{
        border-radius: 12px !important;
        transition: 0.3s all ease !important;
    }}

    /* Warna spesifik Merah Coral untuk tombol Keluar */
    button:has(div:contains("Keluar")) {{
        background: linear-gradient(135deg, #d90429 0%, #d90429 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
        position: fixed !important;
        bottom: 20px !important;
        left: 10px !important;
        width: 280px !important; /* Sesuaikan lebar sidebar kamu */
        z-index: 1000;
    }}

    button:has(div:contains("Keluar")):hover {{
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(221, 45, 74, 0.4) !important;
    }}
    
    </style>
    """, unsafe_allow_html=True)


# --- 2. LOGIKA DATA & PREPROCESSING ---
@st.cache_resource
def get_tools():
    return StemmerFactory().create_stemmer(), StopWordRemoverFactory().create_stop_word_remover()

stemmer, stopword_remover = get_tools()

# --- FUNGSI DATABASE USER (UNTUK LOGIN SATU PINTU) ---
def load_users():
    if not os.path.exists("users_db.csv"):
        # Role 'Admin' untuk admin, 'User Umum' untuk mahasiswa
        df = pd.DataFrame(columns=["username", "password", "role"])
        # Daftarkan Admin pertama kali secara otomatis
        df.loc[0] = ["admin", "admin123", "Admin"] 
        df.to_csv("users_db.csv", index=False)
    return pd.read_csv("users_db.csv")

def save_user(username, password):
    df = load_users()
    if username in df['username'].values:
        return False
    # Pendaftar baru otomatis menjadi 'User Umum'
    new_user = pd.DataFrame([[username, password, "User Umum"]], columns=["username", "password", "role"])
    new_user.to_csv("users_db.csv", mode='a', header=False, index=False)
    return True

def clean_text_fast(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    text = stopword_remover.remove(text)
    return " ".join([stemmer.stem(w) for w in text.split()])

# --- PEMBACAAN DATA ---
if 'main_df' not in st.session_state:
    if os.path.exists('evaluasi matkul.xlsx'):
        df_file = pd.read_excel('evaluasi matkul.xlsx')
        
        # CEK: Apakah ini file hasil simpanan (sudah rapi) atau file kuesioner asli?
        if 'Matkul' in df_file.columns and 'Suka' in df_file.columns:
            # Jika file sudah rapi, langsung ambil saja
            st.session_state.main_df = df_file
        else:
            # Jika ini masih file kuesioner asli yang berantakan, jalankan logika pembersihan lama
            sections = [[2,3,4,5,6], [7,8,9,10,11], [12,13,14,15,16], [17,18,19,20,21], 
                        [22,23,24,25,26], [27,28,29,30,31], [32,33,34,35,36], [37,38,39,40,41], 
                        [42,43,44,45,46], [47,48,49,50,51], [52,53,54,55,56], [57,58,59,60,61]]
            rekap = []
            for sec in sections:
                for _, row in df_file.iterrows():
                    if len(row) > max(sec) and pd.notna(row.iloc[sec[0]]):
                        rekap.append({
                            'Matkul': row.iloc[sec[0]], 
                            'Suka': str(row.iloc[sec[2]]), 
                            'Kendala': str(row.iloc[sec[3]]), 
                            'Umum': str(row.iloc[sec[1]])
                        })
            st.session_state.main_df = pd.DataFrame(rekap)

def get_summary():
    # Memuat model dan tfidf yang sudah dilatih
    model = joblib.load('model_nb_aisyah.pkl')
    tfidf = joblib.load('tfidf_aisyah.pkl')
    
    # Ambil data mentah (255 baris)
    df = st.session_state.main_df.copy()
    
    # Tahap 1: Klasifikasikan SETIAP baris ulasan
    # Gunakan kolom 'Umum' sebagai dasar prediksi Naive Bayes
    df['text_clean'] = df['Umum'].apply(clean_text_fast)
    df['prediksi_label'] = model.predict(tfidf.transform(df['text_clean']))
    
    # Tahap 2: Agregasi (Hitung jumlah orang yang positif/negatif per matkul)
    # 1 dianggap Positif, 0 dianggap Negatif (sesuaikan dengan label modelmu)
    summary = df.groupby('Matkul').agg(
        Ulasan_Positif=('prediksi_label', lambda x: (x == 1).sum()),
        Ulasan_Negatif=('prediksi_label', lambda x: (x == 0).sum()),
        Total_Responden=('Matkul', 'count')
    ).reset_index()
    
    return summary, df

# --- 3. LANDING PAGE ---
if 'role_akses' not in st.session_state: 
    st.session_state.role_akses = None

if st.session_state.role_akses is None:
    # Deskripsi Umum Web
    st.markdown("<h1 style='text-align: center; margin-top: 30px;'>Selamat Datang di Portal Evaluasi</h1>", unsafe_allow_html=True)
    st.markdown("""
        <div style='text-align: center; padding: 30px; border-radius: 20px; margin-bottom: 30px; border-left: 15px ;'>
            <h5>Selamat datang di <b>Sistem Analisis Sentimen Evaluasi Mata Kuliah</b> Program Studi Informatika Universitas Adzkia.<br> 
            Web ini dirancang untuk memproses ulasan mahasiswa menggunakan teknologi <i>Text Mining</i> dengan algoritma Naive Bayes <br> 
            Hasil analisis ini membantu program studi dalam memantau kualitas pembelajaran secara transparan dan interaktif.</h5>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h3 style='text-align: center; color: #ffffff;'>Silakan Login Untuk Mengakses Data</h3>", unsafe_allow_html=True)
    
    col_kiri, col_utama, col_kanan = st.columns([1, 1.5, 1])

    with col_utama: 
        tab_login, tab_register = st.tabs(["🔐 Masuk Sistem", "📝 Daftar Akun Baru"])

        with tab_login:
            st.write("Silakan masukkan akun untuk melanjutkan.")
            input_user = st.text_input("Username / NIM", placeholder="Masukan Username")
            input_pass = st.text_input("Password", type="password", placeholder="******")
            
            # Tombol otomatis mengikuti lebar kolom tengah yang sudah dirampingkan
            if st.button("Continue", type="primary", use_container_width=True):
                users = load_users()
                match = users[(users['username'] == input_user) & (users['password'] == input_pass)]
                
                if not match.empty:
                    st.session_state.role_akses = match.iloc[0]['role']
                    st.success(f"Berhasil masuk sebagai {st.session_state.role_akses}")
                    st.rerun()
                else:
                    st.error("Username atau Password salah.")

        with tab_register:
            st.write("Lengkapi data untuk membuat akun mahasiswa.")
            reg_name = st.text_input("Buat Username", placeholder="username")
            reg_pass = st.text_input("Buat Password", type="password")
            reg_confirm = st.text_input("Konfirmasi Password", type="password")
            
            agree = st.checkbox("Setuju")
            
            if st.button("Registrasi", use_container_width=True):
                if agree:
                    if reg_pass == reg_confirm and reg_name:
                        if save_user(reg_name, reg_pass):
                            st.success("Akun berhasil dibuat! Silakan pindah ke tab Masuk.")
                        else:
                            st.warning("Username tersebut sudah terdaftar.")
                    else:
                        st.error("Pastikan password cocok dan kolom terisi.")
                else:
                    st.warning("Anda harus menyetujui syarat.")
        
        st.markdown("</div>", unsafe_allow_html=True) # Tutup kotak transparan

# --- 4. DASHBOARD UTAMA ---

else:
    summary = get_summary()
    with st.sidebar:
        # Nama Akses (Admin / User)
        st.markdown(f"<h3 style='text-align:center; padding-top:20px; color:white;'>{st.session_state.role_akses}</h3>", unsafe_allow_html=True)
        st.write("") # Spasi
        
        # Garis pembatas awal
        st.markdown("<hr style='margin: 0 -20px; border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
        
        # Daftar Menu
        nav = ["Beranda", "Analisis Sentimen", "Tentang"]
        if st.session_state.role_akses == "Admin": 
            nav.insert(2, "Data Master (Admin)")
        
        # Tampilkan navigasi tanpa label
        menu = st.radio("", nav, label_visibility="collapsed")
        
        if st.button("Keluar"): 
            st.session_state.role_akses = None
            st.rerun()
    if menu == "Beranda":
        st.title("Prodi Informatika Universitas Adzkia")
        
        st.markdown("""
        <div style='background-color:rgba(255,255,255,0.05); padding:20px; border-radius:15px;'>
            <p>Informatika Adzkia berfokus pada pengembangan teknologi yang inovatif dan berbasis karakter mulia. 
            Kami menyiapkan lulusan yang siap bersaing di industri teknologi global.</p>
        </div>
        """, unsafe_allow_html=True)


        st.divider()
        # Membuat dua kolom: kiri untuk Visi, kanan untuk Misi
        col_visi, col_misi = st.columns([1, 1.5], gap="large")

        with col_visi:
            st.markdown("### 🎯 Visi")
            st.markdown("""
                <div style="text-align: justify; color: white; line-height: 1.6;">
                Menjadi program studi yang unggul pada bidang Ilmu Komputer / Informatika 
                dan menghasilkan lulusan yang berkarakter, berprestasi, serta mampu 
                bersaing secara global.
                </div> """, unsafe_allow_html=True)
            

        with col_misi:
            st.markdown("### 🚀 Misi")
            misi_points = [
                "Menyelenggarakan pendidikan dan pembelajaran berkualitas untuk memajukan IPTEK dalam bidang Informatika dengan memperhatikan dan menerapkan nilai-nilai humaniora.",
                "Menyelenggarakan penelitian yang inovatif serta bermanfaat bagi masyarakat dan pengembangan IPTEK di bidang Informatika.",
                "Menyelenggarakan pengabdian kepada masyarakat yang berkualitas dan tepat guna pada bidang Informatika.",
                "Menerapkan tata kelola program studi Informatika yang bersih dan baik (*Clean and Good Governance*).",
                "Menerapkan dan mengembangkan nilai-nilai karakter mulia dan *rahmatan lil ‘alamin* dalam pelaksanaan Tridharma Perguruan Tinggi pada bidang Ilmu Komputer / Informatika."
            ]
            # Bungkus seluruh loop di dalam div justify
            st.markdown('<div style="text-align: justify; color: white;">', unsafe_allow_html=True)
            for i, point in enumerate(misi_points, 1):
                st.markdown(f"**{i}.** {point}")
            st.markdown('</div>', unsafe_allow_html=True)

    elif menu == "Analisis Sentimen":
        summary, raw_classified = get_summary() 
    
        st.title("📊 Dashboard Analisis & Statistik")
        
        # 1. METRIK UTAMA (Berdasarkan total suara per orang)
        total_positif = (raw_classified['prediksi_label'] == 1).sum()
        total_negatif = (raw_classified['prediksi_label'] == 0).sum()
        n_total = len(raw_classified)
    
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Ulasan Masuk", len(raw_classified))
        col2.metric("Total Suara Positif", total_positif)
        col3.metric("Total Suara Negatif", total_negatif)
        
        st.divider()
        
        # 2. GRAFIK PIE (Persentase dari 255 data)
        st.subheader("Persentase Sentimen Keseluruhan")
        raw_classified['Label_Teks'] = raw_classified['prediksi_label'].map({1: 'Positif', 0: 'Negatif'})
        
        fig_pie = px.pie(raw_classified, names='Label_Teks', hole=0.4,
                         color='Label_Teks',
                         color_discrete_map={'Positif':'#90a955', 'Negatif':'#dd2d4a'})
        
        fig_pie.update_layout(
            height=600, 
            margin=dict(l=20, r=20, t=50, b=20),
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font=dict(color="white", size=18),
            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="right", x=1.1)
        )
        st.plotly_chart(fig_pie, use_container_width=True, key="pie_utama") # Pakai Key agar unik
        
        st.divider()

        # 3. GRAFIK BATANG (Sebaran per Matkul)
        st.subheader("Sebaran Persepsi Mahasiswa per Mata Kuliah")
        fig_bar = px.bar(summary, x='Matkul', y=['Ulasan_Positif', 'Ulasan_Negatif'], 
                         color_discrete_map={'Ulasan_Positif':'#90a955', 'Ulasan_Negatif':'#dd2d4a'},
                         barmode='group') 
        
        fig_bar.update_layout(
            height=700,
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font=dict(color="white", size=14),
            xaxis=dict(tickfont=dict(size=12)), # Ukuran teks nama matkul diperbesar
            legend=dict(title_font_size=14, font_size=12)
        )
        st.plotly_chart(fig_bar, use_container_width=True, key="bar_utama")
        
        st.divider()

        # 5. DETAIL PER MATKUL & INPUT ULASAN BARU 
        st.subheader("🔍 Detail & Input Ulasan Baru")
        pilihan = st.selectbox("Pilih Mata Kuliah", sorted(summary['Matkul'].unique()))
        res = summary[summary['Matkul'] == pilihan].iloc[0]
        
        # Tampilkan Detail Angka
        c1, c2 = st.columns(2)
        c1.info(f"Jumlah Mahasiswa Puas: {res['Ulasan_Positif']}")
        c2.error(f"Jumlah Mahasiswa Mengeluh: {res['Ulasan_Negatif']}")


    # --- 1. INISIALISASI---
        if 'notif_sukses' not in st.session_state:
            st.session_state.notif_sukses = None

        with st.expander(f"➕ Berikan Ulasan Baru untuk {pilihan}"):
            # Tampilkan notifikasi jika ada pesan tersimpan
            if st.session_state.notif_sukses:
                st.success(st.session_state.notif_sukses)
                if st.button("Tutup Pesan"):
                    st.session_state.notif_sukses = None
                    st.rerun()
            
            # --- 2. MULAI FORM ---
            with st.form("input_form_cerdas", clear_on_submit=True):
                st.write("Masukkan ulasan Anda mengenai mata kuliah ini:")
                
                ulasan_suka = st.text_input("Apa hal yang paling Anda sukai?", 
                                            placeholder="Contoh: Cara mengajar dosen asik")
                
                ulasan_kendala = st.text_input("Apa kendala atau hal yang kurang?", 
                                               placeholder="Contoh: Materi terlalu cepat disampaikan")
                
                ulasan_umum = st.text_area("Berikan ulasan umum secara menyeluruh:", 
                                           placeholder="Tulis pendapat Anda di sini...")
                
                # Tombol Kirim
                submit_button = st.form_submit_button("Kirim Evaluasi")
                
                if submit_button:
                    if ulasan_umum.strip() == "":
                        st.warning("Mohon isi ulasan pada kolom 'Pendapat Umum'.")
                    else:
                        # 1. Proses Klasifikasi
                        model_obj = joblib.load('model_nb_aisyah.pkl')
                        tfidf_obj = joblib.load('tfidf_aisyah.pkl')
                        u_clean = clean_text_fast(ulasan_umum)
                        pred = model_obj.predict(tfidf_obj.transform([u_clean]))[0]
                        label = "POSITIF 👍" if pred == 1 else "NEGATIF 👎"
                        
                        # 2. Definisikan Data Baru 
                        new_data = pd.DataFrame([{
                            'Matkul': pilihan, 
                            'Suka': ulasan_suka if ulasan_suka else '-', 
                            'Kendala': ulasan_kendala if ulasan_kendala else '-', 
                            'Umum': ulasan_umum
                        }])
                        
                        # 3. Update Dataframe Utama
                        st.session_state.main_df = pd.concat([st.session_state.main_df, new_data], ignore_index=True)
                        
                        # 4. Simpan Pesan dan Refresh
                        st.session_state.notif_sukses = f"✅ Berhasil! Ulasan untuk {pilihan} terdeteksi {label}"
                        st.rerun()

# --- ANALISIS 3 ASPEK UTAMA (FOKUS PERSENTASE) ---
        st.divider()
        st.subheader("🌐 Analisis Perbandingan Aspek Seluruh Mata Kuliah")
        
        # Kamus Kata Kunci 
        kamus_final_100 = {
            'Materi & Kesulitan': [
                'materi', 'modul', 'paham', 'sulit', 'susah', 'berat', 'gampang', 
                'rumus', 'teori', 'pembahasan', 'isi', 'kurikulum', 'topik', 'pelajaran', 
                'konsep', 'ilmu', 'bobot', 'menantang', 'kompleks', 'abstrak', 
                'kalkulus', 'logika', 'mendasar', 'bermanfaat', 'nyambung'
            ],
            'Metode & Praktik': [
                'praktek', 'praktikum', 'coding', 'contoh', 'langsung', 'lab', 
                'komputer', 'implementasi', 'nyata', 'metode', 'penerapan', 'praktekan', 
                'dipraktekkan', 'membangun', 'proyek', 'kelompok', 'cerita', 'dunia kerja', 
                'industri', 'profesi', 'studi kasus', 'ngoding', 'software', 'aplikasi', 'mobile', 'sql', 'bosan'
            ],
            'Dosen & Penyampaian': [
                'dosen', 'ajar', 'jelas', 'suara', 'sampaikan', 'cara mengajar', 
                'bapak', 'ibu', 'beliau', 'menerangkan', 'komunikasi', 'menjelaskan', 
                'asik', 'enjoy', 'nyaman', 'interaksi', 'cerita', 'pengalaman', 'sharing', 
                'baik', 'sabar', 'kompeten', 'menyenangkan', 'penerangan', 'penyampaiannya', 
                'ceramah', 'seru', 'disiplin', 'jarang', 'pelan' 
            ]
        }

        data_rekap_100 = []
        for m_nama in sorted(raw_classified['Matkul'].unique()):
            df_m = raw_classified[raw_classified['Matkul'] == m_nama]
            
            for asp_nama, kws in kamus_final_100.items():
                pattern = '|'.join(kws)
                mask = df_m['Umum'].str.contains(pattern, case=False, na=False)
                df_aspek = df_m[mask]
                
                total_ulasan_aspek = len(df_aspek)
                
                if total_ulasan_aspek > 0:
                    jml_positif = (df_aspek['prediksi_label'] == 1).sum()
                    persen_puas = (jml_positif / total_ulasan_aspek) * 100
                    persen_keluhan = 100 - persen_puas # Sisanya otomatis jadi negatif
                else:
                    # Jika tidak ada yang bahas aspek ini, kita beri nilai 0 agar tidak kosong
                    persen_puas = 0
                    persen_keluhan = 0
                
                # Masukkan data positif
                data_rekap_100.append({
                    'Mata Kuliah': m_nama,
                    'Aspek': asp_nama,
                    'Persentase': persen_puas,
                    'Sentimen': 'Pujian (Positif)'
                })
                # Masukkan data negatif
                data_rekap_100.append({
                    'Mata Kuliah': m_nama,
                    'Aspek': asp_nama,
                    'Persentase': persen_keluhan,
                    'Sentimen': 'Keluhan (Negatif)'
                })

        df_full_100 = pd.DataFrame(data_rekap_100)
        df_full_100 = df_full_100.sort_values(by=['Mata Kuliah'], ascending=True)

        # Visualisasi Stacked Bar yang dibagi per kolom Aspek (Facet)
        fig_full = px.bar(
            df_full_100, 
            x='Persentase', 
            y='Mata Kuliah', 
            color='Sentimen',
            facet_col='Aspek', # Membagi layar jadi 3 kolom (Materi, Metode, Dosen)
            orientation='h',
            barmode='stack', 
            height=1200,
            # Warna Hijau/Biru untuk positif, Merah untuk negatif
            color_discrete_map={
                'Pujian (Positif)': '#219ebc', # Biru 
                'Keluhan (Negatif)': '#ef233c'  # Merah
            },
            text_auto='.0f'
        )

        fig_full.update_yaxes(autorange="reversed")
        fig_full.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font_color="white",
            xaxis_title="Persentase (%)",
            yaxis_title="",
            legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5)
        )

        # Menghapus teks "Aspek=" di atas tiap kolom agar lebih bersih
        fig_full.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

        st.plotly_chart(fig_full, use_container_width=True, key="grafik_full_100_percent")

  
    elif menu == "Data Master (Admin)":
        st.title("⚙️ Manajemen Data Master")
        
        # 1. Fitur Upload Berkas Baru
        up = st.file_uploader("Upload Excel/CSV", type=['xlsx', 'csv'], key="admin_up")
        if up:
            new_df = pd.read_excel(up) if up.name.endswith('.xlsx') else pd.read_csv(up)
            st.session_state.main_df = new_df
            # SIMPAN PERMANEN HASIL UPLOAD
            new_df.to_excel('evaluasi matkul.xlsx', index=False) 
            st.success("Update Berhasil & File Excel Diperbarui!")
            st.rerun()

        st.divider()

        # 2. Tabel Editor 
        edited_df = st.data_editor(st.session_state.main_df, num_rows="dynamic", use_container_width=True, key="master_edit")
        
        # 3. TOMBOL SIMPAN PERMANEN (WAJIB ADA)
        if st.button("💾 Simpan Perubahan", type="primary", use_container_width=True):
            # Update memori aplikasi
            st.session_state.main_df = edited_df 
            
            # TULIS ULANG KE FILE FISIK (Ini biar tidak hilang saat refresh)
            edited_df.to_excel('evaluasi matkul.xlsx', index=False) 
            
            st.success("✅ BERHASIL! Data sekarang sudah tersimpan permanen di file Excel.")
            st.balloons()
            st.rerun()

    elif menu == "Tentang":
        st.title("ℹ️ Tentang Sistem")
        st.divider()
        
        # 1. Ringkasan Sistem
        st.markdown("### 📊 Ringkasan Sistem")
        c1, c2, c3 = st.columns(3)
        c1.metric("Metode", "Naive Bayes")
        c2.metric("Dataset", f"{len(st.session_state.main_df)} Baris")
        c3.metric("Akurasi Model", "93,14%") 

        st.divider()
        
        # 2. Alur Kerja Sistem
        st.markdown("### 🛠️ Alur Kerja Sistem")
        
        # --- TAMBAH DETAIL ALUR ---
        with st.expander("🔍 Tahap 1: Preprocessing (Pembersihan Teks)"):
            st.write("""
            Pada tahap ini, ulasan mahasiswa dibersihkan:
            * **Case Folding**: Mengubah teks menjadi huruf kecil.
            * **Filtering**: Menghapus angka dan tanda baca.
            * **Tokenizing**: Mengubah kalimat menjadi per kata.        
            * **Stopword Removal**: Menghapus kata umum.
            * **Stemming**: Mengubah kata menjadi kata dasar.
            """)

        with st.expander("🔢 Tahap 2: Pembobotan TF-IDF"):
            st.write("""
            Data teks diubah menjadi bentuk angka (vektor) menggunakan metode **TF-IDF**. 
            Metode ini menghitung seberapa penting suatu kata dalam sebuah ulasan relatif terhadap seluruh ulasan yang ada.
            """)

        with st.expander("🤖 Tahap 3: Klasifikasi Naive Bayes"):
            st.write("""
            Algoritma **Naive Bayes** digunakan untuk menghitung probabilitas ulasan masuk ke kategori **Positif** atau **Negatif** berdasarkan pola kata yang telah dipelajari dari data latih.
            """)
        # ------------------------------------------

        st.divider()
        # --- FOOTER (IDENTITAS PENGEMBANG) ---
# Kode ini diletakkan di luar semua blok 'if menu ==' agar selalu muncul
st.markdown("""
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgba(0, 20, 39, 0.9); /* Transparan gelap biar senada background */
        color: #f1f1f1;
        text-align: center;
        padding: 15px 0;
        font-family: 'Poppins', sans-serif;
        border-top: 2px solid #598392;
        z-index: 999;
    }
    .footer b {
        color: #aec3b0; /* Warna aksen untuk nama kamu */
        font-size: 1.1rem;
    }
    .footer p {
        margin: 0;
        font-size: 1rem;
    }
    </style>
    
    <div class="footer">
        <p><b>Sistem Analisis Sentimen Evaluasi Mata Kuliah</b></p>
        <p>Dikembangkan oleh: <b>Aisyah Qurrata Ayun</b> (Informatika Adzkia)</p>
        <p style='font-size: 0.8rem; color: #888;'>&copy; 2026 Tugas Akhir - Universitas Adzkia</p>
    </div>
""", unsafe_allow_html=True)

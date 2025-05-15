import streamlit as st
import json

st.set_page_config(page_title="✨ Proje Öneri Sistemi", page_icon="🚀")
st.title("✨ Proje Öneri Sistemi")

try:
    with open("projects.json", "r", encoding="utf-8") as dosya:
        projeler = json.load(dosya)
except FileNotFoundError:
    st.error("Projeler dosyası bulunamadı! Lütfen 'projects.json' dosyasını kontrol edin.")
    projeler = []

if not projeler:
    st.stop()

diller = sorted(set(p["language"] for p in projeler))
zorluklar = sorted(set(p["difficulty"] for p in projeler))
veritabanlari = sorted(set(p["database"] if p["database"] else "Yok" for p in projeler))
durumlar = ["Hepsi", "Başlandı", "Tamamlandı", "Devam Ediyor"]
kategoriler = sorted(set(p["category"] for p in projeler))
kategoriler = ["Hepsi"] + kategoriler

st.sidebar.header("🔎 Filtreleme Seçenekleri")
secili_dil = st.sidebar.selectbox("Programlama Dili", ["Hepsi"] + diller)
secili_zorluk = st.sidebar.selectbox("Zorluk Seviyesi", ["Hepsi"] + zorluklar)
secili_veritabani = st.sidebar.selectbox("Veritabanı", ["Hepsi"] + veritabanlari)
secili_durum = st.sidebar.selectbox("Proje Durumu", durumlar)
secili_kategori = st.sidebar.selectbox("Proje Kategorisi", kategoriler)
sadece_cevrimici = st.sidebar.checkbox("Sadece çevrimiçi projeleri göster")

def filtrele(proje):
    if secili_dil != "Hepsi" and proje["language"] != secili_dil:
        return False
    if secili_zorluk != "Hepsi" and proje["difficulty"] != secili_zorluk:
        return False
    if secili_veritabani != "Hepsi":
        if secili_veritabani == "Yok" and proje["database"]:
            return False
        elif secili_veritabani != "Yok" and proje["database"] != secili_veritabani:
            return False
    if secili_durum != "Hepsi" and proje["status"] != secili_durum:
        return False
    if secili_kategori != "Hepsi" and proje["category"] != secili_kategori:
        return False
    if sadece_cevrimici and not proje["online"]:
        return False
    return True

filtrelenmis_projeler = list(filter(filtrele, projeler))

st.subheader(f"🔍 {len(filtrelenmis_projeler)} proje bulundu:")

if filtrelenmis_projeler:
    for proje in filtrelenmis_projeler:
        with st.container():
            st.markdown(f"### {proje['title']}")
            st.write(f"**Dil**: {proje['language']} | **Zorluk**: {proje['difficulty']} | **Kategori**: {proje['category']}")
            st.write(f"**Veritabanı**: {proje['database'] if proje['database'] else 'Yok'} | **Durum**: {proje['status']} | {'🌐 Çevrimiçi' if proje['online'] else '💾 Çevrimdışı'}")
            st.write(f"**Açıklama**: {proje['description']}")
            st.markdown(f"[🔗 Projeye Git]({proje['link']})")
            st.markdown("---")
else:
    st.info("Filtrelere uygun proje bulunamadı. 😊")



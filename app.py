import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os

st.set_page_config(page_title="Generator naljepnica", layout="centered")

st.title("Generator naljepnica")
st.title("210!")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def nadji_sliku(broj):
    for ext in [".png", ".jpg", ".jpeg", ".webp"]:
        putanja = os.path.join(BASE_DIR, f"{broj}{ext}")
        if os.path.exists(putanja):
            return putanja
    return None

def font(velicina, bold=False):
    putanje = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf"
    ]

    for putanja in putanje:
        if os.path.exists(putanja):
            return ImageFont.truetype(putanja, velicina)

    st.warning("Nije pronađen pravi font. Koristi se mali default font.")
    return ImageFont.load_default()

def generiraj_naljepnicu(slika_broj, firma, naziv, dimenzije, donji_tekst):
    W, H = 1600, 1000

    img = Image.new("RGB", (W, H), "white")
    draw = ImageDraw.Draw(img)

    margin = 130

    # vanjski okvir
    draw.rounded_rectangle(
        (margin, 90, W - margin, H - 90),
        radius=65,
        outline="black",
        width=5
    )

    # slika vijka
    putanja_slike = nadji_sliku(slika_broj)

    if putanja_slike:
        vijak = Image.open(putanja_slike).convert("RGBA")
        vijak.resize((600, 900))
        img.paste(vijak, (120, 200), vijak)
    else:
        draw.text((220, 360), "Nema slike", fill="black", font=font(35, True))

    # fontovi
    font_firma = font(145, True)
    font_naziv = font(90, True)
    font_dim = font(85, True)
    font_donji = font(80, True)

    x_text = 520

    # naziv firme
    draw.text((x_text, 145), firma, fill="black", font=font_firma)

    # crta
    draw.line((x_text, 285, W - 260, 285), fill="black", width=5)

    # naziv vijka
    draw.text((x_text, 345), naziv, fill="black", font=font_naziv)

    # dimenzije
    draw.text((x_text, 515), dimenzije, fill="black", font=font_dim)

    # donji tekst
    draw.text((x_text, 690), donji_tekst, fill="black", font=font_donji)

    return img


# -----------------------------
# ODABIR SLIKE
# -----------------------------

st.subheader("Odaberi sliku vijka")

if "slika_broj" not in st.session_state:
    st.session_state.slika_broj = 1

col1, col2, col3, col4 = st.columns(4)

with col1:
    putanja1 = nadji_sliku(1)
    if putanja1:
        st.image(putanja1, width=120)
    if st.button("Odaberi 1"):
        st.session_state.slika_broj = 1

with col2:
    putanja2 = nadji_sliku(2)
    if putanja2:
        st.image(putanja2, width=120)
    if st.button("Odaberi 2"):
        st.session_state.slika_broj = 2

with col3:
    putanja3 = nadji_sliku(3)
    if putanja3:
        st.image(putanja3, width=120)
    if st.button("Odaberi 3"):
        st.session_state.slika_broj = 3

with col4:
    putanja4 = nadji_sliku(4)
    if putanja4:
        st.image(putanja4, width=120)
    if st.button("Odaberi 4"):
        st.session_state.slika_broj = 4

st.success(f"Trenutno odabrana slika: {st.session_state.slika_broj}")

slika_broj = st.session_state.slika_broj


# -----------------------------
# INPUTI
# -----------------------------

firma = st.text_input("Naziv firme", "TENNACO d.o.o.")
naziv = st.text_input("Naziv vijka", "Vijak za lim (PH)")
dimenzije = st.text_input("Dimenzije", "4,2 x 38")
donji_tekst = st.text_input("Donji tekst", "DIN 7982 C • 500 kom")


# -----------------------------
# GENERIRANJE
# -----------------------------

if st.button("Generiraj naljepnicu"):
    naljepnica = generiraj_naljepnicu(
        slika_broj,
        firma,
        naziv,
        dimenzije,
        donji_tekst
    )

    st.image(naljepnica, caption="Generirana naljepnica")

    buffer = BytesIO()
    naljepnica.save(buffer, format="PNG")
    buffer.seek(0)

    st.download_button(
        label="Preuzmi naljepnicu",
        data=buffer,
        file_name="naljepnica.png",
        mime="image/png"
    )

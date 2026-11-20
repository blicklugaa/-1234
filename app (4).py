import numpy as np
import streamlit as st
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="AI Creative Studio", page_icon="🎨")

def make_fake_image(shift=0):
    x = np.linspace(0, 255, 400, dtype=np.uint8)
    r = np.tile(x, (400, 1))
    g = np.tile(x[::-1].reshape(-1, 1), (1, 400))
    b = np.full((400, 400), 120 + shift, dtype=np.uint8)
    return Image.fromarray(np.dstack([r, g, b]))

def img_to_bytes(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

if "history" not in st.session_state:
    st.session_state["history"] = []
if "generated" not in st.session_state:
    st.session_state["generated"] = False

st.sidebar.title("Меню")
screen = st.sidebar.radio("Екран", ["Створення", "Результат і фільтри", "Історія"])
show_error = st.sidebar.checkbox("Показати помилку (для тесту)")

if screen == "Створення":
    st.title("AI Creative Studio")
    st.write("Опиши, яке зображення хочеш отримати")

    prompt = st.text_area("Ваш промпт:", placeholder="Наприклад: кіт-астронавт на Місяці")
    style = st.selectbox("Стилі:", ["Без стилю", "Реалістичний", "Акварель", "Мультяшний", "Піксель-Арт"])

    if st.button("Згенерувати зображення"):
        if not prompt:
            st.warning("Спочатку напиши, що саме намалювати")
        elif show_error:
            st.error("Не вдалося згенерувати зображення: сервіс тимчасово недоступний")
        else:
            st.info("🔧 Заглушка: тут буде функція generate_image(), яка відправить промпт у ШІ і поверне картинку")
            st.session_state["generated"] = True
            st.session_state["history"].append({"prompt": prompt, "style": style})
            st.image(make_fake_image(), caption=f"Приклад результату. Стиль: {style}", use_container_width=True)

elif screen == "Результат і фільтри":
    st.title("Результат і фільтри")

    if not st.session_state["generated"]:
        st.warning("Ще немає зображення. Спочатку створи його на екрані Створення")
    else:
        filter_option = st.sidebar.selectbox("Фільтр", [
            "Без фільтра", "Чорно-біле", "Розмиття", "Контури", "Сепія",
            "Віддзеркалення", "Налаштування яскравості", "Налаштування контрасту",
            "Колірний сплеск"
        ])

        if filter_option == "Налаштування яскравості":
            st.sidebar.slider("Рівень яскравості", -100, 100, 0)
        elif filter_option == "Налаштування контрасту":
            st.sidebar.slider("Рівень контрасту", 0.5, 3.0, 1.0, step=0.1)
        elif filter_option == "Колірний сплеск":
            st.sidebar.selectbox("Колір", ["Червоний", "Зелений", "Синій"])

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Від ШІ")
            st.image(make_fake_image(), use_container_width=True)
        with col2:
            st.subheader("Після фільтра")
            st.image(make_fake_image(60), use_container_width=True)

        st.info(f"🔧 Заглушка: тут буде фільтр {filter_option} через OpenCV")

        st.download_button(
            label="Завантажити",
            data=img_to_bytes(make_fake_image(60)),
            file_name="ai_result.png",
            mime="image/png"
        )

elif screen == "Історія":
    st.title("Історія")

    if len(st.session_state["history"]) == 0:
        st.write("Поки що порожньо")
    else:
        for i, item in enumerate(st.session_state["history"]):
            st.write(f"{i + 1}. {item['prompt']} (стиль: {item['style']})")
        st.info("🔧 Заглушка: тут будуть маленькі картинки всіх створених зображень")

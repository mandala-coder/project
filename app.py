import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import io

# 1. НАЛАШТУВАННЯ
st.set_page_config(page_title="Мандала особистості", layout="wide")

st.title("🎨 Цифрова мандала особистості")
st.write("### Математично-мистецький проєкт. Візуалізація біометричних даних")
st.markdown("---")

# 2. ВКЛАДКИ
tab1, tab2 = st.tabs(["🚀 Генератор мандали", "📜 Наукове обґрунтування"])

with tab2:
    st.header("Математична декомпозиція моделі")
    st.write("Простір нормовано. Всі елементи залежать від психотипу (Темпераменту).")

    # --- 1. СОН ---
    st.subheader("1. Топологія Ядра (Сон)")
    st.latex(r"r_{hole} = R_{core} \cdot \left(1 - \frac{S}{12}\right)")

    # --- 2. ДЕНЬ НАРОДЖЕННЯ ---
    st.subheader("2. Гармонічна зірка (День народження)")
    st.latex(r"N_{star} = d")

    # --- 3. ПЕЛЮСТКИ ---
    st.subheader("3. Емоційний шар (Місяць та Впевненість)")
    st.latex(r"r_{rose} = |\cos(\frac{n}{2}\theta)|^p")

    # --- 4. ЕНЕРГЕТИЧНА СІТКА ---
    st.subheader("4. Силова структура (Енергія)")
    st.write("Радіальні промені. Їх кількість та яскравість залежать від Енергії ($T$) та Темпераменту.")
    st.latex(r"N_{rays} = T \times 4")

    # --- 5. СПІРАЛІ ФЕРМА ---
    st.subheader("5. Поле досвіду (Вік)")
    st.write("Точки (події) розташовані за спіраллю Ферма. Їх розмір залежить від Енергії.")
    st.latex(r"Size \propto T \cdot \text{Temperament}")

    # --- 6. ЗРІСТ ---
    st.subheader("6. Захисна межа (Зріст)")
    st.latex(r"N_{peaks} = \frac{H}{10}")

    # --- 7. ТЕМПЕРАМЕНТ ---
    st.subheader("7. Темперамент (Стилізація)")
    st.write("""
    * **Холерик:** Максимальна товщина ліній, повна непрозорість (100%).
    * **Сангвінік:** Середня товщина, висока прозорість.
    * **Флегматик:** Товсті, але дуже прозорі лінії.
    * **Меланхолік:** Тонкі лінії, середня прозорість.
    """)

with tab1:
    # ПАНЕЛЬ КЕРУВАННЯ
    st.sidebar.header("📋 Твої дані")
    with st.sidebar:
        # Група 1: Базові дані
        n = st.number_input("Місяць народження", 1, 12, 6)
        d = st.number_input("День народження", 1, 31, 15)
        
        H = st.slider("Зріст (см)", 100, 220, 170, help="Кількість зубців на межі")
        A = st.slider("Вік", 10, 100, 45, help="Кількість точок у спіралі")
        S = st.slider("Годин сну", 0, 12, 8, help="Щільність центру")
        
        st.markdown("---")
        # Група 2: Психологія
        E = st.slider("Впевненість", 0, 10, 5, help="Гострота пелюсток")
        T = st.slider("Енергія", 1, 10, 5, help="Кількість променів та розмір точок!")
        
        st.markdown("---")
        # Група 3: Стиль
        G = st.radio("Стать", options=[1, -1], format_func=lambda x: "Чоловіча" if x == 1 else "Жіноча")
        # Темперамент тепер ВПЛИВАЄ СИЛЬНО
        temp = st.selectbox("Темперамент", options=["Сангвінік", "Холерик", "Флегматик", "Меланхолік"])
        eye_choice = st.selectbox("Колір очей", options=[1, 2, 3, 4], 
                                  format_func=lambda x: {1:"Блакитні", 2:"Зелені", 3:"Карі", 4:"Янтарні"}[x])

    # ГЕНЕРАЦІЯ
    def generate_mandala():
        # Агресивніші налаштування стилів
        style_map = {
            "Сангвінік": {"lw": 2.0, "alpha": 0.8},
            "Холерик":   {"lw": 4.5, "alpha": 1.0}, # Холерик дуже жирний і непрозорий
            "Флегматик": {"lw": 5.0, "alpha": 0.3}, # Флегматик товстий, але прозорий
            "Меланхолік": {"lw": 1.0, "alpha": 0.7} # Меланхолік тонкий
        }
        s = style_map[temp]
        selected_cmap = {1: cm.winter, 2: cm.summer, 3: cm.autumn, 4: cm.spring}.get(eye_choice, cm.plasma)
        
        t = np.linspace(0, 2 * np.pi, 5000)
        fig = plt.figure(figsize=(8, 8), facecolor='black')
        ax = plt.subplot(111, projection='polar')
        ax.set_facecolor('black')
        
        SCALE = 0.12 
        
        # === 1. ЯДРО (СОН S) ===
        R_core = 2.0 * SCALE
        r_hole = R_core * max(0.0, 1 - (S / 12.0))
        
        ax.fill_between(t, r_hole, R_core, color=selected_cmap(0.9), alpha=s["alpha"])
        ax.plot(t, np.full_like(t, r_hole), color='white', linewidth=s["lw"]*0.3, alpha=0.5)

        # === 2. ЗІРКА (ДЕНЬ НАРОДЖЕННЯ d) ===
        R_layer2 = R_core + 0.3 * SCALE
        r_star = R_layer2 + 0.25 * SCALE * np.cos(d * t)
        ax.plot(t, r_star, color=selected_cmap(0.7), linewidth=s["lw"], alpha=s["alpha"])

        # === 3. ПЕЛЮСТКИ (МІСЯЦЬ n) ===
        R_rose_base = R_layer2 + 0.5 * SCALE
        e_val = (11 - E) / 2
        r_rose = R_rose_base + (np.abs(np.cos(n/2 * t)))**e_val * 2.5 * SCALE
        
        ax.fill(t, r_rose, color=selected_cmap(0.3), alpha=0.3)
        ax.plot(t, r_rose, color=selected_cmap(0.4), linewidth=s["lw"], alpha=s["alpha"])

        # === 4. НАСИЧЕНА СІТКА (ЕНЕРГІЯ T) ===
        max_r_rose = r_rose.max()
        r_grid_end = max_r_rose + 4.0 * SCALE 
        
        # А) РАДІАЛЬНІ ПРОМЕНІ - ТЕПЕР ВИДИМІ
        num_rays = int(T * 4) + 4 # Мінімум 4 промені
        
        for i in range(num_rays):
            angle = (2 * np.pi / num_rays) * i
            # Використовуємо s["lw"] і s["alpha"] для видимості
            ax.plot([angle, angle], [max_r_rose, r_grid_end], 
                    color=selected_cmap(0.6), 
                    linewidth=s["lw"] * 0.6, # Товщина залежить від темпераменту
                    alpha=s["alpha"] * 0.7,  # Прозорість залежить від темпераменту
                    linestyle="-") # Суцільна лінія, щоб було видно

        # Б) ПОПЕРЕЧНІ КІЛЬЦЯ
        r_ticks = np.arange(max_r_rose, r_grid_end, 0.6 * SCALE)
        for r_tick in r_ticks:
            ax.plot(t, np.full_like(t, r_tick), 
                    color=selected_cmap(0.5), 
                    linewidth=s["lw"] * 0.4, 
                    alpha=s["alpha"] * 0.5)

        # === 5. СПІРАЛІ ФЕРМА (ВІК A) - ВЕЛИКІ ТОЧКИ ===
        golden_angle = 2.39996323 
        spacing = 0.08 * SCALE 
        
        points_theta = []
        points_r = []
        colors = []
        sizes = []

        for i in range(1, A + 1):
            theta = i * golden_angle * G
            r = max_r_rose + spacing * np.sqrt(i) * 3.5
            
            points_theta.append(theta)
            points_r.append(r)
            colors.append(selected_cmap(i / A))
            
            # РОЗМІР ТОЧОК ЗБІЛЬШЕНО
            # База: 30. Плюс від Енергії (до 100). Плюс від товщини темпераменту.
            base_size = 30 + (T * 8) 
            sizes.append(base_size * (s["lw"] * 0.8)) # Холерик матиме величезні точки

        # Малюємо точки
        ax.scatter(points_theta, points_r, c=colors, s=sizes, 
                   alpha=s["alpha"], cmap=selected_cmap, edgecolors='none')

        # === 6. МЕЖА (ЗРІСТ H) ===
        border_freq = int(H / 10)
        
        max_dist = max(points_r) if points_r else r_grid_end
        r_border_base = max(r_grid_end, max_dist + 0.5 * SCALE)
        
        p_shape = 0.5 if G == 1 else 1.5
        crown = (np.abs(np.sin(border_freq * t)))**p_shape
        r_border = r_border_base + (0.8 * SCALE * crown)
        
        ax.plot(t, r_border, color=selected_cmap(0.9), 
                linewidth=s["lw"] * 1.5, # Дуже жирна межа для Холерика
                alpha=s["alpha"])

        ax.set_ylim(0, r_border_base * 1.15)
        ax.set_axis_off()
        return fig

    col1, col2 = st.columns([1, 2])
    with col2:
        fig = generate_mandala()
        st.pyplot(fig)
        
        buf = io.BytesIO()
        fig.savefig(buf, format="png", facecolor='black', dpi=300)
        st.download_button("📥 Завантажити PNG", buf.getvalue(), "mandala.png", "image/png")

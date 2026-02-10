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
    st.write("Простір нормовано. Додано полярну координатну сітку для насиченості композиції.")

    # --- 1. СОН ---
    st.subheader("1. Топологія Ядра (Сон)")
    st.latex(r"r_{hole} = R_{core} \cdot \left(1 - \frac{S}{12}\right)")

    # --- 2. ДЕНЬ НАРОДЖЕННЯ ---
    st.subheader("2. Гармонічна зірка (День народження)")
    st.latex(r"N_{star} = d")

    # --- 3. ПЕЛЮСТКИ ---
    st.subheader("3. Емоційний шар (Місяць та Впевненість)")
    st.latex(r"r_{rose} = |\cos(\frac{n}{2}\theta)|^p")

    # --- 4. ЕНЕРГЕТИЧНА СІТКА (НОВЕ) ---
    st.subheader("4. Енергетична сітка (Енергія)")
    st.write("Для створення насиченої структури введено радіальні меридіани.")
    st.write("**Енергія ($T$)** визначає кількість силових ліній (променів), що виходять з центру.")
    st.latex(r"N_{rays} = T \times 4")
    st.write("Висока енергія створює густу сітку, низька — розріджену.")

    # --- 5. СПІРАЛІ ФЕРМА ---
    st.subheader("5. Поле досвіду (Вік)")
    st.write("Точки досвіду (роки життя) накладаються поверх сітки за законом філотаксису.")
    st.latex(r"r_n = c \sqrt{n}, \quad \theta_n = n \times 137.5^\circ")

    # --- 6. ЗРІСТ ---
    st.subheader("6. Захисна межа (Зріст)")
    st.write("Зріст ($H$) визначає кількість вершин зовнішнього бар'єра.")
    st.latex(r"N_{peaks} = \frac{H}{10}")

with tab1:
    # ПАНЕЛЬ КЕРУВАННЯ
    st.sidebar.header("📋 Твої дані")
    with st.sidebar:
        # Група 1: Базові дані
        n = st.number_input("Місяць народження", 1, 12, 6)
        d = st.number_input("День народження", 1, 31, 15)
        
        H = st.slider("Зріст (см)", 100, 220, 170, help="Визначає кількість зубців на межі")
        A = st.slider("Вік", 10, 100, 45, help="Кількість точок у спіралі")
        S = st.slider("Годин сну", 0, 12, 8, help="Визначає щільність центру")
        
        st.markdown("---")
        # Група 2: Психологія
        E = st.slider("Впевненість", 0, 10, 5, help="Гострота пелюсток")
        # T тепер дуже впливове
        T = st.slider("Енергія", 1, 10, 5, help="Кількість променів та розмір точок!")
        
        st.markdown("---")
        # Група 3: Стиль
        G = st.radio("Стать", options=[1, -1], format_func=lambda x: "Чоловіча" if x == 1 else "Жіноча")
        temp = st.selectbox("Темперамент", options=["Сангвінік", "Холерик", "Флегматик", "Меланхолік"])
        eye_choice = st.selectbox("Колір очей", options=[1, 2, 3, 4], 
                                  format_func=lambda x: {1:"Блакитні", 2:"Зелені", 3:"Карі", 4:"Янтарні"}[x])

    # ГЕНЕРАЦІЯ
    def generate_mandala():
        style_map = {
            "Сангвінік": {"lw": 1.5, "alpha": 0.8},
            "Холерик":   {"lw": 2.5, "alpha": 1.0},
            "Флегматик": {"lw": 4.0, "alpha": 0.5},
            "Меланхолік": {"lw": 1.0, "alpha": 0.7}
        }
        s = style_map[temp]
        selected_cmap = {1: cm.winter, 2: cm.summer, 3: cm.autumn, 4: cm.spring}.get(eye_choice, cm.plasma)
        
        t = np.linspace(0, 2 * np.pi, 5000)
        fig = plt.figure(figsize=(8, 8), facecolor='black') # Трохи збільшив полотно
        ax = plt.subplot(111, projection='polar')
        ax.set_facecolor('black')
        
        SCALE = 0.12 
        
        # === 1. ЯДРО (СОН S) ===
        R_core = 2.0 * SCALE
        r_hole = R_core * max(0.0, 1 - (S / 12.0))
        
        ax.fill_between(t, r_hole, R_core, color=selected_cmap(0.9), alpha=s["alpha"]+0.1)
        ax.plot(t, np.full_like(t, r_hole), color='white', linewidth=0.5, alpha=0.5)

        # === 2. ЗІРКА (ДЕНЬ НАРОДЖЕННЯ d) ===
        R_layer2 = R_core + 0.3 * SCALE
        r_star = R_layer2 + 0.25 * SCALE * np.cos(d * t)
        ax.plot(t, r_star, color=selected_cmap(0.7), linewidth=s["lw"]*0.8, alpha=0.8)

        # === 3. ПЕЛЮСТКИ (МІСЯЦЬ n) ===
        R_rose_base = R_layer2 + 0.5 * SCALE
        e_val = (11 - E) / 2
        r_rose = R_rose_base + (np.abs(np.cos(n/2 * t)))**e_val * 2.5 * SCALE
        
        ax.fill(t, r_rose, color=selected_cmap(0.3), alpha=0.3)
        ax.plot(t, r_rose, color=selected_cmap(0.4), linewidth=s["lw"], alpha=0.9)

        # === 4. НАСИЧЕНА СІТКА (ЕНЕРГІЯ T) - НОВЕ ===
        max_r_rose = r_rose.max()
        r_grid_end = max_r_rose + 4.0 * SCALE # Сітка йде до самого краю
        
        # А) РАДІАЛЬНІ ПРОМЕНІ (МЕРИДІАНИ)
        # Кількість променів залежить від Енергії. T=1 -> 4 промені, T=10 -> 40 променів.
        num_rays = int(T * 4) 
        
        for i in range(num_rays):
            angle = (2 * np.pi / num_rays) * i
            # Малюємо промінь від пелюсток до краю
            ax.plot([angle, angle], [max_r_rose, r_grid_end], 
                    color=selected_cmap(0.5), linewidth=0.5, alpha=0.3, linestyle=":")

        # Б) ПОПЕРЕЧНІ КІЛЬЦЯ (ОРБІТИ)
        # Просто для краси і структури, кожні 0.5 scale
        r_ticks = np.arange(max_r_rose, r_grid_end, 0.5 * SCALE)
        for r_tick in r_ticks:
            ax.plot(t, np.full_like(t, r_tick), 
                    color=selected_cmap(0.5), linewidth=0.5, alpha=0.2)

        # === 5. СПІРАЛІ ФЕРМА (ВІК A) ===
        golden_angle = 2.39996323 
        
        # Розширюємо спіраль, щоб вона займала все поле
        # spacing тепер залежить від діаметра
        spacing = 0.08 * SCALE 
        
        points_theta = []
        points_r = []
        colors = []
        sizes = []

        for i in range(1, A + 1):
            theta = i * golden_angle * G
            r = max_r_rose + spacing * np.sqrt(i) * 3.5 # *3.5 щоб розтягнути на все коло
            
            points_theta.append(theta)
            points_r.append(r)
            
            colors.append(selected_cmap(i / A))
            
            # Розмір точок залежить від ЕНЕРГІЇ T (більше енергії = "жирніші" точки)
            # і від віку (чим далі, тим більші)
            base_size = 10 + (T * 3) 
            sizes.append(base_size + (i / A) * 20)

        # Малюємо точки
        ax.scatter(points_theta, points_r, c=colors, s=sizes, alpha=0.9, cmap=selected_cmap, edgecolors='black', linewidth=0.5)

        # === 6. МЕЖА (ЗРІСТ H) ===
        border_freq = int(H / 10)
        
        # Межа охоплює всю конструкцію
        # Знаходимо найдальшу точку або беремо фікс
        max_dist = max(points_r) if points_r else r_grid_end
        r_border_base = max(r_grid_end, max_dist + 0.5 * SCALE)
        
        p_shape = 0.5 if G == 1 else 1.5
        crown = (np.abs(np.sin(border_freq * t)))**p_shape
        r_border = r_border_base + (0.8 * SCALE * crown)
        
        ax.plot(t, r_border, color=selected_cmap(0.9), linewidth=s["lw"]*1.5)

        # Фіксація
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

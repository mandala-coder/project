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
    st.write("Простір нормовано до фіксованого масштабу ($R \\approx 1.5$). Всі мандали мають однаковий розмір.")

    # --- 1. СОН ---
    st.subheader("1. Топологія Ядра (Сон)")
    st.latex(r"r_{hole} = R_{core} \cdot \left(1 - \frac{S}{12}\right)")

    # --- 2. ДЕНЬ НАРОДЖЕННЯ ---
    st.subheader("2. Гармонічна зірка (День народження)")
    st.latex(r"N_{star} = d")

    # --- 3. ПЕЛЮСТКИ ---
    st.subheader("3. Емоційний шар (Місяць та Впевненість)")
    st.latex(r"r_{rose} = |\cos(\frac{n}{2}\theta)|^p")

    # --- 4. СПІРАЛІ (НОВА МОДЕЛЬ) ---
    st.subheader("4. Поле життєвого шляху (Вік та Енергія)")
    st.write("Використовується модель **Спіралі Ферма** (філотаксис), що імітує природні патерни росту (наприклад, розташування насіння соняшника).")
    st.write("* **Вік ($A$):** Точна кількість точок ('подій') у полі.")
    st.write("* **Енергія ($T$):** Визначає щільність пакування. Висока енергія створює густе, насичене поле.")
    st.latex(r"r_n = c \cdot \sqrt{n}, \quad \theta_n = n \cdot 137.5^\circ")
    st.write("Де $n$ — номер року життя, а $137.5^\circ$ — золотий кут.")

    # --- 5. ЗРІСТ ---
    st.subheader("5. Захисна межа (Зріст)")
    st.write("Кількість зубців межі.")
    st.latex(r"N_{peaks} = \frac{H}{10}")

    # --- 6. ТЕМПЕРАМЕНТ ---
    st.subheader("6. Темперамент")
    st.write("Визначає стиль (товщина ліній, прозорість).")

with tab1:
    # ПАНЕЛЬ КЕРУВАННЯ
    st.sidebar.header("📋 Твої дані")
    with st.sidebar:
        # Група 1: Базові дані
        n = st.number_input("Місяць народження", 1, 12, 6)
        d = st.number_input("День народження", 1, 31, 15)
        
        H = st.slider("Зріст (см)", 100, 220, 170, help="Визначає кількість зубців на межі")
        A = st.slider("Вік", 10, 100, 45, help="Кількість точок у спіральному полі")
        S = st.slider("Годин сну", 0, 12, 8, help="Визначає щільність центру")
        
        st.markdown("---")
        # Група 2: Психологія
        E = st.slider("Впевненість", 0, 10, 5, help="Гострота пелюсток")
        T = st.slider("Енергія", 1, 10, 5, help="Щільність пакування спіралі")
        
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
        
        t = np.linspace(0, 2 * np.pi, 4000)
        fig = plt.figure(figsize=(6, 6), facecolor='black')
        ax = plt.subplot(111, projection='polar')
        ax.set_facecolor('black')
        
        SCALE = 0.12 # Глобальний масштаб
        
        # === 1. ЯДРО (СОН S) ===
        R_core = 2.0 * SCALE
        r_hole = R_core * max(0.0, 1 - (S / 12.0))
        
        ax.fill_between(t, r_hole, R_core, color=selected_cmap(0.9), alpha=s["alpha"]+0.1)
        ax.plot(t, np.full_like(t, r_hole), color='white', linewidth=0.5, alpha=0.5)

        # === 2. ЗІРКА (ДЕНЬ НАРОДЖЕННЯ d) ===
        R_layer2 = R_core + 0.3 * SCALE
        r_star = R_layer2 + 0.25 * SCALE * np.cos(d * t)
        ax.plot(t, r_star, color=selected_cmap(0.7), linewidth=s["lw"]*0.8, alpha=0.8)

        # === 3. ПЕЛЮСТКИ (МІСЯЦЬ n, ВПЕВНЕНІСТЬ E) ===
        R_rose_base = R_layer2 + 0.5 * SCALE
        e_val = (11 - E) / 2
        r_rose = R_rose_base + (np.abs(np.cos(n/2 * t)))**e_val * 2.5 * SCALE
        
        ax.fill(t, r_rose, color=selected_cmap(0.3), alpha=0.3)
        ax.plot(t, r_rose, color=selected_cmap(0.4), linewidth=s["lw"], alpha=0.9)

        # === 4. СПІРАЛІ ФЕРМА (ВІК A, ЕНЕРГІЯ T, СТАТЬ G) ===
        # НОВА ЛОГІКА: Малюємо точки, а не лінії.
        max_r_rose = r_rose.max()
        
        # Золотий кут в радіанах
        golden_angle = 2.39996323 
        
        # Щільність пакування залежить від Енергії T.
        # T=1 -> рідко (великий spacing), T=10 -> густо (малий spacing)
        spacing = (12 - T) * 0.008 * SCALE
        
        points_theta = []
        points_r = []
        colors = []
        sizes = []

        for i in range(1, A + 1):
            # Кут: номер точки * золотий кут * напрямок (стать)
            theta = i * golden_angle * G
            # Радіус: корінь з номера точки (властивість спіралі Ферма)
            r = max_r_rose + spacing * np.sqrt(i)
            
            points_theta.append(theta)
            points_r.append(r)
            
            # Колір змінюється від центру до краю
            colors.append(selected_cmap(i / A))
            # Розмір точки трохи росте
            sizes.append(10 + (i / A) * 15 * (s["lw"]/2))

        # Малюємо поле точок (scatter plot)
        ax.scatter(points_theta, points_r, c=colors, s=sizes, alpha=s["alpha"], cmap=selected_cmap, edgecolors='none')

        # === 5. МЕЖА (ЗРІСТ H, СТАТЬ G) ===
        border_freq = int(H / 10)
        
        # Межа має бути далі за найдальшу точку спіралі
        max_spiral_r = max(points_r) if points_r else max_r_rose
        r_border_base = max_spiral_r + 1.5 * SCALE
        
        p_shape = 0.5 if G == 1 else 1.5
        
        crown = (np.abs(np.sin(border_freq * t)))**p_shape
        r_border = r_border_base + (0.8 * SCALE * crown)
        
        ax.plot(t, r_border, color=selected_cmap(0.9), linewidth=s["lw"]*1.5)

        # Фіксація
        ax.set_ylim(0, 1.5)
        ax.set_axis_off()
        return fig

    col1, col2 = st.columns([1, 2])
    with col2:
        fig = generate_mandala()
        st.pyplot(fig)
        
        buf = io.BytesIO()
        fig.savefig(buf, format="png", facecolor='black', dpi=300)
        st.download_button("📥 Завантажити PNG", buf.getvalue(), "mandala.png", "image/png")

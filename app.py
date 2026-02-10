import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import io
import time  # Додали бібліотеку для пауз в анімації

# 1. НАЛАШТУВАННЯ СТОРІНКИ
st.set_page_config(page_title="Мандала особистості", layout="wide")

st.title("🎨 Цифрова мандала особистості")
st.write("### Математично-мистецький проєкт. Візуалізація біометричних даних")
st.markdown("---")

# 2. ПАНЕЛЬ КЕРУВАННЯ (SIDEBAR)
st.sidebar.header("📋 Твої дані")
with st.sidebar:
    # Група 1: Базові дані
    n = st.number_input("Місяць народження", 1, 12, 6)
    d = st.number_input("День народження", 1, 31, 15)
    
    H = st.slider("Зріст (см)", 100, 220, 170)
    A = st.slider("Вік", 10, 100, 45)
    S = st.slider("Годин сну", 0, 12, 8)
    
    st.markdown("---")
    # Група 2: Психологія
    E = st.slider("Впевненість", 0, 10, 5)
    T = st.slider("Енергія", 1, 10, 5)
    
    st.markdown("---")
    # Група 3: Стиль
    G = st.radio("Стать", options=[1, -1], format_func=lambda x: "Чоловіча" if x == 1 else "Жіноча")
    temp = st.selectbox("Темперамент", options=["Сангвінік", "Холерик", "Флегматик", "Меланхолік"])
    eye_choice = st.selectbox("Колір очей", options=[1, 2, 3, 4], 
                              format_func=lambda x: {1:"Блакитні", 2:"Зелені", 3:"Карі", 4:"Янтарні"}[x])

# 3. ФУНКЦІЯ ГЕНЕРАЦІЇ (Оновлена з фазою руху)
def generate_mandala(phase=0):
    # Налаштування стилів
    style_map = {
        "Сангвінік": {"lw": 2.0, "alpha": 0.8},
        "Холерик":   {"lw": 4.5, "alpha": 1.0},
        "Флегматик": {"lw": 5.0, "alpha": 0.3},
        "Меланхолік": {"lw": 1.0, "alpha": 0.7}
    }
    s = style_map[temp]
    selected_cmap = {1: cm.winter, 2: cm.summer, 3: cm.autumn, 4: cm.spring}.get(eye_choice, cm.plasma)
    
    # Створюємо фігуру
    fig = plt.figure(figsize=(8, 8), facecolor='black')
    ax = plt.subplot(111, projection='polar')
    ax.set_facecolor('black')
    
    # Константи
    t = np.linspace(0, 2 * np.pi, 5000)
    SCALE = 0.12 
    
    # === ДИНАМІКА ===
    # breath змінюється від 0.95 до 1.05 (ефект пульсації)
    breath = 1.0 + 0.05 * np.sin(phase)
    
    # === 1. ЯДРО (СОН S) ===
    R_core = 2.0 * SCALE * breath # Пульсує
    r_hole = R_core * max(0.0, 1 - (S / 12.0))
    
    ax.fill_between(t, r_hole, R_core, color=selected_cmap(0.9), alpha=s["alpha"])
    ax.plot(t, np.full_like(t, r_hole), color='white', linewidth=s["lw"]*0.3, alpha=0.5)

    # === 2. ЗІРКА (ДЕНЬ НАРОДЖЕННЯ d) ===
    R_layer2 = R_core + 0.3 * SCALE
    # Обертається (+ phase/20)
    r_star = R_layer2 + 0.25 * SCALE * np.cos(d * (t + phase/20))
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
    
    # Радіальні промені
    num_rays = int(T * 4) + 4
    for i in range(num_rays):
        angle = (2 * np.pi / num_rays) * i + (phase / 50) # Промені теж повільно крутяться
        ax.plot([angle, angle], [max_r_rose, r_grid_end], 
                color=selected_cmap(0.6), 
                linewidth=s["lw"] * 0.6, 
                alpha=s["alpha"] * 0.7,  
                linestyle="-")

    # Поперечні кільця
    r_ticks = np.arange(max_r_rose, r_grid_end, 0.6 * SCALE)
    for r_tick in r_ticks:
        ax.plot(t, np.full_like(t, r_tick), 
                color=selected_cmap(0.5), 
                linewidth=s["lw"] * 0.4, 
                alpha=s["alpha"] * 0.5)

    # === 5. СПІРАЛІ ФЕРМА (ВІК A) ===
    golden_angle = 2.39996323 
    spacing = 0.08 * SCALE 
    
    points_theta = []
    points_r = []
    colors = []
    sizes = []

    for i in range(1, A + 1):
        theta = i * golden_angle * G + (phase / 100) # Точки ледь зміщуються
        r = max_r_rose + spacing * np.sqrt(i) * 3.5
        
        points_theta.append(theta)
        points_r.append(r)
        colors.append(selected_cmap(i / A))
        
        base_size = 30 + (T * 8) 
        sizes.append(base_size * (s["lw"] * 0.8)) 

    ax.scatter(points_theta, points_r, c=colors, s=sizes, 
               alpha=s["alpha"], cmap=selected_cmap, edgecolors='none')

    # === 6. МЕЖА (ЗРІСТ H) ===
    border_freq = int(H / 10)
    
    max_dist = max(points_r) if points_r else r_grid_end
    r_border_base = max(r_grid_end, max_dist + 0.5 * SCALE)
    
    p_shape = 0.5 if G == 1 else 1.5
    # Межа "дихає" в протифазі до ядра
    crown = (np.abs(np.sin(border_freq * t)))**p_shape
    r_border = r_border_base + (0.8 * SCALE * crown * breath)
    
    ax.plot(t, r_border, color=selected_cmap(0.9), 
            linewidth=s["lw"] * 1.5,
            alpha=s["alpha"])

    # Фіксація (Дуже важливо для анімації!)
    ax.set_ylim(0, 3.5) 
    ax.set_axis_off()
    
    return fig

# 4. ВІДОБРАЖЕННЯ (ВКЛАДКИ)
tab1, tab2 = st.tabs(["🚀 Генератор мандали", "📜 Математичне обґрунтування"])

with tab1:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.write("#### Керування")
        st.write("Натисніть галочку, щоб оживити мандалу:")
        run_anim = st.checkbox("🌀 Увімкнути 'Дихання'", value=False)
        
        if not run_anim:
            st.info("Увімкніть анімацію, щоб побачити пульсацію ядра та рух зірок.")
            
            # Кнопка скачування (доступна лише коли анімація вимкнена, щоб не глючило)
            fig_static = generate_mandala(phase=0)
            buf = io.BytesIO()
            fig_static.savefig(buf, format="png", facecolor='black', dpi=300)
            st.download_button("📥 Завантажити PNG", buf.getvalue(), "mandala.png", "image/png")
            plt.close(fig_static)

    with col2:
        placeholder = st.empty()
        
        if run_anim:
            # Цикл анімації
            # Ми робимо 200 кадрів, щоб не перевантажити браузер вічним циклом
            for i in range(200):
                fig = generate_mandala(phase=i * 0.2)
                placeholder.pyplot(fig)
                plt.close(fig) # Обов'язково закриваємо, щоб звільнити пам'ять
                time.sleep(0.05)
        else:
            # Статичний вигляд
            fig = generate_mandala(phase=0)
            placeholder.pyplot(fig)
            plt.close(fig)

with tab2:
    st.header("Математична декомпозиція моделі")
    st.write("""
    Проєкт базується на побудові багатошарової графічної системи в полярних координатах $(r, \\theta)$. 
    Кожен шар є графіком функції, параметри якої визначаються вхідними даними користувача.
    """)
    # (Тут можна залишити ваші формули з попередньої версії)
    st.write("Див. попередню версію для повного списку формул.")

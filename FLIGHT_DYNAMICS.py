import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
from matplotlib.transforms import Affine2D
import numpy as np
from PIL import Image
import os



def descomposicion_velocidades (theta,u, v, w):
    alpha = np.degrees(math.atan(w/u))
    gamma = alpha - theta
    V = math.sqrt(u**2 + v**2 + w**2)
    beta=np.degrees(math.asin(v/V))
    vector_velocidades = [[u],
                          [v],
                          [w]]
    return (w, v, u, alpha, gamma, vector_velocidades,beta)
def yaw_move (zhi):
    zi = np.radians(zhi)
    yaw = np.array([[np.cos(zi), (np.sin(zi)),       0       ],
                   [-np.sin(zi),    np.cos(zi),       0       ],
                   [    0,                0,           1       ]])
    return (yaw)
def pitch_move(theta):
    teta = np.radians(theta)
    pitch = np.array([[np.cos(teta),      0,   -(np.sin(teta))],
                     [     0,             1,           0       ],
                     [np.sin(teta),      0,      np.cos(teta)]])
    return (pitch)
def roll_move (phi):
    pi = np.radians(phi)
    roll =  np.array([[     1,             0,           0       ],
                     [     0,        np.cos(pi), np.sin(pi)  ],
                     [     0,     -(np.sin(pi)), np.cos(pi)  ]])
    return (roll)
def multiplicacion_matricial (matriz1, matriz2):
    filas1 = len(matriz1)
    columnas1 = len(matriz1[0])
    columnas2 = len(matriz2[0])
    matrizr = np.zeros((filas1,columnas2))
    #multiplicacion matricial
    for i in range (filas1):
        for l in range (columnas2):
            for k in range (columnas1):
                matrizr[i][l] += matriz1[i][k]*matriz2[k][l]
    return (matrizr)
def matriz_transpuesta (matriz1):
    matrix_inverted= np.array(matriz1).T
    return (matrix_inverted)


def ejercicio_flight (zhi, theta, phi, u, v, w):
    (w, v, u, alpha, gamma, vector_velocidades,beta) = descomposicion_velocidades (theta, u, v,w)
    roll = roll_move (phi)
    pitch = pitch_move (theta)
    yaw = yaw_move (zhi)
    pitch_roll = multiplicacion_matricial(roll, pitch)
    yaw_pitch_roll = multiplicacion_matricial(pitch_roll, yaw)
    matriz_inversa = matriz_transpuesta(yaw_pitch_roll)
    velocidades_NED = multiplicacion_matricial(matriz_inversa, vector_velocidades)
    return vector_velocidades, velocidades_NED, alpha, beta, gamma


def marco(ax):
    ax.set_aspect('equal')
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(-2.2, 2.2)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(1.8)


# =========================
# FUNCION PARA COLOCAR IMAGEN PEQUEÑA CENTRADA Y ROTADA
# =========================
def poner_imagen(ax, img_file, angulo_deg, zoom=0.4, sentido="horario"):
    img = Image.open(img_file).convert("RGBA")  # fondo transparente
    w, h = img.size
    img_small = img.resize((int(w*zoom), int(h*zoom)), resample=Image.Resampling.LANCZOS)

    # Determina rotación según sentido
    if sentido == "horario":
        angulo_rot = -angulo_deg
    else:
        angulo_rot = angulo_deg  # antihorario

    extent = [-0.7, 0.7, -0.7, 0.7]
    ax.imshow(img_small, extent=extent, transform=Affine2D().rotate_deg(angulo_rot) + ax.transData, zorder=0)

def graficar(yaw_deg,pitch_deg,roll_deg):
    yaw   = np.deg2rad(yaw_deg)
    pitch = np.deg2rad(pitch_deg)
    roll  = np.deg2rad(roll_deg)

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    verde = "green"
    
    # =====================================================
    # YAW – plano XY
    # =====================================================
    ax = axes[0]
    marco(ax)
    ax.set_title("Yaw – plano XY")

    # Ejes
    ax.arrow(0, 0, 0, 1.8, head_width=0.08, fc='black', zorder=1)
    ax.arrow(0, 0, 0, -1.8, head_width=0.08, fc='black', zorder=1)
    ax.arrow(0, 0, 1.8, 0, head_width=0.08, fc='black', zorder=1)
    ax.arrow(0, 0, -1.8, 0, head_width=0.08, fc='black', zorder=1)

    ax.text(-0.25, 1.95, "X+", color=verde, fontweight='bold', zorder=2)
    ax.text(-0.25, -2.05, "X-", color=verde, zorder=2)
    ax.text(1.9, -0.2, "Y+", color=verde, fontweight='bold', zorder=2)
    ax.text(-2.1, -0.2, "Y-", color=verde, zorder=2)

    # Vector de yaw
    x = 1.4 * np.sin(yaw)
    y = 1.4 * np.cos(yaw)
    ax.arrow(0, 0, x, y, head_width=0.07, fc='purple', ec='purple', linewidth=2.5, zorder=3)
    ax.text(x*1.1, y*1.1, f"Después de yaw\n({yaw_deg:+.0f}°)", fontweight='bold', zorder=4)

    # Arco de yaw
    theta_ini = 90
    theta_fin = 90 - yaw_deg
    arc = Arc((0, 0), 1.1, 1.1, theta1=min(theta_ini, theta_fin),
            theta2=max(theta_ini, theta_fin), color='purple', linewidth=2, zorder=3)
    ax.add_patch(arc)

    # Imagen central
    poner_imagen(ax, "yawp.jpeg", yaw_deg, sentido="horario")

    # =====================================================
    # PITCH – plano XZ
    # =====================================================
    ax = axes[1]
    marco(ax)
    ax.set_title("Pitch – plano XZ")

    # Ejes
    ax.arrow(0, 0, 1.8, 0, head_width=0.08, fc='black', zorder=1)
    ax.arrow(0, 0, -1.8, 0, head_width=0.08, fc='black', zorder=1)
    ax.arrow(0, 0, 0, 1.8, head_width=0.08, fc='black', zorder=1)
    ax.arrow(0, 0, 0, -1.8, head_width=0.08, fc='black', zorder=1)

    ax.text(1.9, -0.2, "X+", color=verde, fontweight='bold', zorder=2)
    ax.text(-2.1, -0.2, "X-", color=verde, zorder=2)
    ax.text(-0.35, 1.95, "Z-", color=verde, fontweight='bold', zorder=2)
    ax.text(-0.35, -2.05, "Z+", color=verde, zorder=2)

    # Vector de pitch
    x = 1.4 * np.cos(pitch)
    z = 1.4 * np.sin(pitch)
    ax.arrow(0, 0, x, z, head_width=0.07, fc='red', ec='red', linewidth=2.5, zorder=3)
    ax.text(x*1.05, z*1.05, f"Después de pitch\n({pitch_deg:+.0f}°)", fontweight='bold', zorder=4)

    # Arco de pitch
    arc = Arc((0, 0), 1.1, 1.1, theta1=min(0, pitch_deg), theta2=max(0, pitch_deg),
            color='red', linewidth=2, zorder=3)
    ax.add_patch(arc)

    # Imagen central
    poner_imagen(ax, "pitchp.jpeg", pitch_deg, sentido="antihorario")

    # =====================================================
    # ROLL – plano YZ
    # =====================================================
    ax = axes[2]
    marco(ax)
    ax.set_title("Roll – plano YZ")

    # Ejes
    ax.arrow(0, 0, 1.8, 0, head_width=0.08, fc='black', zorder=1)
    ax.arrow(0, 0, -1.8, 0, head_width=0.08, fc='black', zorder=1)
    ax.arrow(0, 0, 0, 1.8, head_width=0.08, fc='black', zorder=1)
    ax.arrow(0, 0, 0, -1.8, head_width=0.08, fc='black', zorder=1)

    ax.text(-2.1, -0.2, "Y+", color=verde, fontweight='bold', zorder=2)
    ax.text(1.9, -0.2, "Y-", color=verde, zorder=2)
    ax.text(-0.35, -2.05, "Z+", color=verde, zorder=2)
    ax.text(-0.35, 1.95, "Z-", color=verde, fontweight='bold', zorder=2)

    # Vector de roll
    y = -1.4 * np.cos(roll)
    z = -1.4 * np.sin(roll)
    ax.arrow(0, 0, y, z, head_width=0.07, fc='blue', ec='blue', linewidth=2.5, zorder=3)
    ax.text(y*1.05, z*1.05, f"Después de roll\n({roll_deg:+.0f}°)", fontweight='bold', zorder=4)

    # Arco de roll
    arc = Arc((0, 0), 1.1, 1.1, theta1=min(180, 180 + roll_deg),
            theta2=max(180, 180 + roll_deg), color='blue', linewidth=2, zorder=3)
    ax.add_patch(arc)

    # Imagen central
    poner_imagen(ax, "rollp.jpeg", roll_deg, sentido="antihorario")

    plt.tight_layout()
    plt.show()
# =========================
# FUNCION PARA COLOCAR IMAGEN CENTRADA
# =========================
def poner_imagen_centrada(ax, img_file):
    img = Image.open(img_file).convert("RGBA")
    extent = [-1.1, 1.1, -1.1, 1.1]  # tamaño grande
    ax.imshow(img, extent=extent, zorder=0)

# =========================
# FUNCION PARA DIBUJAR AGUJA TRIANGULAR CON PUNTA MÁS GORDITA
# =========================
def dibujar_aguja(ax, angulo_rad, largo=1.04, ancho_base=0.15, punta_ancho=0.03):
    """
    Triángulo con punta ligeramente más ancha.
    - angulo_rad: rotación de la aguja
    - largo: longitud total de la aguja
    - ancho_base: ancho de la base trasera
    - punta_ancho: ancho en la punta
    """
    # Definir triángulo (punta más ancha que antes)
    x_tri = np.array([-punta_ancho/2, punta_ancho/2, ancho_base/2, -ancho_base/2])
    y_tri = np.array([largo, largo, 0, 0])
    
    # Rotación según yaw (horaria para ángulos positivos)
    R = np.array([[np.cos(-angulo_rad), -np.sin(-angulo_rad)],
                  [np.sin(-angulo_rad),  np.cos(-angulo_rad)]])
    puntos_rotados = R @ np.vstack([x_tri, y_tri])
    
    ax.fill(puntos_rotados[0], puntos_rotados[1], color='red', zorder=1)

def heading (yaw_deg):
    yaw = np.deg2rad(yaw_deg)
    # =========================
    # CREAR FIGURA Y EJE
    # =========================
    fig, ax = plt.subplots(figsize=(6,6))
    ax.set_aspect('equal')
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(-2.2, 2.2)
    ax.axis('off')  # sin ejes visibles
    plt.title("Heading Indicator", fontsize=16, fontweight='bold')
    
    poner_imagen_centrada(ax, "hi.jpeg")
    
    # =========================
    # DIBUJAR LA AGUJA
    # =========================
    dibujar_aguja(ax, yaw)

    plt.show()


# =========================
# FUNCIONES AUXILIARES
def pitch_transform(theta):
    """
    Transformación básica de pitch para mover el avioncito
    Conserva signo: positivo → sube, negativo → baja
    """
    theta = abs(theta)
    if 0 <= theta <= 90:
        return theta
    elif 91 <= theta <= 180:
        return 180 - theta
    elif 181 <= theta <= 270:
        return -(theta - 180)
    elif 271 <= theta <= 360:
        return -(360 - theta)
    else:
        return 0

# =========================
# FUNCIONES DE DIBUJO
def dibujar_aguja_triangulo(ax, largo=0.7):
    punta_x = [-0.01/2, 0, 0.01/2]
    punta_y = [0, largo, 0]
    ax.fill(punta_x, punta_y, color='red', zorder=2)
    ax.plot([0,0], [0,largo], color='red', linewidth=6, solid_capstyle='round', zorder=2)

def dibujar_avion_perpendicular(ax, largo=0.5, punta=0.05):
    x = np.array([-largo/2, largo/2])
    y = np.array([0, 0])
    ax.plot(x, y, color='blue', linewidth=3, solid_capstyle='round', zorder=3)
    punta_x = [-punta/2, 0, punta/2]
    punta_y = [0, punta, 0]
    ax.fill(punta_x, punta_y, color='blue', zorder=3)

def dibujar_avion_horizontal(ax, desplazamiento, largo=1.3, punta=0.08):
    x = np.array([-largo/2, largo/2])
    y = np.array([0,0]) + desplazamiento
    ax.plot(x, y, color='blue', linewidth=4, solid_capstyle='round', zorder=1)
    ax.plot([0,-punta/2],[desplazamiento,desplazamiento+punta], color='blue', linewidth=3, zorder=1)
    ax.plot([0,punta/2],[desplazamiento,desplazamiento+punta], color='blue', linewidth=3, zorder=1)

# =========================
# LÓGICA FINAL DE VUELO INVERTIDO
def esta_invertido(pitch, roll):
    pitch_invertido = (91 <= pitch <= 270) or (-270 <= pitch <= -91)
    pitch_recto = not pitch_invertido
    roll_rango = (91 <= roll <= 270) or (-270 <= roll <= -91)

    if pitch_invertido and not roll_rango:
        return True
    elif pitch_recto and roll_rango:
        return True
    else:
        return False

def horizonte(pitch_deg,angle_deg):
    # =========================
    # RUTA DE IMAGEN
    img_path = "ha.jpeg"
    if not os.path.exists(img_path):
        raise FileNotFoundError(f"No se encuentra la imagen '{img_path}'.")

    # =========================
    # CARGAR IMAGEN
    img_original = Image.open(img_path).convert("RGBA")  # Convertir a RGBA

    # =========================
    # ELIMINAR FONDO BLANCO PARA ROLL
    img_data = img_original.getdata()
    new_data = []
    for item in img_data:
        if item[0] > 240 and item[1] > 240 and item[2] > 240:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
    img_roll = img_original.copy()
    img_roll.putdata(new_data)


    # Aplicar signo
    pitch_disp = pitch_transform(abs(pitch_deg))
    if pitch_deg < 0:
        pitch_disp = -pitch_disp

    # =========================
    # ROTAR IMAGEN PARA ROLL
    img_rotated = img_roll.rotate(angle_deg, resample=Image.BICUBIC, expand=True)



    invertido = esta_invertido(pitch_deg, angle_deg)
    if invertido:
        mensaje = f"¡Vuelo invertido!\nPitch: {pitch_deg:.1f}°"
    else:
        mensaje = f"Pitch: {pitch_deg:.1f}°"

    # =========================
    # CREAR FIGURA CON DOS SUBPLOTS (PITCH IZQUIERDA, ROLL DERECHA)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12,6))

    # --- PITCH (IZQUIERDA) ---
    ax1.set_aspect('equal')
    ax1.set_xlim(-1,1)
    ax1.set_ylim(-1,1)
    ax1.axis('off')
    ax1.imshow(img_original, extent=[-1.6,1.6,-1.6,1.6], zorder=0)

    # ====== DESPLAZAMIENTO DEL AVIONCITO SEGÚN PITCH ======
    # Escalamos para que el avioncito suba o baje según el signo
    desplazamiento = pitch_disp / 90.0  # 90° = 1 unidad
    desplazamiento = np.clip(desplazamiento, -1.0, 1.0)  # limitar a límites de la gráfica
    dibujar_avion_horizontal(ax1, desplazamiento)
    # ======================================================

    bbox_props = dict(boxstyle="round,pad=0.4", fc="red", ec="black", alpha=0.8)
    ax1.text(0.95, 0.95, mensaje, ha='right', va='top', fontsize=12,
            color='white', fontweight='bold', bbox=bbox_props, transform=ax1.transAxes, zorder=2)
    ax1.set_title("Horizonte Artificial", fontsize=14, fontweight='bold')

    # --- ROLL (DERECHA) ---
    ax2.set_aspect('equal')
    ax2.set_xlim(-1.5,1.5)
    ax2.set_ylim(-1.5,1.5)
    ax2.axis('off')
    ax2.imshow(img_rotated, extent=[-1.4,1.4,-1.4,1.4], zorder=1)
    dibujar_aguja_triangulo(ax2, largo=0.6)
    dibujar_avion_perpendicular(ax2, largo=1, punta=0.05)
    ax2.set_title("Roll de la aeronave", fontsize=14)

    plt.tight_layout()
    plt.show()

def tabla_resultados(zhi, theta, phi, vector_body, velocidades_NED, alpha, beta, gamma):

    u = vector_body[0][0]
    v = vector_body[1][0]
    w = vector_body[2][0]

    VN = velocidades_NED[0][0]
    VE = velocidades_NED[1][0]
    VD = velocidades_NED[2][0]

    print("\n====================================================")
    print("                TABLA DE RESULTADOS")
    print("====================================================")

    print("\nANGULOS DE ROTACION")

    print(f"Yaw   (ψ) = {zhi:.2f} deg")
    print(f"Pitch (θ) = {theta:.2f} deg")
    print(f"Roll  (φ) = {phi:.2f} deg")

    print("\nVELOCIDADES BODY FRAME")

    print(f"u = {u:.3f} m/s")
    print(f"v = {v:.3f} m/s")
    print(f"w = {w:.3f} m/s")

    print("\nVELOCIDADES NED FRAME")

    print(f"VN = {VN:.3f} m/s")
    print(f"VE = {VE:.3f} m/s")
    print(f"VD = {VD:.3f} m/s")

    print("\nANGULOS AERODINAMICOS")

    print(f"Alpha (α) = {alpha:.3f} deg")
    print(f"Beta  (β) = {beta:.3f} deg")
    print(f"Gamma (γ) = {gamma:.3f} deg")

    print("====================================================\n")
    
print ("Bienvenido ingeniero al programa de simulacion de vuelo")
print ("Cual caso desea experimentar\n 1 Vuelo recto y nivelado\n 2 Vuelo ascendente o descendente\n 3 Giro en vuelo\n 4 vuelo libre")
opcion = int(input("Digite el numero del caso que desea probar >> "))
if opcion == 1:
    print("\nCASO 1: Vuelo recto nivelado")
    phi = 0
    theta = 0
    zhi = 0
    u = 50
    v = 0
    w = 0
    ejercicio_flight(zhi,theta,phi,u,v,w)
    graficar(zhi, theta, phi)
    heading (zhi)
    horizonte(theta,phi)
    vector_body, velocidades_NED, alpha, beta, gamma = ejercicio_flight(zhi,theta,phi,u,v,w)
    tabla_resultados(zhi,theta,phi,vector_body,velocidades_NED,alpha,beta,gamma)
elif opcion == 2:
    print("\nCASO 2: Ascenso")
    phi = 0
    theta = 10
    zhi = 0
    u = 45
    v = 0
    w = -8
    ejercicio_flight(zhi,theta,phi,u,v,w)
    graficar(zhi, theta, phi)
    heading (zhi)
    horizonte(theta,phi)
    vector_body, velocidades_NED, alpha, beta, gamma = ejercicio_flight(zhi,theta,phi,u,v,w)
    tabla_resultados(zhi,theta,phi,vector_body,velocidades_NED,alpha,beta,gamma)
elif opcion == 3:
    phi = 20
    theta = 0
    zhi = 30
    u = 50
    v = 5
    w = 0
    ejercicio_flight(zhi,theta,phi,u,v,w)
    graficar(zhi, theta, phi)
    heading (zhi)
    horizonte(theta,phi)
    vector_body, velocidades_NED, alpha, beta, gamma = ejercicio_flight(zhi,theta,phi,u,v,w)
    tabla_resultados(zhi,theta,phi,vector_body,velocidades_NED,alpha,beta,gamma)
elif opcion == 4:
    print ("Iniciando Mision de vuelo")
    print ("Digite las condiciones en las cuales se encuentra la aeronave, para iniciar simulacion")   
    zhi = float(input("Digite el angulo de yaw que posee la aeronave >>  "))
    theta = float(input("Digite el angulo de pitch que posee la aeronave >>  "))
    phi = float(input("Digite el angulo de roll que posee la aeronave >>  "))
    u = float(input("Ingrese la velocidad con la que se encuentra la aeronave en el eje longitudinal >>  "))
    v = float(input("Ingrese la velocidad con la que se encuentra la aeronave en el eje lateral >>  "))
    w = float(input("Ingrese la velocidad con la que se encuentra la aeronave en en el eje vertical >>  "))
    ejercicio_flight(zhi,theta,phi,u,v,w)
    graficar(zhi, theta, phi)
    heading (zhi)
    horizonte(theta,phi)
    vector_body, velocidades_NED, alpha, beta, gamma = ejercicio_flight(zhi,theta,phi,u,v,w)
    tabla_resultados(zhi,theta,phi,vector_body,velocidades_NED,alpha,beta,gamma)
else:
    print("Elija una de las opciones indicadas")
import pygame
import sys
import os

pygame.init()

# --- Configuración básica ---
fuente = pygame.font.SysFont(None, 60)
pantalla = pygame.display.set_mode((1280, 720))
fps = pygame.time.Clock()
juego = True

bloque_x = 0
bloque_y = 0
material_activo = 1  # empieza con agua seleccionado
menu_activo = 0
cargar_menu = False
cargar = ""
guardar = ""

# --- Colores ---
azul = (15, 19, 255)
negro = (0, 0, 0)

# --- Función para cargar imágenes ---
def img(n):
    return pygame.image.load(os.path.join("assets", n))

# --- Imágenes ---
agua = img("agua.png")
pasto = img("pasto.png")
arena = img("arena.png")
piedra = img("piedra.png")
nieve = img("nieve.png")

arbol_m = img("arbol_m.png")
arbol_p = img("arbol_p.png")
arbol_a = img("arbol_a.png")
arbol_r = img("arbol_r.png")
arbol_n = img("arbol_n.png")

fondo = img("fondo.png")
agua_activo = img("agua_activo.png")
pasto_activo = img("pasto_activo.png")
arena_activo = img("arena_activo.png")
piedra_activo = img("piedra_activo.png")
nieve_activo = img("nieve_activo.png")
arbol_activo = img("arbol_activo.png")

menu_configuracion = img("menu_configuracion.png")
menu_guardar = img("menu_guardar.png")
menu_cargar = img("menu_cargar.png")

# --- Mapas iniciales ---
mapa = [[1 for _ in range(40)] for _ in range(20)]  # todo agua
mapa_arboles = [[0 for _ in range(40)] for _ in range(20)]  # sin árboles

# --- Funciones de guardado y carga ---
def guardar_mapa(nombre, mapa, mapa_arboles):
    with open(nombre + ".txt", "w") as f:
        # Terrenos
        for fila in mapa:
            f.write("".join(str(b) for b in fila) + "\n")
        # Separador
        f.write("--ARBOT--\n")
        # Árboles
        for fila in mapa_arboles:
            f.write("".join(str(b) for b in fila) + "\n")

def cargar_mapa(nombre):
    mapa_c = [[1 for _ in range(40)] for _ in range(20)]
    mapa_arboles_c = [[0 for _ in range(40)] for _ in range(20)]
    try:
        with open(nombre + ".txt", "r") as f:
            lineas = f.read().splitlines()
        sep = lineas.index("--ARBOT--")
        for y, fila in enumerate(lineas[:sep]):
            for x, val in enumerate(fila):
                mapa_c[y][x] = int(val)
        for y, fila in enumerate(lineas[sep+1:]):
            for x, val in enumerate(fila):
                mapa_arboles_c[y][x] = int(val)
    except:
        pass
    return mapa_c, mapa_arboles_c

# --- Posición inicial de mouse ---
mouse_pos = (0, 0)

# --- Loop principal ---
while juego:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            juego = False
        elif event.type == pygame.KEYDOWN:
            if menu_activo == 2:  # Guardar
                if event.key == pygame.K_BACKSPACE:
                    guardar = guardar[:-1]
                elif event.key == pygame.K_RETURN:
                    guardar_mapa(guardar, mapa, mapa_arboles)
                    guardar = ""
                elif event.key == pygame.K_ESCAPE:
                    menu_activo = 0
                else:
                    guardar += event.unicode
            elif cargar_menu:  # Cargar
                if event.key == pygame.K_BACKSPACE:
                    cargar = cargar[:-1]
                elif event.key == pygame.K_RETURN:
                    mapa, mapa_arboles = cargar_mapa(cargar)
                    cargar = ""
                    cargar_menu = False
                elif event.key == pygame.K_ESCAPE:
                    menu_activo = 0
                    cargar_menu = False
                else:
                    cargar += event.unicode

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            # Materiales y árbol
            if menu_activo == 0:
                if 198 <= my <= 710:  # zona del mapa
                    bx = int(mx / 32)
                    by = int((my - 198) / 32)
                    if material_activo == 6:  # Toggle árbol
                        mapa_arboles[by][bx] = 0 if mapa_arboles[by][bx] == 1 else 1
                    else:  # Poner terreno
                        mapa[by][bx] = material_activo
                        mapa_arboles[by][bx] = 0
                elif 45 <= my <= 152:  # barra de materiales
                    # Botones de materiales (distancias según tus instrucciones)
                    botones = [
                        (32, 32 + 107),   # agua
                        (32 + 107 + 48, 32 + 107 + 48 + 107),  # pasto
                        (32 + 2*(107 + 48), 32 + 2*(107 + 48) + 107),  # arena
                        (32 + 3*(107 + 48), 32 + 3*(107 + 48) + 107),  # piedra
                        (32 + 4*(107 + 48), 32 + 4*(107 + 48) + 107),  # nieve
                        # árbol al final
                    ]
                    # Simplificación: clic sobre botón selecciona material
                    # (podés ajustar coordenadas exactas si querés)
                    if mx < 200:
                        material_activo = 1  # agua
                    elif mx < 400:
                        material_activo = 2  # pasto
                    elif mx < 600:
                        material_activo = 3  # arena
                    elif mx < 800:
                        material_activo = 4  # piedra
                    elif mx < 1000:
                        material_activo = 5  # nieve
                    else:
                        material_activo = 6  # árbol

            # Menú configuración / guardar
            if menu_activo == 1:
                if 310 <= mx <= 592:
                    if 175 <= my <= 237:
                        cargar_menu = True
                        cargar = ""
                    elif 310 <= my <= 372:
                        juego = False
                    elif 445 <= my <= 507:
                        menu_activo = 0
            if menu_activo == 2:
                if 45 <= my <= 152:
                    if 946 <= mx <= 1053:
                        menu_activo = 1
                        guardar = ""
                    elif 1113 <= mx <= 1220:
                        menu_activo = 0
                        guardar = ""

    # --- Dibujar pantalla ---
    pantalla.fill(azul)
    pantalla.blit(fondo, (0, 0))

    # Material activo
    if material_activo == 1:
        pantalla.blit(agua_activo, (60, 45))
    elif material_activo == 2:
        pantalla.blit(pasto_activo, (227, 45))
    elif material_activo == 3:
        pantalla.blit(arena_activo, (394, 45))
    elif material_activo == 4:
        pantalla.blit(piedra_activo, (561, 45))
    elif material_activo == 5:
        pantalla.blit(nieve_activo, (728, 45))
    elif material_activo == 6:
        pantalla.blit(arbol_activo, (900, 45))

    # Dibujar mapa
    for y in range(20):
        for x in range(40):
            px = x * 32
            py = y * 32 + 198
            # Terrenos
            t = mapa[y][x]
            if t == 1:
                pantalla.blit(agua, (px, py))
            elif t == 2:
                pantalla.blit(pasto, (px, py))
            elif t == 3:
                pantalla.blit(arena, (px, py))
            elif t == 4:
                pantalla.blit(piedra, (px, py))
            elif t == 5:
                pantalla.blit(nieve, (px, py))
            # Árboles
            if mapa_arboles[y][x] == 1:
                # Selecciona imagen según terreno debajo
                if t == 1:
                    pantalla.blit(arbol_m, (px, py))
                elif t == 2:
                    pantalla.blit(arbol_p, (px, py))
                elif t == 3:
                    pantalla.blit(arbol_a, (px, py))
                elif t == 4:
                    pantalla.blit(arbol_r, (px, py))
                elif t == 5:
                    pantalla.blit(arbol_n, (px, py))

    # Menús
    if menu_activo == 1:
        pantalla.blit(menu_configuracion, (200, 100))
        if cargar_menu:
            pantalla.blit(menu_cargar, (390, 250))
            texto = fuente.render(cargar, True, negro)
            rect = texto.get_rect(center=(1280//2, 421))
            pantalla.blit(texto, rect)
    if menu_activo == 2:
        pantalla.blit(menu_guardar, (390, 250))
        texto = fuente.render(guardar, True, negro)
        rect = texto.get_rect(center=(1280//2, 421))
        pantalla.blit(texto, rect)

    mouse_pos = pygame.mouse.get_pos()
    pygame.display.flip()
    fps.tick(30)

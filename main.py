import pygame

import asyncio

pygame.init()

# --- Configuración básica ---
fuente = pygame.font.SysFont(None, 60)
pantalla = pygame.display.set_mode((1280, 720))
fps = pygame.time.Clock()
juego = True

bloque_x = 0
bloque_y = 0
material_activo = 1
menu_activo = 0
cargar_menu = False
cargar = ""
guardar = ""

# --- Colores ---
azul = (15, 19, 255)
negro = (0, 0, 0)

# --- Función para cargar imágenes (compatible con Web) ---
def img(n):
    return pygame.image.load("assets/" + n)

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
mapa = [[1 for _ in range(40)] for _ in range(20)]
mapa_arboles = [[0 for _ in range(40)] for _ in range(20)]

# --- Guardado/carga 100% Web-safe ---
def guardar_mapa(nombre, mapa, mapa_arboles):
    try:
        with open(nombre + ".txt", "w") as f:
            for fila in mapa:
                f.write("".join(str(b) for b in fila) + "\n")
            f.write("--ARBOL--\n")
            for fila in mapa_arboles:
                f.write("".join(str(b) for b in fila) + "\n")
    except Exception as e:
        print("Error guardando:", e)

def cargar_mapa(nombre):
    mapa_c = [[1 for _ in range(40)] for _ in range(20)]
    mapa_arboles_c = [[0 for _ in range(40)] for _ in range(20)]
    try:
        with open(nombre + ".txt", "r") as f:
            lineas = f.read().splitlines()
        sep = lineas.index("--ARBOL--")
        for y, fila in enumerate(lineas[:sep]):
            for x, val in enumerate(fila):
                mapa_c[y][x] = int(val)
        for y, fila in enumerate(lineas[sep+1:]):
            for x, val in enumerate(fila):
                mapa_arboles_c[y][x] = int(val)
    except:
        print("No se pudo cargar el archivo.")
    return mapa_c, mapa_arboles_c

mouse_pos = (0, 0)

async def main():
    global juego, menu_activo, material_activo
    global cargar_menu, cargar, guardar
    global mapa, mapa_arboles
    while juego:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                juego = False

            elif event.type == pygame.KEYDOWN:
                if menu_activo == 2:  # Guardar
                    if event.key == pygame.K_BACKSPACE:
                        guardar = guardar[:-1]
                        menu_activo = 0
                    elif event.key == pygame.K_RETURN:
                        guardar_mapa(guardar, mapa, mapa_arboles)
                        guardar = ""
                    elif event.key == pygame.K_ESCAPE:
                        menu_activo = 0
                    else:
                        guardar += event.unicode

                elif cargar_menu:
                    if event.key == pygame.K_BACKSPACE:
                        cargar = cargar[:-1]
                    elif event.key == pygame.K_RETURN:
                        mapa, mapa_arboles = cargar_mapa(cargar)
                        cargar = ""
                        cargar_menu = False
                    elif event.key == pygame.K_ESCAPE:
                        cargar_menu = False
                        menu_activo = 0
                    else:
                        cargar += event.unicode

                # Abrir menú configuración con ESC
                elif event.key == pygame.K_ESCAPE:
                    menu_activo = 1

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                if menu_activo == 0:
                    if 198 <= my <= 710:
                        bx = mx // 32
                        by = (my - 198) // 32
                        if 0 <= bx < 40 and 0 <= by < 20:
                            if material_activo == 6:
                                mapa_arboles[by][bx] ^= 1
                            else:
                                mapa[by][bx] = material_activo
                                mapa_arboles[by][bx] = 0

                    elif 45 <= my <= 152:
                        if 34 <= mx <= 141:
                            material_activo = 1

                        elif 186 <= mx <= 293:
                            material_activo = 2

                        elif 338 <= mx <= 445:
                            material_activo = 3

                        elif 492 <= mx <= 597:
                            material_activo = 4

                        elif 646 <= mx <= 749:
                            material_activo = 5

                        elif 800 <= mx <= 901:
                            material_activo = 6

                        elif 946 <= mx <= 1053:
                            menu_activo = 1
                        
                        elif 1113 <= mx <= 1220:
                            menu_activo = 2


                if menu_activo == 1:
                    if 310 <= mx <= 592:
                        if 175 <= my <= 237:
                            cargar_menu = True
                            cargar = ""
                        elif 310 <= my <= 372:
                            juego = False
                        elif 445 <= my <= 507:
                            menu_activo = 0

        pantalla.fill(azul)
        pantalla.blit(fondo, (0, 0))

        if material_activo == 1:
            pantalla.blit(agua_activo, (34, 45))
        elif material_activo == 2:
            pantalla.blit(pasto_activo, (186, 45))
        elif material_activo == 3:
            pantalla.blit(arena_activo, (338, 45))
        elif material_activo == 4:
            pantalla.blit(piedra_activo, (490, 45))
        elif material_activo == 5:
            pantalla.blit(nieve_activo, (646, 45))
        elif material_activo == 6:
            pantalla.blit(arbol_activo, (807, 45))

        for y in range(20):
            for x in range(40):
                px = x * 32
                py = y * 32 + 198
                t = mapa[y][x]

                if t == 1: pantalla.blit(agua, (px, py))
                elif t == 2: pantalla.blit(pasto, (px, py))
                elif t == 3: pantalla.blit(arena, (px, py))
                elif t == 4: pantalla.blit(piedra, (px, py))
                elif t == 5: pantalla.blit(nieve, (px, py))

                if mapa_arboles[y][x] == 1:
                    if t == 1: pantalla.blit(arbol_m, (px, py))
                    elif t == 2: pantalla.blit(arbol_p, (px, py))
                    elif t == 3: pantalla.blit(arbol_a, (px, py))
                    elif t == 4: pantalla.blit(arbol_r, (px, py))
                    elif t == 5: pantalla.blit(arbol_n, (px, py))

        if menu_activo == 1:
            pantalla.blit(menu_configuracion, (200, 100))
            if cargar_menu:
                pantalla.blit(menu_cargar, (390, 250))
                texto = fuente.render(cargar, True, negro)
                pantalla.blit(texto, texto.get_rect(center=(640, 421)))

        if menu_activo == 2:
            pantalla.blit(menu_guardar, (390, 250))
            texto = fuente.render(guardar, True, negro)
            pantalla.blit(texto, texto.get_rect(center=(640, 421)))
        

        pygame.display.flip()
        fps.tick(30)
        await asyncio.sleep(0)

asyncio.run(main())

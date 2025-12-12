import pygame
import asyncio
import pathlib

pygame.init()
pygame.mixer.quit()
fuente = pygame.font.SysFont(None, 60)
pantalla = pygame.display.set_mode((1280, 720))
bloque_x = 0
bloque_y = 0
material_activo = 1
menu_activo = 0
cargar_menu = False
cargar = ""
guardar = ""

azul = (15, 19, 255)
negro = (0, 0, 0)

def img(n):
    path = str(pathlib.Path("assets") / n)
    return pygame.image.load(path)

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

mapa = [[1 for _ in range(40)] for _ in range(20)]
mapa_arboles = [[0 for _ in range(40)] for _ in range(20)]

def guardar_mapa(nombre, mapa, mapa_arboles):
    with open(nombre + ".txt", "w") as f:
        for fila in mapa:
            f.write("".join(str(b) for b in fila) + "\n")
        f.write("--ARBOL--\n")
        for fila in mapa_arboles:
            f.write("".join(str(b) for b in fila) + "\n")

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

async def main():
    global material_activo, menu_activo, cargar_menu, guardar, cargar
    global mapa, mapa_arboles
    juego = True
    while juego:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                juego = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_activo = 1
                elif event.key == pygame.K_RETURN:
                    if menu_activo == 2:
                        guardar_mapa(guardar, mapa, mapa_arboles)
                        guardar = ""
                        menu_activo = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                bx = mx // 32
                by = (my - 198) // 32
                if 0 <= bx < 40 and 0 <= by < 20 and menu_activo == 0:
                    if material_activo == 6:
                        mapa_arboles[by][bx] ^= 1
                    else:
                        mapa[by][bx] = material_activo
                        mapa_arboles[by][bx] = 0

        pantalla.fill(azul)
        pantalla.blit(fondo, (0, 0))
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
        pygame.display.flip()
        await asyncio.sleep(0)

asyncio.ensure_future(main())

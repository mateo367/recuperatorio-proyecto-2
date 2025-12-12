import pygame
import sys

pygame.init()

pantalla = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Editor de Mapas")
fuente = pygame.font.SysFont(None, 50)
fps = pygame.time.Clock()

AZUL = (15, 19, 255)
NEGRO = (0, 0, 0)

MATERIAL_AGUA = 1
MATERIAL_PASTO = 2
MATERIAL_ARENA = 3
MATERIAL_PIEDRA = 4
MATERIAL_NIEVE = 5
MATERIAL_ARBOL = 6

material_activo = MATERIAL_AGUA

agua = pygame.image.load("agua.png")
pasto = pygame.image.load("pasto.png")
arena = pygame.image.load("arena.png")
piedra = pygame.image.load("piedra.png")
nieve = pygame.image.load("nieve.png")

agua_a = pygame.image.load("agua_activo.png")
pasto_a = pygame.image.load("pasto_activo.png")
arena_a = pygame.image.load("arena_activo.png")
piedra_a = pygame.image.load("piedra_activo.png")
nieve_a = pygame.image.load("nieve_activo.png")

arbol_m = pygame.image.load("arbol_m.png")
arbol_p = pygame.image.load("arbol_p.png")
arbol_a = pygame.image.load("arbol_a.png")
arbol_r = pygame.image.load("arbol_r.png")
arbol_n = pygame.image.load("arbol_n.png")

mapa = [[1 for _ in range(40)] for _ in range(20)]
mapa_arboles = [[0 for _ in range(40)] for _ in range(20)]

botones = {
    MATERIAL_AGUA:  (60,  45),
    MATERIAL_PASTO: (227, 45),
    MATERIAL_ARENA: (394, 45),
    MATERIAL_PIEDRA:(561, 45),
    MATERIAL_NIEVE: (728, 45),
    MATERIAL_ARBOL: (895, 45)
}

boton_imgs = {
    MATERIAL_AGUA: agua_a,
    MATERIAL_PASTO: pasto_a,
    MATERIAL_ARENA: arena_a,
    MATERIAL_PIEDRA: piedra_a,
    MATERIAL_NIEVE: nieve_a,
    MATERIAL_ARBOL: arbol_p
}

def arbol_por_material(material_base):
    if material_base == MATERIAL_AGUA: return arbol_m
    if material_base == MATERIAL_PASTO: return arbol_p
    if material_base == MATERIAL_ARENA: return arbol_a
    if material_base == MATERIAL_PIEDRA: return arbol_r
    if material_base == MATERIAL_NIEVE: return arbol_n
    return arbol_p

juego = True
while juego:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            juego = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = mouse_pos

            for mat, pos in botones.items():
                bx, by = pos
                if bx <= x <= bx+100 and by <= y <= by+100:
                    material_activo = mat

            if 198 <= y <= 198 + 20*32:
                gx = x // 32
                gy = (y - 198) // 32

                if 0 <= gx < 40 and 0 <= gy < 20:
                    if material_activo == MATERIAL_ARBOL:
                        mapa_arboles[gy][gx] = 1
                    else:
                        mapa[gy][gx] = material_activo
                        mapa_arboles[gy][gx] = 0

    pantalla.fill(AZUL)

    for mat, pos in botones.items():
        px, py = pos
        if mat == material_activo:
            pantalla.blit(boton_imgs[mat], (px, py))
        else:
            pantalla.blit(pygame.transform.scale(boton_imgs[mat], (100,100)), (px, py))

    for fy in range(20):
        for fx in range(40):
            base = mapa[fy][fx]
            px = fx * 32
            py = fy * 32 + 198

            if base == MATERIAL_AGUA:
                pantalla.blit(agua, (px, py))
            elif base == MATERIAL_PASTO:
                pantalla.blit(pasto, (px, py))
            elif base == MATERIAL_ARENA:
                pantalla.blit(arena, (px, py))
            elif base == MATERIAL_PIEDRA:
                pantalla.blit(piedra, (px, py))
            elif base == MATERIAL_NIEVE:
                pantalla.blit(nieve, (px, py))

            if mapa_arboles[fy][fx] == 1:
                pantalla.blit(arbol_por_material(base), (px, py))

    pygame.display.flip()
    fps.tick(30)

pygame.quit()
sys.exit()

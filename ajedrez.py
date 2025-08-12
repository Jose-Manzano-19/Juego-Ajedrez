import pygame
import sys

# Inicializamos Pygame
pygame.init()

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
COLOR_TABLERO = (125, 135, 150)

# Tamaño de la pantalla
TAMANO_CELDA = 60
ANCHO = 8 * TAMANO_CELDA
ALTO = 8 * TAMANO_CELDA
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Ajedrez")

# Variables globales
turno = "blanco"  # El turno comienza con el jugador blanco

# Clases de las piezas
class Pieza(pygame.sprite.Sprite):
    def __init__(self, color, imagen, posicion, tipo):
        super().__init__()
        self.color = color
        self.tipo = tipo  # "torre", "caballo", "alfíl", "reina", "rey", "peón"
        self.image = pygame.image.load(imagen)
        self.image = pygame.transform.scale(self.image, (TAMANO_CELDA, TAMANO_CELDA))
        self.rect = self.image.get_rect()
        self.rect.topleft = posicion
        self.posicion = posicion  # Guarda la posición (fila, columna)

    def update(self):
        pass

    def obtener_posicion(self):
        return self.posicion

    def mover(self, nueva_posicion):
        self.rect.topleft = nueva_posicion
        self.posicion = (nueva_posicion[0] // TAMANO_CELDA, nueva_posicion[1] // TAMANO_CELDA)


# Función para dibujar el tablero
def dibujar_tablero():
    for fila in range(8):
        for columna in range(8):
            color = COLOR_TABLERO if (fila + columna) % 2 == 0 else (255, 255, 255)
            pygame.draw.rect(screen, color, pygame.Rect(columna * TAMANO_CELDA, fila * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA))


# Función para crear las piezas
def crear_piezas():
    piezas = pygame.sprite.Group()

    # Piezas blancas
    piezas.add(Pieza("blanco", "imagenes/torre_blanco.png", (0, 0), "torre"))
    piezas.add(Pieza("blanco", "imagenes/caballo_blanco.png", (TAMANO_CELDA, 0), "caballo"))
    piezas.add(Pieza("blanco", "imagenes/alfil_blanco.png", (2 * TAMANO_CELDA, 0), "alfíl"))
    piezas.add(Pieza("blanco", "imagenes/reina_blanco.png", (3 * TAMANO_CELDA, 0), "reina"))
    piezas.add(Pieza("blanco", "imagenes/rey_blanco.png", (4 * TAMANO_CELDA, 0), "rey"))
    piezas.add(Pieza("blanco", "imagenes/alfil_blanco.png", (5 * TAMANO_CELDA, 0), "alfíl"))
    piezas.add(Pieza("blanco", "imagenes/caballo_blanco.png", (6 * TAMANO_CELDA, 0), "caballo"))
    piezas.add(Pieza("blanco", "imagenes/torre_blanco.png", (7 * TAMANO_CELDA, 0), "torre"))

    # Peones blancos
    for i in range(8):
        piezas.add(Pieza("blanco", "imagenes/peon_blanco.png", (i * TAMANO_CELDA, TAMANO_CELDA), "peón"))

    # Piezas negras
    piezas.add(Pieza("negro", "imagenes/torre_negro.png", (0, 7 * TAMANO_CELDA), "torre"))
    piezas.add(Pieza("negro", "imagenes/caballo_negro.png", (TAMANO_CELDA, 7 * TAMANO_CELDA), "caballo"))
    piezas.add(Pieza("negro", "imagenes/alfil_negro.png", (2 * TAMANO_CELDA, 7 * TAMANO_CELDA), "alfíl"))
    piezas.add(Pieza("negro", "imagenes/reina_negro.png", (3 * TAMANO_CELDA, 7 * TAMANO_CELDA), "reina"))
    piezas.add(Pieza("negro", "imagenes/rey_negro.png", (4 * TAMANO_CELDA, 7 * TAMANO_CELDA), "rey"))
    piezas.add(Pieza("negro", "imagenes/alfil_negro.png", (5 * TAMANO_CELDA, 7 * TAMANO_CELDA), "alfíl"))
    piezas.add(Pieza("negro", "imagenes/caballo_negro.png", (6 * TAMANO_CELDA, 7 * TAMANO_CELDA), "caballo"))
    piezas.add(Pieza("negro", "imagenes/torre_negro.png", (7 * TAMANO_CELDA, 7 * TAMANO_CELDA), "torre"))

    # Peones negros
    for i in range(8):
        piezas.add(Pieza("negro", "imagenes/peon_negro.png", (i * TAMANO_CELDA, 6 * TAMANO_CELDA), "peón"))

    return piezas


# Función para verificar si una casilla está vacía
def casilla_vacia(posicion, piezas):
    for pieza in piezas:
        if pieza.obtener_posicion() == (posicion[0] // TAMANO_CELDA, posicion[1] // TAMANO_CELDA):
            return False
    return True


# Función para verificar si un jugador está en Jaque
def en_jaque(piezas, color_rey):
    rey = None
    for pieza in piezas:
        if pieza.tipo == "rey" and pieza.color == color_rey:
            rey = pieza
            break

    for pieza in piezas:
        if pieza.color != color_rey:  # Solo comprobamos las piezas del oponente
            if pieza.tipo == "torre":
                if es_movimiento_torre_valido(pieza.posicion, rey.posicion):
                    return True
            # Implementar las verificaciones para otras piezas (alfiles, caballos, etc.)

    return False


# Funciones para los movimientos válidos de cada pieza
def es_movimiento_torre_valido(posicion_inicial, posicion_final):
    fila_inicial, col_inicial = posicion_inicial
    fila_final, col_final = posicion_final
    if fila_inicial == fila_final or col_inicial == col_final:
        return True
    return False

# Función principal para ejecutar el juego
def main():
    piezas = crear_piezas()
    clock = pygame.time.Clock()
    seleccionada = None

    while True:
        screen.fill((0, 0, 0))  # Fondo negro
        dibujar_tablero()
        
        piezas.update()
        piezas.draw(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                fila, columna = x // TAMANO_CELDA, y // TAMANO_CELDA
                
                # Selección de pieza
                if seleccionada is None:
                    for pieza in piezas:
                        if pieza.rect.collidepoint(event.pos) and pieza.color == turno:
                            seleccionada = pieza
                else:
                    # Mover la pieza seleccionada
                    if casilla_vacia(event.pos, piezas):
                        seleccionada.mover((fila * TAMANO_CELDA, columna * TAMANO_CELDA))
                        seleccionada = None
                        # Cambiar turno
                        turno = "negro" if turno == "blanco" else "blanco"

        # Verificar si alguien está en jaque
        if en_jaque(piezas, "blanco"):
            print("¡Jaque al Blanco!")
        if en_jaque(piezas, "negro"):
            print("¡Jaque al Negro!")

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()

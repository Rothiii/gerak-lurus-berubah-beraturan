import random
import pygame

# Inisialisasi Pygame
class Lingkaran(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        a = random.randint(0, 255)
        b = random.randint(0, 255)
        c = random.randint(0, 255)
        radius = random.randint(10, 30)  # Radius lingkaran

        # Membuat permukaan lingkaran dengan ukuran diameter
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)

        # Menggambar lingkaran pada permukaan dengan warna putih
        pygame.draw.circle(self.image, (a,b,c), (radius, radius), radius)

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 1000)
        self.rect.y = random.randint(-50, -20)
        self.speed = random.randint(3, 9)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 600:
            self.rect.x = random.randint(0, 1000)
            self.rect.y = random.randint(-50, -20)
            self.speed = random.randint(3, 9)


import pygame
import player as playerScript
from bus import bus_left, bus_right
import random
from money import Coin, Collector
from pygame import mixer
mixer.init()
gameOver = mixer.Sound('muffled-sound-of-falling-game-character-131797.mp3')

pygame.init()

# ------------ VARIABLES ---------------------------------------------------------------------------

left_color = (255, 128, 128)
right_color = (128, 255, 255)
buses_left = []
buses_right = []
width = 600
height = 600
true_height = 700
score = 0
player = playerScript.Player(width // 2, height // 2)
coin = None
collector = None
entered_area = False
# screen variables
screen = pygame.display.set_mode((width, true_height))
pygame.display.set_caption("Game Over Screen")
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FONT_LARGE = pygame.font.Font(None, 48)
FONT_SMALL = pygame.font.Font(None, 32)

# ------------ GAME OVER ---------------------------------------------------------------------------


def game_over_screen():
    global buses_left
    global buses_right
    global score
    global player
    global collector

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Restart the game here
                    player = playerScript.Player(width // 2, height // 2)
                    score = 0
                    buses_right = []
                    buses_left = []
                    collector = Collector(width, height, true_height)
                    return  # Exit the game over screen loop and resume the game

        screen.fill(BLACK)
        game_over_text = FONT_LARGE.render("Game Over", True, WHITE)
        game_over_score = FONT_LARGE.render(
            f"Score: {score}", True, WHITE)
        restart_text = FONT_SMALL.render("Press Enter to restart", True, WHITE)
        screen.blit(game_over_text, (width/2 - game_over_text.get_width() /
                    2, height/2 - game_over_text.get_height()))
        screen.blit(game_over_score, (width/2 - game_over_score.get_width() /
                    2, height/2 - game_over_score.get_height() - 200))
        screen.blit(restart_text, (width/2 - restart_text.get_width() /
                    2, height/2 + restart_text.get_height()))
        pygame.display.flip()


def main():
    global score
    global player
    global coin
    global collector
    global entered_area
    score = 0
    player = playerScript.Player(width // 2, height // 2)
    coin = Coin(width, height, true_height, player)
    collector = Collector(width, height, true_height)
    safe_zone_left = pygame.Rect(0, height, width // 2, true_height - height)
    safe_zone_right = pygame.Rect(width // 2, 0,
                                  width, true_height - height)

    window = pygame.display.set_mode((width, true_height))
    pygame.display.set_caption("2dimensions")
    clock = pygame.time.Clock()
    running = True

    def setSpawnTime():
        if score != 0:
            if random.randint(0, int(60 * 2/(score/5))) == 0:
                buses_left.append(bus_left(width, right_color, 0))
            if random.randint(0, int(60 * 2/(score/5))) == 0:
                buses_right.append(bus_right(width, left_color, true_height))
        else:
            if random.randint(0, 60 * 2) == 0:
                buses_left.append(bus_left(width, right_color, 0))

            if random.randint(0, 60 * 2) == 0:
                buses_right.append(bus_right(width, left_color, true_height))

    def buses_left_loop():
        for bus in buses_left:
            bus.fly_down()
            bus.draw(window)

            if bus.rect.y > height:
                buses_left.remove(bus)

            if bus.rect.colliderect(player.rect):
                gameOver.play()
                game_over_screen()

    def buses_right_loop():
        for bus in buses_right:
            bus.fly_up()
            bus.draw(window)

            if bus.rect.y < true_height - height:
                buses_right.remove(bus)

            if bus.rect.colliderect(player.rect):
                gameOver.play()
                game_over_screen()

    while running:
        prev_score = score
        pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        window.fill(left_color, (0, 0, width / 2, height))

        window.fill(right_color, (width / 2,
                    true_height - height, width, height))

        pygame.gfxdraw.box(window, (0, height, width // 2,
                           (true_height - height) - 110), (4, 63, 77, 50))
        pygame.gfxdraw.box(window, (width // 2, 0,
                                    width, true_height - height + 11), (4, 63, 77, 50))

        playerScript.handle_input(player)

        setSpawnTime()
        buses_left_loop()
        buses_right_loop()

        pygame.draw.line(window, (255, 255, 255), (0, height - 2),
                         (width // 2, height - 2), 5)

        pygame.draw.line(window, (255, 255, 255), (width // 2, true_height - height + 2),
                         (width, true_height - height + 2), 5)

        pygame.draw.line(window, (4, 63, 77), (width / 2, 0),
                         (width / 2, true_height), 5)

        window.fill((4, 63, 77), safe_zone_right)

        window.fill((4, 63, 77), safe_zone_left)

        player.draw(window, playerScript.handle_color(
            player, screenSize=(width, height)))

        # check if player rect enters safe zone and only call function once until it leaves
        if entered_area == False and score > 5 and player.small == False:
            if safe_zone_left.contains(player.rect):
                player.shrink()
                score -= 5
                entered_area = True
            elif safe_zone_right.contains(player.rect):
                player.shrink()
                score -= 5
                entered_area = True

        if not player.rect.colliderect(safe_zone_left) and not player.rect.colliderect(safe_zone_right):
            entered_area = False

        if coin.check_collision(player):
            score += 1
            player.add()

        if prev_score != score:
            coin = Coin(width, height, true_height, player)

        coin.draw(window)
        collector.draw(window)

        font = pygame.font.Font(None, 32)
        text = font.render(f'{score}', True, (255, 255, 255))
        text_rect = text.get_rect(center=(collector.x, collector.y))
        window.blit(text, text_rect)

        font = pygame.font.Font(None, 32)
        text = font.render(f'SAFEZONE', True, (255, 255, 255))
        text_rect = text.get_rect(
            center=((width/2)/2, true_height - (true_height - height)/2))
        text_rect2 = text.get_rect(
            center=(width - (width/2)/2, 0 + (true_height - height)/2))

        font = pygame.font.Font(None, 20)
        text2 = font.render(
            f'minus 5 to score ', True, (255, 255, 255))
        text_rect3 = text2.get_rect(
            center=((width/2)/2, true_height - ((true_height - height)/2) + 20))
        text_rect4 = text2.get_rect(
            center=(width - (width/2)/2, 0 + ((true_height - height)/2) + 20))
        text3 = font.render(
            f'entering', True, (255, 255, 255))
        text_rect5 = text3.get_rect(
            center=((width/2)/2, true_height - ((true_height - height)/2) - 22))
        text_rect6 = text3.get_rect(
            center=(width - (width/2)/2, 0 + ((true_height - height)/2) - 22))

        window.blit(text, text_rect)
        window.blit(text, text_rect2)
        window.blit(text2, text_rect3)
        window.blit(text2, text_rect4)
        window.blit(text3, text_rect5)
        window.blit(text3, text_rect6)

        player.draw(window, playerScript.handle_color(
            player, screenSize=(width, height)))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()

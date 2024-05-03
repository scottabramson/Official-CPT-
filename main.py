import pygame as pg
import sys
from settings import *
from tilemap import *
from os import path
from button import *
from splashscreen import *
from game import *
from tilemap import *

pg.init()



# Background Animation
frames = []
for i in range(1, 23):  # Adjust the range based on your frame count
    # Load each frame image
    frame = pg.image.load(f"schoolbusgif/schoolbus{i}.jpg")
    # Scale the frame to fill the screen
    scaled_frame = pg.transform.scale(frame, (WIDTH, HEIGHT))
    # Append the scaled frame to the frames list
    frames.append(scaled_frame)

# Frame settings
current_frame = 0  # Start with the first frame
frame_count = len(frames)  # Total number of frames




def get_font(size):  # Returns Press-Start-2P in the desired size
    return pg.font.Font("assets/font.ttf", size)

def play():
    while True:  # This infinite loop will prevent `play` from ever returning
        PLAY_MOUSE_POS = pg.mouse.get_pos()
        g = Game()
        g.new()
        g.run()
        g.show_go_screen()


def options():
    while True:
        OPTIONS_MOUSE_POS = pg.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460),
                              text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pg.display.update()
def main_menu():
    print("Entered main menu")
    global current_frame

    clock = pg.time.Clock()
    while True:
        SCREEN.blit(frames[current_frame], (0, 0))
        MENU_MOUSE_POS = pg.mouse.get_pos()

        MENU_TEXT = get_font(40).render("The Bell Doesn't Dismiss You!", True, "white")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pg.image.load("menubuttons/Play Rect.png"), pos=(640, 250),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pg.image.load("menubuttons/Options Rect.png"), pos=(640, 400),
                                text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pg.image.load("menubuttons/Quit Rect.png"), pos=(640, 550),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()

                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pg.quit()
                    sys.exit()

        # Update the frame index for the next loop iteration
        current_frame = (current_frame + 1) % frame_count

        # Control the frame rate
        clock.tick(10)

        pg.display.update()

splash = splashscreen()
splash.show_start_screen()
main_menu()

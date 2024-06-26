import pygame
import random

# Αρχικοποίηση Pygame και mixer
pygame.init()
pygame.mixer.init()

# Διαστάσεις παραθύρου
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Math Master")

# Χρώματα
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Φόρτωση εικόνων
start_img = pygame.image.load('lets_start.png')
correct_img = pygame.image.load('correct.png')
incorrect_img = pygame.image.load('incorrect.png')
background_img = pygame.image.load('background.png')
help_img = pygame.image.load('help.png')
help_img = pygame.transform.scale(help_img, (50, 50))

# Κλιμάκωση της εικόνας background
background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

# Μικρότερη κλιμάκωση των εικόνων correct_img και incorrect_img
scaled_size = (int(correct_img.get_width() * 0.5), int(correct_img.get_height() * 0.5))
correct_img_small = pygame.transform.scale(correct_img, scaled_size)
incorrect_img_small = pygame.transform.scale(incorrect_img, scaled_size)

# Υπολογισμός συντεταγμένων για κεντράρισμα των εικόνων
correct_img_x = (screen_width - correct_img_small.get_width()) // 2
correct_img_y = (screen_height - correct_img_small.get_height()) // 2
incorrect_img_x = correct_img_x
incorrect_img_y = correct_img_y

# Συντεταγμένες για την εικόνα βοήθειας
help_img_x = 10
help_img_y = 10

# Ορισμός μεταβλητών κίνησης
help_img_offset = 5
help_img_direction = 1

# Φόρτωση ήχων
pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.play(-1)  # Παίζει σε loop

correct_sound = pygame.mixer.Sound('correct.mp3')
incorrect_sound = pygame.mixer.Sound('incorrect.mp3')

# Ρύθμιση γραμματοσειράς
font = pygame.font.Font(None, 74)
smallfont = pygame.font.Font(None, 36)

def show_message(message, x, y, color=black, font=smallfont):
    text = font.render(message, True, color)
    screen.blit(text, (x, y))

def show_question(question, x, y, color=black):
    text = font.render(question, True, color)
    screen.blit(text, (x, y))

def end_game_message(score):
    if score >= 80:
        return "Εξαιρετικά τα πήγες!"
    elif score >= 50:
        return "Τα πήγες καλά!"
    else:
        return "Προσπάθησε ξανά!"

running = True
game_started = False
answer_input = ""
question_generated = False
score = 0
level = 1
hints_used = 0
show_end_screen = False

def generate_question(level):
    if level == 1:
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        answer = num1 + num2
        question = f"{num1} + {num2} = ?"
    elif level == 2:
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        answer = num1 * num2
        question = f"{num1} * {num2} = ?"
    return question, answer

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not game_started:
                if event.key == pygame.K_SPACE:
                    game_started = True
            else:
                if event.key == pygame.K_RETURN:
                    if question_generated and answer_input.isdigit():
                        user_answer = int(answer_input)
                        print(f"User answer: {user_answer}, Correct answer: {answer}")  # Debugging print
                        if user_answer == answer:
                            screen.blit(correct_img_small, (correct_img_x, correct_img_y))
                            correct_sound.play()
                            pygame.display.flip()
                            pygame.time.wait(300)  # Αναμονή 0.3 δευτερολέπτου
                            score += 10  # Επιβράβευση
                            new_level = score // 50 + 1  # Υπολογισμός νέου επιπέδου
                            if new_level > level:
                                level = new_level
                                show_message("Μπράβο, πάμε στο επόμενο επίπεδο δυσκολίας", 150, 300, black)
                                pygame.display.flip()
                                pygame.time.wait(2000)  # Αναμονή 2 δευτερολέπτων
                            else:
                                pygame.display.flip()
                                pygame.time.wait(2000)  # Αναμονή 2 δευτερολέπτων
                        else:
                            screen.blit(incorrect_img_small, (incorrect_img_x, incorrect_img_y))
                            incorrect_sound.play()
                            pygame.display.flip()
                            pygame.time.wait(300)  # Αναμονή 0.3 δευτερολέπτου
                        answer_input = ""
                        question_generated = False
                        if score >= 100:  # Ολοκλήρωση του παιχνιδιού
                            game_started = False
                            show_end_screen = True
                    else:
                        question, answer = generate_question(level)
                        print(f"New question generated: {question}, Answer: {answer}")  # Debugging print
                        question_generated = True
                elif event.key == pygame.K_h:  # Παροχή υπόδειξης
                    hints_used += 1
                    show_message(f"Hint: {answer}", 300, 400, black)
                    pygame.display.flip()
                    pygame.time.wait(2000)
                elif event.key == pygame.K_BACKSPACE:
                    answer_input = answer_input[:-1]
                else:
                    answer_input += event.unicode

        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            if help_img_x <= mouse_x <= help_img_x + help_img.get_width() and help_img_y <= mouse_y <= help_img_y + help_img.get_height():
                help_img_y += help_img_offset * help_img_direction
                if help_img_y <= 5 or help_img_y >= 15:
                    help_img_direction *= -1
            else:
                help_img_y = 10  # Επαναφορά στην αρχική θέση όταν ο δείκτης δεν είναι πάνω στην εικόνα

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if help_img_x <= mouse_x <= help_img_x + help_img.get_width() and help_img_y <= mouse_y <= help_img_y + help_img.get_height():
                # Η βοήθεια έχει αφαιρεθεί, οπότε αγνοήστε αυτό το συμβάν
                pass

    if not game_started:
        screen.fill(white)
        screen.blit(start_img, (150, 100))
        show_message("Press SPACE", 320, 400)
        if show_end_screen:
            screen.fill(white)
            end_message = end_game_message(score)
            show_message(end_message, 200, 300, black, font)
            pygame.display.flip()
            pygame.time.wait(5000)  # Αναμονή 5 δευτερολέπτων πριν κλείσει το πρόγραμμα
            running = False
    else:
        screen.blit(background_img, (0, 0))
        screen.blit(help_img, (help_img_x, help_img_y))
        if question_generated:
            show_question(question, 300, 250, black)
            show_message(f" Η απάντησή σου: {answer_input}", 300, 350, black)
            show_message(f"Πόντοι: {score}", 650, 50, black)
            show_message(f"Επίπεδο: {level}", 650, 100, black)
            show_message(f"Βοήθειες: {hints_used}", 650, 150, black)
    
    pygame.display.flip()

pygame.quit()

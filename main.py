import pygame
import sys
import random


# инициализация Pygame
pygame.init()

# основные параметры игры
screen_width, screen_height = 1920, 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Подземелье AITU')

# шрифт и цвет текста
font = pygame.font.Font(None, 60)
white_color = (255, 255, 255)

# изображения для фона, включая изображение для победы и вступления
background_image = pygame.transform.scale(pygame.image.load('C:/Users/10ash/PycharmProjects/pythonProject2/photos/game_background.jpg'),(screen_width, screen_height))
background_image_for_win = pygame.transform.scale(pygame.image.load('C:/Users/10ash/PycharmProjects/pythonProject2/photos/background_image_for_win.jpeg'),(screen_width, screen_height))
intro_image = pygame.transform.scale(pygame.image.load('C:/Users/10ash/PycharmProjects/pythonProject2/photos/intro_image.jpg'),(screen_width, screen_height))
heart_image = pygame.transform.scale(pygame.image.load('C:/Users/10ash/PycharmProjects/pythonProject2/photos/heart.jpg'), (50, 50))

# звуковые эффекты
level_up_sound = pygame.mixer.Sound('C:/Users/10ash/PycharmProjects/pythonProject2/audios/new_level.wav')
lose_life_sound = pygame.mixer.Sound('C:/Users/10ash/PycharmProjects/pythonProject2/audios/incorrect.wav')
intro_sound = pygame.mixer.Sound('C:/Users/10ash/PycharmProjects/pythonProject2/audios/intro_sound.wav')

# список уровней
levels = [
    {"background": "C:/Users/10ash/PycharmProjects/pythonProject2/photos/back3.jpg", "question": "Какова формула энергии?", "answers": ["S = v*t", "F = m*g", "E = m*c^2", "F = m*a"], "correct_answer": 2},
    {"background": "C:/Users/10ash/PycharmProjects/pythonProject2/photos/back4.jpg", "question": "Сколько материков на Земле?", "answers": ["5", "7", "6", "8"], "correct_answer": 2},
    {"background": "C:/Users/10ash/PycharmProjects/pythonProject2/photos/back1.jpg", "question": "Немезида была богиней ...", "answers": ["Воды", "Возмездия", "Красоты", "Победы"], "correct_answer": 1},
    {"background": "C:/Users/10ash/PycharmProjects/pythonProject2/photos/back6.jpg", "question": "Кто запатентовал телефон?", "answers": ["Александр Белл", "Альберт Эйнштейн", "Томас Эдисон", "Антонио Меуччи"], "correct_answer": 0},
    {"background": "C:/Users/10ash/PycharmProjects/pythonProject2/photos/back7.jpg", "question": "В какой области не присуждается Нобелевская премия?", "answers": ["Медицина", "Химия", "Литература", "Математика"], "correct_answer": 3},
    {"background": "C:/Users/10ash/PycharmProjects/pythonProject2/photos/back8.jpg", "question": "Какое число обозначается римской буквой С?", "answers": ["50", "100", "500", "1000"], "correct_answer": 1},
    {"background": "C:/Users/10ash/PycharmProjects/pythonProject2/photos/back9.jpg", "question": "Чего, согласно пословице, в мешке не утаишь?", "answers": ["Шила", "Зерна", "Кота", "Совести"], "correct_answer": 0},
    {"background": "C:/Users/10ash/PycharmProjects/pythonProject2/photos/back12.jpg", "question": "В какой части дерева происходит процесс фотосинтеза?", "answers": ["В стволе", "В корнях", "В ветках", "В листьях"], "correct_answer": 3},
    {"background": "C:/Users/10ash/PycharmProjects/pythonProject2/photos/back13.jpg", "question": "Чему равен угол в равностороннем треугольнике?", "answers": ["90", "60", "30", "45"], "correct_answer": 1},
    {"background": "C:/Users/10ash/PycharmProjects/pythonProject2/photos/back14.jpg", "question": "Кто, по легенде, открыл закон всемирного тяготения?", "answers": ["Роберт Оппенгеймер", "Альберт Эйнштейн", "Иссак Ньютон", "Чарльз Дарвин"], "correct_answer": 2},
    {"background": "C:/Users/10ash/PycharmProjects/pythonProject2/photos/back15.jpg", "question": "Аллигаторова груша- это ...", "answers": ["Слива", "Манго", "Авокадо", "Бергамот"], "correct_answer": 2},
]

# начальное состояние игры
game_state = {'current_level': 1, 'lives': 3}
menu_active = True
level_started = False

# функции для отрисовки текста на экране
def draw_text(text, font, color, surface, x, y, background=None):
    # Создаем объект текста, устанавливаем его позицию и отображаем на экране
    text_obj = font.render(text, True, color, background)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)
    return text_rect

# функция для отображения главного меню
def show_menu():
    # фоновое изображение
    screen.blit(background_image, (0, 0))

    # текст меню
    draw_text('Подземелье AITU', font, white_color, screen, screen_width / 2, screen_height / 4)
    draw_text('Начать игру', font, white_color, screen, screen_width / 2, screen_height / 2)
    draw_text('Выйти из игры', font, white_color, screen, screen_width / 2, (screen_height / 2) + 100)
    draw_lives(game_state['lives'], (screen_width / 5.6) + 1385, (screen_height / 10))
    pygame.display.flip()

# функция для отображения ознакомительного меню перед началом игры
def show_intro():
    intro_active = True
    while intro_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                intro_sound.stop() # останавливаем воспроизведение звука
                intro_active = False  # закрыть ознакомительное меню при любом вводе

        intro_sound.play()  # воспроизвести звуковой файл
        screen.blit(intro_image, (0, 0))
        intro_text = [
            "По непонятным причинам вы проснулись в подземелье",
            "ваша цель - выжить и выбраться на поверхность",
            "для этого придется отвечать на вопросы",
            "у вас есть 3 жизни, будьте внимательны!",
            "Нажмите любую кнопку или кликните, чтобы начать игру."
        ]
        for i, line in enumerate(intro_text):
            draw_text(line, font, white_color, screen, screen_width / 2, screen_height / 3 + i * 60)

        pygame.display.flip()

# функция для отображения экрана проигрыша
def show_game_over():
    screen.blit(background_image, (0, 0))
    draw_text('Вы заблудились в катакомбах, попробуйте поискать выход снова.', font, white_color, screen, screen_width / 2, screen_height / 2)
    pygame.display.flip()
    pygame.time.wait(10) # время увидеть сообщение о проигрыше

# функция для игры на уровне
def play_level(level_data):
    global answer_rects
    # загрузка и отображение фонового изображение уровня
    background = pygame.transform.scale(pygame.image.load(level_data["background"]), (screen_width, screen_height))
    screen.blit(background, (0, 0))

    # Отображение жизней (сердечек) в правом верхнем углу
    heart_x = screen_width - 70
    heart_y = 20
    for life in range(game_state['lives']):
        screen.blit(heart_image, (heart_x, heart_y))
        heart_y += 60

    # отображение вопроса
    question = level_data["question"]
    answers = level_data["answers"]
    correct_answer = level_data["correct_answer"]

    draw_text(question, font, white_color, screen, screen_width / 2, 150)  # отображаем вопрос

    # варианты ответов
    answer_rects = []
    start_y = 500  # начальная позиция для ответов
    spacing = 100  # расстояние между вариантами ответов

    # для каждого ответа создаем текст и зону для клика
    for i, answer in enumerate(answers):
        text_rect = draw_text(answer, font, white_color, screen, screen_width / 2, start_y + i * spacing)
        # создаем Rect вокруг текста для определения области клика без отрисовки рамки
        hit_rect = pygame.Rect(text_rect.left - 30, text_rect.top - 30, text_rect.width + 40, text_rect.height + 40)
        answer_rects.append((hit_rect, i == correct_answer))
    draw_lives(game_state['lives'], (screen_width / 5.6) + 1385, (screen_height / 10))
    pygame.display.flip()
    return answer_rects

# функция для проверки ответа
def check_answer(answer_rects, mouse_pos):
    # проверяем, был ли клик в зоне правильного ответа
    for rect, is_correct in answer_rects:
        if rect.collidepoint(mouse_pos):
            return is_correct
    return False

# функция обработки кликов в меню
def menu_click_handling(mouse_x, mouse_y):
    global menu_active, game_state, level_started
    # определяем зоны клика для кнопок "Начать игру" и "Выйти из игры"
    start_game_rect = pygame.Rect(screen_width / 2 - 100, screen_height / 2 - 50, 200, 50)
    exit_game_rect = pygame.Rect(screen_width / 2 - 100, screen_height / 2 + 70, 200, 50)

    if start_game_rect.collidepoint((mouse_x, mouse_y)):
        menu_active = False
        game_state = {'current_level': 1, 'lives': 3}  # сбросить состояние игры
        show_intro()  # отображаем ознакомительное меню перед началом игры
        level_started = True
        play_level(levels[game_state['current_level'] - 1])  # запустить первый уровень
    elif exit_game_rect.collidepoint((mouse_x, mouse_y)):
        pygame.quit()
        sys.exit()

# функция для перехода на следующий уровень
def next_level():
    global game_state, level_started, answer_rects
    level_up_sound.play()
    fade_out(screen_width, screen_height)
    game_state['current_level'] += 1
    if game_state['current_level'] > len(levels):
        # обновляем экран
        screen.blit(background_image_for_win, (0, 0))
        # отображаем сообщение "Вы выиграли!"
        draw_text('Это был сон? Пора заняться учебой', font, white_color, screen, screen_width / 2, screen_height / 2)
        # обновляем дисплей
        pygame.display.flip()
        # даем время увидеть сообщение
        pygame.time.wait(2000)
        reset_game()
    else:
        answer_rects = play_level(levels[game_state['current_level'] - 1])

def draw_lives(lives, x, y):
    for i in range(lives):
        screen.blit(heart_image, (x - (i * 50 + 50), y))  # Отрисовка сердец справа налево

# Функция для анимации затемнения экрана
def fade_out(width, height):
    fade_surface = pygame.Surface((width, height))
    fade_surface.fill((0,0,0))
    for alpha in range(0, 300):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0,0))
        pygame.display.update()
        pygame.time.delay(1)

# функция для обработки неправильного ответа
def wrong_answer():
    global game_state
    lose_life_sound.play()
    game_state['lives'] -= 1
    if game_state['lives'] <= 0:
        show_game_over()
        pygame.time.wait(2000)  # Даем время увидеть сообщение о проигрыше
        reset_game()
    else:
        # Перезагружаем текущий уровень, чтобы дать возможность ответить заново
        fade_out_heart(screen_width, screen_height)
        play_level(levels[game_state['current_level'] - 1])

def fade_out_heart(width, height):
    fade_surface = pygame.Surface((width, height))
    fade_surface.fill((255, 255, 255))  # Белый цвет для "закрашивания" сердечек
    for heart_x in range(50, (game_state['lives'] + 1) * 60, 60):  # Анимация для каждого сердечка
        fade_surface.set_alpha(0)  # Прозрачность 0 (сердечко исчезает)
        screen.blit(fade_surface, (heart_x, 50))
        pygame.display.update()
        pygame.time.delay(100)  # Задержка для визуализации анимации

# функция для сброса игры и возвращения в главное меню
def reset_game():
    global menu_active, level_started, game_state
    menu_active = True
    level_started = False
    game_state = {'current_level': 1, 'lives': 3}
    show_menu()

random.shuffle(levels)
# главный игровой цикл
def game_loop():
    global menu_active, level_started, game_state, answer_rects
    answer_rects = []  # Инициализация пустым списком до начала игрового цикла
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if menu_active:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    menu_click_handling(*event.pos)
            elif level_started and event.type == pygame.MOUSEBUTTONDOWN:
                # Проверка наличия answer_rects перед использованием
                if answer_rects:
                    correct = check_answer(answer_rects, event.pos)
                    if correct:
                        next_level()
                    else:
                        wrong_answer()

        if menu_active:
            show_menu()
        pygame.display.flip()

# Обязательно добавьте вызов game_loop() для запуска игрового цикла
game_loop()

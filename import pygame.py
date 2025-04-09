<<<<<<< HEAD
import pygame
import sys
import recommend_academy  # 기존 추천 함수 사용

pygame.init()
screen = pygame.display.set_mode((900, 700))
pygame.display.set_caption("학원 추천 프로그램")
font = pygame.font.Font(None, 36)

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)

font = pygame.font.Font('CookieRun Regular.ttf', 22)

user_choices = {
    "수강 인원": None,
    "수강 연령층": None,
    "수강 과목": None,
    "수강 목적": None,
    "자유 입력": "",
    "현재 위치": "",
}

step = 0
recommendations = []

class Button:
    def __init__(self, text, pos, callback):
        self.text = text
        self.rect = pygame.Rect(pos[0], pos[1], 350, 50)
        self.callback = callback

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect)
        txt_surface = font.render(self.text, True, BLACK)
        screen.blit(txt_surface, (self.rect.x + 10, self.rect.y + 10))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.callback()

class InputBox:
    def __init__(self, x, y, w, h, label):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = GRAY
        self.text = ""
        self.txt_surface = font.render(self.text, True, BLACK)
        self.active = False
        self.label = label

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = LIGHT_BLUE if self.active else GRAY
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                user_choices[self.label] = self.text
                self.text = ""
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            self.txt_surface = font.render(self.text, True, BLACK)

    def draw(self, screen):
        screen.blit(font.render(f"{self.label} 입력:", True, BLACK), (self.rect.x, self.rect.y - 35))
        pygame.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 10))

def make_buttons():
    if step == 0:
        return [
            Button("10인 미만", (275, 150), lambda: select_and_next("수강 인원", "10인 미만")),
            Button("10인 이상", (275, 220), lambda: select_and_next("수강 인원", "10인 이상")),
        ]
    elif step == 1:
        return [
            Button("초등학생", (275, 150), lambda: select_and_next("수강 연령층", "초등학생")),
            Button("중학생", (275, 220), lambda: select_and_next("수강 연령층", "중학생")),
            Button("고등학생", (275, 290), lambda: select_and_next("수강 연령층", "고등학생")),
        ]
    elif step == 2:
        return [
            Button("국어", (275, 150), lambda: select_and_next("수강 과목", "국어")),
            Button("수학", (275, 220), lambda: select_and_next("수강 과목", "수학")),
            Button("영어", (275, 290), lambda: select_and_next("수강 과목", "영어")),
            Button("과학", (275, 360), lambda: select_and_next("수강 과목", "과학")),
        ]
    elif step == 3:
        return [
            Button("내신", (275, 150), lambda: select_and_next("수강 목적", "내신")),
            Button("수능 대비", (275, 220), lambda: select_and_next("수강 목적", "수능 대비")),
            Button("선행", (275, 290), lambda: select_and_next("수강 목적", "선행")),
        ]
    return []

def select_and_next(field, value):
    global step
    user_choices[field] = value
    step += 1

def main():
    global step, recommendations
    clock = pygame.time.Clock()
    input_boxes = [
        InputBox(250, 250, 400, 50, "hyunjae witch"),
        InputBox(250, 350, 400, 50, "hyunjae location"),
    ]

    while True:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if step < 4:
                for btn in make_buttons():
                    btn.handle_event(event)
            elif step < 6:
                for box in input_boxes:
                    box.handle_event(event)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and step == 5:
                step += 1
                recommendations = recommend_academy(user_choices)

        if step < 4:
            screen.blit(font.render(f"{list(user_choices.keys())[step]}을(를) 선택하세요", True, BLACK), (200, 60))
            for btn in make_buttons():
                btn.draw(screen)
        elif step < 6:
            screen.blit(font.render("자유 텍스트 및 현재 위치 입력 (엔터로 다음)", True, BLACK), (200, 150))
            for box in input_boxes:
                box.draw(screen)
        else:
            screen.blit(font.render("추천된 학원 목록:", True, BLACK), (150, 60))
            y = 120
            if recommendations:
                for rec in recommendations:
                    screen.blit(font.render(str(rec), True, BLACK), (150, y))
                    y += 40
            else:
                screen.blit(font.render("추천 결과가 없습니다.", True, BLACK), (150, y))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
=======
import pygame
import sys
import recommend_academy  # 기존 추천 함수 사용

pygame.init()
screen = pygame.display.set_mode((900, 700))
pygame.display.set_caption("학원 추천 프로그램")
font = pygame.font.Font(None, 36)

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)

user_choices = {
    "수강 인원": None,
    "수강 연령층": None,
    "수강 과목": None,
    "수강 목적": None,
    "자유 입력": "",
    "현재 위치": "",
}

step = 0
recommendations = []

class Button:
    def __init__(self, text, pos, callback):
        self.text = text
        self.rect = pygame.Rect(pos[0], pos[1], 350, 50)
        self.callback = callback

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect)
        txt_surface = font.render(self.text, True, BLACK)
        screen.blit(txt_surface, (self.rect.x + 10, self.rect.y + 10))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.callback()

class InputBox:
    def __init__(self, x, y, w, h, label):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = GRAY
        self.text = ""
        self.txt_surface = font.render(self.text, True, BLACK)
        self.active = False
        self.label = label

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = LIGHT_BLUE if self.active else GRAY
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                user_choices[self.label] = self.text
                self.text = ""
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            self.txt_surface = font.render(self.text, True, BLACK)

    def draw(self, screen):
        screen.blit(font.render(f"{self.label} 입력:", True, BLACK), (self.rect.x, self.rect.y - 35))
        pygame.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 10))

def make_buttons():
    if step == 0:
        return [
            Button("10인 미만", (275, 150), lambda: select_and_next("수강 인원", "10인 미만")),
            Button("10인 이상", (275, 220), lambda: select_and_next("수강 인원", "10인 이상")),
        ]
    elif step == 1:
        return [
            Button("초등학생", (275, 150), lambda: select_and_next("수강 연령층", "초등학생")),
            Button("중학생", (275, 220), lambda: select_and_next("수강 연령층", "중학생")),
            Button("고등학생", (275, 290), lambda: select_and_next("수강 연령층", "고등학생")),
        ]
    elif step == 2:
        return [
            Button("국어", (275, 150), lambda: select_and_next("수강 과목", "국어")),
            Button("수학", (275, 220), lambda: select_and_next("수강 과목", "수학")),
            Button("영어", (275, 290), lambda: select_and_next("수강 과목", "영어")),
            Button("과학", (275, 360), lambda: select_and_next("수강 과목", "과학")),
        ]
    elif step == 3:
        return [
            Button("내신", (275, 150), lambda: select_and_next("수강 목적", "내신")),
            Button("수능 대비", (275, 220), lambda: select_and_next("수강 목적", "수능 대비")),
            Button("선행", (275, 290), lambda: select_and_next("수강 목적", "선행")),
        ]
    return []

def select_and_next(field, value):
    global step
    user_choices[field] = value
    step += 1

def main():
    global step, recommendations
    clock = pygame.time.Clock()
    input_boxes = [
        InputBox(250, 250, 400, 50, "자유 입력"),
        InputBox(250, 350, 400, 50, "현재 위치"),
    ]

    while True:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if step < 4:
                for btn in make_buttons():
                    btn.handle_event(event)
            elif step < 6:
                for box in input_boxes:
                    box.handle_event(event)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and step == 5:
                step += 1
                recommendations = recommend_academy(user_choices)

        if step < 4:
            screen.blit(font.render(f"{list(user_choices.keys())[step]}을(를) 선택하세요", True, BLACK), (200, 60))
            for btn in make_buttons():
                btn.draw(screen)
        elif step < 6:
            screen.blit(font.render("자유 텍스트 및 현재 위치 입력 (엔터로 다음)", True, BLACK), (200, 150))
            for box in input_boxes:
                box.draw(screen)
        else:
            screen.blit(font.render("추천된 학원 목록:", True, BLACK), (150, 60))
            y = 120
            if recommendations:
                for rec in recommendations:
                    screen.blit(font.render(str(rec), True, BLACK), (150, y))
                    y += 40
            else:
                screen.blit(font.render("추천 결과가 없습니다.", True, BLACK), (150, y))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
>>>>>>> d6bd9d9333203be48c8d624b8a626a7e0db20f16

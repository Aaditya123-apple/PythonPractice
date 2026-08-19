"""
Tic Tac Toe — two players, local.

Run:
    pip install pygame
    python main.py
"""

from __future__ import annotations

import random
import sys

import pygame

WIN_LINES = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)

BG = (15, 23, 42)
PANEL = (30, 41, 59)
PANEL_HOVER = (36, 48, 68)
TEXT = (248, 250, 252)
MUTED = (148, 163, 184)
RED_X = (239, 68, 68)
BLUE_O = (56, 189, 248)
GREEN = (34, 197, 94)
GREEN_MARK = (5, 46, 22)
GOLD = (251, 191, 36)
WHITE = (248, 250, 252)

WIDTH, HEIGHT = 460, 640
BOARD_TOP = 210
BOARD_SIZE = 400
GAP = 10
MARGIN = 30


class Confetti:
    def __init__(self) -> None:
        self.bits: list[dict] = []
        self.until = 0

    def burst(self) -> None:
        colors = [RED_X, GREEN, BLUE_O, GOLD, WHITE]
        self.bits = [
            {
                "x": random.uniform(0, WIDTH),
                "y": random.uniform(-80, -10),
                "w": random.uniform(6, 12),
                "h": random.uniform(4, 8),
                "vx": random.uniform(-2, 2),
                "vy": random.uniform(3, 8),
                "rot": random.uniform(0, 360),
                "spin": random.uniform(-8, 8),
                "color": random.choice(colors),
            }
            for _ in range(180)
        ]
        self.until = pygame.time.get_ticks() + 3500

    def clear(self) -> None:
        self.bits = []
        self.until = 0

    def update(self) -> None:
        if not self.bits:
            return
        if pygame.time.get_ticks() > self.until:
            self.clear()
            return
        for b in self.bits:
            b["x"] += b["vx"]
            b["y"] += b["vy"]
            b["rot"] += b["spin"]

    def draw(self, screen: pygame.Surface) -> None:
        for b in self.bits:
            surf = pygame.Surface((int(b["w"]), int(b["h"])), pygame.SRCALPHA)
            surf.fill(b["color"])
            rotated = pygame.transform.rotate(surf, b["rot"])
            rect = rotated.get_rect(center=(b["x"], b["y"]))
            screen.blit(rotated, rect)


class Game:
    def __init__(self) -> None:
        self.scores = {"p1": 0, "p2": 0, "draw": 0}
        self.game_number = 1
        self.confetti = Confetti()
        self.font = pygame.font.SysFont("segoeui", 22)
        self.big = pygame.font.SysFont("segoeui", 36, bold=True)
        self.small = pygame.font.SysFont("segoeui", 16)
        self.title = pygame.font.SysFont("segoeui", 32, bold=True)
        self.start_game(reset_number=False)

    def who_starts(self) -> str:
        return "X" if self.game_number % 2 == 1 else "O"

    @staticmethod
    def player_of(mark: str) -> int:
        return 1 if mark == "X" else 2

    def start_game(self, *, reset_number: bool) -> None:
        if reset_number and (self.over or any(self.cells)):
            self.game_number += 1
        self.cells: list[str | None] = [None] * 9
        self.over = False
        self.win_line: tuple[int, ...] | None = None
        self.winner: int | None = None
        self.current = self.who_starts()
        self.confetti.clear()
        p = self.player_of(self.current)
        self.status = (
            f"Game {self.game_number}: {self.current} starts — Player {p}'s turn"
        )
        self.status_kind = "turn"

    def find_win(self, mark: str) -> tuple[int, ...] | None:
        for line in WIN_LINES:
            if all(self.cells[i] == mark for i in line):
                return line
        return None

    def play(self, index: int) -> None:
        if self.over or self.cells[index]:
            return
        self.cells[index] = self.current
        line = self.find_win(self.current)
        if line:
            self.over = True
            self.win_line = line
            winner = self.player_of(self.current)
            self.winner = winner
            if winner == 1:
                self.scores["p1"] += 1
                self.status = "Player 1 wins! Player 2 loses."
            else:
                self.scores["p2"] += 1
                self.status = "Player 2 wins! Player 1 loses."
            self.status_kind = "win"
            self.confetti.burst()
            return
        if all(self.cells):
            self.over = True
            self.scores["draw"] += 1
            self.status = "It's a draw."
            self.status_kind = "draw"
            return
        self.current = "O" if self.current == "X" else "X"
        p = self.player_of(self.current)
        self.status = f"Player {p}'s turn ({self.current})"
        self.status_kind = "turn"

    def cell_rect(self, i: int) -> pygame.Rect:
        cell = (BOARD_SIZE - 2 * GAP) // 3
        col, row = i % 3, i // 3
        x = MARGIN + col * (cell + GAP)
        y = BOARD_TOP + row * (cell + GAP)
        return pygame.Rect(x, y, cell, cell)

    def new_game_rect(self) -> pygame.Rect:
        return pygame.Rect(WIDTH // 2 - 90, HEIGHT - 58, 180, 40)

    def handle_click(self, pos: tuple[int, int]) -> None:
        if self.new_game_rect().collidepoint(pos):
            self.start_game(reset_number=True)
            return
        if self.over:
            return
        for i in range(9):
            if self.cell_rect(i).collidepoint(pos):
                self.play(i)
                break

    def draw_mark(self, screen: pygame.Surface, rect: pygame.Rect, mark: str, won: bool) -> None:
        color = GREEN_MARK if won else (RED_X if mark == "X" else BLUE_O)
        if mark == "X":
            pad = 22
            width = 10
            pygame.draw.line(
                screen, color,
                (rect.left + pad, rect.top + pad),
                (rect.right - pad, rect.bottom - pad),
                width,
            )
            pygame.draw.line(
                screen, color,
                (rect.right - pad, rect.top + pad),
                (rect.left + pad, rect.bottom - pad),
                width,
            )
        else:
            pygame.draw.circle(screen, color, rect.center, rect.width // 2 - 18, 10)

    def draw_card(
        self,
        screen: pygame.Surface,
        rect: pygame.Rect,
        title: str,
        mark: str,
        score: int,
        mark_color: tuple[int, int, int],
        active: bool,
        winner: bool,
        loser: bool,
    ) -> None:
        border = GREEN if winner else ((100, 116, 139) if active else (0, 0, 0, 0))
        pygame.draw.rect(screen, PANEL, rect, border_radius=14)
        if winner or active:
            pygame.draw.rect(screen, border, rect, 2, border_radius=14)
        if loser:
            overlay = pygame.Surface(rect.size, pygame.SRCALPHA)
            overlay.fill((15, 23, 42, 120))
            screen.blit(overlay, rect.topleft)
        t = self.small.render(title, True, MUTED)
        m = self.font.render(mark, True, mark_color)
        s = self.big.render(str(score), True, TEXT)
        screen.blit(t, t.get_rect(center=(rect.centerx, rect.y + 16)))
        screen.blit(m, m.get_rect(center=(rect.centerx, rect.y + 40)))
        screen.blit(s, s.get_rect(center=(rect.centerx, rect.y + 78)))

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(BG)
        heading = self.title.render("Tic Tac Toe", True, TEXT)
        screen.blit(heading, heading.get_rect(center=(WIDTH // 2, 28)))
        sub = self.small.render("Player 1 is X  ·  Player 2 is O", True, MUTED)
        screen.blit(sub, sub.get_rect(center=(WIDTH // 2, 58)))

        p1 = pygame.Rect(20, 80, 130, 110)
        dr = pygame.Rect(165, 80, 130, 110)
        p2 = pygame.Rect(310, 80, 130, 110)
        self.draw_card(
            screen, p1, "PLAYER 1", "X", self.scores["p1"], RED_X,
            not self.over and self.current == "X",
            self.winner == 1, self.winner == 2,
        )
        self.draw_card(
            screen, dr, "DRAWS", "—", self.scores["draw"], GOLD,
            False, False, False,
        )
        self.draw_card(
            screen, p2, "PLAYER 2", "O", self.scores["p2"], BLUE_O,
            not self.over and self.current == "O",
            self.winner == 2, self.winner == 1,
        )

        kind_color = {"win": GREEN, "draw": GOLD, "turn": TEXT}[self.status_kind]
        status = self.font.render(self.status, True, kind_color)
        screen.blit(status, status.get_rect(center=(WIDTH // 2, 208)))

        mouse = pygame.mouse.get_pos()
        for i in range(9):
            rect = self.cell_rect(i)
            won = bool(self.win_line and i in self.win_line)
            fill = GREEN if won else (PANEL_HOVER if rect.collidepoint(mouse) and not self.over and not self.cells[i] else PANEL)
            pygame.draw.rect(screen, fill, rect, border_radius=16)
            if self.cells[i]:
                self.draw_mark(screen, rect, self.cells[i], won)

        btn = self.new_game_rect()
        pygame.draw.rect(screen, WHITE, btn, border_radius=22)
        label = self.font.render("New game", True, BG)
        screen.blit(label, label.get_rect(center=btn.center))

        self.confetti.update()
        self.confetti.draw(screen)


def main() -> None:
    pygame.init()
    pygame.display.set_caption("Tic Tac Toe")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game.handle_click(event.pos)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                game.start_game(reset_number=True)

        game.draw(screen)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()

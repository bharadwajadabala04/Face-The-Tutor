# alerts/message_queue.py
import pygame
from backend.notify_tutor import notify_tutor
from config import MAX_WARNINGS

pygame.mixer.init()
pygame.mixer.music.load("alerts/alert.wav")

class WarningManager:
    def __init__(self):
        self.warning_count = {}

    def issue_warning(self, issue):
        print(f"[WARNING] {issue}")
        pygame.mixer.music.play()
        self.warning_count[issue] = self.warning_count.get(issue, 0) + 1

        if self.warning_count[issue] >= MAX_WARNINGS:
            notify_tutor(issue)

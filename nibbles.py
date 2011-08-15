#!/usr/bin/env python
import curses
import time
import random

class Nibbles:
    def __init__(self, stdscr):
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        height, width = stdscr.getmaxyx()
        self.playboard = stdscr.subwin(height - 3, width, 0, 0)
        self.playboard.keypad(1)
        self.playboard.nodelay(1)
        self.dashboard = stdscr.subwin(3, width, height - 3, 0)
        self.dashboard.keypad(1)
        self.dashboard.nodelay(1)
        self.play()

    def change_direction(self, c):
        d = self.nibbles[0][-1]
        if (c == ord('h')) or (c == curses.KEY_LEFT):
            if d == 'left' or d == 'right':
                pass
            else:
                self.nibbles[0][-1] = 'left'
        elif (c == ord('j')) or (c == curses.KEY_DOWN):
            if  d == 'up' or d == 'down':
                pass
            else:
                self.nibbles[0][-1] = 'down'
        elif (c == ord('k')) or (c == curses.KEY_UP):
            if d == 'up' or d == 'down':
                pass
            else:
                self.nibbles[0][-1] = 'up'
        elif (c == ord('l')) or (c == curses.KEY_RIGHT):
            if d == 'left' or d == 'right':
                pass
            else:
                self.nibbles[0][-1] = 'right'
        elif c == ord('q'):
            self.quit()
        elif c == ord(' '):
            self.pause()
        else:
            pass
        
    def move_forward(self):
        x, y, d = self.nibbles[0][0], self.nibbles[0][1], self.nibbles[0][2]
        if d == 'up':
            self.nibbles.insert(0, [x, y-1, d])
            self.playboard.addstr(self.nibbles[0][1], self.nibbles[0][0], 
                    '^', (curses.A_BOLD | curses.color_pair(1)))
        elif d == 'down':
            self.nibbles.insert(0, [x, y+1, d])
            self.playboard.addstr(self.nibbles[0][1], self.nibbles[0][0],
                    'v', (curses.A_BOLD | curses.color_pair(1)))
        elif d == 'left':
            self.nibbles.insert(0, [x-1, y, d])
            self.playboard.addstr(self.nibbles[0][1], self.nibbles[0][0], 
                    '<', (curses.A_BOLD | curses.color_pair(1)))
        elif d == 'right':
            self.nibbles.insert(0, [x+1, y, d])
            self.playboard.addstr(self.nibbles[0][1], self.nibbles[0][0],
                    '>', (curses.A_BOLD | curses.color_pair(1)))
        else:
            pass
        self.playboard.addstr(self.nibbles[-1][1], self.nibbles[-1][0], ' ')
        self.nibbles = self.nibbles[:-1]
    
    def place_an_apple(self):
        flag = True
        height, width = self.playboard.getmaxyx()
        while flag:
            x, y = random.randint(1, width - 2), random.randint(1, height - 2)
            if x == self.apple[0] and y == self.apple[1]:
                continue
            for nibble in self.nibbles:
                a, b = nibble[0], nibble[1]
                if (a == x) and (b == y):
                    break
            else:
                flag = False
            self.apple = [x, y]
            self.playboard.addstr(self.apple[1], self.apple[0], '*', (
                curses.A_BOLD | curses.color_pair(2)))
    
    def judge(self):
        x, y, d = self.nibbles[0][0], self.nibbles[0][1], self.nibbles[0][2]
        height, width = self.playboard.getmaxyx()
        if x == self.apple[0] and y == self.apple[1]:
            self.score += 1
            self.speed = (self.score / 10) + 1;
            self.dashboard.addstr(1, 3, 'score: %s' % self.score, (
                curses.A_REVERSE | curses.A_BOLD | curses.color_pair(3)))
            self.dashboard.addstr(1, 15, 'speed: %s' % self.speed, (
                curses.A_REVERSE | curses.A_BOLD | curses.color_pair(3)))
            if d == 'up':
                self.nibbles.insert(0, [x, y-1, d])
                self.playboard.addstr(self.nibbles[0][1], self.nibbles[0][0],
                        '^', (curses.A_BOLD |  curses.color_pair(1)))
            elif d == 'down':
                self.nibbles.insert(0, [x, y+1, d])
                self.playboard.addstr(self.nibbles[0][1], self.nibbles[0][0],
                        'v', (curses.A_BOLD | curses.color_pair(1)))
            elif d == 'left':
                self.nibbles.insert(0, [x-1, y, d])
                self.playboard.addstr(self.nibbles[0][1], self.nibbles[0][0],
                        '<', (curses.A_BOLD | curses.color_pair(1)))
            elif d == 'right':
                self.nibbles.insert(0, [x+1, y, d])
                self.playboard.addstr(self.nibbles[0][1], self.nibbles[0][0],
                        '>', (curses.A_BOLD | curses.color_pair(1)))
            else:
                pass
            self.place_an_apple()
        elif (x == 0) or (x == width - 1) or (y == 0) or (y == height - 1):
            self.replay()
        else:
            pass
    
    def replay(self):
        self.playboard.erase()
        self.playboard.border(0)
        self.playboard.refresh()
        y, x = self.playboard.getmaxyx()
        s = "Press 'q' to quit game,"
        self.playboard.addstr(y/2, x/2 - len(s)/2, s, (curses.A_BOLD |
            curses.color_pair(2)))
        s = "others to replay."
        self.playboard.addstr(y/2+1, x/2 - len(s)/2, s, (curses.A_BOLD |
            curses.color_pair(2)))
        self.playboard.nodelay(0)
        c = self.playboard.getch()
        if c == ord('q'):
            self.quit()
        else:
            self.playboard.nodelay(1)
            self.play()
    
    def play(self):
        self.playboard.erase()
        self.playboard.border(0)
        self.dashboard.erase()
        self.dashboard.border(0)
        self.nibbles    = []
        self.score      = 0
        self.speed      = 1
        y, x = self.playboard.getmaxyx()
        self.apple = [int(x/2), int(y/2)]
        self.nibbles.append([int(x/4), int(y/2), 'right'])
        self.playboard.addstr(self.apple[1], self.apple[0], '*', (
            curses.A_BOLD | curses.color_pair(2)))
        self.playboard.addstr(self.nibbles[0][1], self.nibbles[0][0], '>', (
            curses.A_BOLD | curses.color_pair(1)))
        self.dashboard.addstr(1, 3, 'score: %s' % self.score, (
            curses.A_REVERSE | curses.A_BOLD | curses.color_pair(3)))
        self.dashboard.addstr(1, 15, 'speed: %s' % self.speed, (
            curses.A_REVERSE | curses.A_BOLD | curses.color_pair(3)))
        try:
            while True:
                c = self.playboard.getch()
                self.change_direction(c)
                self.move_forward()
                self.judge()
                self.playboard.refresh()
                self.dashboard.refresh()
                time.sleep(0.1 / self.speed)
        except:
            return

    def pause(self):
        self.playboard.nodelay(0)
        while True:
            c = self.playboard.getch()
            if c == ord(' '):
                self.playboard.nodelay(1)
                return

    def quit(self):
        raise Exception()

def main():
    curses.wrapper(Nibbles)

if __name__ == '__main__':
    main()

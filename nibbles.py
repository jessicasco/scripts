#!/usr/bin/env python
#coding=utf-8
import curses
import time
import random

stdscr      = None
dashboard   = None
nibbles     = []
apple       = None
score       = 0
speed       = 1

def init():
    global stdscr, dashboard, nibbles, apple, score, speed
    screen = curses.initscr()
    y, x = screen.getmaxyx()
    stdscr = screen.subwin(y-3, x, 0, 0)
    stdscr.keypad(1)
    stdscr.nodelay(1)
    dashboard = screen.subwin(3, x, y-3, 0)
    dashboard.keypad(1)
    dashboard.nodelay(1)
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)

def quit():
    global stdscr, dashboard, nibbles, apple, score, speed
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    if not curses.endwin():
        import sys
        sys.exit(0)

def adjust(c):
    global stdscr, dashboard, nibbles, apple, score, speed
    a, b, d = nibbles[0][0], nibbles[0][1], nibbles[0][2]
    if (c == ord('h')) or (c == curses.KEY_LEFT):
        if d == 'left' or d == 'right':
            pass
        else:
            nibbles[0][-1] = 'left'
    elif (c == ord('j')) or (c == curses.KEY_DOWN):
        if  d == 'up' or d == 'down':
            pass
        else:
            nibbles[0][-1] = 'down'
    elif (c == ord('k')) or (c == curses.KEY_UP):
        if d == 'up' or d == 'down':
            pass
        else:
            nibbles[0][-1] = 'up'
    elif (c == ord('l')) or (c == curses.KEY_RIGHT):
        if d == 'left' or d == 'right':
            pass
        else:
            nibbles[0][-1] = 'right'
    elif c == ord('q'):
        quit()
    elif c == ord(' '):
        pause()
    else:
        pass

def pause():
    global stdscr, dashboard, nibbles, apple, score, speed
    stdscr.nodelay(0)
    while True:
        c = stdscr.getch()
        if c == ord(' '):
            stdscr.nodelay(1)
            break
    
def move():
    global stdscr, dashboard, nibbles, apple, score, speed
    a, b, d = nibbles[0][0], nibbles[0][1], nibbles[0][2]
    if d == 'up':
        nibbles.insert(0, [a, b-1, d])
        stdscr.addstr(nibbles[0][1], nibbles[0][0], '^', (curses.A_BOLD |
            curses.color_pair(1)))
    elif d == 'down':
        nibbles.insert(0, [a, b+1, d])
        stdscr.addstr(nibbles[0][1], nibbles[0][0], 'v', (curses.A_BOLD |
            curses.color_pair(1)))
    elif d == 'left':
        nibbles.insert(0, [a-1, b, d])
        stdscr.addstr(nibbles[0][1], nibbles[0][0], '<', (curses.A_BOLD |
            curses.color_pair(1)))
    elif d == 'right':
        nibbles.insert(0, [a+1, b, d])
        stdscr.addstr(nibbles[0][1], nibbles[0][0], '>', (curses.A_BOLD |
            curses.color_pair(1)))
    else:
        pass
    stdscr.addstr(nibbles[-1][1], nibbles[-1][0], ' ')
    nibbles = nibbles[:-1]

def rearrangeApple(x, y):
    global stdscr, dashboard, nibbles, apple, score, speed
    flag = True
    while flag:
        a, b = random.randint(1, x-2), random.randint(1, y-2)
        if a == apple[0] and b == apple[1]:
            continue
        for nibble in nibbles:
            aa, bb = nibble[0], nibble[1]
            if (aa == a) and (bb == b):
                break
        else:
            flag = False
        apple = [a, b]
        stdscr.addstr(apple[1], apple[0], '*', (curses.A_BOLD |
            curses.color_pair(2)))

def judge(x, y):
    global stdscr, dashboard, nibbles, apple, score, speed
    a, b, d = nibbles[0][0], nibbles[0][1], nibbles[0][2]
    if a == apple[0] and b == apple[1]:
        score += 1
        speed = (score / 10) + 1;
        dashboard.addstr(1, 3, 'score: %s' % score, (curses.A_REVERSE |
                curses.A_BOLD | curses.color_pair(3)))
        dashboard.addstr(1, 15, 'speed: %s' % speed, (curses.A_REVERSE |
                curses.A_BOLD | curses.color_pair(3)))
        if d == 'up':
            nibbles.insert(0, [a, b-1, d])
            stdscr.addstr(nibbles[0][1], nibbles[0][0], '^', (curses.A_BOLD
                |  curses.color_pair(1)))
        elif d == 'down':
            nibbles.insert(0, [a, b+1, d])
            stdscr.addstr(nibbles[0][1], nibbles[0][0], 'v', (curses.A_BOLD
                | curses.color_pair(1)))
        elif d == 'left':
            nibbles.insert(0, [a-1, b, d])
            stdscr.addstr(nibbles[0][1], nibbles[0][0], '<', (curses.A_BOLD
                | curses.color_pair(1)))
        elif d == 'right':
            nibbles.insert(0, [a+1, b, d])
            stdscr.addstr(nibbles[0][1], nibbles[0][0], '>', (curses.A_BOLD
                | curses.color_pair(1)))
        else:
            pass
        rearrangeApple(x, y)
    elif (a == 0) or (a == x - 1) or (b == 0) or (b == y-1):
        restart()
    else:
        pass

def restart():
    global stdscr, dashboard, nibbles, apple, score, speed
    stdscr.erase()
    stdscr.border(0)
    stdscr.refresh()
    y, x = stdscr.getmaxyx()
    s = "Press 'q' to quit game,"
    stdscr.addstr(y/2, x/2 - len(s)/2, s, (curses.A_BOLD |
        curses.color_pair(2)))
    s = "others to replay."
    stdscr.addstr(y/2+1, x/2 - len(s)/2, s, (curses.A_BOLD |
        curses.color_pair(2)))
    stdscr.nodelay(0)
    c = stdscr.getch()
    if c == ord('q'):
        quit()
    else:
        stdscr.nodelay(1)
        game()

def game():
    global stdscr, dashboard, nibbles, apple, score, speed
    nibbles     = []
    apple       = None
    score       = 0
    speed       = 1
    stdscr.erase()
    stdscr.border(0)
    dashboard.erase()
    dashboard.border(0)
    y, x = stdscr.getmaxyx()
    apple = [int(x/2), int(y/2)]
    stdscr.addstr(apple[1], apple[0], '*', (curses.A_BOLD |
        curses.color_pair(2)))
    nibbles.append([int(x/4), int(y/2), 'right'])
    stdscr.addstr(nibbles[0][1], nibbles[0][0], '>', (curses.A_BOLD |
        curses.color_pair(1)))
    dashboard.addstr(1, 3, 'score: %s' % score, (curses.A_REVERSE |
        curses.A_BOLD | curses.color_pair(3)))
    dashboard.addstr(1, 15, 'speed: %s' % speed, (curses.A_REVERSE |
                curses.A_BOLD | curses.color_pair(3)))
    while True:
        c = stdscr.getch()
        adjust(c)
        move()
        try:
            judge(x, y)
        except:
            break
        stdscr.refresh()
        dashboard.refresh()
        time.sleep(0.1/speed)
    quit()

def main():
    init()
    game()

if __name__ == '__main__':
    main()

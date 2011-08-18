python << EOF

import curses
import time
import random

class Shape():
    def __init__(self, win, all_points):
        self.win = win
        self.all_points = all_points
        self.height, self.width = win.getmaxyx()
        self.state = 0
        self.set_points()
        self.commands = {
                ord('h'): self.move_left,
                ord('j'): self.quick_down,
                ord('k'): self.transform,
                ord('l'): self.move_right,
                ord(' '): self.pause,
                ord('q'): self.quit,
                -1      : self.move_down,
                }

    def set_points(self):
        pass

    def quick_down(self):
        pass

    def transform(self):
        pass

    def draw(self, char):
        for point in self.points:
            self.win.addstr(point[1], point[0], char)

    def move_down(self):
        self.draw(' ')
        for i in range(len(self.points)):
            self.points[i][1] += 1
        self.draw('*')
        time.sleep(0.1)

    def move_left(self):
        self.draw(' ')
        for i in range(len(self.points)):
            self.points[i][0] -= 1
        self.draw('*')
        self.move_down()

    def move_right(self):
        self.draw(' ')
        for i in range(len(self.points)):
            self.points[i][0] += 1
        self.draw('*')
        self.move_down()

    def play(self):
        while not self.stop():
            c = self.win.getch()
            self.commands.get(c, self.move_down)()
            self.win.refresh()

    def stop(self):
        for point in self.points:
            if (([point[0], point[1]+1] in self.all_points) or
                    (point[1]+1 == self.height-1)):
                for point in self.points:
                    self.all_points.append([point[0], point[1]])
                return True
        return False

    def pause(self):
        self.win.nodelay(0)
        while True:
            c = self.win.getch()
            if c == ord(' '):
                self.win.nodelay(1)
                return

    def quit(self):
        raise Exception()

class I(Shape):
    """
         *
    **** *
         *
         *
    """
    def __init__(self, win, points):
        Shape.__init__(self, win, points)
        self.play()

    def transform(self):
        self.draw(' ')
        x, y = self.points[0]
        if self.state == 0:
            self.state = 1
            self.points = [[x+1, y-2], [x+1, y-1], [x+1, y], [x+1, y+1]]
        elif self.state == 1:
            self.state = 0
            self.points = [[x-1, y+1], [x, y+1], [x+1, y+1], [x+2, y+1]]
        else:
            pass
        self.draw('*')

    def set_points(self):
        y = 3
        x = random.randint(0+1, self.width-1-4)
        self.points = [[x, y], [x+1, y], [x+2, y], [x+3, y]]

class J(Shape):
    """
         *
    ***  * *   **
      * ** *** *
               *
    """
    def __init__(self, win, points):
        Shape.__init__(self, win, points)
        self.play()

    def transform(self):
        self.draw(' ')
        x, y = self.points[0]
        if self.state == 0:
            self.state = 1
            self.points = [[x+1, y-1], [x+1, y], [x+1, y+1], [x, y+1]]
        elif self.state == 1:
            self.state = 2
            self.points = [[x+1, y+2], [x, y+2], [x-1, y+2], [x-1, y+1]]
        elif self.state == 2:
            self.state = 3
            self.points = [[x-2, y+1], [x-2, y], [x-2, y-1], [x-1, y-1]]
        elif self.state == 3:
            self.state = 0
            self.points = [[x-1, y-2], [x, y-2], [x+1, y-2], [x+1, y-1]]
        else:
            pass
        self.draw('*')

    def set_points(self):
        y = 2
        x = random.randint(0+1, self.width-1-3)
        self.points = [[x, y], [x+1, y], [x+2, y], [x+2, y+1]]

class L(Shape):
    """
    *      
    *  *** **   *
    ** *    * ***
            *
    """
    def __init__(self, win, points):
        Shape.__init__(self, win, points)
        self.play()
    
    def transform(self):
        self.draw(' ')
        x, y = self.points[0]
        if self.state == 0:
            self.state = 1
            self.points = [[x+2, y+1], [x+1, y+1], [x, y+1], [x, y+2]]
        elif self.state == 1:
            self.state = 2
            self.points = [[x-1, y+2], [x-1, y+1], [x-1, y], [x-2, y]]
        elif self.state == 2:
            self.state = 3
            self.points = [[x-2, y-1], [x-1, y-1], [x, y-1], [x, y-2]]
        elif self.state == 3:
            self.state = 0
            self.points = [[x+1, y-2], [x+1, y-1], [x+1, y], [x+2, y]]
        else:
            pass
        self.draw('*')

    def set_points(self):
        y = 2
        x = random.randint(0+1, self.width-1-3)
        self.points = [[x, y], [x+1, y], [x+2, y], [x, y+1]]

class O(Shape):
    def __init__(self, win, points):
        Shape.__init__(self, win, points)
        self.play()

    def set_points(self):
        y = 1
        x = random.randint(0+1, self.width-1-2)
        self.points = [[x, y], [x+1, y], [x, y+1], [x+1, y+1]]

class S(Shape):
    """
    *
    **  **
     * **
    """
    def __init__(self, win, points):
        Shape.__init__(self, win, points)
        self.play()

    def transform(self):
        self.draw(' ')
        x, y = self.points[0]
        if self.state == 0:
            self.state = 1
            self.points = [[x+2, y+1], [x+1, y+1], [x+1, y+2], [x, y+2]]
        elif self.state == 1:
            self.state = 0
            self.points = [[x-2, y-1], [x-2, y], [x-1, y], [x-1, y+1]]
        else:
            pass
        self.draw('*')

    def set_points(self):
        y = 2
        x = random.randint(0+1, self.width-1-3)
        self.points = [[x+1, y], [x+2, y], [x, y+1], [x+1, y+1]]

class T(Shape):
    """
         *  *  *
    *** ** *** **
     *   *     *
    """
    def __init__(self, win, points):
        Shape.__init__(self, win, points)
        self.play()

    def transform(self):
        self.draw(' ')
        x, y = self.points[0]
        if self.state == 0:
            self.state = 1
            self.points = [[x+1, y-1], [x+1, y], [x+1, y+1], [x, y]]
        elif self.state == 1:
            self.state = 2
            self.points = [[x+1, y+1], [x, y+1], [x-1, y+1], [x, y]]
        elif self.state == 2:
            self.state = 3
            self.points = [[x-1, y+1], [x-1, y], [x-1, y-1], [x, y]]
        elif self.state == 3:
            self.state = 0
            self.points = [[x-1, y-1], [x, y-1], [x+1, y-1], [x, y]]
        else:
            pass
        self.draw('*')

    def set_points(self):
        y = 2
        x = random.randint(0+1, self.width-1-3)
        self.points = [[x, y], [x+1, y], [x+2, y], [x+1, y+1]]

class Z(Shape):
    """
         *
    **  **
     ** *
    """
    def __init__(self, win, points):
        Shape.__init__(self, win, points)
        self.play()

    def transform(self):
        self.draw(' ')
        x, y = self.points[0]
        if self.state == 0:
            self.state = 1
            self.points = [[x+2, y-1], [x+2, y], [x+1, y], [x+1, y+1]]
        elif self.state == 1:
            self.state = 0
            self.points = [[x-2, y+1], [x-1, y+1], [x-1, y+2], [x, y+2]]
        else:
            pass
        self.draw('*')

    def set_points(self):
        y = 2
        x = random.randint(0+1, self.width-1-3)
        self.points = [[x, y], [x+1, y], [x+1, y+1], [x+2, y+1]]

class Tetris():
    def __init__(self, stdscr):
        curses.curs_set(0)
        height, width = stdscr.getmaxyx()
        self.shapeboard = stdscr.subwin(height, width/3, 0, 0)
        self.shapeboard.keypad(1)
        self.shapeboard.nodelay(1)
        self.playboard = stdscr.subwin(height, width/3, 0, width/3)
        self.y, self.x = self.playboard.getmaxyx()
        self.playboard.keypad(1)
        self.playboard.nodelay(1)
        self.playboard.border(0)
        self.infoboard = stdscr.subwin(height, width - width/3*2, 0, width/3*2)
        self.infoboard.keypad(1)
        self.infoboard.nodelay(1)
        self.points = []
        self.score = 0
        self.shapes = [I, J, L, O, S, T, Z]
        self.play()

    def get_score(self):
        i = self.y -1 -1
        while i > 0:
            for j in range(0+1, self.x-1):
                if [i, j] not in self.points:
                    i -= 1
                    break
            else:
                self.score += 1
                for j in range(0+1, self.x-1):
                    self.playboard.addstr(j, i, ' ')
                    self.points.remove([i, j])
                for j in range(len(self.points)):
                    if self.points[j][1] < i:
                        self.playboard.addstr(self.points[j][1],
                                self.points[j][0], ' ')
                        self.points[j][1] += 1
                        self.playboard.addstr(self.points[j][1],
                                self.points[j][0], '*')

    def play(self):
        try:
            while True:
                random.choice(self.shapes)(self.playboard, self.points)
                self.get_score()
                self.shapeboard.refresh()
                self.playboard.refresh()
                self.infoboard.refresh()
        except :
            return 

def main():
    curses.wrapper(Tetris)

if __name__ == '__main__':
    main()

EOF

redraw!

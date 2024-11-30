from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

class BoatGame:
    def __init__(self):
        self.boat1_x = 100
        self.boat2_x = 400
        self.boat_y = 40
        self.obstacles = []
        self.bullets1 = []
        self.bullets2 = []
        self.score1 = 0
        self.score2 = 0

#saowmi
    def move_boat1(self,dx):
        new_x = self.boat1_x + dx
        self.boat1_x = max(20, min(480, new_x))

    def move_boat2(self,dx):
        new_x = self.boat2_x + dx
        self.boat2_x = max(20, min(480, new_x))

    def MidPointAlgo(self, x1, y1, x2, y2):
        zone = self.findZone(x1, y1, x2, y2)
        if zone == 0:
            self.drawLine(x1, y1, x2, y2, zone)
        else:
            (a, b, c, d) = self.changeToZone0(x1, y1, x2, y2, zone)
            self.drawLine(a, b, c, d, zone)

    def findZone(self, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        if abs(dx) >= abs(dy):
            if dx > 0 and dy > 0:
                zone = 0
            elif dx <= 0 and dy > 0:
                zone = 3
            elif dx <= 0 and dy <= 0:
                zone = 4
            elif dx > 0 and dy <= 0:
                zone = 7
        else:
            if dx > 0 and dy > 0:
                zone = 1
            elif dx <= 0 and dy > 0:
                zone = 2
            elif dx <= 0 and dy <= 0:
                zone = 5
            elif dx > 0 and dy <= 0:
                zone = 6

        return zone

    def changeToOriginal(self, x1, y1, zone):
        if zone == 0:
            return x1, y1
        elif zone == 1:
            return y1, x1
        elif zone == 2:
            return -y1, x1
        elif zone == 3:
            return -x1, y1
        elif zone == 4:
            return -x1, -y1
        elif zone == 5:
            return -y1, -x1
        elif zone == 6:
            return y1, -x1
        elif zone == 7:
            return x1, -y1

    def changeToZone0(self, x1, y1, x2, y2, zone):
        if zone == 0:
            return x1, y1, x2, y2
        elif zone == 1:
            return y1, x1, y2, x2
        elif zone == 2:
            return y1, -x1, y2, -x2
        elif zone == 3:
            return -x1, y1, -x2, y2
        elif zone == 4:
            return -x1, -y1, -x2, -y2
        elif zone == 5:
            return -y1, -x1, -y2, -x2
        elif zone == 6:
            return -y1, x1, -y2, x2
        elif zone == 7:
            return x1, -y1, x2, -y2

    def writePixel(self, x, y, zone):
        if zone == 0:
            glBegin(GL_POINTS)
            glVertex2f(x, y)
            glEnd()
        else:
            (x_prime, y_prime) = self.changeToOriginal(x, y, zone)
            glPointSize(2)
            glBegin(GL_POINTS)
            glVertex2f(x_prime, y_prime)
            glEnd()

    def drawLine(self, x1, y1, x2, y2, zone):
        dx = x2 - x1
        dy = y2 - y1

        d = 2 * dy - dx

        incE = 2 * dy
        incNE = 2 * (dy - dx)

        y = y1
        x = x1
        while x <= x2:
            self.writePixel(x, y, zone)

            if d > 0:
                d += incNE
                y += 1
            else:
                d += incE

            x += 1

    def boat1part1(self, x, y):
        glColor3f(0.5, 0.5, 1.0)
        self.MidPointAlgo(x, y, x + 30, y)
        self.MidPointAlgo(x, y, x - 5, y + 20)
        self.MidPointAlgo(x + 30, y, x + 35, y + 20)
        self.MidPointAlgo(x + 35, y + 20, x - 5, y + 20)

    def boat1part2(self, x, y):
        glColor3f(1.0, 1.0, 1.0)
        self.MidPointAlgo(x + 25, y + 20, x + 15, y + 35)
        self.MidPointAlgo(x + 15, y + 35, x + 5, y + 20)

    def boat2part1(self, x, y):
        glColor3f(0.5, 0.5, 1.0)
        self.MidPointAlgo(x + 80, y, x + 110, y)
        self.MidPointAlgo(x + 80, y, x + 75, y + 20)
        self.MidPointAlgo(x + 110, y, x + 115, y + 20)
        self.MidPointAlgo(x + 75, y + 20, x + 115, y + 20)

    def boat2part2(self, x, y):
        glColor3f(1.0, 1.0, 1.0)
        self.MidPointAlgo(x + 85, y + 20, x + 93, y + 35)
        self.MidPointAlgo(x + 100, y + 20, x + 93, y + 35)
#elora
    def draw_points(self,x, y, size):
        points = np.array([[x, y]], dtype=np.float32)
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(2, GL_FLOAT, 0, points)
        glPointSize(size)
        glDrawArrays(GL_POINTS, 0, 1)
        glDisableClientState(GL_VERTEX_ARRAY)

    def draw_circle(self,x0, y0, radius, s):
        x = radius
        y = 0
        err = 0

        while x >= y:
            self.draw_points(x + x0, y + y0, s)
            self.draw_points(x + x0, y + y0, s)
            self.draw_points(y + x0, x + y0, s)
            self.draw_points(-y + x0, x + y0, s)
            self.draw_points(-x + x0, y + y0, s)
            self.draw_points(-x + x0, -y + y0, s)
            self.draw_points(-y + x0, -x + y0, s)
            self.draw_points(y + x0, -x + y0, s)
            self.draw_points(x + x0, -y + y0, s)

            if err <= 0:
                y += 1
                err += 2 * y + 1
            if err > 0:
                x -= 1
                err -= 2 * x + 1

    def draw_obstacles(self):
        new_obstacles = []
        for obstacle in self.obstacles:
            obstacle[1] -= 5
            if obstacle[1] > -20:
                glColor3f(0.45, 0.2, 0.2)
                obstacle_translation_matrix = np.array([
                    [1, 0, 0, obstacle[0]],
                    [0, 1, 0, obstacle[1]],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]
                ])
                glPushMatrix()
                glMultMatrixf(obstacle_translation_matrix.transpose())
                self.draw_circle(0, 0, 20, 1.0)
                glPopMatrix()
                new_obstacles.append(obstacle)
            else:
                self.score1 += 1
                self.score2 += 1
        self.obstacles = new_obstacles

    def check_collision(self):
        for obstacle in self.obstacles:
            if abs(obstacle[0] - self.boat1_x) < 20 and obstacle[1] < 40:
                print("Game Over! Player 2 is the winner. Score:", self.score2)
                glutLeaveMainLoop()
                return True
            elif abs(obstacle[0] - self.boat2_x) < 20 and obstacle[1] < 40:
                print("Game Over! Player 1 is the winner. Score:", self.score1)
                glutLeaveMainLoop()
                return True
        return False

    def draw_bullet(self, x, y):
        glColor3f(1.0, 0.0, 0.0)

        bullet_translation_matrix = np.array([
            [1, 0, 0, x],
            [0, 1, 0, y],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        glPushMatrix()
        glMultMatrixf(bullet_translation_matrix.transpose())
        glBegin(GL_QUADS)
        glVertex2f(-2, 2)
        glVertex2f(2, 2)
        glVertex2f(2, -2)
        glVertex2f(-2, -2)
        glEnd()
        glPopMatrix()


# sharon
    def draw_bullets(self):
        for bullet in self.bullets1:
            self.draw_bullet(bullet[0], bullet[1])
        for bullet in self.bullets2:
            self.draw_bullet(bullet[0], bullet[1])


    def check_bullet_collision(self):
        new_bullets1 = []
        new_bullets2 = []

        for bullet in self.bullets1:
            hit = False
            for obstacle in self.obstacles:
                if (
                    abs(bullet[0] - obstacle[0]) < 20
                    and abs(bullet[1] - obstacle[1]) < 20
                ):
                    hit = True
                    self.obstacles.remove(obstacle)
                    self.score1 += 1
                    break

            if not hit and bullet[1] < 800:
                new_bullets1.append(bullet)

        for bullet in self.bullets2:
            hit = False
            for obstacle in self.obstacles:
                if (
                    abs(bullet[0] - obstacle[0]) < 20
                    and abs(bullet[1] - obstacle[1]) < 20
                ):
                    hit = True
                    self.obstacles.remove(obstacle)
                    self.score2 += 1
                    break

            if not hit and bullet[1] < 800:
                new_bullets2.append(bullet)

        self.bullets1 = new_bullets1
        self.bullets2 = new_bullets2

    def keyboard(self,key, x, y):
        if key == b'q':
            glutLeaveMainLoop()
        elif key == b'a':
            self.move_boat1(-10)
        elif key == b'd':
            self.move_boat1(10)
        elif key == b's':
            self.bullets1.append([self.boat1_x, self.boat_y])
        elif key == b'j':
            self.move_boat2(-10)
        elif key == b'l':
            self.move_boat2(10)
        elif key == b'k':
            self.bullets2.append([self.boat2_x, self.boat_y])

    def timer(self,value):
        self.obstacles.append([np.random.randint(50, 750), 600])
        glutTimerFunc(500, self.timer, 0)

    def iterate(self):
        glViewport(0, 0, 800, 800)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, 800, 0.0, 800, 0.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def show_screen(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        self.iterate()

        # Update bullet positions
        self.bullets1 = [[x, y + 5] for x, y in self.bullets1]
        self.bullets2 = [[x, y + 5] for x, y in self.bullets2]

        # Draw boats
        self.boat1part1(self.boat1_x, self.boat_y)
        self.boat1part2(self.boat1_x, self.boat_y)
        self.boat2part1(self.boat2_x, self.boat_y)
        self.boat2part2(self.boat2_x, self.boat_y)

        self.draw_obstacles()
        self.draw_bullets()
        self.check_bullet_collision()

        if self.check_collision():
            return

        glColor3f(1.0, 1.0, 1.0)
        glRasterPos2f(10, 10)
        glutSwapBuffers()

if __name__ == "__main__":
    game = BoatGame()
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(600, 600)
    glutInitWindowPosition(0, 0)
    wind = glutCreateWindow(b"Boat Game Simulator")
    glutDisplayFunc(game.show_screen)
    glutIdleFunc(game.show_screen)
    glutKeyboardFunc(game.keyboard)
    glutTimerFunc(500, game.timer, 0)
    glutMainLoop()
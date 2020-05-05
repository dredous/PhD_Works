import pygame
from pygame.locals import *
from pygame.math import Vector2
import numpy as np
import math

width = 1024
height = 768

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
GREEN = (  0, 255,   0)
RED   = (255,   0,   0)
GRAY = (125, 125, 125)
bezier_pos = (0,0,200,40)
reset_pos = (600, 0, 200, 40)
hermite_pos = (200,0,200,40)
showcurve_pos = (width - 200, 200, 150, 40)
unshowcurve_pos = (width - 200, 240, 150, 40)
count = 0
mid = False
curve_tightness = 0.5
tangents = [[50,50], [50,50]]

def C(n, i):
    f = math.factorial
    return f(n) / (f(i) * f(n - i))

def checkPos(pts, target_pts):
    if target_pts[0] <= pts[0] <= target_pts[0] + target_pts[2] and target_pts[1] <= pts[1] <= target_pts[1] + target_pts[3]:
        return True
    else:
        return False

def ptline(pt0, pt1, alpha):
    return (1 - alpha) * pt0 + alpha * pt1

def drawPoint(pt, color='GREEN', thick = 3):
    pygame.draw.circle(screen, color, pt, thick)

def drawLine(pt0, pt1, color = 'GREEN', thick = 3, ncircles = 1000):
    drawPoint(pt1, color, thick)
    if pt0 != pt1:
        for i in range(-1 * ncircles, 2 * (ncircles + 1)):
            pt_x = ptline(pt0[0], pt1[0], i / ncircles)
            pt_y = ptline(pt0[1], pt1[1], i / ncircles)
            drawPoint([int(pt_x), int(pt_y)], color, thick=2)

def drawPolylines(color='GREEN', thick=3):
    if count == 1:
        # print("Count = 1")
        drawLine(rects[0].topleft, rects[0].topleft, color)
    else:
        # print("Count > 3")
        for i in range(count - 1):
            drawLine(rects[i].topleft, rects[i + 1].topleft, color, ncircles=1000)

def drawButtons(screen, button1):
    pygame.draw.rect(screen, GRAY, button1)
    # pygame.draw.rect(screen, RED, rectangle)
    # pygame.draw.rect(screen, RED, rectangle)

def drawText(screen, texts, buttons):
    for i in range (len(texts) - 1):
        screen.blit(texts[i], (buttons[i].topleft[0] + 70, buttons[i].topleft[1] + 10))
    # screen.blit(texts[len(texts) - 1], (buttons[len(buttons) - 1].topright[0] + 70, buttons[len(buttons) - 1].topright[1] + 10))

def tangent_point(pts):
        return [curve_tightness * (pts[2][i] - pts[0][i]) for i in range(len(pts[0]))]

def bezier(p):
    step = 40.0
    results = []
    n = len(p) - 1
    for i in range (int(step) + 1):
        x=0
        y=0
        t = i/step
        for j in range (n+1):
            b = C(n, j) * (1-t)**(n-j) * t**j
            x += b * p[j][0]
            y += b * p[j][1]
        results.append((int(x), int(y)))
    return results
def hermit_interp(pt, t, tangent):
    h1 = 2*(t**3) - 3*(t**2) + 1
    h2 = -2*(s**3) + 3*(t**2)
    h3 = t**3 - 2*(t**2) + t
    h4 = t**3 - t**2
    return pt[0]*h0 + pt[1]*h1 + tangent[0]*h2 + tangent[1]*h3

def hermite(p):
    step = 40.0
    results = []
    for j in range(len(p)):
        for i in range (int(steps) + 1):
            t = i / step
            if j > 0:
                tangent_x = [tangents[j][0] for j in range(j - 1, j+1)]
                tangent_y = [tangents[j][1] for j in range(j - 1, j+1)]
                if j < len(p) - 1:
                    mid = True
                    vec_xh = p[j-1:j+2][0]
                    vec_yh = p[j-1:j+2][1]
                else:
                    mid = False
                    vec_xh = p[j-1:j+1][0]
                    vec_yh = p[j-1:j+1][1]
                qt_x = hermit_interp(vec_xh, t, tangent_x)
                qt_y = hermit_interp(vec_yh, t, tangent_y)
                results.append(int(qt_x), int(qt_y))

            


pygame.init()
status = "Line"
screen = pygame.display.set_mode((width, height))
rects = []
texts = []
buttons = []
selectedRect = None
# rect = pygame.rect.Rect(20, 20, 17, 17)
rect_drag = False
font = pygame.font.Font('freesansbold.ttf', 20) 
text = font.render('Bezier', True, RED)
text2 = font.render('Hermit', True, RED)
text3 = font.render('Spline', True, RED)
text4 = font.render('Reset', True, RED)
text5 = font.render(status, True, RED)
text6 = font.render('Show Curve ', True, RED)
text7 = font.render('Hide Curve ', True, RED)
texts.append(text)
texts.append(text2)
texts.append(text3)
texts.append(text4)
texts.append(text5)
running = True
buttonBezier = pygame.Rect(0,0,200,40)
buttonHermite = pygame.Rect(200,0,200,40)
buttonSpline = pygame.Rect(400,0,200,40)
buttonReset = pygame.Rect(600, 0, 200, 40)
buttonShowCurve = pygame.Rect(width - 200, 200, 150, 40)
buttonNotShowCurve = pygame.Rect(width - 200, 240, 150, 40)
buttons.append(buttonBezier)
buttons.append(buttonSpline)
buttons.append(buttonHermite)
buttons.append(buttonReset)
poly_type = 0
button_hover = False
show_curve = False
points = []
while running:
    pt_res = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 or event.button == 3:
                if checkPos(event.pos, bezier_pos):
                    poly_type = 1
                    button_hover = True
                    status = "Bezier"
                elif checkPos(event.pos, reset_pos):
                    poly_type = 0
                    button_hover = True
                    rects = []
                    points = []
                    status = "Line"
                elif checkPos(event.pos, hermite_pos):
                    poly_type = 2
                    button_hover = True
                    status = "Hermit"
                elif checkPos(event.pos, showcurve_pos):
                    show_curve = True
                    button_hover = True
                elif checkPos(event.pos, unshowcurve_pos):
                    show_curve = False
                    button_hover = True
                else:
                    for rectangle in rects:
                        if rectangle.collidepoint(event.pos):
                            offset = Vector2(rectangle.topleft) - event.pos
                            selectedRect = rectangle

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if selectedRect == None and button_hover == False:
                    mouse_x, mouse_y = event.pos
                    pt = [mouse_x, mouse_y]
                    new_rect = pygame.rect.Rect(mouse_x-5, mouse_y-5, 10, 10)
                    rects.append(new_rect)
                    points.append(pt)
                    # print(len(points))
                count += 1
                button_hover = False
                # if len(points) > 1:
                #     tangents[0] = [0,0]
                #     tangents[len(points) - 1] = [0, 0]
                #     tangents.insert(len(points) - 1, tangent_point(points[len(points) - 2: len(points) + 1]))
                # print(len(tangents))
            elif event.button == 3:
                if selectedRect:
                    index = rects.index(selectedRect)
                    pt = points[index]
                    rects.remove(selectedRect)
                    points.remove(pt)
            selectedRect = None
        elif event.type == pygame.MOUSEMOTION:
            if selectedRect:
                index = rects.index(selectedRect)
                selectedRect.topleft = event.pos + offset
                points[index] = selectedRect.center
    
    screen.fill(WHITE)
    # drawButtons(screen, buttonBezier)
    pygame.draw.rect(screen, GRAY, buttonBezier, 2)
    pygame.draw.rect(screen, GRAY, buttonHermite, 2)
    pygame.draw.rect(screen, GRAY, buttonSpline, 2)
    pygame.draw.rect(screen, GRAY, buttonReset, 2)
    pygame.draw.rect(screen, GRAY, buttonShowCurve, 2)
    pygame.draw.rect(screen, GRAY, buttonNotShowCurve, 2)
    for rectangle in rects:
        pygame.draw.rect(screen, RED, rectangle)
    # if len(rects)>0:
    #     # print(len(rects))
    #     drawPolylines(GREEN, 1)
    # screen.blit(text, (50, 10))
    drawText(screen, texts, buttons)
    if len(points) > 1:
        pygame.draw.lines(screen, BLACK, False, points, 2)
    if poly_type == 1:
        pt_res = bezier(points)
        # pygame.draw.lines(screen, GREEN, False, pt_res, 2)
    # elif poly_type == 2:
    #     pt_res = hermite(points)
    if show_curve:
        if len(pt_res) > 0:
            pygame.draw.lines(screen, GREEN, False, pt_res, 2)
    
    # pygame.draw.lines(screen, GREEN, False, pt_res, 2)
    screen.blit(text6, (buttonShowCurve.topleft[0] + 15, buttonShowCurve.topleft[1] + 10))
    screen.blit(text7, (buttonNotShowCurve.topleft[0] + 15, buttonNotShowCurve.topleft[1] + 10))
    pygame.display.update()
# print(pt_res)
pygame.quit()
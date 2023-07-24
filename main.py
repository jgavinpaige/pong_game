import pygame

import math
import random

def main():
    #initialize pygame
    pygame.init()
    clock = pygame.time.Clock()
    pygame.font.init() 
    font = pygame.font.Font(None, 40)
    subtitle = pygame.font.Font(None, 20)
    
    #define constant variables
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 460
    
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    
    PADDLE_HEIGHT = 100
    PADDLE_WIDTH = 10
    PADDLE_SPEED = 10
    
    #define and initialize game variables
    iterate = True
    player1_score = player2_score = 0
    player1_yPos = player2_yPos = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2
    player1_xPos = 20
    player2_xPos = SCREEN_WIDTH - 20 - PADDLE_WIDTH
    ball_width = 20
    ball_x = SCREEN_WIDTH // 2 - ball_width // 2
    ball_y = SCREEN_HEIGHT // 2 - ball_width // 2
    ball_xSpeed = random.choice((-1, 1)) * 3
    ball_ySpeed = random.choice((-1, 1)) * 5
    
    #set up window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pong")
    player1_text = font.render(str(player1_score), True, (120, 120, 120))
    player2_text = font.render(str(player2_score), True, (120, 120, 120))
    
    p1_text_rect = player1_text.get_rect(center=(SCREEN_WIDTH // 4, 20))
    p2_text_rect = player2_text.get_rect(center=(3 * SCREEN_WIDTH // 4, 20))
    screen.blit(player1_text, p1_text_rect)
    screen.blit(player2_text, p2_text_rect)
    
    paused = True
    start_screen = True
    
    #run game loop
    while iterate:
        #main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                iterate = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                if event.key == pygame.K_SPACE and (start_screen or paused):
                    start_screen = False
                    paused = False
                    ball_x = SCREEN_WIDTH // 2 - ball_width // 2
                    ball_y = SCREEN_HEIGHT // 2 - ball_width // 2
                    ball_xSpeed = random.choice((-1, 1)) * 3
                    ball_ySpeed = random.choice((-1, 1)) * 5
                    player1_score = player2_score = 0
                    
                    player2_text = font.render(str(player2_score), True, (120, 120, 120))
                    player1_text = font.render(str(player1_score), True, (120, 120, 120))
        
        if start_screen: 
            screen.fill(BLACK)
             
            start_text = font.render("Press 'space' to begin!", True, WHITE)
            insturctions_text = subtitle.render("**Left side uses w/s keys and right side uses up/down arrows**", True, WHITE)
            pause_text = subtitle.render("Press 'ESC' to pause or unpause", True, WHITE)
            
            start_text_rect = start_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2-20))
            screen.blit(start_text, start_text_rect)
            
            instructions_text_rect = insturctions_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT-200))
            screen.blit(insturctions_text, instructions_text_rect)
            
            screen.blit(pause_text, (10, 10))
        elif not paused:
            keys = pygame.key.get_pressed()
            #move player1's paddle
            if keys[pygame.K_w]:
                if player1_yPos - PADDLE_SPEED >= 0:
                    player1_yPos -= PADDLE_SPEED
                else:
                    player1_yPos = 0
            elif keys[pygame.K_s]:
                if player1_yPos + PADDLE_HEIGHT + PADDLE_SPEED <= SCREEN_HEIGHT:
                    player1_yPos += PADDLE_SPEED
                else:
                    player1_yPos = SCREEN_HEIGHT - PADDLE_HEIGHT
            if keys[pygame.K_UP]:
                if player2_yPos - PADDLE_SPEED >= 0:
                    player2_yPos -= PADDLE_SPEED
                else:
                    player2_yPos = 0
            elif keys[pygame.K_DOWN]:
                if player2_yPos + PADDLE_HEIGHT + PADDLE_SPEED <= SCREEN_HEIGHT:
                    player2_yPos += PADDLE_SPEED
                else:
                    player2_yPos = SCREEN_HEIGHT - PADDLE_HEIGHT
                    
            #----game logic----
            
            #check collision with screen top and bottom
            if ball_y + ball_width > SCREEN_HEIGHT:
                ball_ySpeed *= -1
                ball_y -= ball_y - SCREEN_HEIGHT + ball_width
            if ball_y < 0:
                ball_ySpeed *= -1
                ball_y *= -1
                
            #check for collision with player 1 paddle
            if ball_xSpeed < 0 and ball_x > player1_xPos + PADDLE_WIDTH and ball_x + ball_xSpeed <= player1_xPos + PADDLE_WIDTH:
                if ball_y + ball_width >= player1_yPos and ball_y <= player1_yPos + PADDLE_HEIGHT:
                    ball_xSpeed *= -1
            #player 2 paddle collision
            if ball_xSpeed > 0 and ball_x + ball_width < player2_xPos and ball_x + ball_width + ball_xSpeed >= player2_xPos:
                if ball_y + ball_width >= player2_yPos and ball_y <= player2_yPos + PADDLE_HEIGHT:
                    ball_xSpeed *= -1
                        
            #check if ball scored a point
            if ball_x + ball_width < 0 or ball_x > SCREEN_WIDTH:
                #add scores
                if ball_xSpeed < 0:
                    player2_score += 1
                    player2_text = font.render(str(player2_score), True, (120, 120, 120))
                else:
                    player1_score += 1
                    player1_text = font.render(str(player1_score), True, (120, 120, 120))
                #reset ball
                ball_x = SCREEN_WIDTH // 2 - ball_width // 2
                ball_y = SCREEN_HEIGHT // 2 - ball_width // 2
                ball_xSpeed = random.choice((-1, 1)) * 3
                ball_ySpeed = random.choice((-1, 1)) * 5
                
            ball_x += ball_xSpeed
            ball_y += ball_ySpeed
                
            
            #drawing commands
            screen.fill(BLACK)
            draw_dashed_line(screen, (120, 120, 120), (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))
            
            #draw paddles
            pygame.draw.rect(screen, WHITE, (20, player1_yPos, PADDLE_WIDTH, PADDLE_HEIGHT))
            pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH - PADDLE_WIDTH - 20, player2_yPos, PADDLE_WIDTH, PADDLE_HEIGHT))
            
            #draw ball
            pygame.draw.rect(screen, WHITE, (ball_x, ball_y, ball_width, ball_width))
            
            
            screen.blit(player1_text, p1_text_rect)
            screen.blit(player2_text, p2_text_rect)
        else:
            screen.fill((180, 180, 180))
            message = subtitle.render("Press 'ESC' to Resume or 'SPACE' to Restart", True, WHITE)
            message_rect = message.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(message, message_rect)
        
        #update screen
        pygame.display.flip()
        
        clock.tick(60)
    
    pygame.quit()
    
def draw_dashed_line(screen, color, p1, p2, line_width=5):
    line_height = line_width * 3
    
    try:
        theta = math.atan(abs((p1[1] - p2[1]) / (p1[0] - p2[0])))
    except ZeroDivisionError:
        theta = math.pi / 2
    
    y_step = math.sin(theta) * line_height
    x_step = math.cos(theta) * line_height
    
    drawing_pt_x = p1[0]
    drawing_pt_y = p1[1]
    
    while between_two_points((drawing_pt_x, drawing_pt_y), p1, p2):
        end_x = drawing_pt_x + x_step
        end_y = drawing_pt_y + y_step
        pygame.draw.line(screen, color, (drawing_pt_x, drawing_pt_y), (end_x, end_y), width=line_width) 
        drawing_pt_x += x_step*2
        drawing_pt_y += y_step*2  
    
def between_two_points(target_pt, pt1, pt2):
    #check if target point lies between the x values and y values
    try:
        slope = (pt1[1] - pt2[1]) / (pt1[0] - pt2[0])
        y_intercept = pt1[1] - slope * pt1[0]
        return target_pt[1] == slope * target_pt[0] + y_intercept
    except ZeroDivisionError:
        return not ((target_pt[1] > pt1[1] and target_pt[1] > pt2[1]) \
            or (target_pt[1] < pt1[1] and target_pt[1] < pt2[1]))
    
if __name__ == '__main__':
    main()
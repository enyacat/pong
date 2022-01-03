# Implementation of classic arcade game Pong
# Copy paste code into the codeskulptor https://py2.codeskulptor.org/ to play
import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
score1 = 0
score2 = 0

# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    # initialize ball_pos and ball_vel for bal in middle of table
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [0, 0]
    if direction == RIGHT:
        ball_vel = [random.randrange(2, 6), random.randrange(-2, 0, 2)]
    elif direction == LEFT:
        ball_vel = [-random.randrange(2, 6), random.randrange(-2, 0, 2)]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    paddle1_pos = [HALF_PAD_WIDTH, 200]
    paddle2_pos = [WIDTH - HALF_PAD_WIDTH, 200]        
    paddle1_vel = 0
    paddle2_vel = 0
    if LEFT:
        spawn_ball(LEFT)
    elif RIGHT:
        spawn_ball(RIGHT)
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle2_vel, LEFT, RIGHT
         
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    # determine whether paddle and ball collide 
    if ((ball_pos[0] <= BALL_RADIUS + PAD_WIDTH) and (ball_pos[1] - paddle1_pos[1]) ** 2 < HALF_PAD_HEIGHT ** 2) or \
       ((ball_pos[0] >= WIDTH - PAD_WIDTH) and (ball_pos[1] - paddle2_pos[1]) ** 2 < HALF_PAD_HEIGHT ** 2):
        ball_vel[0] = - ball_vel[0] * 1.1
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 4, "Red", "White")    
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos[1] += paddle1_vel
    paddle2_pos[1] += paddle2_vel
    if paddle1_pos[1] < HALF_PAD_HEIGHT:
        paddle1_pos[1] = HALF_PAD_HEIGHT
    elif paddle1_pos[1] > HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos[1] = HEIGHT - HALF_PAD_HEIGHT        
    if paddle2_pos[1] < HALF_PAD_HEIGHT:
        paddle2_pos[1] = HALF_PAD_HEIGHT
    elif paddle2_pos[1] > HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos[1] = HEIGHT - HALF_PAD_HEIGHT
    # draw paddles    
    canvas.draw_polygon([[paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT], 
                         [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], 
                         [0, paddle1_pos[1] + HALF_PAD_HEIGHT], 
                         [0, paddle1_pos[1] - HALF_PAD_HEIGHT]], 2, 'Yellow', 'Orange')
    canvas.draw_polygon([[paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT],
                         [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT], 
                         [paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT],
                         [paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT]], 2, 'Yellow', 'Orange')        
    # draw scores
    canvas.draw_text(str(score1), [PAD_WIDTH + 10,20], 20, "Red")
    canvas.draw_text(str(score2), [WIDTH - PAD_WIDTH - 30,20], 20, "Blue") 
    # updating scores
    if ball_pos[0] < - BALL_RADIUS:
        score2 += 1
        LEFT = False
        RIGHT = True
        new_game()
    elif ball_pos[0] > WIDTH + BALL_RADIUS:
        score1 += 1
        RIGHT = False
        LEFT = True
        new_game()
    
def keydown(key):
    global paddle1_vel, paddle2_vel, paddle1_pos, paddle2_pos
    acc = 3        
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -acc
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = acc    
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -acc
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = acc
    
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"] or key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP["up"] or key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0

def reset():
    global score1, score2, LEFT, RIGHT
    score1 = 0
    score2 = 0
    LEFT = True
    RIGHT = False
    new_game()

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
Reset_button = frame.add_button('Restart', reset, 70)

# start frame
new_game()
frame.start()

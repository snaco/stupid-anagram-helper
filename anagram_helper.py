### Anagram Helper
### Why the hell did I spend 2 days learning how to use curses to make this?
### I don't know, but it was kind of fun. I liked using spinners for not spinners.
### There is a stupid bug in here, I'm not fixing it. I've got Elden Ring to play.
### Just don't be too quick with the backspace or anything for that matter. Or just
### don't use this script. It's not like it's useful. If you want to make an anagram,
### use a crayon and a piece of paper it will probably be faster.
### Don't get me started on my use of global variables. I'm not fixing that either.
### It's python's fault for not having a way to pass by reference.

import curses
from time import sleep
import re
import random

frame = 0
valid_characters = re.compile(r'[a-zA-Z ]')
running = True
input_text = ''
initial_phrase = ''
base_character_set = []
working_character_set = []
anagram = ''
error = None
meme_spinner = ['your', 'mom', 'is', 'an', 'anagram']
arrow_spinner = ['▹▹▹▹▹', '▸▹▹▹▹', '▹▸▹▹▹', '▹▹▸▹▹', '▹▹▹▸▹', '▹▹▹▹▸']

def draw_prompt(window: curses.window):
    current_arrow_frame = arrow_spinner[frame % 6]
    for i in range(0, len(current_arrow_frame)):
        window.addch(1, i, current_arrow_frame[i], curses.color_pair(i + 35))

def screen_initial_phrase(window: curses.window):
    global input_text
    curses.curs_set(1)
    prompt = 'Enter a base phrase'
    draw_prompt(window)
    window.addstr(0, 0, prompt)
    window.addstr(1, 6, input_text)

def effect_save_input(_):
    global input_text, base_character_set, app_step, working_character_set, initial_phrase
    initial_phrase = '' + input_text
    carr = [char for char in input_text.replace(' ', '')]
    carr.sort()
    base_character_set = [char for char in carr]
    working_character_set = [char for char in carr]
    input_text = ''
    app_step += 1

def screen_anagram_input(window: curses.window):
    global input_text, anagram, working_character_set, error, app_step
    curses.curs_set(1)
    window.addstr(0, 0, 'Remaining Letters: ' + ''.join(working_character_set))
    draw_prompt(window)
    window.addstr(1, 6, input_text)
    if error is not None:
        window.addstr(2, 0, error)
    if len(working_character_set) == 0:
        anagram = input_text
        input_text = ''
        app_step += 1

def screen_results(window: curses.window):
    global initial_phrase, anagram
    curses.curs_set(0)
    window.addstr(0, 0, 'Your starting phrase: ' + initial_phrase, curses.color_pair(1))
    window.addstr(1, 0, 'Your anagram:         ' + anagram, curses.color_pair(2))
    window.addstr(2, 0, 'Press any key to exit')

meme_frame = 0

def screen_meme_on_em(window: curses.window):
    global meme_spinner, meme_frame, running
    window.clear()
    window.refresh()
    window.addstr(int(random.random() * 7), int(random.random() * 7), meme_spinner[meme_frame])
    meme_frame += 1
    if meme_frame > len(meme_spinner):
        window.clear()
        running = False
    window.refresh()
    sleep(random.random())

def handle_input(window: curses.window):
    global input_text, running, app_steps, app_step, base_character_set, error, working_character_set
    try:
        key = window.get_wch()
        if app_steps[app_step] == screen_results:
            if key != -1:
                app_step += 1
        if (valid_characters.match(key) is None):
            # detect backspace
            if str(key) == '\x7f':
                refunded_character = input_text[-1]
                input_text = input_text[:-1]
                if app_steps[app_step] == screen_anagram_input and refunded_character != ' ':
                    working_character_set.append(refunded_character)
                    working_character_set.sort()
                error = None
            # detect escape key
            if str(key) == '\x1b':
                next_key = window.getch()
                if next_key == -1:
                    window.clear()
                    running = False
                else:
                    next_key = window.getch()
            # detect enter key
            if str(key) == '\n':
                app_step += 1
        else:
            if app_steps[app_step] == screen_initial_phrase:
                input_text += key
            elif app_steps[app_step] == screen_anagram_input:
                if key == ' ' and input_text[-1] != ' ': 
                    input_text += key
                    error = None
                elif key in working_character_set:
                    input_text += key
                    working_character_set.remove(key)
                    error = None
                elif key != ' ':
                    error = 'Invalid character'
    except:
        pass

app_steps = [screen_initial_phrase, effect_save_input, screen_anagram_input, screen_results, screen_meme_on_em]
app_step = 0

def main(window: curses.window):
    global running, app_step, app_steps, frame
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)
    window.nodelay(True)
    while running:
        frame = (frame + 1) % 1000000 # don't look at this line like that
        try:
            handle_input(window)
            window.clear()
            app_steps[app_step](window)
        except IndexError:
            running = False
        window.refresh()
    window.clear()
    window.addstr(0, 0, 'Goodbye!')
    window.refresh()
    sleep(1)
    window.clear()

window = curses.initscr()
curses.echo(False)
curses.halfdelay(1)
main(window)
curses.endwin()

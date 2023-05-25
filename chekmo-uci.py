#!/usr/bin/env python3

#
# PDP-8's CHEKMO-II chess engine UCI adapter
#
# (C) 2016 Oleg Kalachev <okalachev@gmail.com>
#
# http://github.com/okalachev/chekmo
#

from subprocess import Popen, PIPE
import pty
import os
import sys
import atexit


LOG = False
pdir = os.path.dirname(os.path.realpath(__file__))


def which(pgm):
    path = os.getenv('PATH') + os.path.pathsep + '/usr/local/bin'
    for p in path.split(os.path.pathsep):
        p = os.path.join(p, pgm)
        if os.path.exists(p) and os.access(p, os.X_OK):
            return p


def log(s):
    if not LOG: return
    with open(pdir + '/log.txt', 'a') as d:
        d.write(s + '\n')
        d.flush()


def wait_prompt():
    parsed_side = None
    while True:
        x = chekmo.stdout.read(1).decode()
        if x == '?':
            break
        if x in ['W', 'B']:
            parsed_side = x
    chekmo.stdout.read(1)  # skip space char
    return parsed_side


def send(s):
    pin.write(s + '\r')
    pin.flush()


def read_line():
    return chekmo.stdout.readline().decode()


master, slave = pty.openpty()  # create a pseudoterminal to control pdp8 simulator

chekmo = Popen([which('pdp8'), pdir + '/simh-script'], stdout=PIPE, stdin=slave, close_fds=True, shell=False)
pin = os.fdopen(master, 'w')
atexit.register(lambda: chekmo.kill())  # kill pdp8 simulator process on exit

print('CHEKMO-II UCI ADAPTER')
log('=========\nrun with ' + ' '.join(sys.argv))

CASTLING = {
    'W': {'O-O-O': 'e1c1', 'O-O': 'e1g1'},
    'B': {'O-O-O': 'e8c8', 'O-O': 'e8g8'}
}

while True:
    command = input()
    log(command)
    words = command.split()
    cleaned = ' '.join(words)
    if len(words) == 0:
        continue
    cmd = words[0]

    # Process a UCI command
    if cmd == 'uci':
        print('id name CHEKMO-II')
        print('id author John E. Comeauin')
        print('option name Blitz mode type check default false')
        print('uciok', flush=True)
    elif cmd == 'isready':
        print('readyok', flush=True)
    elif cmd == 'ucinewgame':
        wait_prompt()
        send('re')
    elif cmd == 'position' and words[1] == 'startpos' and len(words) == 2:
        wait_prompt()
        send('re')
    elif cmd == 'position' and words[1] == 'startpos' and words[2] == 'moves':
        moves = words[3:]
        wait_prompt()
        send('re')  # reset the board
        for move in moves:
            if len(move) == 5:
                # pawn promotion move
                move = move[:4] + '=' + move[-1]
            wait_prompt()
            send(move)  # make moves
    elif cmd == 'go':
        side = wait_prompt()
        send('mv')
        read_line()
        move = read_line().strip()
        if CASTLING[side].get(move):
            move = CASTLING[side].get(move)
        else:
            move = move.replace('-', '').replace('=', '').replace('+', '').replace(':', '').strip().lower()
        print('bestmove ' + move, flush=True)
    elif cleaned == 'setoption name Blitz mode value true':
        wait_prompt()
        send('bm')
    elif cleaned == 'setoption name Blitz mode value false':
        wait_prompt()
        send('tm')
    elif cmd == 'quit':
        sys.exit()
    else:
        print('Unknown command: ' + command)

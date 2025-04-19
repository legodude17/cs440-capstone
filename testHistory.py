from board import Board

board = Board()
board.decode(".,0,4 .h.rrH...rR....Dd.R...C.....m.R..errR.DCd........c.r....hrr.R..H")

move = board.random_move()
print(board.move_str(move))
board.do_move(move)

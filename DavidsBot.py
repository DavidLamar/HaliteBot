import hlt
from hlt import NORTH, EAST, SOUTH, WEST, STILL, Move, Square
import random

##################################################################################################################################
## Setup
##################################################################################################################################
myID, game_map = hlt.get_init();
hlt.send_init("HAL(ite)_9000");

best_border = None;


##################################################################################################################################
## Actual Bot Code
##################################################################################################################################

def assign_move(square):

    target, direction = max(((neighbor, direction) for direction, neighbor in enumerate(game_map.neighbors(square))
                                if neighbor.owner != myID),
                                default = (None, None),
                                key = lambda t: heuristic(t[0]));
    
    if target is not None and target.strength < square.strength:
        return Move(square, direction);
        
    elif (square.strength < square.production * 5):
        return Move(square, STILL);

    border = any(neighbor.owner != myID for neighbor in game_map.neighbors(square));
    if not border:
        nearest_border_square, border_direction = find_border(square);
        if(game_map.get_target(square, border_direction).strength + square.strength > 255):
            return Move(square, STILL);
        else:
            return Move(square, border_direction);

    return move_border(square, direction);
    

def move_border(square, outwards_direction):
    direction = outwards_direction;
    if( any( (neighbor.owner != myID and neighbor.owner != 0) for neighbor in game_map.neighbors(square)) ):
        best_border = square;
        
    if(direction == NORTH or direction == SOUTH):
        dir1 = EAST;
        dir2 = WEST;
    else:
        dir1 = NORTH;
        dir2 = SOUTH;

    ideal_dir = decide_move(square, dir1, dir2);
    if(ideal_dir != None and game_map.get_target(square, ideal_dir).strength > square.strength):
        return Move(square, ideal_dir);
    else:
        #Stay still if we can't combine well
        return Move(square, STILL);

def decide_move(square, direction1, direction2):
    neighbor1 = game_map.get_target(square, direction1);
    neighbor2 = game_map.get_target(square, direction2);
    if( (neighbor1.owner == myID
        and square.strength + neighbor1.strength < 256
        and square.strength + neighbor1.strength > square.strength + square.production)
        or square.strength == 255):
        return direction1;
    elif( (neighbor2.owner == myID
        and square.strength + neighbor2.strength < 256
        and square.strength + neighbor2.strength > square.strength + square.production)
        or square.strength == 255):
        return direction2;
    return None;
        
def find_border(square):
    if(best_border != None):
        return get_direction(square, best_border);
    
    direction = NORTH;
    tile = square;
    max_distance = min(game_map.width, game_map.height) / 2;
    
    for d in (NORTH, EAST, SOUTH, WEST):
        distance = 0;
        current = square
        while current.owner == myID and distance < max_distance:
            distance += 1;
            current = game_map.get_target(current, d);
            
        #Reset max distance, because we've found a shorter path to a border
        if (distance < max_distance):
            max_distance = distance;
            tile = current;
            direction = d;

    return (tile, direction);

def get_direction(sq1, sq2):
    self = game_map;
    dx = min(abs(sq1.x - sq2.x), sq1.x + self.width - sq2.x, sq2.x + self.width - sq1.x);
    dy = min(abs(sq1.y - sq2.y), sq1.y + self.height - sq2.y, sq2.y + self.height - sq1.y);
    if(abs(dx) > abs(dy)):
        return EAST if dx < 0 else WEST;
    else:
        return NORTH if dy < 0 else SOUTH;

def heuristic(square):
    if (square.owner == 0 and square.strength > 0):
        return square.production / square.strength;
    else:
        return sum(neighbor.strength for neighbor in game_map.neighbors(square) if neighbor.owner not in (0, myID));

while True:
    game_map.get_frame()
    moves = [assign_move(square) for square in game_map if square.owner == myID]
    hlt.send_frame(moves)










    

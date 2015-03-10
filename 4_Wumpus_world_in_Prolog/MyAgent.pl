init_agent:-
  retractall(curLocation(_,_)),
  retractall(preLocation(_,_)),
  retractall(direction(_)),
  retractall(gold(_)),
  retractall(isSafe(_,_)),
  retractall(noPit(_,_)),
  retractall(noWumpus(_,_)),
  retractall(turnCount(_)),
  retractall(arrow(_)),
  retractall(actCount(_)),
  assert(actCount(0)),
  assert(arrow(1)),
  assert(turnCount(0)),
  assert(curLocation(1,1)),
  assert(direction(0)),
  assert(gold(0)),
  assert(noWumpus(1,1)),
  assert(noPit(1,1)),
  assert(isSafe(1,1)).

safe(X,Y):- isSafe(X,Y); ( noPit(X,Y),noWumpus(X,Y) ).

turn_left:- direction(D),retract(direction(D)), D1 is (D+90) mod 360, assert(direction(D1)).

turn_right:- direction(D),retract(direction(D)), D1 is (D-90) mod 360, assert(direction(D1)).

randomTurn(Act):- random(0,99, R), turnCount(C),retractall(turnCount(_)),C1 is C + 1, assert(turnCount(C1)),
        ((R < 50, Act = turnleft, turn_left);
          (R >= 50,Act = turnright, turn_right)).

changeSaveLoc:- curLocation(X,Y), direction(D),
    retractall(preLocation(_,_)),assert(preLocation(X,Y)),
    retractall(curLocation(X,Y)),
    (D = 0, X1 is X + 1, Y1 is Y,assert(curLocation(X1,Y1));
     D = 90, X1 is X, Y1 is Y + 1,assert(curLocation(X1,Y1));
     D = 180, X1 is X - 1, Y1 is Y,assert(curLocation(X1,Y1));
     D = 270, X1 is X, Y1 is Y - 1,assert(curLocation(X1,Y1))).
     
run_agent([no,_,_,_,_],_):- curLocation(X,Y),assert(noWumpus(X,Y)),
    X1 is X + 1, X2 is X - 1, Y1 is Y + 1, Y2 is Y - 1,
    assert(noWumpus(X1,Y)),
    assert(noWumpus(X2,Y)),
    assert(noWumpus(X,Y1)),
    assert(noWumpus(X,Y2)),
    fail.

run_agent([_,no,_,_,_],_):- curLocation(X,Y),assert(noPit(X,Y)),
    X1 is X + 1, X2 is X - 1, Y1 is Y + 1, Y2 is Y - 1,
    assert(noPit(X1,Y)),
    assert(noPit(X2,Y)),
    assert(noPit(X,Y1)),
    assert(noPit(X,Y2)),
    fail.
    
run_agent(_,_):- actCount(A),A > 90, retractall(gold(_)),assert(gold(1)),
    fail.
    
updateActCount:- actCount(A),retractall(actCount(_)),A1 is A + 1, assert(actCount(A1)).

run_agent([_,_,yes,_,_],grab):- curLocation(X,Y),assert(isSafe(X,Y)),
    gold(N), retractall(gold(N)), N1 is N+1, assert(gold(N1)),
    updateActCount,display_world.

run_agent([_,_,_,_,_], climb):- curLocation(1,1), gold(N),N > 0,
    updateActCount,display_world.
    
%run_agent([yes|_],shoot):- curLocation(1,1),display_world.
run_agent([yes|_],climb):- curLocation(1,1),turnCount(C),C >= 16,updateActCount,display_world.
run_agent([_,yes|_],climb):- curLocation(1,1),turnCount(C),C >= 16,updateActCount,display_world.
%run_agent([yes|_],climb):- curLocation(1,1),display_world.
%run_agent([_,yes|_],climb):- curLocation(1,1),display_world.

run_agent([_,_,_,yes,_],Act):-
    retractall(curLocation(_,_)), preLocation(X,Y),
    randomTurn(Act),
    assert(curLocation(X,Y)),
    updateActCount,display_world.

run_agent(_,goforward):- curLocation(X,Y),direction(D),
    ( D = 0,  X1 is X + 1, Y1 is Y;
      D = 90, X1 is X,     Y1 is Y + 1;
      D =180, X1 is X - 1, Y1 is Y;
      D =270, X1 is X,     Y1 is Y - 1),
      safe(X1,Y1),changeSaveLoc,
      retractall(turnCount(_)),assert(turnCount(0)),
    updateActCount,display_world.
    
run_agent([no,no,no,no,_], goforward):- curLocation(X,Y), assert(isSafe(X,Y)),changeSaveLoc,
    X1 is X + 1, X2 is X - 1, Y1 is Y + 1, Y2 is Y - 1,
    assert(isSafe(X1,Y)),
    assert(isSafe(X2,Y)),
    assert(isSafe(X,Y1)),
    assert(isSafe(X,Y2)),
    retractall(turnCount(_)),assert(turnCount(0)),
    updateActCount,display_world.
    
run_agent(_,goforward):- turnCount(C),C >= 20, changeSaveLoc,
    retractall(turnCount(_)),assert(turnCount(0)),updateActCount,display_world.

run_agent([yes|_],shoot):- arrow(1),retractall(arrow(_)),assert(arrow(0)),updateActCount,display_world.

run_agent([yes,_,_,_,_],Act):-
    turnCount(C),
    ( (C < 20, randomTurn(Act));
      (C >= 20, Act = goforwoard, changeSaveLoc, retractall(turnCount(_)),assert(turnCount(0))) ),
    updateActCount,display_world.

run_agent([_,yes,_,_,_],Act):-
    turnCount(C),
    ( (C < 20, randomTurn(Act));
      (C >= 20, Act = goforwoard, changeSaveLoc, retractall(turnCount(_)),assert(turnCount(0))) ),
    updateActCount,display_world.
    
    







     
     


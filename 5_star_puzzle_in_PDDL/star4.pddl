(define (problem star4)
  (:domain starpz)
  (:objects O C B A d1 d2 d3 d4 )
  (:init
    (isrod C)(isrod B)(isrod d1)
    (iscenter O)
    (smaller d1 C)(smaller d1 B)(smaller d1 A)
    (smaller d2 C)(smaller d2 B)(smaller d2 A)
    (smaller d3 C)(smaller d3 B)(smaller d3 A)
    (smaller d4 C)(smaller d4 B)(smaller d4 A)
    (smaller d1 O)(smaller d2 O)(smaller d3 O)(smaller d4 O)

    (smaller d1 d2)(smaller d1 d3)(smaller d1 d4)
    (smaller d2 d3)(smaller d2 d4)
    (smaller d3 d4)
    
    (clear C)(clear B)(clear d1)(clear O)
    (on d1 d2)(on d2 d3)(on d3 d4)(on d4 A)
  )
  (:goal 
    (and (on d1 d2)(on d2 d3)(on d3 d4)(on d4 C) )
  )
)

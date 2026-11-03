; Light: turn an initially unlit lamp on.
(define (domain light)
  (:requirements :strips)
  (:predicates (on ?l) (off ?l))
  (:action turn-on
    :parameters (?l)
    :precondition (off ?l)
    :effect (and (on ?l) (not (off ?l))))
)

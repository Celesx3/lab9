; Light-already-on: the goal holds initially, so no action is needed.
(define (problem light-already-on)
  (:domain light)
  (:objects lamp)
  (:init (on lamp))
  (:goal (on lamp))
)

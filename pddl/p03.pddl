; P03: reverse the tower a-b-c-d into d-c-b-a.
(define (problem p03)
  (:domain blocksworld)
  (:objects a b c d - block)
  (:init (on a b) (on b c) (on c d) (ontable d)
         (clear a) (handempty))
  (:goal (and (on d c) (on c b) (on b a)))
)

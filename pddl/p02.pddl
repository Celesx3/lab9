; P02: Sussman anomaly, initially c on a and b on the table.
(define (problem p02)
  (:domain blocksworld)
  (:objects a b c - block)
  (:init (on c a) (ontable a) (ontable b)
         (clear c) (clear b) (handempty))
  (:goal (and (on a b) (on b c)))
)

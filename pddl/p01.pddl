; P01: build a on b on c from three separate table blocks.
(define (problem p01)
  (:domain blocksworld)
  (:objects a b c - block)
  (:init (ontable a) (ontable b) (ontable c)
         (clear a) (clear b) (clear c) (handempty))
  (:goal (and (on a b) (on b c)))
)

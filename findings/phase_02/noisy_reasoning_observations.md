# noisy reasoning observations

observation 01

graph corruption can create shortcut reasoning paths.

example:

clean:
cat -> mammal -> animal -> living_thing

noisy:
cat -> living_thing

both produce a correct answer.

however the noisy path bypasses the expected ontology.

implication:

graph corruption can increase hallucination-like behavior
where answers remain correct but explanations become less
faithful to the underlying knowledge structure.
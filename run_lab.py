"""Reproduce the first half of Lab 9 and save actual planner/simulator logs."""

from importlib.metadata import version
from pathlib import Path
import subprocess
import sys

from sim import parse_plan


ROOT = Path(__file__).resolve().parent
PDDL = ROOT / "pddl"
RESULTS = ROOT / "results"


def run(command, log_name, expected_code=0):
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True,
                            encoding="utf-8", errors="replace", timeout=60)
    output = result.stdout + result.stderr
    (RESULTS / log_name).write_text(output, encoding="utf-8")
    if result.returncode != expected_code:
        raise RuntimeError(f"{log_name}: exit {result.returncode}\n{output}")
    return output


def main():
    RESULTS.mkdir(exist_ok=True)
    run([sys.executable, "-m", "pyperplan", "--help"], "pyperplan_help.txt")
    summary = [f"Python {sys.version.split()[0]}; pyperplan {version('pyperplan')}"]
    cases = [("light_domain.pddl", "light_problem.pddl", 1),
             ("light_domain.pddl", "light_already_on.pddl", 0),
             ("blocks_domain.pddl", "p01.pddl", 4),
             ("blocks_domain.pddl", "p02.pddl", 6),
             ("blocks_domain.pddl", "p03.pddl", 8)]
    for domain, problem, expected_length in cases:
        problem_path = PDDL / problem
        solution = Path(str(problem_path) + ".soln")
        # Remove stale output before solving; an old plan must not mask failure.
        solution.unlink(missing_ok=True)
        run([sys.executable, "-m", "pyperplan", "-s", "bfs",
             str(PDDL / domain), str(problem_path)], problem + ".planner.txt")
        plan = parse_plan(solution)
        if len(plan) != expected_length:
            raise AssertionError(f"{problem}: expected {expected_length}, got {len(plan)}")
        if problem == "light_problem.pddl" and plan != [("turn-on", ("lamp",))]:
            raise AssertionError("Unexpected light plan")
        if domain == "blocks_domain.pddl":
            run([sys.executable, str(ROOT / "sim.py"), str(problem_path)],
                problem + ".sim.txt")
        summary.append(f"PASS {problem}: {len(plan)} actions")

    examples = ROOT / "examples"
    examples.mkdir(exist_ok=True)
    for name, actions, expected_fragment in [
        ("invalid_stack", "(stack a b)\n", "step 0"),
        ("invalid_two_pickups", "(pick-up a)\n(pick-up b)\n", "step 1"),
    ]:
        # Generate these fixtures so the repository needs no .soln files.
        plan_path = examples / (name + ".soln")
        plan_path.write_text(actions, encoding="utf-8")
        output = run([sys.executable, str(ROOT / "sim.py"), str(PDDL / "p01.pddl"),
                      str(plan_path)], name + ".sim.txt", 1)
        if expected_fragment not in output or "missing precondition" not in output:
            raise AssertionError(f"{name}: wrong rejection reason")
        if name == "invalid_two_pickups" and "(handempty)" not in output.split("missing precondition:")[-1]:
            raise AssertionError("Second pickup must fail because the hand is occupied")
        summary.append(f"PASS {name}: rejected at {expected_fragment}")
    text = "\n".join(summary) + "\n"
    (RESULTS / "summary.txt").write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()

"""Independent Blocksworld STRIPS simulator for Lab 9, Step 5.

The action rules below are explicit; no planner operators are imported.
Only the problem's positive init/goal facts are read from PDDL.
"""

import argparse
from pathlib import Path
import re


def applicable(state, pre):
    return pre <= state


def apply(state, add, delete):
    """Delete first, then add; never mutate the input state."""
    return frozenset((state - delete) | add)


def make_action(name, args):
    """Return (precondition, add, delete) sets for a grounded action."""
    arities = {"pick-up": 1, "put-down": 1, "stack": 2, "unstack": 2}
    if name not in arities:
        raise ValueError(f"Unknown action: {name}")
    if len(args) != arities[name]:
        raise ValueError(f"{name} requires {arities[name]} arguments")
    x = args[0]
    if name == "pick-up":
        return (
            {("ontable", x), ("clear", x), ("handempty",)},
            {("holding", x)},
            {("ontable", x), ("clear", x), ("handempty",)},
        )
    if name == "put-down":
        return (
            {("holding", x)},
            {("ontable", x), ("clear", x), ("handempty",)},
            {("holding", x)},
        )
    y = args[1]
    if name == "stack":
        return (
            {("holding", x), ("clear", y)},
            {("on", x, y), ("clear", x), ("handempty",)},
            {("holding", x), ("clear", y)},
        )
    return (
        {("on", x, y), ("clear", x), ("handempty",)},
        {("holding", x), ("clear", y)},
        {("on", x, y), ("clear", x), ("handempty",)},
    )


def parse_plan(path):
    """Read one parenthesized action per line, ignoring PDDL comments."""
    plan = []
    for number, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        line = line.partition(";")[0].strip().lower()
        if not line:
            continue
        if not re.fullmatch(r"\([a-z][a-z0-9-]*(?:\s+[a-z0-9-]+)*\)", line):
            raise ValueError(f"Invalid plan syntax on line {number}: {line}")
        name, *args = line[1:-1].split()
        plan.append((name, tuple(args)))
    return plan


def format_facts(facts):
    return ", ".join("(" + " ".join(fact) + ")" for fact in sorted(facts))


def check(init, goal, plan):
    """Print a full trace and return success. Action indices start at zero."""
    state = frozenset(init)
    print("Initial:", format_facts(state))
    for step, (name, args) in enumerate(plan):
        label = "(" + " ".join((name, *args)) + ")"
        try:
            pre, add, delete = make_action(name, args)
        except ValueError as error:
            print(f"FAIL at step {step}: {error}")
            return False
        if not applicable(state, pre):
            print(f"FAIL at step {step}: {label}; missing precondition: "
                  + format_facts(pre - state))
            return False
        state = apply(state, add, delete)
        print(f"Step {step}: {label} -> {format_facts(state)}")
    missing = set(goal) - state
    if missing:
        print("FAIL: goal not reached; missing:", format_facts(missing))
        return False
    print(f"PASS: goal reached in {len(plan)} actions.")
    return True


def read_problem(path):
    """Read positive init/goal atoms from these lab STRIPS problems.

    This intentionally small S-expression reader is not a full PDDL parser.
    The planner parses and type-checks the complete PDDL separately.
    """
    text = re.sub(r";[^\n]*", "", Path(path).read_text(encoding="utf-8")).lower()
    tokens = re.findall(r"\(|\)|[^\s()]+", text)
    stack, roots = [], []
    for token in tokens:
        if token == "(":
            node = []
            (stack[-1] if stack else roots).append(node)
            stack.append(node)
        elif token == ")":
            if not stack:
                raise ValueError("Unmatched closing parenthesis")
            stack.pop()
        else:
            if not stack:
                raise ValueError("Text outside a PDDL expression")
            stack[-1].append(token)
    if stack or len(roots) != 1:
        raise ValueError("Unbalanced or multiple PDDL expressions")
    root = roots[0]
    if not root or root[0] != "define":
        raise ValueError("Expected a define expression")
    sections = {part[0]: part[1:] for part in root[1:] if isinstance(part, list) and part}

    def atom(node):
        if not isinstance(node, list) or not node or not all(isinstance(x, str) for x in node):
            raise ValueError("Expected a positive ground atom")
        if node[0] in {"and", "not", "or", "exists", "forall", "="}:
            raise ValueError("Only positive ground atoms are supported")
        return tuple(node)

    init = frozenset(atom(node) for node in sections[":init"])
    goal_node, = sections[":goal"]
    goal_atoms = goal_node[1:] if goal_node and goal_node[0] == "and" else [goal_node]
    return init, frozenset(atom(node) for node in goal_atoms)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("problem", type=Path)
    parser.add_argument("plan", type=Path, nargs="?", help="Defaults to PROBLEM.soln")
    args = parser.parse_args()
    try:
        init, goal = read_problem(args.problem)
        plan = parse_plan(args.plan or Path(str(args.problem) + ".soln"))
        return 0 if check(init, goal, plan) else 1
    except (OSError, ValueError, KeyError) as error:
        print(f"ERROR: {error}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

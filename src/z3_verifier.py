from z3 import Solver, Bool, And, Or, Not, Xor, Implies, unsat


def to_z3(expr, variables, entity=None):
    t = expr["type"]

    # Atomic predicate
    if t == "atom":
        arguments = expr.get("arguments")

        # Binary / multi-argument predicate
        if arguments and len(arguments) > 1:
            normalized_arguments = []

            for arg in arguments:
                if arg == "x" and entity is not None:
                    arg = entity

                normalized_arguments.append(arg)

            name = (
                f"{expr['predicate']}_"
                + "_".join(normalized_arguments)
            )

        else:
            current_entity = expr["entity"]

            if current_entity == "x" and entity is not None:
                current_entity = entity

            name = f"{expr['predicate']}_{current_entity}"

        if name not in variables:
            variables[name] = Bool(name)

        return variables[name]

    # Negation
    if t == "not":
        return Not(
            to_z3(
                expr["operand"],
                variables,
                entity
            )
        )

    # AND
    if t == "and":
        return And(
            to_z3(expr["left"], variables, entity),
            to_z3(expr["right"], variables, entity)
        )

    # OR
    if t == "or":
        return Or(
            to_z3(expr["left"], variables, entity),
            to_z3(expr["right"], variables, entity)
        )

    # XOR
    if t == "xor":
        return Xor(
            to_z3(expr["left"], variables, entity),
            to_z3(expr["right"], variables, entity)
        )

    # Implication
    if t == "implies":
        return Implies(
            to_z3(expr["left"], variables, entity),
            to_z3(expr["right"], variables, entity)
        )

    # Universal quantifier
    #
    # The actual grounding is performed in verify_formulas()
    # because it needs access to the complete set of entities.
    if t == "forall":
        return to_z3(
            expr["body"],
            variables,
            entity
        )

    # Existential quantifier
    #
    # The actual grounding is performed in verify_formulas().
    if t == "exists":
        return to_z3(
            expr["body"],
            variables,
            entity
        )

    raise ValueError(
        f"Unsupported expression type: {t}"
    )


def extract_entities(expr):
    entities = set()

    if expr["type"] == "atom":

        arguments = expr.get("arguments")

        if arguments:
            for argument in arguments:
                if argument != "x":
                    entities.add(argument)

        elif expr["entity"] != "x":
            entities.add(expr["entity"])

    elif expr["type"] == "not":
        entities.update(
            extract_entities(expr["operand"])
        )

    elif expr["type"] in {"forall", "exists"}:
        entities.update(
            extract_entities(expr["body"])
        )

    elif expr["type"] in {
        "and",
        "or",
        "xor",
        "implies"
    }:
        entities.update(
            extract_entities(expr["left"])
        )

        entities.update(
            extract_entities(expr["right"])
        )

    return entities


def verify_formulas(formulas, query):
    solver = Solver()
    variables = {}

    entities = set()

    # Collect entities from premises
    for formula in formulas:
        entities.update(
            extract_entities(formula)
        )

    # Collect entities from query
    entities.update(
        extract_entities(query)
    )

    for formula in formulas:

        # Universal quantifier:
        # instantiate over every known entity.
        if formula["type"] == "forall":

            for entity in entities:
                solver.add(
                    to_z3(
                        formula,
                        variables,
                        entity
                    )
                )

        # Existential quantifier:
        #
        # For this finite-grounded implementation,
        # the existential statement is true if at least
        # one known entity satisfies the body.
        elif formula["type"] == "exists":

            existential_candidates = []

            for entity in entities:
                existential_candidates.append(
                    to_z3(
                        formula,
                        variables,
                        entity
                    )
                )

            if existential_candidates:
                solver.add(
                    Or(*existential_candidates)
                )

        else:
            solver.add(
                to_z3(
                    formula,
                    variables
                )
            )

    query_expr = to_z3(
        query,
        variables
    )

    # Check whether query is necessarily true.
    solver.push()

    solver.add(
        Not(query_expr)
    )

    if solver.check() == unsat:
        solver.pop()

        return {
            "valid": True,
            "truth": True,
            "message": (
                "The query logically follows "
                "from the premises."
            )
        }

    solver.pop()

    # Check whether query is necessarily false.
    solver.push()

    solver.add(
        query_expr
    )

    if solver.check() == unsat:
        solver.pop()

        return {
            "valid": True,
            "truth": False,
            "message": (
                "The negation of the query logically "
                "follows from the premises."
            )
        }

    solver.pop()

    return {
        "valid": True,
        "truth": None,
        "message": (
            "The premises do not determine the query."
        )
    }


if __name__ == "__main__":

    from src.fol_parser import parse_formula

    print("Testing direct fact...")

    formulas = [
        parse_formula("Student(rina)")
    ]

    query = parse_formula("Student(rina)")

    print(
        verify_formulas(
            formulas,
            query
        )
    )

    print("\nTesting rule inference...")

    formulas = [
        parse_formula("∀x (Student(x) → Person(x))"),
        parse_formula("Student(rina)")
    ]

    query = parse_formula("Person(rina)")

    print(
        verify_formulas(
            formulas,
            query
        )
    )

    print("\nTesting unknown...")

    formulas = [
        parse_formula("Student(rina)")
    ]

    query = parse_formula("Musician(rina)")

    print(
        verify_formulas(
            formulas,
            query
        )
    )

    print("\nTesting negative fact...")

    formulas = [
        parse_formula("¬Student(rina)")
    ]

    query = parse_formula("Student(rina)")

    print(
        verify_formulas(
            formulas,
            query
        )
    )

    print("\nTesting binary predicate...")

    formulas = [
        parse_formula("Love(miroslav, music)")
    ]

    query = parse_formula("Love(miroslav, music)")

    print(
        verify_formulas(
            formulas,
            query
        )
    )

    print("\nTesting existential quantifier...")

    formulas = [
        parse_formula(
            "∃x (Musician(x) → Love(x, music))"
        )
    ]

    query = parse_formula(
        "Love(miroslav, music)"
    )

    print(
        verify_formulas(
            formulas,
            query
        )
    )
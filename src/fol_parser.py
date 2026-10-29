import re


def normalize_entity(entity):
    """
    Normalize entity names so different spellings refer to the same constant.

    Examples:
        seaEel   -> sea_eel
        SeaEel   -> sea_eel
        sea_eel  -> sea_eel
    """
    entity = entity.strip()

    # camelCase / PascalCase -> snake_case
    entity = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", entity)

    return entity.lower()


def normalize_formula(formula):
    formula = formula.strip()

    # Normalize whitespace
    formula = re.sub(r"\s+", " ", formula)

    # Normalize common ASCII operators to the symbols
    # expected by the parser
    formula = formula.replace("->", "→")

    return formula

def parse_atom(formula):
    formula = normalize_formula(formula)

    if formula.startswith("¬"):
        atom = formula[1:].strip()

        return {
            "type": "not",
            "operand": parse_atom(atom)
        }

    # Supports:
    # Predicate(entity)
    # Predicate(entity1, entity2)
    match = re.fullmatch(
        r"(\w+)\s*\(\s*(.*?)\s*\)",
        formula
    )

    if not match:
        raise ValueError(f"Unsupported atom: {formula}")

    predicate = match.group(1).lower()

    arguments = [
        normalize_entity(arg.strip())
        for arg in match.group(2).split(",")
    ]

    if len(arguments) == 1:
        return {
            "type": "atom",
            "predicate": predicate,
            "entity": arguments[0]
        }

    return {
        "type": "atom",
        "predicate": predicate,
        "entity": arguments[0],
        "arguments": arguments
    }


def parse_formula(formula):
    formula = normalize_formula(formula)

    # Universal quantifier
    if formula.startswith("∀x"):
        body = formula[2:].strip()

        if body.startswith("(") and body.endswith(")"):
            body = body[1:-1].strip()

        return {
            "type": "forall",
            "body": parse_expression(body)
        }

    # Existential quantifier
    if formula.startswith("∃x"):
        body = formula[2:].strip()

        if body.startswith("(") and body.endswith(")"):
            body = body[1:-1].strip()

        return {
            "type": "exists",
            "body": parse_expression(body)
        }

    return parse_expression(formula)


def parse_expression(formula):
    formula = normalize_formula(formula)

    while (
        formula.startswith("(")
        and formula.endswith(")")
        and is_balanced(formula[1:-1])
    ):
        formula = formula[1:-1].strip()

    # Implication
    position = find_operator(formula, "→")

    if position != -1:
        return {
            "type": "implies",
            "left": parse_expression(formula[:position]),
            "right": parse_expression(formula[position + 1:])
        }

    # XOR
    position = find_operator(formula, "⊕")

    if position != -1:
        return {
            "type": "xor",
            "left": parse_expression(formula[:position]),
            "right": parse_expression(formula[position + 1:])
        }

    # OR
    position = find_operator(formula, "∨")

    if position != -1:
        return {
            "type": "or",
            "left": parse_expression(formula[:position]),
            "right": parse_expression(formula[position + 1:])
        }

    # AND
    position = find_operator(formula, "∧")

    if position != -1:
        return {
            "type": "and",
            "left": parse_expression(formula[:position]),
            "right": parse_expression(formula[position + 1:])
        }

    # Negation
    if formula.startswith("¬"):
        return {
            "type": "not",
            "operand": parse_expression(formula[1:].strip())
        }

    return parse_atom(formula)


def find_operator(formula, operator):
    depth = 0

    for i, char in enumerate(formula):

        if char == "(":
            depth += 1

        elif char == ")":
            depth -= 1

        elif char == operator and depth == 0:
            return i

    return -1


def is_balanced(formula):
    depth = 0

    for char in formula:

        if char == "(":
            depth += 1

        elif char == ")":
            depth -= 1

        if depth < 0:
            return False

    return depth == 0

import re

from src.llm_reasoner import load_model


# ============================================================
# SYMBOL EXTRACTION
# ============================================================

def extract_symbols(premises_fol):
    """
    Extract predicates and named entities from the formal premises.
    """

    predicates = set()
    entities = set()

    for formula in premises_fol:

        # ----------------------------------------------------
        # Predicate names
        # ----------------------------------------------------

        for match in re.finditer(
            r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\(",
            formula
        ):
            name = match.group(1)

            if name.lower() not in {
                "forall",
                "exists",
                "x",
                "y",
                "z"
            }:
                predicates.add(name)

        # ----------------------------------------------------
        # Arguments / entities
        # ----------------------------------------------------

        for match in re.finditer(
            r"\b[A-Za-z_][A-Za-z0-9_]*\s*\(([^()]*)\)",
            formula
        ):
            arguments = match.group(1)

            for argument in arguments.split(","):

                argument = argument.strip()

                if argument.lower() in {
                    "x",
                    "y",
                    "z"
                }:
                    continue

                if re.fullmatch(
                    r"[A-Za-z_][A-Za-z0-9_]*",
                    argument
                ):
                    entities.add(argument)

    return sorted(predicates), sorted(entities)


# ============================================================
# NORMALIZATION
# ============================================================

def normalize_entity(entity):
    """
    Convert names such as seaEel -> sea_eel.
    """

    entity = entity.strip()

    entity = re.sub(
        r"(?<=[a-z0-9])(?=[A-Z])",
        "_",
        entity
    )

    return entity.lower()


def normalize_text(text):
    """
    Normalize natural-language text for matching.
    """

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# ENTITY MATCHING
# ============================================================

def find_entity(conclusion, entities):
    """
    Find the entity mentioned in the natural-language conclusion.
    """

    normalized_conclusion = normalize_text(
        conclusion
    )

    # Prefer longest entity names first.
    ordered_entities = sorted(
        entities,
        key=len,
        reverse=True
    )

    for entity in ordered_entities:

        normalized_entity = normalize_text(
            entity.replace("_", " ")
        )

        if normalized_entity in normalized_conclusion:
            return normalize_entity(entity)

    # Handle common full-name forms.
    conclusion_words = normalized_conclusion.split()

    for entity in ordered_entities:

        normalized_entity = normalize_entity(
            entity
        )

        entity_words = normalized_entity.split("_")

        if all(
            word in conclusion_words
            for word in entity_words
        ):
            return normalized_entity

    return None


# ============================================================
# PREDICATE MATCHING
# ============================================================

def predicate_aliases(predicate):
    """
    Generate natural-language forms for a predicate.
    """

    p = predicate.lower()

    aliases = {
        p,
        p.rstrip("s"),
        p + "s",
    }

    if p.endswith("s"):
        aliases.add(
            p[:-1]
        )

    # Common FOLIO wording variations.
    special = {
        "drinks": [
            "drink",
            "drinks",
            "drinking",
            "regularly drinks",
            "regularly drink",
        ],

        "jokes": [
            "joke",
            "jokes",
            "joking",
        ],

        "loves": [
            "love",
            "loves",
            "loved",
        ],

        "specialize": [
            "specialize",
            "specialized",
            "specialises",
            "specializes",
        ],

        "breathe": [
            "breathe",
            "breathes",
            "breathing",
        ],

        "paper": [
            "paper",
        ],

        "person": [
            "person",
            "people",
        ],
    }

    aliases.update(
        special.get(p, [])
    )

    return aliases


def find_predicate(
    conclusion,
    predicates
):
    """
    Find the predicate expressed in the conclusion.

    Uses only predicates that actually occur
    in the formal premises.
    """

    text = normalize_text(
        conclusion
    )

    candidates = []

    for predicate in predicates:

        for alias in predicate_aliases(
            predicate
        ):

            alias_normalized = normalize_text(
                alias
            )

            if not alias_normalized:
                continue

            pattern = (
                r"\b"
                + re.escape(alias_normalized)
                + r"\b"
            )

            if re.search(
                pattern,
                text
            ):
                candidates.append(
                    (
                        len(alias_normalized),
                        predicate
                    )
                )

    if not candidates:
        return None

    # Prefer the longest natural-language match.
    candidates.sort(
        reverse=True
    )

    return candidates[0][1]


# ============================================================
# POLARITY
# ============================================================

def has_negation(conclusion):
    """
    Detect explicit negative wording.
    """

    text = normalize_text(
        conclusion
    )

    negative_patterns = [
        r"\bnot\b",
        r"\bnever\b",
        r"\bno\b",
        r"\bis not\b",
        r"\bare not\b",
        r"\bdoes not\b",
        r"\bdoesnt\b",
        r"\bdo not\b",
        r"\bdont\b",
    ]

    return any(
        re.search(
            pattern,
            text
        )
        for pattern in negative_patterns
    )


# ============================================================
# LOGICAL CONNECTIVE DETECTION
# ============================================================

def split_logical_parts(conclusion):
    """
    Split a natural-language conclusion into logical parts.

    Supports:
        A or B
        A and B

    Returns:
        ("or", parts)
        ("and", parts)
        (None, [conclusion])
    """

    # OR has lower precedence than AND,
    # so split OR first.

    or_parts = re.split(
        r"\bor\b",
        conclusion,
        flags=re.IGNORECASE
    )

    if len(or_parts) > 1:
        return "or", [
            part.strip()
            for part in or_parts
            if part.strip()
        ]

    and_parts = re.split(
        r"\band\b",
        conclusion,
        flags=re.IGNORECASE
    )

    if len(and_parts) > 1:
        return "and", [
            part.strip()
            for part in and_parts
            if part.strip()
        ]

    return None, [
        conclusion.strip()
    ]


# ============================================================
# DETERMINISTIC FORMALIZATION
# ============================================================

def deterministic_formalize(
    conclusion,
    predicates,
    entities,
    inherited_entity=None
):
    """
    Convert a natural-language conclusion into FOL
    without using Qwen whenever possible.

    The important feature here is that an entity found
    in the complete conclusion is inherited by sub-parts.

    Example:

        Sea eel breathes or is a paper.

    becomes:

        Breathe(sea_eel) ∨ Paper(sea_eel)
    """

    conclusion = conclusion.strip()

    if not conclusion:
        return None

    # --------------------------------------------------------
    # Find entity
    # --------------------------------------------------------

    entity = find_entity(
        conclusion,
        entities
    )

    # If this is a sub-expression such as:
    #
    # "is a paper"
    #
    # it may not repeat the entity. Use the entity
    # discovered from the parent expression.

    if entity is None:
        entity = inherited_entity

    if entity is None:
        return None

    # --------------------------------------------------------
    # Split logical connective
    # --------------------------------------------------------

    operator, parts = split_logical_parts(
        conclusion
    )

    if operator is not None:

        formulas = []

        for part in parts:

            result = deterministic_formalize(
                part,
                predicates,
                entities,
                inherited_entity=entity
            )

            if result is None:
                return None

            formulas.append(
                result
            )

        if operator == "or":
            return " ∨ ".join(formulas)

        if operator == "and":
            return " ∧ ".join(formulas)

    # --------------------------------------------------------
    # Predicate
    # --------------------------------------------------------

    predicate = find_predicate(
        conclusion,
        predicates
    )

    if predicate is None:
        return None

    predicate = predicate.strip()

    # --------------------------------------------------------
    # Negation
    # --------------------------------------------------------

    negative = has_negation(
        conclusion
    )

    formula = (
        f"{predicate}({entity})"
    )

    if negative:
        formula = (
            f"¬{formula}"
        )

    return formula


# ============================================================
# QWEN FALLBACK
# ============================================================

def qwen_formalize(
    conclusion,
    predicates,
    entities,
    premises_fol,
    premises_text
):
    """
    Ask Qwen for structured extraction.

    Qwen is NOT allowed to directly generate arbitrary FOL.

    It extracts:
        ENTITY
        PREDICATE
        OPERATOR
        NEGATED

    For compound conclusions, multiple blocks may be returned.
    """

    tokenizer, model = load_model()

    predicate_list = ", ".join(
        predicates
    )

    entity_list = ", ".join(
        entities
    )

    messages = [
        {
            "role": "system",
            "content": (
                "You extract logical information from a conclusion.\n\n"

                "DO NOT generate First-Order Logic.\n\n"

                "For every logical part of the conclusion, "
                "return one block using exactly:\n"
                "ENTITY=<entity>\n"
                "PREDICATE=<predicate>\n"
                "NEGATED=<true or false>\n\n"

                "If the conclusion contains OR or AND, "
                "return one block for each part.\n\n"

                f"Allowed entities: {entity_list}\n"
                f"Allowed predicates: {predicate_list}\n\n"

                "Use ONLY the allowed entity and predicate names.\n"
                "Never invent an entity.\n"
                "Never invent a predicate.\n"
                "Never add explanations."
            )
        },
        {
            "role": "user",
            "content": (
                f"Premises:\n{premises_text}\n\n"
                f"Formal premises:\n{premises_fol}\n\n"
                f"Conclusion:\n{conclusion}\n"
            )
        }
    ]

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt"
    )

    outputs = model.generate(
        **inputs,
        max_new_tokens=80,
        do_sample=False
    )

    input_length = inputs[
        "input_ids"
    ].shape[1]

    generated_tokens = outputs[0][
        input_length:
    ]

    response = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True
    ).strip()

    print(
        "\n========== QWEN EXTRACTION =========="
    )

    print(response)

    # --------------------------------------------------------
    # Parse every structured block
    # --------------------------------------------------------

    pattern = re.compile(
        r"ENTITY\s*=\s*([A-Za-z_][A-Za-z0-9_]*)"
        r".*?"
        r"PREDICATE\s*=\s*([A-Za-z_][A-Za-z0-9_]*)"
        r".*?"
        r"NEGATED\s*=\s*(true|false)",
        re.IGNORECASE | re.DOTALL
    )

    matches = pattern.findall(
        response
    )

    if not matches:
        return None

    valid_entities = {
        normalize_entity(e)
        for e in entities
    }

    valid_predicates = {
        p.lower(): p
        for p in predicates
    }

    formulas = []

    for entity_raw, predicate_raw, negated_raw in matches:

        entity = normalize_entity(
            entity_raw
        )

        predicate_key = predicate_raw.lower()

        # Validate entity.
        if entity not in valid_entities:
            continue

        # Validate predicate.
        if predicate_key not in valid_predicates:
            continue

        predicate = valid_predicates[
            predicate_key
        ]

        negated = (
            negated_raw.lower()
            == "true"
        )

        formula = (
            f"{predicate}({entity})"
        )

        if negated:
            formula = (
                f"¬{formula}"
            )

        formulas.append(
            formula
        )

    if not formulas:
        return None

    # --------------------------------------------------------
    # Determine compound connective from conclusion
    # --------------------------------------------------------

    if re.search(
        r"\bor\b",
        conclusion,
        flags=re.IGNORECASE
    ):
        return " ∨ ".join(
            formulas
        )

    if re.search(
        r"\band\b",
        conclusion,
        flags=re.IGNORECASE
    ):
        return " ∧ ".join(
            formulas
        )

    return formulas[0]


# ============================================================
# MAIN FORMALIZER
# ============================================================

def formalize_conclusion(
    conclusion,
    premises_fol=None,
    premises_text=None
):
    """
    Convert a natural-language conclusion into FOL.

    Strategy:

        1. Deterministic extraction
        2. Qwen structured extraction fallback
        3. Return only validated predicates/entities

    Examples:

        "Sea eel breathes."
            ->
        Breathe(sea_eel)

        "Sea eel breathes or is a paper."
            ->
        Breathe(sea_eel) ∨ Paper(sea_eel)

        "Sea eel breathes and is a paper."
            ->
        Breathe(sea_eel) ∧ Paper(sea_eel)

        "Sea eel does not breathe."
            ->
        ¬Breathe(sea_eel)
    """

    premises_fol = premises_fol or []

    predicates, entities = extract_symbols(
        premises_fol
    )

    print(
        "\n========== FORMALIZATION =========="
    )

    print(
        "Conclusion:",
        conclusion
    )

    print(
        "Allowed predicates:",
        predicates
    )

    print(
        "Allowed entities:",
        entities
    )

    # --------------------------------------------------------
    # STEP 1: Deterministic
    # --------------------------------------------------------

    result = deterministic_formalize(
        conclusion,
        predicates,
        entities
    )

    if result is not None:

        print(
            "Method: deterministic"
        )

        print(
            "FOL:",
            result
        )

        return result

    # --------------------------------------------------------
    # STEP 2: Qwen fallback
    # --------------------------------------------------------

    print(
        "Deterministic extraction failed."
    )

    print(
        "Method: Qwen structured extraction"
    )

    result = qwen_formalize(
        conclusion,
        predicates,
        entities,
        premises_fol,
        premises_text
    )

    if result is not None:

        print(
            "FOL:",
            result
        )

        return result

    # --------------------------------------------------------
    # STEP 3: Fail safely
    # --------------------------------------------------------

    raise ValueError(
        "Could not safely formalize the conclusion "
        "using the available predicates and entities."
    )


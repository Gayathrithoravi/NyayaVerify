def validate_structure(reasoning):
    required_sections = [
        "samshaya",
        "pramana",
        "pancha_avayava",
        "tarka",
        "hetvabhasa",
        "nirnaya",
        "conclusion"
    ]

    missing_sections = []

    for section in required_sections:
        if section not in reasoning:
            missing_sections.append(section)

    missing_pancha_avayava = []

    pancha = reasoning.get(
        "pancha_avayava",
        {}
    )

    if not isinstance(pancha, dict):
        pancha = {}

    required_pancha = [
        "pratijna",
        "hetu",
        "udaharana",
        "upanaya",
        "nigamana"
    ]

    for item in required_pancha:
        if item not in pancha:
            missing_pancha_avayava.append(item)

    return {
        "valid": (
            len(missing_sections) == 0
            and len(missing_pancha_avayava) == 0
        ),
        "missing_sections": missing_sections,
        "missing_pancha_avayava": missing_pancha_avayava
    }
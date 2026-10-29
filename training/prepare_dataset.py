import json
from pathlib import Path


def create_nyaya_record(
    problem,
    samshaya,
    pramana,
    pratijna,
    hetu,
    udaharana,
    upanaya,
    nigamana,
    tarka,
    hetvabhasa,
    nirnaya,
    label
):
    return {
        "instruction": "Solve the logical problem using the six Nyaya stages.",
        "input": problem,
        "output": {
            "samshaya": samshaya,
            "pramana": pramana,
            "pancha_avayava": {
                "pratijna": pratijna,
                "hetu": hetu,
                "udaharana": udaharana,
                "upanaya": upanaya,
                "nigamana": nigamana
            },
            "tarka": tarka,
            "hetvabhasa": hetvabhasa,
            "nirnaya": nirnaya,
            "label": label
        }
    }


def main():

    examples = []

    # Example 1
    examples.append(
        create_nyaya_record(
            problem=(
                "All squares have four sides. "
                "All four-sided things are shapes. "
                "Therefore, all squares are shapes."
            ),
            samshaya=(
                "It is uncertain whether being a square is sufficient "
                "to establish that something is a shape."
            ),
            pramana=(
                "The premises state that every square has four sides "
                "and every four-sided thing is a shape."
            ),
            pratijna="All squares are shapes.",
            hetu="Squares have four sides.",
            udaharana=(
                "Whatever has four sides is a shape, according to the premise."
            ),
            upanaya=(
                "A square has four sides, so the rule applies to the square."
            ),
            nigamana="Therefore, the square is a shape.",
            tarka=(
                "If a square were not a shape, then it would contradict "
                "the rule that every four-sided thing is a shape."
            ),
            hetvabhasa="No fallacy is detected.",
            nirnaya="The conclusion follows from the premises.",
            label="True"
        )
    )

    # Example 2
    examples.append(
        create_nyaya_record(
            problem="Rock is a turtle. Is Rock a turtle?",
            samshaya="There is a question about whether Rock is a turtle.",
            pramana="The premise directly states that Rock is a turtle.",
            pratijna="Rock is a turtle.",
            hetu="The premise explicitly identifies Rock as a turtle.",
            udaharana="A statement directly asserting a fact supports that fact.",
            upanaya="The statement applies directly to Rock.",
            nigamana="Therefore, Rock is a turtle.",
            tarka="Assuming Rock is not a turtle contradicts the given premise.",
            hetvabhasa="No fallacy is detected.",
            nirnaya="Rock is a turtle.",
            label="True"
        )
    )

    # Example 3
    examples.append(
        create_nyaya_record(
            problem="Tom is an ocellated wild turkey. Is Tom an ocellated wild turkey?",
            samshaya=(
                "It must be determined whether the premise supports "
                "the conclusion about Tom."
            ),
            pramana="The premise directly states the property of Tom.",
            pratijna="Tom is an ocellated wild turkey.",
            hetu="Tom is explicitly described as an ocellated wild turkey.",
            udaharana="A directly stated fact supports the same conclusion.",
            upanaya="The fact applies directly to Tom.",
            nigamana="Therefore, Tom is an ocellated wild turkey.",
            tarka="Denying the conclusion would contradict the given fact.",
            hetvabhasa="No fallacy is detected.",
            nirnaya="Tom is an ocellated wild turkey.",
            label="True"
        )
    )

    # Example 4
    examples.append(
        create_nyaya_record(
            problem="Marvin is not from Mars. Is Marvin an alien?",
            samshaya=(
                "It is uncertain whether Marvin being not from Mars "
                "is sufficient to establish that Marvin is an alien."
            ),
            pramana=(
                "The premise only states that Marvin is not from Mars; "
                "it does not establish that Marvin is an alien."
            ),
            pratijna="Marvin is an alien.",
            hetu="No sufficient premise establishes that Marvin is an alien.",
            udaharana=(
                "A conclusion cannot be established when the premises "
                "do not provide a supporting rule or fact."
            ),
            upanaya=(
                "The available premise about Marvin does not establish alien status."
            ),
            nigamana="Therefore, Marvin cannot be established as an alien.",
            tarka=(
                "Assuming that Marvin is an alien does not follow from "
                "the premise that he is not from Mars."
            ),
            hetvabhasa="The reasoning would contain an unsupported inference.",
            nirnaya="The conclusion 'Marvin is an alien' is not supported.",
            label="False"
        )
    )

    output_path = Path("training/nyaya_training_examples.json")

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(examples, file, indent=2, ensure_ascii=False)

    print(f"Created {len(examples)} Nyaya training examples.")
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    main()
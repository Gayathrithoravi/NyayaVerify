from flask import Flask, request, jsonify
from flask_cors import CORS

from src.pipeline import run_pipeline


app = Flask(__name__)

CORS(app)


@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "status": "running",
        "service": "NyayaVerify API"
    })


@app.route("/verify", methods=["POST"])
def verify():

    data = request.get_json()

    premises = data.get("premises", "")
    conclusion = data.get("conclusion", "")

    if not premises.strip():

        return jsonify({
            "error": "Premises are required."
        }), 400


    if not conclusion.strip():

        return jsonify({
            "error": "Conclusion is required."
        }), 400


    try:

        # Convert the text premises into a list.
        premises_text = [
            line.strip()
            for line in premises.split("\n")
            if line.strip()
        ]


        # Temporary simple FOL conversion
        # for the frontend connection test.
        #
        # The full FOLIO-based formalization
        # will be connected later.

        premises_fol = []

        for premise in premises_text:

            lower = premise.lower()

            if lower == "ravi is a researcher.":

                premises_fol.append(
                    "Researcher(ravi)"
                )

            elif lower == "every researcher is curious.":

                premises_fol.append(
                    "∀x (Researcher(x)→Curious(x))"
                )


        result = run_pipeline(
            problem=(
                "Determine whether the conclusion "
                "follows from the given premises."
            ),
            conclusion=conclusion,
            premises_fol=premises_fol,
            premises_text=premises_text
        )


        verification = result[
            "logical_verification"
        ]


        truth = verification.get(
            "truth"
        )


        if truth is True:

            prediction = "TRUE"

        elif truth is False:

            prediction = "FALSE"

        else:

            prediction = "UNKNOWN"


        return jsonify({

            "status": "success",

            "result": prediction,

            "conclusion": conclusion,

            "formalized_conclusion":
                result[
                    "formalized_conclusion"
                ],

            "verification":
                verification,

            "reasoning":
                result[
                    "reasoning"
                ],

            "structure_validation":
                result[
                    "structure_validation"
                ]

        })


    except Exception as e:

        return jsonify({

            "status": "error",

            "error": str(e)

        }), 500


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
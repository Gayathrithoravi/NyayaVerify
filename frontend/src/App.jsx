import { useState } from "react";
import "./App.css";

const nyayaStages = [
  {
    number: "01",
    title: "Samshaya",
    subtitle: "Doubt / Uncertainty",
    description:
      "Identifies the logical question and determines what needs to be established.",
  },
  {
    number: "02",
    title: "Pramana",
    subtitle: "Evidence",
    description:
      "Examines the supplied premises as the supporting evidence for the conclusion.",
  },
  {
    number: "03",
    title: "Pancha Avayava",
    subtitle: "Five-Part Argument",
    description:
      "Constructs the five-part logical argument used to support the conclusion.",
  },
  {
    number: "04",
    title: "Tarka",
    subtitle: "Counter-Check",
    description:
      "Tests the reasoning through alternative possibilities and contradiction checks.",
  },
  {
    number: "05",
    title: "Hetvabhasa",
    subtitle: "Fallacy Check",
    description:
      "Checks whether the reasoning contains unsupported or invalid logical relationships.",
  },
  {
    number: "06",
    title: "Nirnaya",
    subtitle: "Final Determination",
    description:
      "Produces the final determination before formal logical verification.",
  },
];

function App() {
  const [premises, setPremises] = useState("");
  const [conclusion, setConclusion] = useState("");

  const [verified, setVerified] = useState(false);
  const [verifying, setVerifying] = useState(false);
  const [activeStage, setActiveStage] = useState(0);

  const [result, setResult] = useState("UNKNOWN");
  const [backendData, setBackendData] = useState(null);
  const [showDetails, setShowDetails] = useState(false);

  const handleVerify = async () => {
    if (!premises.trim() || !conclusion.trim()) {
      alert("Please enter both premises and a conclusion.");
      return;
    }

    setVerifying(true);
    setVerified(false);
    setShowDetails(false);
    setBackendData(null);
    setResult("UNKNOWN");
    setActiveStage(1);

    // Animate stages while backend works
    const stages = [1, 2, 3, 4, 5, 6];

    stages.forEach((stage, index) => {
      setTimeout(() => {
        setActiveStage(stage);
      }, index * 300);
    });

    try {
      const response = await fetch(
        "http://127.0.0.1:5000/verify",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            premises: premises,
            conclusion: conclusion,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.error || "Verification failed."
        );
      }

      setBackendData(data);

      if (data.result === "TRUE") {
        setResult("TRUE");
      } else if (data.result === "FALSE") {
        setResult("FALSE");
      } else {
        setResult("UNKNOWN");
      }

      setActiveStage(6);
      setVerified(true);
      setShowDetails(true);
    } catch (error) {
      console.error("Backend error:", error);

      alert(
        "Could not connect to the NyayaVerify backend.\n\n" +
          error.message
      );

      setVerified(false);
      setResult("UNKNOWN");
    } finally {
      setVerifying(false);
    }
  };

  const getResultClass = () => {
    if (result === "TRUE") {
      return "verified";
    }

    if (result === "FALSE") {
      return "false-result";
    }

    return "";
  };

  return (
    <div className="app">

      {/* ================= SIDEBAR ================= */}

      <aside className="sidebar">

        <div className="logo">

          <div className="logo-icon">
            N
          </div>

          <div>
            <h2>NyayaVerify</h2>
            <span>Explainable Logic</span>
          </div>

        </div>


        <nav>

          <a
            href="#verify"
            className="nav-item active"
          >
            <span>⌂</span>
            Verify Logic
          </a>

          <a
            href="#reasoning"
            className="nav-item"
          >
            <span>◈</span>
            Nyaya Reasoning
          </a>

          <a
            href="#formal"
            className="nav-item"
          >
            <span>◇</span>
            Formal Logic
          </a>

          <a
            href="#evaluation"
            className="nav-item"
          >
            <span>▣</span>
            Evaluation
          </a>

        </nav>


        <div className="sidebar-bottom">

          <div className="system-status">

            <span className="status-dot"></span>

            <div>
              <strong>
                System Online
              </strong>

              <small>
                Qwen + Z3
              </small>
            </div>

          </div>

        </div>

      </aside>


      {/* ================= MAIN ================= */}

      <main className="main">

        {/* ================= HEADER ================= */}

        <header className="header">

          <div>

            <p className="eyebrow">
              EXPLAINABLE AI · FORMAL VERIFICATION
            </p>

            <h1>
              Verify. Explain.
              <span> Reason.</span>
            </h1>

            <p className="subtitle">
              A local LLM reasoning system inspired by
              Navya-Nyaya, combined with First-Order Logic
              and Z3 theorem proving.
            </p>

          </div>


          <div className="header-badge">

            <span className="status-dot"></span>

            LOCAL MODEL

          </div>

        </header>


        {/* ================= INPUT ================= */}

        <section
          className="input-section"
          id="verify"
        >

          <div className="section-heading">

            <div>

              <span className="section-number">
                01
              </span>

              <div>
                <h2>
                  Give me a logical problem
                </h2>

                <p>
                  Enter premises and a conclusion
                  to verify.
                </p>
              </div>

            </div>

          </div>


          <div className="input-grid">

            <div className="input-card">

              <label>
                PREMISES
              </label>

              <textarea
                value={premises}
                onChange={(e) =>
                  setPremises(e.target.value)
                }
                placeholder={
                  "Example:\nRavi is a researcher.\nEvery researcher is curious."
                }
              />

            </div>


            <div className="input-card">

              <label>
                CONCLUSION
              </label>

              <textarea
                value={conclusion}
                onChange={(e) =>
                  setConclusion(e.target.value)
                }
                placeholder="Example: Ravi is curious."
              />

            </div>

          </div>


          <button
            className="verify-button"
            onClick={handleVerify}
            disabled={verifying}
          >

            {verifying ? (
              <>
                <span className="spinner"></span>
                Verifying Logic...
              </>
            ) : (
              <>
                Verify with Nyaya
                <span className="arrow">
                  →
                </span>
              </>
            )}

          </button>

        </section>


        {/* ================= REASONING ================= */}

        <section
          id="reasoning"
        >

          <div className="section-heading">

            <div>

              <span className="section-number">
                02
              </span>

              <div>

                <h2>
                  Six stages of reasoning
                </h2>

                <p>
                  The logical problem passes through
                  six structured Nyaya stages.
                </p>

              </div>

            </div>

          </div>


          <div className="reasoning-grid">

            {nyayaStages.map((stage) => {

              const stageNumber =
                Number(stage.number);

              const isActive =
                activeStage === stageNumber;

              const isComplete =
                activeStage > stageNumber ||
                verified;

              let statusClass = "waiting";
              let statusText = "WAITING";

              if (isActive && verifying) {
                statusClass = "processing";
                statusText = "PROCESSING";
              } else if (isComplete) {
                statusClass = "complete";
                statusText = "COMPLETE";
              }

              return (

                <div
                  key={stage.number}
                  className={`reasoning-card ${
                    isActive
                      ? "active-stage"
                      : ""
                  } ${
                    isActive && verifying
                      ? "processing-stage"
                      : ""
                  }`}
                >

                  <div className="card-top">

                    <span className="card-number">
                      {stage.number}
                    </span>

                    <span
                      className={`stage-status ${statusClass}`}
                    >
                      {statusText}
                    </span>

                  </div>


                  <h3>
                    {stage.title}
                  </h3>


                  <span className="card-subtitle">
                    {stage.subtitle}
                  </span>


                  <p>
                    {stage.description}
                  </p>

                </div>

              );

            })}

          </div>


          {/* PIPELINE PROGRESS */}

          <div className="pipeline-progress">

            <div className="progress-header">

              <span>
                NYAYA REASONING PIPELINE
              </span>

              <strong>
                {activeStage} / 6
              </strong>

            </div>


            <div className="progress-track">

              <div
                className="progress-fill"
                style={{
                  width:
                    `${(activeStage / 6) * 100}%`,
                }}
              ></div>

            </div>

          </div>

        </section>


        {/* ================= PANCHA AVAYAVA ================= */}

        <section
          className="avayava-section"
        >

          <div className="section-heading">

            <div>

              <span className="section-number">
                03
              </span>

              <div>

                <h2>
                  Pancha Avayava
                </h2>

                <p>
                  The five-part structure of the
                  logical argument.
                </p>

              </div>

            </div>

          </div>


          <div className="avayava-grid">

            <div className="argument-card">

              <span className="argument-number">
                01
              </span>

              <div>
                <h3>
                  Pratijna
                </h3>

                <span>
                  Proposition
                </span>
              </div>

              <p>
                States the proposition or claim
                that needs to be established.
              </p>

            </div>


            <div className="argument-card">

              <span className="argument-number">
                02
              </span>

              <div>
                <h3>
                  Hetu
                </h3>

                <span>
                  Reason
                </span>
              </div>

              <p>
                Provides the reason or evidence
                supporting the proposition.
              </p>

            </div>


            <div className="argument-card">

              <span className="argument-number">
                03
              </span>

              <div>
                <h3>
                  Udaharana
                </h3>

                <span>
                  Example
                </span>
              </div>

              <p>
                Gives a general example showing
                the relationship between reason
                and proposition.
              </p>

            </div>


            <div className="argument-card">

              <span className="argument-number">
                04
              </span>

              <div>
                <h3>
                  Upanaya
                </h3>

                <span>
                  Application
                </span>
              </div>

              <p>
                Applies the general reasoning
                to the specific case.
              </p>

            </div>


            <div className="argument-card">

              <span className="argument-number">
                05
              </span>

              <div>
                <h3>
                  Nigamana
                </h3>

                <span>
                  Conclusion
                </span>
              </div>

              <p>
                States the final conclusion derived
                from the complete argument.
              </p>

            </div>

          </div>

        </section>


        {/* ================= FORMAL LOGIC ================= */}

        <section
          className="logic-section"
          id="formal"
        >

          <div className="section-heading">

            <div>

              <span className="section-number">
                04
              </span>

              <div>

                <h2>
                  From language to formal logic
                </h2>

                <p>
                  Natural language is converted into
                  machine-verifiable First-Order Logic.
                </p>

              </div>

            </div>

          </div>


          <div className="logic-flow">

            <div className="logic-box">

              <span>
                NATURAL LANGUAGE
              </span>

              <strong>
                {conclusion ||
                  "Ravi is curious."}
              </strong>

              <p>
                User-provided conclusion.
              </p>

            </div>


            <div className="flow-arrow">
              →
            </div>


            <div className="logic-box">

              <span>
                FIRST-ORDER LOGIC
              </span>

              <strong className="formula">

                {backendData?.formalized_conclusion ||
                  "Curious(ravi)"}

              </strong>

              <p>
                Formal representation generated
                by the reasoning system.
              </p>

            </div>


            <div className="flow-arrow">
              →
            </div>


            <div className="logic-box">

              <span>
                Z3 VERIFICATION
              </span>

              <strong>

                <span className="verification-status">

                  <span
                    className={`mini-status ${
                      verified
                        ? "complete"
                        : ""
                    }`}
                  ></span>

                  {verified
                    ? "Verified"
                    : "Waiting"}

                </span>

              </strong>

              <p>
                Formal logical verification.
              </p>

            </div>

          </div>

        </section>


        {/* ================= RESULT ================= */}

        <section>

          <div className="section-heading">

            <div>

              <span className="section-number">
                05
              </span>

              <div>

                <h2>
                  Logical determination
                </h2>

                <p>
                  Final result from the verification
                  pipeline.
                </p>

              </div>

            </div>

          </div>


          <div
            className={`result-card ${getResultClass()}`}
          >

            <div className="result-icon">

              {result === "TRUE"
                ? "✓"
                : result === "FALSE"
                ? "✕"
                : "?"}

            </div>


            <div>

              <span>
                VERIFICATION RESULT
              </span>

              <h2>
                {result}
              </h2>

              <p>

                {verified
                  ? "The result was produced by the NyayaVerify reasoning and Z3 verification pipeline."
                  : "Enter a logical problem and run verification."}

              </p>

            </div>


            {verified && (

              <span className="result-badge">
                Z3 VERIFIED
              </span>

            )}

          </div>


          {/* RESULT DETAILS */}

          {showDetails && backendData && (

            <div className="result-details">

              <div className="detail-header">

                <div>

                  <span>
                    VERIFICATION DETAILS
                  </span>

                  <h3>
                    NyayaVerify Pipeline Output
                  </h3>

                </div>


                <div className="confidence-badge">

                  {backendData.result}

                </div>

              </div>


              <div className="detail-grid">

                <div>

                  <span>
                    NATURAL LANGUAGE CONCLUSION
                  </span>

                  <strong>
                    {backendData.conclusion ||
                      conclusion}
                  </strong>

                </div>


                <div>

                  <span>
                    FORMALIZED CONCLUSION
                  </span>

                  <strong className="detail-formula">
                    {backendData.formalized_conclusion ||
                      "Not available"}
                  </strong>

                </div>


                <div>

                  <span>
                    STRUCTURE
                  </span>

                  <strong className="success-text">

                    {backendData
                      .structure_validation
                      ?.valid
                      ? "VALID"
                      : "CHECK"}

                  </strong>

                </div>

              </div>

            </div>

          )}

        </section>


        {/* ================= EVALUATION ================= */}

        <section
          id="evaluation"
        >

          <div className="section-heading">

            <div>

              <span className="section-number">
                06
              </span>

              <div>

                <h2>
                  FOLIO benchmark
                </h2>

                <p>
                  Dataset used to evaluate logical
                  reasoning performance.
                </p>

              </div>

            </div>

          </div>


          <div className="metrics-grid">

            <div className="metric-card">

              <span>
                DATASET
              </span>

              <strong>
                FOLIO
              </strong>

              <p>
                Logical reasoning benchmark
              </p>

            </div>


            <div className="metric-card">

              <span>
                CLASSES
              </span>

              <strong>
                3
              </strong>

              <p>
                True · False · Unknown
              </p>

            </div>


            <div className="metric-card">

              <span>
                MODEL
              </span>

              <strong>
                Qwen 1.5B
              </strong>

              <p>
                Local CPU inference
              </p>

            </div>


            <div className="metric-card">

              <span>
                VERIFIER
              </span>

              <strong>
                Z3
              </strong>

              <p>
                Formal theorem prover
              </p>

            </div>

          </div>

        </section>


        {/* ================= FOOTER ================= */}

        <footer>

          <div>

            <strong>
              NyayaVerify
            </strong>

            <span>
              &nbsp; Explainable and Verifiable
              LLM Reasoning
            </span>

          </div>


          <span>
            Local AI · Formal Logic · Navya-Nyaya
          </span>

        </footer>

      </main>

    </div>
  );
}

export default App;
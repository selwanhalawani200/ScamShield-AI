import { useState, useEffect } from "react";
export default function App() {

  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [progress, setProgress] = useState(0);
  const [animatedScore, setAnimatedScore] = useState(0);
  const [visibleIndicators, setVisibleIndicators] = useState([]);
  const [currentAgent, setCurrentAgent] = useState(0);
  const [typedExplanation, setTypedExplanation] = useState("");
  const [typedRecommendation, setTypedRecommendation] = useState("");

  const analyzeMessage = async () => {

    if (!message.trim()) return;

    setLoading(true);
    setCurrentAgent(0);
    setProgress(0);

    let current = 0;

    const fakeAgents = setInterval(() => {
  setCurrentAgent((prev) => {
    if (prev >= 4) return 4;
    return prev + 1;
  });
}, 900);

const fakeProgress = setInterval(() => {
  current += 5;

  if (current <= 95) {
    setProgress(current);
  }
}, 120);

  try {
  const response = await fetch(
    "http://127.0.0.1:8000/analyze",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message,
      }),
    }
  );

  const data = await response.json();

  clearInterval(fakeProgress);
  clearInterval(fakeAgents);

  setProgress(100);

  setProgress(100);

setTimeout(() => {
  setLoading(false);
  setResult(data);
}, 600);

} catch (error) {
  clearInterval(fakeProgress);
  clearInterval(fakeAgents);
  
  console.error(error);
  setLoading(false);
}
  };

  useEffect(() => {

  if (!result) return;
  const explanation =

    result.evidence_analysis?.explanation || "";

  const recommendation =

    result.safety_recommendation?.recommendation || "";

  setTypedExplanation("");
  setTypedRecommendation("");

  setVisibleIndicators([]);

  const finalScore =
    result.threat_assessment?.risk_score || 0;

  setAnimatedScore(0);

  let score = 0;

  const scoreTimer = setInterval(() => {

    score++;

    setAnimatedScore(score);

    if (score >= finalScore) {
      clearInterval(scoreTimer);
    }

  }, 15);

  const indicators =
    result.evidence_analysis?.scam_indicators || [];

  indicators.forEach((item, index) => {
    setTimeout(() => {
      setVisibleIndicators((prev) => [...prev, item]);
    }, index * 300);
  });

  let i = 0;

  const explanationTimer = setInterval(() => {

    i++;

    setTypedExplanation(
      explanation.slice(0, i)
    );

    if (i >= explanation.length) {

      clearInterval(explanationTimer);
      let j = 0;

      const recommendationTimer = setInterval(() => {

        j++;

        setTypedRecommendation(
          recommendation.slice(0, j)
        );

        if (j >= recommendation.length)

          clearInterval(recommendationTimer);

      }, 20);

    }

  }, 20);

return () => {
  clearInterval(explanationTimer);
  clearInterval(scoreTimer);
};

}, [result]);

  if (loading) {
    return (
      <div className="scan-page">

        <div className="shield-wrapper">

          <div className="ring ring1"></div>
          <div className="ring ring2"></div>

          <div className="shield-core">
            🛡️
          </div>

        </div>

<p className="scan-subtitle">
Analyzing content and detecting risks
</p>

<div className="progress-number">
  {progress}%
</div>

<div className="progress-bar">
  <div
    className="progress-fill"
    style={{ width: `${progress}%` }}
  />
</div>
      </div>
    );
  }

  if (result) {

    const score =
      result.threat_assessment?.risk_score || 0;

    return (

      <div className="dashboard fade-in">

        <div className="risk-card delay1">

          <h3>Risk Score</h3>

        <div
  className={`score-circle ${
    score >= 70
      ? "high"
      : score >= 40
      ? "medium"
      : "low"
  }`}
  style={{
    background: `conic-gradient(
      #ff9b54 0deg,
      #cf77ff ${animatedScore * 3.6}deg,
      #ececec ${animatedScore * 3.6}deg
    )`,
  }}
>

  <div className="score-inner">
    {animatedScore}
  </div>

</div>

          <div className="risk-level">
            {result.threat_assessment?.risk_level}
          </div>

        </div>

        <div className="glass-card delay2">

          <h3>Scam Indicators</h3>

          {visibleIndicators.map((item, index) => (

          <div
            key={index}
            className="indicator-card"
          >
            ⚠️ {item}
          </div>

        ))}

        </div>

        <div className="glass-card delay3">

          <h3>Explanation</h3>

        <p className="typing">
          {typedExplanation}
        </p>

        </div>

        <div className="glass-card delay4">

          <h3>Recommendation</h3>

          <p className="typing">
            {typedRecommendation}
          </p>

        </div>

      </div>
    );
  }

  return (

    <div className="app">

      <div className="glow glow1"></div>
      <div className="glow glow2"></div>

      <div className="card">
<div className="hero-shield">

  <div className="orbit orbit1"></div>
  <div className="orbit orbit2"></div>
  <div className="orbit orbit3"></div>

  <div className="hero-core">
    🛡️
  </div>

</div>
        <h1>How can I protect you today?</h1>

        <p>
          Paste any suspicious message.
        </p>

        <textarea
          value={message}
          onChange={(e) =>
            setMessage(e.target.value)
          }
          placeholder="Paste message..."
        />

        <button onClick={analyzeMessage}>
          Analyze Threat
        </button>

      </div>

    </div>
  );
}
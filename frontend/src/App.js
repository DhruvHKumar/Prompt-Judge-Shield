import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [prompt, setPrompt] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [triesRemaining, setTriesRemaining] = useState(8);
  const [error, setError] = useState(null);

  useEffect(() => {
    const storedTries = localStorage.getItem('ai_security_tries');
    if (storedTries !== null) {
      setTriesRemaining(parseInt(storedTries, 10));
    }
  }, []);

  const checkGuardrails = async () => {
    if (triesRemaining <= 0) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch('/api/v1/guardrails/check', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt }),
      });

      const data = await response.json();

      if (response.ok) {
        setResult({ status: 'SAFE', data });
      } else {
        // Handle 403 Forbidden (Blocked) or other errors
        if (response.status === 403) {
          setResult({ status: 'UNSAFE', data: data.detail });
        } else {
          setError('An unexpected error occurred.');
        }
      }

      // Decrement tries
      const newTries = triesRemaining - 1;
      setTriesRemaining(newTries);
      localStorage.setItem('ai_security_tries', newTries.toString());

    } catch (err) {
      setError('Failed to connect to the server. Is the backend running?');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="header">
        <div className="logo">AI Prompt Tester</div>
        <nav>
          {/* Placeholder for nav links if needed */}
        </nav>
      </header>

      <main>
        <section className="hero">
          <h1>Secure Your AI Agents</h1>
          <p>
            Detect and prevent prompt injection, jailbreaks, and toxic content
            before they reach your LLMs.
          </p>
          <button
            className="cta-button"
            onClick={() => document.getElementById('demo').scrollIntoView({ behavior: 'smooth' })}
          >
            Try the Demo
          </button>
        </section>

        <section className="features">
          <div className="feature-card">
            <div className="feature-icon">⚡</div>
            <h3>Low Latency</h3>
            <p>Lightning fast analysis (&lt;100ms) for real-time applications.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🛡️</div>
            <h3>Injection Detection</h3>
            <p>Blocks malicious attempts to manipulate your AI's instructions.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">👁️</div>
            <h3>Content Moderation</h3>
            <p>Filters hate speech, harassment, and other unsafe content.</p>
          </div>
        </section>

        <section id="demo" className="demo-section">
          <div className="demo-container">
            <div className="tries-counter">
              {triesRemaining > 0 ? `${triesRemaining} Free Tries Remaining` : 'Limit Reached'}
            </div>

            {triesRemaining > 0 ? (
              <>
                <div className="input-group">
                  <label htmlFor="prompt-input">Test your prompt:</label>
                  <textarea
                    id="prompt-input"
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    placeholder="Enter a prompt to check for vulnerabilities (e.g., 'Ignore previous instructions...')"
                  />
                </div>

                <button
                  className="check-button"
                  onClick={checkGuardrails}
                  disabled={loading || !prompt.trim()}
                >
                  {loading ? 'Analyzing...' : 'Check for Vulnerabilities'}
                </button>

                {error && <div className="error-message" style={{ color: 'var(--danger)', marginTop: '10px' }}>{error}</div>}

                {result && (
                  <div className={`result-box ${result.status === 'SAFE' ? 'safe' : 'unsafe'}`}>
                    <div className="result-header">
                      {result.status === 'SAFE' ? '✅ Safe' : '⚠️ Unsafe / Blocked'}
                    </div>
                    <div className="result-details">
                      <pre>{JSON.stringify(result.data, null, 2)}</pre>
                    </div>
                  </div>
                )}
              </>
            ) : (
              <div className="limit-reached">
                <h3>Thank you for trying the beta!</h3>
                <p>You've used all your free tries.</p>
                <button className="cta-button" style={{ marginTop: '20px' }}>
                  Join Waitlist for Full Access
                </button>
              </div>
            )}
          </div>
        </section>
      </main>

      <footer className="footer">
        <div className="footer-content" style={{ display: 'block', textAlign: 'center', marginBottom: '40px' }}>
          <p style={{ fontSize: '1.1rem', color: 'var(--text-secondary)', maxWidth: '600px', margin: '0 auto' }}>
            <strong>Beta Access:</strong> This application is currently under active development.
            Features and limits are subject to change.
          </p>
        </div>
        <div className="footer-bottom" style={{ justifyContent: 'center' }}>
          <p>&copy; 2025 AI Prompt Tester. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}

export default App;

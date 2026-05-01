import { useState } from "react";
import "./Login.css";

interface LoginProps {
  onLogin: () => void;
}

function Login({ onLogin }: LoginProps) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [rememberMe, setRememberMe] = useState(false);
  const [loading, setLoading] = useState(false);
  const [shake, setShake] = useState(false);

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !password) {
      setShake(true);
      setTimeout(() => setShake(false), 500);
      return;
    }
    setLoading(true);
    // Simulate brief loading then navigate
    setTimeout(() => {
      setLoading(false);
      onLogin();
    }, 1200);
  };

  const handleSocialLogin = () => {
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      onLogin();
    }, 800);
  };

  return (
    <div className="login-wrapper">
      {/* Animated background elements */}
      <div className="balloon balloon-1">🎈</div>
      <div className="balloon balloon-2">🎈</div>
      <div className="balloon balloon-3">🎈</div>

      {/* Hero text overlay */}
      <div className="hero-text">
        <div className="hero-line-left"></div>
        <span>Welcome to</span>
        <div className="hero-line-right"></div>
        <h1 className="hero-title">Explore the World!</h1>
        <p className="hero-subtitle">— Your Journey Begins Here —</p>
      </div>

      {/* Login Card */}
      <div className={`login-card ${shake ? "shake" : ""}`}>
        <div className="card-header">
          <h2 className="card-title">Login</h2>
          <p className="card-subtitle">Please sign in to continue</p>
        </div>

        <form onSubmit={handleLogin} className="login-form">
          <div className="input-group">
            <span className="input-icon">✉️</span>
            <input
              type="email"
              placeholder="Email Address"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="login-input"
              autoComplete="email"
            />
          </div>

          <div className="input-group">
            <span className="input-icon">🔒</span>
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="login-input"
              autoComplete="current-password"
            />
          </div>

          <div className="login-options">
            <label className="remember-label">
              <input
                type="checkbox"
                checked={rememberMe}
                onChange={(e) => setRememberMe(e.target.checked)}
                className="remember-checkbox"
              />
              <span className="remember-text">Remember Me</span>
            </label>
            <button type="button" className="forgot-link">
              Forgot Password?
            </button>
          </div>

          <button
            type="submit"
            className={`login-btn ${loading ? "loading" : ""}`}
            disabled={loading}
          >
            {loading ? (
              <span className="spinner"></span>
            ) : (
              "Login"
            )}
          </button>
        </form>

        <div className="social-section">
          <p className="social-label">Or Login with</p>
          <div className="social-buttons">
            <button className="social-btn facebook" onClick={handleSocialLogin} title="Login with Facebook">
              <svg viewBox="0 0 24 24" fill="white" width="20" height="20">
                <path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>
              </svg>
            </button>
            <button className="social-btn google" onClick={handleSocialLogin} title="Login with Google">
              <svg viewBox="0 0 24 24" width="20" height="20">
                <path fill="white" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                <path fill="white" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                <path fill="white" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                <path fill="white" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
              </svg>
            </button>
            <button className="social-btn twitter" onClick={handleSocialLogin} title="Login with Twitter">
              <svg viewBox="0 0 24 24" fill="white" width="20" height="20">
                <path d="M23 3a10.9 10.9 0 0 1-3.14 1.53 4.48 4.48 0 0 0-7.86 3v1A10.66 10.66 0 0 1 3 4s-4 9 5 13a11.64 11.64 0 0 1-7 2c9 5 20 0 20-11.5a4.5 4.5 0 0 0-.08-.83A7.72 7.72 0 0 0 23 3z"/>
              </svg>
            </button>
          </div>
        </div>

        <p className="create-account">
          New here?{" "}
          <button type="button" className="create-link" onClick={onLogin}>
            Create an Account
          </button>
        </p>
      </div>
    </div>
  );
}

export default Login;
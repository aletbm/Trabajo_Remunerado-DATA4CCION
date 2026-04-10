
CSS = """
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&display=swap');
  @import url('https://fonts.googleapis.com/css2?family=Saira+Stencil:ital,wght@0,100..900;1,100..900&display=swap');

  /* ── Base ─────────────────────────────────────────────────────────────── */
  html, body, [class*="css"] {
      background-color: #050810;
      color: #c8d6e8;
      font-family: 'Saira Stencil', sans-serif;
  }
  .stApp { background-color: #050810; }

  /* Streamlit chrome — mantenemos el menú visible */
  footer, header { visibility: hidden; }
  .block-container { padding: 2rem 3rem 1rem 3rem; max-width: 1400px; }

  /* ── Tipografía hero ──────────────────────────────────────────────────── */
  .hero-title {
      font-family: 'Saira Stencil', sans-serif;
      font-weight: 800;
      font-size: clamp(2rem, 4vw, 3.4rem);
      letter-spacing: -0.01em;
      line-height: 1.05;
      color: #e8f0ff;
      margin: 0;
  }
  .hero-title > span{
      font-family: 'Saira Stencil', sans-serif;
      font-weight: 800;
      font-size: clamp(3rem, 4vw, 3.4rem);
      letter-spacing: -0.01em;
      line-height: 1.05;
      color: #e8f0ff;
      margin: 0;
  }
  .hero-sub {
      font-family: 'Space Mono', monospace;
      font-size: 0.72rem;
      letter-spacing: 0.22em;
      text-transform: uppercase;
      color: #4a90d9;
      margin-bottom: 0.4rem;
  }
  .hero-desc {
      font-family: 'Saira Stencil', sans-serif;
      font-size: 0.95rem;
      color: #7a94b8;
      max-width: 540px;
      line-height: 1.6;
      margin-top: 0.6rem;
  }

  h3 > span{
      font-family: 'Saira Stencil', sans-serif;
      font-weight: 800;
      letter-spacing: -0.01em;
      line-height: 1.05;
      color: #e8f0ff;
      margin: 0;
  }

  label[data-testid="stWidgetLabel"] > span > div > p {
      font-family: 'Saira Stencil', sans-serif;
      font-size: 0.95rem;
      color: #7a94b8;
      max-width: 540px;
      line-height: 1.6;
      margin-top: 0.6rem;
 } 

  /* ── Divisor ──────────────────────────────────────────────────────────── */
  .hz-line {
      border: none;
      border-top: 1px solid #1a2540;
      margin: 1.5rem 0;
  }

  /* ── KPI cards ────────────────────────────────────────────────────────── */
  .metric-card {
      background: linear-gradient(135deg, #0c1425 0%, #0a1020 100%);
      border: 1px solid #1a2d50;
      border-radius: 4px;
      padding: 1.1rem 1.4rem;
      position: relative;
      overflow: hidden;
  }
  .metric-card::before {
      content: '';
      position: absolute;
      top: 0; left: 0;
      width: 3px; height: 100%;
      background: linear-gradient(180deg, #0a3d62, #1e5fa8, #d94a7a, #ff2060);
  }
  .metric-card.accent::before { background: linear-gradient(180deg, #1e5fa8, #d94a7a, #ff2060); }
  .metric-card.green::before  { background: linear-gradient(180deg, #0a3d62, #1e5fa8, #d94a7a); }
  .metric-label {
      font-family: 'Space Mono', monospace;
      font-size: 0.62rem;
      letter-spacing: 0.18em;
      text-transform: uppercase;
      color: #4a72a0;
      margin-bottom: 0.3rem;
  }
  .metric-value {
      font-family: 'Saira Stencil', sans-serif;
      font-weight: 700;
      font-size: 2rem;
      color: #3F90CC;
      line-height: 1;
  }
  .metric-delta {
      font-family: 'Space Mono', monospace;
      font-size: 0.68rem;
      color: #4ad98a;
      margin-top: 0.3rem;
  }
  .metric-delta.neg { color: #d94a7a; }

  /* ── Selectbox métrica ────────────────────────────────────────────────── */
  div[data-baseweb="select"] > div > div > div {
      font-family: 'Space Mono', monospace;
      font-size: 0.8rem;
      letter-spacing: -0.01em;
      text-transform: uppercase;
      color: #4a72a0 !important;
  }
  div[data-baseweb="select"] > div {
      background: #050810 !important;
      border: 1px solid #1a2d50 !important;
      border-radius: 3px !important;
  }

  div[data-baseweb="popover"] > div > div > ul > div > div li {
      font-family: 'Space Mono', monospace;
      font-size: 0.8rem;
      letter-spacing: -0.01em;
      text-transform: uppercase;
      color: #4a72a0 !important;
  }
  div[data-baseweb="popover"] > div > div > ul > div > div {
      background: #050810 !important;
      border: 1px solid #1a2d50 !important;
      border-radius: 3px !important;
  }

  /* ── Info tags ────────────────────────────────────────────────────────── */
  .info-tag {
      display: inline-block;
      background: #0d1e38;
      border: 1px solid #1a3560;
      border-radius: 2px;
      padding: 0.15rem 0.5rem;
      font-family: 'Space Mono', monospace;
      font-size: 0.6rem;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: #3a70b0;
  }

  /* ── Ranking rows ─────────────────────────────────────────────────────── */
  .country-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0.55rem 0;
      border-bottom: 1px solid #0f1e35;
      font-size: 0.82rem;
  }
  .country-name { font-family: 'Saira Stencil', sans-serif; color: #90b0d8; font-weight: 700; }
  .bar-wrap { flex: 1; margin: 0 1rem; height: 4px; background: #0c1830; border-radius: 2px; }
  .bar-fill  { height: 100%; border-radius: 2px; }

  /* ── Scrollbar ────────────────────────────────────────────────────────── */
  ::-webkit-scrollbar { width: 4px; }
  ::-webkit-scrollbar-track { background: #050810; }
  ::-webkit-scrollbar-thumb { background: #1a2d50; border-radius: 2px; }

  /* ── Slider temporal ──────────────────────────────────────────────────── */
  div[data-testid="stSlider"] > div {
      padding: 0 !important;
  }
  div[data-testid="stSlider"] .st-emotion-cache-1d7yssp,
  div[data-testid="stSlider"] [class*="sliderThumb"] {
      background: linear-gradient(135deg, #1e5fa8, #d94a7a) !important;
      border: none !important;
      box-shadow: 0 0 6px #d94a7a88 !important;
  }
  div[data-testid="stSlider"] [class*="sliderTrack"] {
      background: linear-gradient(90deg, #0a3d62, #1e5fa8, #d94a7a, #ff2060) !important;
  }
  div[data-testid="stSlider"] [class*="sliderRail"] {
      background: #1a2d50 !important;
  }
  div[data-testid="stSlider"] p {
      font-family: 'Space Mono', monospace !important;
      font-size: 0.65rem !important;
      color: #c8b090 !important;
      letter-spacing: 3px !important;
  }
</style>
"""
# src/dashboard.py
from flask import Flask, render_template_string
import pandas as pd
import os
from supabase_client import supabase

app = Flask(__name__)
REPORT_PATH = os.path.join(os.path.dirname(__file__), "..", "reports", "analysis.csv")

HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>Honeypot Dashboard</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="p-4">
  <div class="container">
    <h1>Honeypot Dashboard</h1>
    <p>
      <a class="btn btn-primary" href="/refresh">Fetch latest logs → DB</a>
      <a class="btn btn-secondary" href="/analyze">Run Analyzer</a>
      <a class="btn btn-success" href="/view">View Report</a>
    </p>
    <div id="content">{{ content|safe }}</div>
  </div>
</body>
</html>
"""

@app.route("/")
def index():
    content = "<p>Use buttons to fetch logs from .log file, run analysis, or view report.</p>"
    return render_template_string(HTML, content=content)

@app.route("/refresh")
def refresh():
    # call supabase uploader (reads local logs and pushes)
    from log_uploader import upload_logs_to_db
    upload_logs_to_db()
    return render_template_string(HTML, content="<p>Logs uploaded to Supabase.</p>")

@app.route("/analyze")
def analyze():
    from analyzer import run_analysis
    run_analysis()
    return render_template_string(HTML, content="<p>Analyzer run completed.</p>")

@app.route("/view")
def view():
    if os.path.exists(REPORT_PATH):
        df = pd.read_csv(REPORT_PATH)
        table = df.to_html(classes="table table-striped", index=False)
        return render_template_string(HTML, content=table)
    else:
        return render_template_string(HTML, content="<p>No report yet. Run analyzer.</p>")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

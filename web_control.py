from flask import Flask, request, render_template_string
from telegram_control import settings  # ← تأكد أن هذا الملف موجود في مشروعك

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Bot Settings</title>
    <style>
        body { font-family: Arial; margin: 30px; background: #f4f4f4; }
        form { background: white; padding: 20px; border-radius: 10px; width: 300px; }
        h2 { color: #444; }
        label { font-weight: bold; }
        input, select { width: 100%; margin-bottom: 15px; padding: 8px; }
        button { padding: 10px; background: #2a9d8f; color: white; border: none; width: 100%; }
    </style>
</head>
<body>
    <h2>📊 Bot Settings Control</h2>
    <form method="post">
        <label>Mode:</label>
        <select name="mode">
            <option value="percent" {% if use_percentage %}selected{% endif %}>Percentage</option>
            <option value="fixed" {% if not use_percentage %}selected{% endif %}>Fixed</option>
        </select>

        <label>Risk %:</label>
        <input type="number" step="0.01" name="risk" value="{{ risk }}">

        <label>Fixed Amount ($):</label>
        <input type="number" name="fixed_amount" value="{{ fixed_amount }}">

        <label>Leverage:</label>
        <input type="number" name="leverage" value="{{ leverage }}">

        <button type="submit">💾 Save Settings</button>
    </form>
</body>
</html>
"""

@app.route("/settings", methods=["GET", "POST"])
def bot_settings():
    if request.method == "POST":
        mode = request.form.get("mode", "percent")
        settings["use_percentage"] = (mode == "percent")
        settings["risk"] = float(request.form.get("risk", 0.05))
        settings["fixed_amount"] = float(request.form.get("fixed_amount", 50))
        settings["leverage"] = int(request.form.get("leverage", 10))
    return render_template_string(
        HTML_TEMPLATE,
        use_percentage=settings["use_percentage"],
        risk=settings["risk"],
        fixed_amount=settings["fixed_amount"],
        leverage=settings["leverage"]
    )

# شغل على منفذ مختلف لتفادي التعارض مع keep_alive
app.run(host="0.0.0.0", port=8080)


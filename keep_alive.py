from flask import Flask, request, render_template_string
from threading import Thread
from settings import settings, save_settings# ← تأكد أن الملف موجود

app = Flask(__name__)

# واجهة HTML بسيطة
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Bot Settings</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(to right, #2c3e50, #3498db);
            color: #fff;
            display: flex;
            justify-content: center;
            align-items: flex-start;
            height: 100vh;
            padding-top: 50px;
        }
        form {
            background: #ffffff10;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
            width: 320px;
            backdrop-filter: blur(10px);
        }
        h2 {
            text-align: center;
            color: #ffffff;
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: 600;
        }
        input, select {
            width: 100%;
            padding: 10px;
            margin-bottom: 20px;
            border: none;
            border-radius: 5px;
            font-size: 14px;
        }
        button {
            width: 100%;
            padding: 12px;
            background-color: #2ecc71;
            color: white;
            font-size: 16px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
        }
        .success-message {
            background: #2ecc71;
            padding: 10px;
            text-align: center;
            margin-bottom: 15px;
            border-radius: 5px;
            display: none;
        }
    </style>
</head>
<body>
    <form method="post" onsubmit="showMessage()">
        <h2>📊 Bot Settings</h2>
        <div class="success-message" id="success">✅ Settings saved!</div>

        <label>Mode</label>
        <select name="mode">
            <option value="percent" {% if use_percentage %}selected{% endif %}>Percentage</option>
            <option value="fixed" {% if not use_percentage %}selected{% endif %}>Fixed</option>
        </select>

        <label>Risk %</label>
        <input type="number" step="0.01" name="risk" value="{{ risk }}">

        <label>Fixed Amount ($)</label>
        <input type="number" name="fixed_amount" value="{{ fixed_amount }}">

        <label>Leverage</label>
        <input type="number" name="leverage" value="{{ leverage }}">

        <button type="submit">💾 Save Settings</button>
    </form>

    <script>
        function showMessage() {
            setTimeout(function() {
                document.getElementById("success").style.display = "block";
            }, 100);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return '✅ Bot is running! Visit /settings to configure it.'

@app.route('/settings', methods=["GET", "POST"])
def bot_settings():
    if request.method == "POST":
        mode = request.form.get("mode", "percent")
        settings["use_percentage"] = (mode == "percent")
        settings["risk"] = float(request.form.get("risk", 0.05))
        settings["fixed_amount"] = float(request.form.get("fixed_amount", 50))
        settings["leverage"] = int(request.form.get("leverage", 10))
        save_settings(settings)  # 🔥 احفظ التغييرات هنا

    return render_template_string(
        HTML_TEMPLATE,
        use_percentage=settings["use_percentage"],
        risk=settings["risk"],
        fixed_amount=settings["fixed_amount"],
        leverage=settings["leverage"]
    )
def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

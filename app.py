from flask import Flask, render_template, request

app = Flask(__name__)

def analyze_client(data):
    data = data.lower()

    risk_score = 0
    missing_fields = []

    if "income" not in data:
        missing_fields.append("Income details")
        risk_score += 2

    if "id" not in data:
        missing_fields.append("Government ID")
        risk_score += 2

    if "address" not in data:
        missing_fields.append("Address proof")
        risk_score += 1

    if "loan" in data or "debt" in data:
        risk_score += 3

    if risk_score >= 5:
        risk_level = "High Risk"
        suggestion = "Manual review required before approval."
    elif risk_score >= 3:
        risk_level = "Medium Risk"
        suggestion = "Request additional documents."
    else:
        risk_level = "Low Risk"
        suggestion = "Safe to proceed with onboarding."

    return {
        "risk_level": risk_level,
        "missing_fields": missing_fields,
        "suggestion": suggestion
    }


@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        client_data = request.form.get("client_data")
        result = analyze_client(client_data)

    return render_template("index.html", result=result)

# Webhook route
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("Received client data:", data)
    return {"status": "success"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

from datetime import datetime
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    start_date = ""
    end_date = ""
    error = None

    if request.method == "POST":
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")

        try:
            d1 = datetime.strptime(start_date, "%Y-%m-%d")
            d2 = datetime.strptime(end_date, "%Y-%m-%d")

            delta = d2 - d1
            total_days = delta.days

            if total_days < 0:
                error = "End date is earlier than start date. Showing absolute difference."
                total_days = abs(total_days)
                d1, d2 = d2, d1

            weeks = total_days // 7
            remaining_days = total_days % 7

            # Approximate months and years
            years = d2.year - d1.year
            months = (d2.year - d1.year) * 12 + (d2.month - d1.month)
            if d2.day < d1.day:
                months -= 1

            result = {
                "total_days": total_days,
                "weeks": weeks,
                "remaining_days": remaining_days,
                "months": max(0, months),
                "years": round(total_days / 365.25, 2),
                "start": d1.strftime("%B %d, %Y"),
                "end": d2.strftime("%B %d, %Y"),
            }
        except ValueError:
            error = "Please enter valid dates."

    return render_template(
        "index.html",
        result=result,
        start_date=start_date,
        end_date=end_date,
        error=error,
    )


if __name__ == "__main__":
    app.run(debug=True)

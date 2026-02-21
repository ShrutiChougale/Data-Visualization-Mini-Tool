from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'

# Directly load your uploaded CSV
df = pd.read_csv("sales_data.csv")

@app.route("/", methods=["GET"])
def index():
    columns = df.columns
    return render_template("plot.html", columns=columns)


@app.route("/plot", methods=["POST"])
def plot():
    x_col = request.form["x_col"]
    y_col = request.form["y_col"]
    plot_type = request.form["plot_type"]

    plt.figure()

    if plot_type == "line":
        plt.plot(df[x_col], df[y_col])
    elif plot_type == "bar":
        plt.bar(df[x_col], df[y_col])
    elif plot_type == "scatter":
        plt.scatter(df[x_col], df[y_col])

    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title(f"{y_col} vs {x_col}")

    plot_path = os.path.join(app.config['UPLOAD_FOLDER'], "plot.png")
    plt.savefig(plot_path)
    plt.close()

    return render_template("plot.html", columns=df.columns, plot_url=plot_path)


if __name__ == "__main__":
    app.run(debug=True)
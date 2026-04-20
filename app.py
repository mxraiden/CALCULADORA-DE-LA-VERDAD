from flask import Flask, render_template_string, request
import itertools
import re

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Tabla de Verdad</title>
<style>
body {
    font-family: Arial;
    background: #0f172a;
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}
.container {
    background: #1e293b;
    padding: 20px;
    border-radius: 15px;
    width: 600px;
}
input {
    width: 100%;
    padding: 10px;
    margin-bottom: 10px;
}
button {
    padding: 10px;
    margin: 5px;
}
table {
    width: 100%;
    margin-top: 10px;
    border-collapse: collapse;
}
th, td {
    border: 1px solid white;
    padding: 5px;
    text-align: center;
}
.error {
    color: red;
}
</style>
</head>
<body>

<div class="container">
<h3>Grupo 5</h3>
<h2>Calculadora de Tabla de Verdad</h2>

<form method="post">
<input type="text" name="expr" placeholder="Ej: p && (q || !r) ^ p">
<button type="submit">Generar</button>
</form>

{% if error %}
<div class="error">{{error}}</div>
{% endif %}

{% if table %}
<table>
<tr>
{% for h in headers %}
<th>{{h}}</th>
{% endfor %}
</tr>

{% for row in table %}
<tr>
{% for cell in row %}
<td>{{cell}}</td>
{% endfor %}
</tr>
{% endfor %}
</table>

<form method="post">
<input type="hidden" name="expr" value="{{expr}}">
<input type="hidden" name="download" value="1">
<button type="submit">Descargar CSV</button>
</form>

{% endif %}
</div>

</body>
</html>
"""

def get_vars(expr):
    return sorted(set(re.findall(r"[a-z]", expr)))

def generate_table(expr):
    vars = get_vars(expr)
    combos = list(itertools.product([0,1], repeat=len(vars)))
    table = []

    for combo in combos:
        values = dict(zip(vars, combo))
        e = expr

        for v in values:
            e = e.replace(v, str(bool(values[v])))

        e = e.replace("&&", " and ")
        e = e.replace("||", " or ")
        e = e.replace("!", " not ")
        e = e.replace("^", " != ")  # XOR

        result = eval(e)
        table.append(list(combo) + [int(result)])

    return vars, table

@app.route("/", methods=["GET", "POST"])
def home():
    table = []
    headers = []
    error = None
    expr = ""

    if request.method == "POST":
        expr = request.form.get("expr", "").strip()

        if not expr:
            error = "⚠️ Ingresa una expresión lógica"
        else:
            try:
                vars, table = generate_table(expr)
                headers = vars + [expr]

                if request.form.get("download"):
                    csv = ",".join(headers) + "\\n"
                    for row in table:
                        csv += ",".join(map(str,row)) + "\\n"
                    return csv, 200, {
                        "Content-Type": "text/csv",
                        "Content-Disposition": "attachment; filename=tabla.csv"
                    }

            except:
                error = "❌ Error en la expresión lógica"

    return render_template_string(HTML, table=table, headers=headers, error=error, expr=expr)

if __name__ == "__main__":
    app.run(debug=True)
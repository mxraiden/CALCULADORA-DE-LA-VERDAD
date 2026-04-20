import streamlit as st
import itertools
import re
import pandas as pd

st.title("Grupo 5")
st.header("Calculadora de Tabla de Verdad")

expr = st.text_input("Ingresa la expresión lógica:", "")

def get_vars(expr):
    return sorted(set(re.findall(r"[a-z]", expr)))

def evaluate(expr, values):
    e = expr
    for v in values:
        e = e.replace(v, str(bool(values[v])))

    e = e.replace("&&", " and ")
    e = e.replace("||", " or ")
    e = e.replace("!", " not ")
    e = e.replace("^", " != ")

    return eval(e)

if st.button("Generar Tabla"):
    if not expr.strip():
        st.error("⚠️ Ingresa una expresión lógica")
    else:
        try:
            vars = get_vars(expr)
            combos = list(itertools.product([0,1], repeat=len(vars)))

            data = []
            for combo in combos:
                values = dict(zip(vars, combo))
                result = evaluate(expr, values)
                data.append(list(combo) + [int(result)])

            df = pd.DataFrame(data, columns=vars + [expr])

            st.dataframe(df)

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("Descargar CSV", csv, "tabla.csv", "text/csv")

        except:
            st.error("❌ Error en la expresión lógica")

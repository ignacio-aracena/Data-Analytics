"""
Validación automática del notebook Clase 07 — CART.

Verifica que TODOS los claims numéricos/factuales del notebook coincidan
con lo que el modelo realmente produce. Corre esto después de cualquier
cambio para no caer en errores como "este es el predictor más fuerte"
sin haberlo verificado contra el árbol.

Uso:
    /usr/bin/python3 .validar.py
"""
import json
import sys
import re
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import classification_report, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor


HERE = Path(__file__).parent
NOTEBOOK = HERE / "practica07.ipynb"
DATASET = HERE / "netflix_suscriptores.csv"


def reproducir_modelos():
    """Reproduce el pipeline exacto del notebook."""
    df = pd.read_csv(DATASET)
    df_m = pd.get_dummies(
        df,
        columns=["plan", "genero_favorito", "dispositivo_principal"],
        drop_first=True,
    )
    df_m["usa_descargas_offline"] = df_m["usa_descargas_offline"].astype(int)

    features = [c for c in df_m.columns if c not in ["churn_30d", "horas_proximo_mes"]]
    X = df_m[features]
    y_clf = df_m["churn_30d"]
    y_reg = df_m["horas_proximo_mes"]

    X_train, X_test, yclf_train, yclf_test, yreg_train, yreg_test = train_test_split(
        X, y_clf, y_reg, test_size=0.30, random_state=42, stratify=y_clf
    )

    clf = DecisionTreeClassifier(
        max_depth=3, min_samples_leaf=15, class_weight="balanced", random_state=42,
    )
    clf.fit(X_train, yclf_train)

    reg = DecisionTreeRegressor(max_depth=3, min_samples_leaf=30, random_state=42)
    reg.fit(X_train, yreg_train)

    return {
        "df": df,
        "features": features,
        "clf": clf,
        "reg": reg,
        "yclf_test": yclf_test,
        "yclf_pred": clf.predict(X_test),
        "yreg_test": yreg_test,
        "yreg_pred": reg.predict(X_test),
        "X_train": X_train,
        "X_test": X_test,
        "yclf_train": yclf_train,
        "yreg_train": yreg_train,
    }


def leer_notebook_texto():
    """Devuelve todo el texto de markdowns + outputs concatenado."""
    nb = json.loads(NOTEBOOK.read_text())
    blobs = []
    for c in nb["cells"]:
        src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
        blobs.append(src)
        for out in c.get("outputs", []):
            if out.get("output_type") == "stream":
                blobs.append("".join(out.get("text", [])))
    return "\n".join(blobs)


def asser_eq(check_name, esperado, real, tol=0.02):
    """Compara dos valores numéricos con tolerancia. Devuelve (ok, msg)."""
    if abs(esperado - real) <= tol:
        return True, f"  ✓ {check_name}: notebook dice {esperado}, real {real:.3f}"
    return False, f"  ✗ {check_name}: notebook dice {esperado}, real {real:.3f}  ← DIVERGE"


def main():
    ok_total = True
    print("=" * 72)
    print("VALIDACIÓN DEL NOTEBOOK · Clase 07 CART")
    print("=" * 72)

    pip = reproducir_modelos()
    nb_text = leer_notebook_texto()

    # === 1. Métricas clasificación ===
    print("\n[1] Métricas de clasificación")
    rep = classification_report(
        pip["yclf_test"], pip["yclf_pred"], target_names=["Se queda", "Churn"], output_dict=True
    )
    recall = rep["Churn"]["recall"]
    precision = rep["Churn"]["precision"]
    for claim, valor_esperado, valor_real in [
        ("recall 0.80 en Churn", 0.80, recall),
        ("precision 0.27 en Churn", 0.27, precision),
    ]:
        ok, msg = asser_eq(claim, valor_esperado, valor_real)
        print(msg)
        ok_total &= ok

    # === 2. Métricas regresión ===
    print("\n[2] Métricas de regresión")
    rmse = np.sqrt(mean_squared_error(pip["yreg_test"], pip["yreg_pred"]))
    r2 = r2_score(pip["yreg_test"], pip["yreg_pred"])
    for claim, valor_esperado, valor_real, tol in [
        ("RMSE 11 h", 11.21, rmse, 0.5),
        ("R² 0.69", 0.687, r2, 0.02),
    ]:
        ok, msg = asser_eq(claim, valor_esperado, valor_real, tol=tol)
        print(msg)
        ok_total &= ok

    # === 3. Overfitting ===
    print("\n[3] Sanity check de overfitting")
    acc_train = pip["clf"].score(pip["X_train"], pip["yclf_train"])
    acc_test = pip["clf"].score(pip["X_test"], pip["yclf_test"])
    r2_train_reg = pip["reg"].score(pip["X_train"], pip["yreg_train"])
    r2_test_reg = pip["reg"].score(pip["X_test"], pip["yreg_test"])

    gap_clf = abs(acc_train - acc_test)
    gap_reg = abs(r2_train_reg - r2_test_reg)
    print(f"  Clasificación — acc train {acc_train:.3f} | test {acc_test:.3f} | gap {gap_clf:.3f}")
    print(f"  Regresión     — R² train {r2_train_reg:.3f}  | test {r2_test_reg:.3f}  | gap {gap_reg:.3f}")
    if gap_clf < 0.05 and gap_reg < 0.05:
        print("  ✓ Ambos gaps < 0.05 → no hay overfitting")
    else:
        print("  ✗ Hay overfitting visible. Revisar max_depth o min_samples_leaf.")
        ok_total = False

    # === 4. Primer corte del árbol de clasificación ===
    print("\n[4] Estructura del árbol de clasificación")
    root_clf = pip["features"][pip["clf"].tree_.feature[0]]
    print(f"  Root feature real: {root_clf}")

    # Buscar en el notebook si se menciona explícitamente qué variable corta primero
    claims_root = re.findall(
        r"[Ee]l primer corte.+?`(\w+)`", nb_text
    )
    if claims_root:
        for c in claims_root:
            if c == root_clf:
                print(f"  ✓ Claim '`{c}`' coincide con la realidad")
            else:
                print(f"  ✗ Claim '`{c}`' NO coincide (real: `{root_clf}`)  ← DIVERGE")
                ok_total = False
    else:
        print("  · Sin claim explícito del primer corte en el notebook.")

    # === 5. Importancia de variables ===
    print("\n[5] Importancia de variables — clasificador")
    imp = pd.Series(pip["clf"].feature_importances_, index=pip["features"]).sort_values(ascending=False)
    top3 = imp.head(3)
    for feat, val in top3.items():
        print(f"  {feat:35} {val:.3f}")

    # === 6. Leakage check ===
    print("\n[6] Sanity de leakage")
    if "churn_30d" not in pip["features"] and "horas_proximo_mes" not in pip["features"]:
        print("  ✓ Targets fuera del set de features")
    else:
        print("  ✗ HAY LEAKAGE: target dentro de features")
        ok_total = False

    # === 7. Dataset ===
    print("\n[7] Sanity de datos")
    print(f"  Shape: {pip['df'].shape}")
    print(f"  Nulos: {pip['df'].isnull().sum().sum()}")
    print(f"  Duplicados: {pip['df'].duplicated().sum()}")
    print(f"  Balance churn: {pip['df']['churn_30d'].value_counts(normalize=True).round(3).to_dict()}")

    # === Resumen ===
    print("\n" + "=" * 72)
    if ok_total:
        print("✓ VALIDACIÓN OK — todos los claims numéricos/factuales coinciden")
        return 0
    else:
        print("✗ HAY DIVERGENCIAS — revisar las marcas '← DIVERGE' arriba")
        return 1


if __name__ == "__main__":
    sys.exit(main())

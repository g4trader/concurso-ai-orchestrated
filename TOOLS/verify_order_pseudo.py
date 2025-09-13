# verify_order_pseudo.py — Pseudo‑código (não executável neste estágio)
# Objetivo: validar STORY/ORDER/OUTPUTS de uma história.

import os, json, yaml

def load_yaml(path): ...
def read_text(path): ...  # ler arquivo UTF‑8 e retornar string

def validate_contains(path, must_include):
    text = read_text(path)
    misses = [s for s in must_include if s not in text]
    return misses  # vazio = ok

def validate_order(story_dir):
    order = load_yaml(os.path.join(story_dir, "ORDER.yml"))
    report = {"story": os.path.basename(story_dir), "steps": []}
    for step in order["steps"]:
        out = step["output"]
        status = {"role": step["role"], "output": out, "ok": True, "checks": []}

        # file_exists
        if not os.path.exists(os.path.join(story_dir, out)):
            status["ok"] = False
            status["checks"].append({"file_exists": False})
        else:
            status["checks"].append({"file_exists": True})

        # contains
        for cond in step.get("postconditions", []):
            if "contains" in cond:
                file = cond["contains"]["file"]
                must = cond["contains"]["must_include"]
                misses = validate_contains(os.path.join(story_dir, file), must)
                if misses:
                    status["ok"] = False
                    status["checks"].append({"contains": {"ok": False, "missing": misses}})
                else:
                    status["checks"].append({"contains": {"ok": True}})

        report["steps"].append(status)

    report["ok"] = all(s["ok"] for s in report["steps"])
    return report

# Uso:
# print(json.dumps(validate_order("playdevs/STORIES/CEB-001"), indent=2, ensure_ascii=False))

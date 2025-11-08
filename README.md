# Cloud-Native Diet Analysis – Project 2 (Phase 2)

This repository contains the **Phase 2: Cloud Dashboard** for the Diet Analytics project.  
In this phase, the backend is deployed to **Azure Functions**, and a **Flask Dashboard** is built to visualize nutritional insights from the `All_Diets.csv` dataset.

---

## 🧭 Overview

- **Backend:** Azure Functions (serverless processing)
- **Frontend:** Flask web dashboard
- **Data:** All_Diets.csv (contains real recipe and nutrition data)
- **Deployment:** Azure Function App + Azure App Service
- **Version Control:** GitHub + CI/CD (GitHub Actions)

---

## 📁 Folder Structure

```text
.
├─ app.py                          # Flask dashboard (frontend controller)
├─ All_Diets.csv                   # Dataset for visualizations
│
├─ templates/
│  └─ insights.html                # Flask HTML template (UI)
│
├─ static/
│  └─ insights.css                 # Dashboard CSS styling
│
├─ functions_nutrition/            # Azure Function backend
│  ├─ __init__.py                  # Main function logic
│  ├─ function.json                # HTTP/Blob trigger configuration
│  ├─ host.json                    # Function host config
│  └─ local.settings.json          # Local dev config (ignored in git)
│
├─ .github/workflows/
│  └─ deploy.yml                   # CI/CD build pipeline
│
├─ requirements.txt
├─ README.md
└─ .gitignore
```

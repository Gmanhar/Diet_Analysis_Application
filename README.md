# Cloud-Native Diet Analysis – Project 2 (Phase 2)

This repository contains the Phase 2 (cloud) version of the Diet Analytics project.  
In this phase, the data-processing backend is deployed to **Azure Functions**, and a **Flask dashboard** is added to visualize nutritional insights from the `All_Diets.csv` dataset.

---

## Overview

- Backend: Azure Functions (serverless, HTTP + blob trigger)
- Frontend: Flask web dashboard
- Data source: `All_Diets.csv`
- Cloud: Azure Function App + (to be deployed) Azure App Service
- Repo: GitHub with CI/CD workflow

---

## Folder Structure

```text
.
├─ app.py                          # Flask dashboard entrypoint
├─ All_Diets.csv                   # Nutrition dataset
│
├─ templates/
│  └─ insights.html                # Flask HTML template
│
├─ static/
│  └─ insights.css                 # Dashboard styling
│
├─ functions_nutrition/            # Azure Function backend
│  ├─ __init__.py                  # Function code
│  ├─ function.json                # trigger/binding config
│  ├─ host.json                    # function host config
│  └─ local.settings.json          # local dev settings (not for prod)
│
├─ .github/workflows/
│  └─ deploy.yml                   # CI/CD pipeline (build/test)
│
├─ requirements.txt
└─ .gitignore
```

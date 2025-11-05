# Cloud-Native Diet Analysis – Project 2

This repository contains the Phase 2 version of the diet analytics project.  
Phase 1 ran everything locally (Ubuntu VM, Azurite, Docker).  
Phase 2 adds Azure Functions, CI/CD, and a cleaner folder structure.

## 1. Folder Structure

```text
.
├─ data_analysis.py
├─ docker/
│  └─ Dockerfile
├─ functions_nutrition/
│  ├─ __init__.py
│  ├─ function.json
│  ├─ host.json
│  └─ requirements.txt
└─ .github/
   └─ workflows/
      └─ deploy.yml
```

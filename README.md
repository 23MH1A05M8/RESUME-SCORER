## Day 5 — Résumé Scorer Streamlit

**Live URL:** [https://<your-app>.streamlit.app](https://resume-scorer-kkaftbsmwjdnupaqiqk2o9.streamlit.app/)
**Code:** app.py  |  **Acceptance log:** acceptance_log.md
**Tools:** Continue.dev + Groq (llama-3.1-8b-instant) + Streamlit Community Cloud

### Features
- Fit score with rationale
- 4-axis bar chart breakdown (technical skills, soft skills, experience relevance, project fit)
- Missing skills + free learning resources with direct links

### Reflection
- **Vibe vs engineered:** Vibe-coded. To productionise, I'd add caching, rate limiting per user, and better error handling for when Groq returns malformed JSON.
- **What Continue.dev did well:** Scaffolded the Streamlit layout fast and generated both the bar chart and learning resources sections in one prompt update.
- **What I had to fix:** Continue.dev introduced indentation errors when adding new features — had to manually correct the prompt block and missing skills section back to the right indent level. Also had to switch from Gemini to Groq due to 503 availability issues, and update the model from the decommissioned llama3-8b-8192 to llama-3.1-8b-instant.

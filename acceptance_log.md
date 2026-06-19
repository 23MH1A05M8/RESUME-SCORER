## Day 5 Lab 5A — Continue.dev Acceptance Log

1. Accepted: bar_chart visualization of sub-scores
   Why: makes the score breakdown immediately scannable as a visual chart rather than raw numbers; four axes (technical, soft skills, experience, project fit) give a much clearer picture of where the candidate stands

2. Accepted: prompt modification adding 4 sub-score fields (technical_skills_match, soft_skills_match, experience_relevance, project_fit)
   Why: needed for the bar chart to work; keeps the prompt-output contract clear — the model knows exactly what fields to return and the UI knows exactly what fields to read

3. Accepted: st.bar_chart showing 4 sub-scores
   Why: field names in the chart dict match the updated Groq prompt exactly; labels are human-readable while keys match the JSON response

4. Accepted: prompt updated to include 4 sub-scores + learning_resources in a single prompt update
   Why: single prompt update covers both Feature A (bar chart sub-scores) and Feature B (learning resources) together; cleaner than two separate prompt changes and reduces the chance of inconsistency between prompt versions

5. Accepted: learning_resources structure as List of Dicts with keys skill, resource_type, link
   Why: actionable for students — a fit score alone is not useful; knowing which skill to learn next and having a direct link to a free resource makes the output immediately usable for placement prep

6. Accepted: requirements block for learning_resources (exactly 3 resources, YouTube Channel or Free Course, direct link)
   Why: constrains the model output so it is consistent every run — without "exactly 3", the model might return 1 or 7 randomly; without the resource_type constraint, it might return paid courses which defeats the purpose for students

7. Accepted: st.subheader + loop for Top 3 Learning Resources section
   Why: renders each resource as a clickable markdown link with skill name and resource type clearly labelled; the .get('learning_resources', []) fallback prevents a crash if the model omits the field

8. Accepted: try/except json.JSONDecodeError block
   Why: the model occasionally wraps its response in markdown code fences even when instructed not to; the except block shows the raw response instead of crashing, making debugging much easier

9. Accepted: code fence stripping logic (if raw.startswith("```"))
   Why: Groq's llama model sometimes adds ```json ... ``` around the response despite the prompt saying not to; this guard strips those fences before json.loads so parsing succeeds reliably

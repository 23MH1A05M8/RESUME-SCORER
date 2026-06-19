import streamlit as st
from groq import Groq
import json

st.set_page_config(page_title='Résumé Scorer', layout='wide')
st.title('Résumé vs JD Fit Scorer')
st.caption('Day 5 Lab 5A — Free tools end-to-end')

col1, col2 = st.columns(2)
with col1:
    resume = st.text_area('Paste résumé', height=400)
with col2:
    jd = st.text_area('Paste job description', height=400)

api_key = st.secrets.get('GROQ_API_KEY', None) or st.text_input('Groq API key', type='password',
                        help='Free key from console.groq.com')

if st.button('Score') and resume and jd and api_key:
    with st.spinner('Scoring...'):
        try:
            client = Groq(api_key=api_key)

            prompt = f"""You are a placement coach. Given this résumé and JD,
return ONLY valid JSON with no extra text, no markdown, no code fences.
Format: {{
  "score": int 0-100,
  "rationale": str,
  "technical_skills_match": int 0-100,
  "soft_skills_match": int 0-100,
  "experience_relevance": int 0-100,
  "project_fit": int 0-100,
  "missing_skills": [str],
  "suggestions": [str],
  "learning_resources": [
    {{"skill": str, "resource_type": str, "link": str}}
  ]
}}

Requirements for learning_resources:
- Provide exactly 3 resources for the top 3 missing skills.
- resource_type should be "YouTube Channel" or "Free Course".
- link should be a direct link to the resource or a YouTube search link for that skill.

Résumé:
{resume}

JD:
{jd}"""

            resp = client.chat.completions.create(
                model='llama-3.1-8b-instant',
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            )

            raw = resp.choices[0].message.content.strip()

            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            raw = raw.strip()

            result = json.loads(raw)

            st.metric('Fit Score', f"{result['score']}/100")
            st.bar_chart({
                "Technical Skills": result["technical_skills_match"],
                "Soft Skills": result["soft_skills_match"],
                "Experience Relevance": result["experience_relevance"],
                "Project Fit": result["project_fit"]
            })
            st.subheader('Rationale')
            st.write(result['rationale'])
            st.subheader('Missing skills')
            for s in result['missing_skills']:
                st.write(f'- {s}')
            st.subheader('Top 3 Learning Resources')
            for res in result.get('learning_resources', []):
                st.write(f"**{res['skill']}** ({res['resource_type']}): [Link]({res['link']})")
            st.subheader('Suggestions')
            for s in result['suggestions']:
                st.write(f'- {s}')

        except json.JSONDecodeError:
            st.error("Could not parse the response as JSON.")
            st.code(raw, language='text')
        except Exception as e:
            st.error(f"API error: {str(e)}")
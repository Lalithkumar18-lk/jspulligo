import streamlit as st

st.set_page_config(page_title="JSPulligo - Job Skill Recommender", page_icon="💼")

st.title("💼 JSPulligo - Job Skill Recommendation System")
st.write("Enter your skills and get job recommendations!")

# Predefined Job Roles and Skills
job_database = {
    "Data Scientist": ["python", "machine learning", "pandas", "numpy", "statistics"],
    "Web Developer": ["html", "css", "javascript", "react", "django"],
    "Database Administrator": ["sql", "mysql", "postgresql", "database", "oracle"],
    "AI Engineer": ["python", "deep learning", "tensorflow", "pytorch", "nlp"],
    "Business Analyst": ["excel", "power bi", "sql", "statistics", "communication"]
}

# User Input
user_input = st.text_input("Enter your skills (comma separated):")

if st.button("Find Matching Job"):
    if user_input:
        user_skills = [skill.strip().lower() for skill in user_input.split(",")]

        best_match = None
        highest_score = 0

        for job, skills in job_database.items():
            match_count = len(set(user_skills) & set(skills))
            score = (match_count / len(skills)) * 100

            if score > highest_score:
                highest_score = score
                best_match = job

        if best_match:
            st.success(f"🎯 Best Match: {best_match}")
            st.info(f"🔍 Skill Match: {highest_score:.2f}%")
        else:
            st.warning("No matching job found. Try adding more skills.")
    else:
        st.error("Please enter your js skills!")

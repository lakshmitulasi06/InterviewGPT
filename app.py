import streamlit as st
import tempfile
from resume_parser import extract_resume_text
from skill_extractor import extract_skills
from rag import create_vector_store, generate_question
from evaluator import evaluate_answer

# App Configuration Settings
st.set_page_config(
    page_title="InterviewGPT",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 InterviewGPT")
st.subheader("AI Interview Coach using RAG + Groq")
st.markdown("---")

# Session State Persistence Initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "candidate_profile" not in st.session_state:
    st.session_state.candidate_profile = None
if "vectordb" not in st.session_state:
    st.session_state.vectordb = None
if "current_question" not in st.session_state:
    st.session_state.current_question = None
if "tech_scores" not in st.session_state:
    st.session_state.tech_scores = []
if "comm_scores" not in st.session_state:
    st.session_state.comm_scores = []

# Layout Dashboard Setup
col_left, col_right = st.columns([2, 1])

with col_right:
    st.header("📊 Performance Metrics")
    if st.session_state.tech_scores:
        avg_tech = sum(st.session_state.tech_scores) / len(st.session_state.tech_scores)
        avg_comm = sum(st.session_state.comm_scores) / len(st.session_state.comm_scores)
        
        st.metric("Avg Technical Rating", f"{avg_tech:.1f} / 10")
        st.metric("Avg Communication Rating", f"{avg_comm:.1f} / 10")
        
        st.subheader("Technical Score Trend")
        st.line_chart(st.session_state.tech_scores)
    else:
        st.info("Complete an interview round to populate your evaluation charts.")
        
    st.markdown("---")
    st.header("📝 Candidate Profile Context")
    
    resume = st.file_uploader("Upload Resume PDF", type=["pdf"])
    if resume is not None and st.session_state.candidate_profile is None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(resume.read())
            resume_path = tmp.name
        
        with st.spinner("Analyzing resume structure..."):
            resume_text = extract_resume_text(resume_path)
            st.session_state.candidate_profile = extract_skills(resume_text)
        st.success("Resume processed successfully!")

    if st.session_state.candidate_profile:
        st.json(st.session_state.candidate_profile)

with col_left:
    st.header("💬 Live Interview Simulator")
    
    interview_pdf = st.file_uploader("Upload Interview Master PDF", type=["pdf"])
    if interview_pdf is not None and st.session_state.vectordb is None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(interview_pdf.read())
            pdf_path = tmp.name
        with st.spinner("Building vector indexing database..."):
            st.session_state.vectordb = create_vector_store(pdf_path)
        st.success("Question bank indexed! You are ready to begin.")

    st.markdown("---")
    
    # Display running interaction logs
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Core Action Logic
    if st.session_state.vectordb and st.session_state.candidate_profile:
        if st.session_state.current_question is None:
            if st.button("🚀 Start Interview / Next Question"):
                history_text = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.chat_history])
                
                with st.spinner("AI Interviewer is formulating a challenge..."):
                    new_q = generate_question(
                        st.session_state.vectordb, 
                        st.session_state.candidate_profile, 
                        history_text
                    )
                    st.session_state.current_question = new_q
                    st.session_state.chat_history.append({"role": "assistant", "content": new_q})
                st.rerun()

    if st.session_state.current_question:
        with st.form(key="answer_form", clear_on_submit=True):
            user_answer = st.text_area("Your Response:", height=150, placeholder="Type your full technical explanation here...")
            submit_button = st.form_submit_button(label="Submit Answer")
            
            if submit_button:
                if user_answer.strip() == "":
                    st.warning("Please enter a response before submitting.")
                else:
                    st.session_state.chat_history.append({"role": "user", "content": user_answer})
                    
                    with st.spinner("Evaluating response quality metrics..."):
                        evaluation = evaluate_answer(st.session_state.current_question, user_answer)
                    
                    # Log extracted evaluation structures directly to session memory metrics
                    if "error" not in evaluation:
                        st.session_state.tech_scores.append(evaluation.get("technical_score", 0))
                        st.session_state.comm_scores.append(evaluation.get("communication_score", 0))
                        
                        # Generate markdown structured response output block
                        feedback_report = f"""
### ⚖️ Evaluation Report
* **Technical Score:** {evaluation.get('technical_score')}/10
* **Communication Score:** {evaluation.get('communication_score')}/10

#### 🌟 Strengths
{" ".join(['- ' + s + '\n' for s in evaluation.get('strengths', [])])}

#### ⚠️ Weaknesses & Missing Concepts
{" ".join(['- ' + w + '\n' for w in evaluation.get('weaknesses', [])])}
{" ".join(['- ' + m + '\n' for m in evaluation.get('missing_concepts', [])])}

#### 💡 Ideal Reference Answer
*{evaluation.get('improved_answer')}*
                        """
                        st.session_state.chat_history.append({"role": "assistant", "content": feedback_report})
                    else:
                        st.error("Evaluation error encountered.")
                        
                    # Reset single question context tracking to prompt next iteration loop path
                    st.session_state.current_question = None
                    st.rerun()

st.markdown("---")
st.caption("InterviewGPT Platform | GenAI & Prompt Engineering Prototype Portfolio")
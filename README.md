# 🎯 Streamlit A/B Testing Tool

A **user-friendly** web application for conducting **statistical tests** in A/B experiments. Built with **Streamlit**, this tool allows analysts and experimenters to input sample sizes, metrics, and choose statistical tests (**T-Test, Chi-Square, ANOVA**). It also supports **Bayesian testing** for probability-based insights, with clear result interpretations.

🚀 **Simplify your experiment analysis with an interactive and intuitive UI!**

---

## 🔥 Features
✅ **Supports common statistical tests:**  
   - **T-Test** (for comparing means of two groups)  
   - **Chi-Square Test** (for categorical data)  
   - **ANOVA** (for comparing multiple groups)  
   
✅ **Bayesian Testing** – Get probability-based insights into experiment success.  

✅ **Handles continuous and categorical data** for flexible experiment analysis.  

✅ **Interactive Streamlit UI** – No coding required!  

✅ **Clear visualizations** of test results with easy-to-understand interpretations.  

---

## 📦 Installation

To run the tool locally, follow these steps:

```bash
# Clone the repository
git clone https://github.com/BeiHaiMatcha/Streamlit-AB-Testing-Tool.git
cd Streamlit-AB-Testing-Tool

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py

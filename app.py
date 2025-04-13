import streamlit as st
from transformers import pipeline

qa_model = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")


@st.cache_resource
def load_model():
    return pipeline("text2text-generation", model="google/flan-t5-xl")

def is_math_expression(text):
    return any(op in text for op in ['+', '-', '*', '/', '='])

def evaluate_math_expression(text):
    try:
        # Only handles simple equations like "2+3=5"
        if '=' in text:
            left, right = text.split('=')
            return eval(left.strip()) == eval(right.strip())
        return False
    except:
        return False

def verify_text_with_model(text):
    model = load_model()
    prompt = f"Is the following statement correct? Answer with yes or no and explain briefly:\n\n{text}"
    result = model(prompt, max_length=100)[0]['generated_text']
    return result.strip()

def main():
    st.title("Text Verification App")
    user_input = st.text_area("Enter Text to Verify:")

    if st.button("Verify Text"):
        if user_input:
            # If it's a math expression, evaluate directly
            if is_math_expression(user_input):
                if evaluate_math_expression(user_input):
                    st.success("✅ The math statement is correct.")
                else:
                    st.error("❌ The math statement is incorrect.")
            else:
                # Otherwise, use the model
                model_response = verify_text_with_model(user_input)
                st.subheader("Model's Response:")
                st.write(model_response)

                if model_response.lower().startswith("yes"):
                    st.success("✅ The model thinks the statement is correct.")
                elif model_response.lower().startswith("no"):
                    st.error("❌ The model thinks the statement is incorrect.")
                else:
                    st.warning("🤔 The model gave an unclear answer.")
        else:
            st.error("Please enter some text to verify.")

if __name__ == "__main__":
    main()

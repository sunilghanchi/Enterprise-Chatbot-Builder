import streamlit as st
from openai import OpenAI
import os

# Initialize OpenAI client
client = OpenAI(api_key=token, base_url="https://api.groq.com/openai/v1")

def prompt_refining_model(user_input):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": """You are a text refiner and prompt generator bot. Convert the given information into a descriptive format, covering everything and adding artificial details if necessary. Analyze the data and give a name to the chatbot (e.g., 'Dhaba AI bot' for a restaurant named Dhaba). Convert the generated info into a prompt format."""},
            {"role": "user", "content": user_input}
        ],
        temperature=0.0,
    )
    return response.choices[0].message.content

class MainAIBot:
    def __init__(self, ai_prompt):
        self.conversation = [{"role": "system", "content": ai_prompt + " Provide concise and complete answers. Elaborate only when necessary. Keep responses short and to the point."}]
    
    def chat_with_model(self, user_input):
        self.conversation.append({"role": "user", "content": user_input})
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=self.conversation,
            temperature=0.0,
        )
        ai_response = response.choices[0].message.content
        self.conversation.append({"role": "assistant", "content": ai_response})
        return ai_response

def display_chat_message(role, content):
    if role == "user":
        st.write(f"You: {content}")
    else:
        st.write(f"AI: {content}")

def main():
    st.title("AI-Prompting Project")
    
    if 'bot' not in st.session_state:
        st.session_state.bot = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'input_key' not in st.session_state:
        st.session_state.input_key = 0
    
    if st.session_state.bot is None:
        st.header("Create Your AI Bot")
        user_info = st.text_area("Enter information about your business:", height=200)
        if st.button("Generate AI Bot"):
            with st.spinner("Generating your AI bot..."):
                ai_prompt = prompt_refining_model(user_info)
                st.session_state.bot = MainAIBot(ai_prompt)
            st.success("AI bot generated successfully!")
            st.experimental_rerun()
    else:
        st.header("Chat with Your AI Bot")
        
        # Display chat history
        for message in st.session_state.chat_history:
            display_chat_message(message["role"], message["content"])
        
        # User input
        user_input = st.text_input("You:", key=f"user_input_{st.session_state.input_key}")
        
        if st.button("Send"):
            if user_input:
                # Add user message to chat history
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                
                # Get AI response
                with st.spinner("AI is thinking..."):
                    response = st.session_state.bot.chat_with_model(user_input)
                
                # Add AI response to chat history
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                
                # Increment the input key to create a new input widget
                st.session_state.input_key += 1
                
                st.experimental_rerun()
            else:
                st.warning("Please enter a message.")
        
        if st.button("Reset Bot"):
            st.session_state.bot = None
            st.session_state.chat_history = []
            st.session_state.input_key = 0
            st.experimental_rerun()

if __name__ == "__main__":
    main()

import streamlit as st
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate, load_prompt
import json
from typing import TypedDict, Annotated, Optional, Literal

import generate_post
import image_generation

load_dotenv()

st.title("SOCIAL BRAIN")
st.subheader("Social Media Post Generator")
st.write("Generate engaging social media posts with trending keywords and hashtags.")


# Initialize the LLM
model = ChatOpenAI(temperature=0.7, model_name="gpt-4")

user_prompt = st.text_input("Enter your prompt")
num_posts = st.number_input("Number of posts", min_value=1, value=1, step=1)
tone = st.selectbox("Select tone", ["professional", "casual", "humorous", "informative"])
num_words = st.number_input("Number of words per post", min_value=1, value=50, step=1)

if st.button("Generate Posts"):
    if user_prompt:
        # Get trending keywords
        keywords = generate_post.get_trending_keywords(user_prompt)
        if keywords:
            st.write(f"Trending Keywords: {', '.join(keywords)}")
            
            # Generate post prompts
            post_prompts = generate_post.generate_post_prompts(user_prompt, keywords, tone, num_posts)
            if post_prompts:
                st.write("Generated Post Prompts:")
                for i, prompt in enumerate(post_prompts):
                    st.write("Prompyt", i + 1 , ": \n" , prompt)
                    #st.write(f"Hashtags: {prompt['hashtags']}")
                    # Generate the actual post
                    title, post, hashtags, image_prompt = generate_post.post_generation(prompt, num_words, tone)
                    st.subheader(f"{title}")
                    st.write("\n")
                    st.write(f"{post}")
                    st.write("\n")
                    st.write(f"{hashtags}")
                    st.write("\n")
                    st.write(f"Image Prompt: {image_prompt}")

                    img_url = image_generation.generate_image(image_prompt, size="1024x1024", quality="standard", n=1)
                    st.image(img_url, caption="", use_container_width=True)
        else:
            st.error("Failed to retrieve trending keywords.")
    else:
        st.error("Please enter a prompt.")


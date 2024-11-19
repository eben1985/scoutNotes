import ollama
import json
import streamlit as st


def extract_team_list(image_path, team_name, team_color, prompt):
    """
    Extract the team list from an image using the llama3.2-vision model.

    Parameters:
        image_path (str): The file path of the uploaded image.
        team_name (str): The name of the team.
        team_color (str): The color of the team jerseys.

    Returns:
        dict: A dictionary with player numbers and names.
    """
    # prompt = f"""
    # Analyze the image and extract the list of players for the team.
    # The team list includes player numbers and their corresponding names.
    # Return the information as a JSON object with player numbers as keys and names as values.
    # Do all the players on the image, do not stop untill all the palyers on the image has been captured.
    # There should be 23 players
    # """

    # Use the Ollama API to process the image and extract information
    response = ollama.chat(
        model='llama3.2-vision',
        messages=[
            {
                'role': 'user',
                'content': prompt,
                'images': [image_path]
            }
        ]
    )
    return response


# Streamlit UI
st.title("Team List Extractor with Llama3.2-Vision")
st.markdown("Upload an image of a team list and extract player names and numbers.")

# Input for team name and color
team_name = st.text_input("Enter the team name:", placeholder="e.g., Tigers")
team_color = st.text_input("Enter the team color:", placeholder="e.g., Blue")

prompt = st.text_area("Prompt", value=f""" Analyze the image and extract the list of players for the team.
    The team list includes player numbers and their corresponding names.
    Return the information as a JSON object with player numbers as keys and names as values.
    Do all the players on the image, do not stop untill all the palyers on the image has been captured.
    There should be 23 players""")

# File uploader for the image
uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

# Button to process the image
if uploaded_image:

    st.image("temp_image.jpg", caption="Uploaded Image",width=300)

    with st.spinner("Extracting team list..."):
        team_list = extract_team_list("temp_image.jpg", team_name, team_color,prompt)

    if team_list:
        st.success("Extraction successful!")
        st.json(team_list)
    else:
        st.error("Failed to extract the team list.")
else:
    st.info("Please upload an image, and enter the team name and color.")



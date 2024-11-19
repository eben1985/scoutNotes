import ollama
import json
import streamlit as st
from io import StringIO

def extract_team_list(image_path, prompt):
    """
    Extract the team list from an image using the llama3.2-vision model.
    """
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

def extract_notes(image_path, prompt, team_list):
    """
    Extract comments or notes from the uploaded text file using the LLM.
    """
    response = ollama.chat(
        model='llama3.2-vision',
        messages=[
            {
                'role': 'user',
                'content': f"{prompt}\n\nTeam List:\n{team_list}",
                'images': [image_path]
            }
        ]
    )
    return response

# def generate_summary(team_list, notes):
#     """
#     Generate a summary linking team list information to corresponding notes.
#     """
#     summary = []
#     for player_num, player_name in team_list.items():
#         player_notes = [note for note in notes if player_num in note or player_name in note]
#         summary.append({
#             "Player Number": player_num,
#             "Player Name": player_name,
#             "Comments": " ".join(player_notes) if player_notes else "No comments."
#         })
#     return summary

# Streamlit UI
st.title("Enhanced Team List and Notes Analyzer")
st.markdown("Upload team sheets and notes to generate a summary of player details and comments.")

# Input for custom prompt
team_prompt = st.text_area("Team Sheet Prompt", value="""Analyze the image and extract the list of players for the team.
The team list includes player numbers and their corresponding names.
Return the information as a JSON object with player numbers as keys and names as values.
Do all the players on the image, do not stop until all the players on the image have been captured.
There should be 23 players.""")

notes_prompt = st.text_area("Notes Prompt", value="""fAnalyze the notes and extract any comments related to players.
Link the comments to the players using their numbers or names.
make a list of the number of the player, the names and the comments. The notes contains fractions of player informatin 
make sure that you link all the relevant information to the correct player by using this lis of player numbers and names in the teamliist.""")

# File uploader for multiple team sheet images
uploaded_team_images = st.file_uploader("Upload team sheet images", type=["png", "jpg", "jpeg"], accept_multiple_files=False)

# File uploader for notes
uploaded_notes = st.file_uploader("Upload notes", type=["txt","png", "jpg", "jpeg"], accept_multiple_files=False)

# Process button
if st.button("Generate Summary") and uploaded_team_images and uploaded_notes:
    # Process team sheets
    st.image(uploaded_team_images, caption="Uploaded Image",width=300)
    st.image(uploaded_notes, caption="Uploaded Image",width=300)

    with st.spinner("Extracting team list..."):
        team_list = extract_team_list(uploaded_team_images, team_prompt)

    if team_list:
        st.success("Extraction successful!")
        st.json(team_list)
    else:
        st.error("Failed to extract the team list.")


    # Process notes
    with st.spinner("Extracting notes..."):
        notes_response = extract_notes(uploaded_notes, notes_prompt, team_list)
        st.write(notes_response)


    # # Generate summary
    # with st.spinner("Generating summary..."):
    #     summary = generate_summary(team_list, notes_response)
    #     st.success("Summary generated successfully!")
    #     st.json(summary)

#     # Allow user to download the summary
#     summary_json = json.dumps(summary, indent=4)
#     st.download_button("Download Summary", data=summary_json, file_name="team_summary.json", mime="application/json")
# else:
#     st.info("Please upload both team sheets and notes before generating the summary.")

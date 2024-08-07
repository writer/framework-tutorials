import writer as wf
import writer.ai
from prompts import soap_notes_prompt, icd_codes_prompt

# Chat event handler
def handle_simple_message(state, payload):
    state["conversation"] += payload
    
    for chunk in state["conversation"].stream_complete():
        state["conversation"] += chunk
    
# Generate button event handler
def handle_generate_button(state):
    state["message"] = "% Generating SOAP notes..."
    conversation_history = state["conversation"].serialized_messages
    notes_prompt = soap_notes_prompt(conversation_history)
    state["notes"] = writer.ai.complete(notes_prompt, config={"model": "palmyra-med-32k", "max_tokens": 1000})
    
    state["message"] = "% Generating ICD-10 codes..."
    codes_prompt = icd_codes_prompt(conversation_history, state["notes"])
    state["icd_codes"] = writer.ai.complete(codes_prompt, config={"model": "palmyra-med-32k", "max_tokens": 1000})
    state["message"] = None

# Sample chat history between doctor and patient
history = [
    {"role": "user", "content": "Hello. Please tell me about your syptoms."},
    {"role": "assistant", "content": "Hello doctor, I've been having some severe lower back pain for a few days now."},
    {"role": "user", "content": "I'm sorry to hear about your discomfort. Can you tell me if the pain is localized or does it spread to other areas?"},
    {"role": "assistant", "content": "It's mostly in the lower back, but sometimes I feel it shooting down my left leg."},
    {"role": "user", "content": "Does anything in particular seem to trigger the pain or make it worse?"},
    {"role": "assistant", "content": "It gets worse when I'm sitting for long periods or when I try to stand up."},
    {"role": "user", "content": "Have you tried any treatments at home, like applying heat or taking any over-the-counter medications?"},
    {"role": "assistant", "content": "I've used a heating pad and taken ibuprofen, but they only provide temporary relief."},
    {"role": "user", "content": "Given the nature of your symptoms, it sounds like it could be related to sciatica, especially with the pain radiating down your leg. I'm going to prescribe a medication called gabapentin to help manage the pain and nerve symptoms."},
    {"role": "assistant", "content": "Thank you, doctor. How often should I take the medication?"},
    {"role": "user", "content": "I'll start you on a low dose, and we can adjust it based on how you respond. You'll take it three times a day. It's important to take it exactly as prescribed to manage your symptoms effectively."},
    {"role": "assistant", "content": "Understood. Should I continue with the heating pad and ibuprofen as well?"},
    {"role": "user", "content": "Yes, you can continue those as needed for additional relief. We'll review everything during your follow-up visit."},
    {"role": "assistant", "content": "I appreciate your help. I'll start the medication and keep you updated on how I feel."}
]

# Initialize the state with the conversation history and initial values
wf.init_state({
    "my_app": {
        "title": "PATIENT INTERACTION PORTAL"
    },
    "conversation": writer.ai.Conversation(history, config={"model": "palmyra-med-32k"}),
    "notes": "SOAP notes from patient interaction will appear here.",
    "icd_codes": "Extracted ICD-10 codes will appear here.",
    "message": None
})  

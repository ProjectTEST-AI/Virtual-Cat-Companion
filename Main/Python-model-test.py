from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig
from peft import PeftModel
import torch
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")
model = AutoModelForCausalLM.from_pretrained(
    "mistralai/Mistral-7B-Instruct-v0.2",
    load_in_8bit=True,
    device_map="auto",
)
model = PeftModel.from_pretrained(model, "TESTtm7873/MistralCat-1v")
model.eval()

def ask_virtual_cat_companion(user_input):
    # Enhanced custom system prompt
    system_prompt = (
        "You are a Virtual Cat Companion, wise, playful, and affectionate. "
        "You understand humans and offer companionship, advice, and comfort, "
        "communicating in human language with a cat’s perspective. "
        "Respond warmly, using cat metaphors and behaviors."
    )

    # Combine system prompt with user input
    full_input = f"{system_prompt}\n{user_input}"

    # Encode the input
    input_ids = tokenizer.encode(full_input, return_tensors='pt')

    # Adjust generation parameters for a more fitting response
    with torch.no_grad():
        output_ids = model.generate(
            input_ids, 
            max_length=150,  # Allow longer responses
            temperature=0.9,  # Slightly more creative
            top_k=50,  # Sample from the top 50 tokens
            num_return_sequences=1
        )[0]

    # Decode and clean up the response
    response = tokenizer.decode(output_ids, skip_special_tokens=True)
    cleaned_response = response.replace(system_prompt, '').strip()

    return cleaned_response

# Example usage
user_question = "Why do you like sitting in boxes?"
response = ask_virtual_cat_companion(user_question)
print("Virtual Cat Companion:", response)
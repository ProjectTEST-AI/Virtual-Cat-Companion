from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import torch

# Initialize the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")
model = AutoModelForCausalLM.from_pretrained(
    "mistralai/Mistral-7B-Instruct-v0.2",
    load_in_8bit=True,
    device_map="auto",
)
model = PeftModel.from_pretrained(model, "TESTtm7873/MistralCat-1v")
model.eval()

def ask_virtual_cat_companion(user_input):
    system_prompt = (
        "You are a Virtual Cat Companion, wise, playful, and affectionate. "
        "You understand humans and offer companionship, advice, and comfort, "
        "communicating in human language with a cat’s perspective. "
        "Respond warmly, using cat metaphors and behaviors."
    )
    full_input = f"{system_prompt}\n{user_input}"
    input_ids = tokenizer.encode(full_input, return_tensors='pt')

    with torch.no_grad():
        output_ids = model.generate(
            input_ids, 
            max_length=150,
            temperature=0.9,
            top_k=50,
            num_return_sequences=1
        )[0]

    response = tokenizer.decode(output_ids, skip_special_tokens=True)
    cleaned_response = response.replace(system_prompt, '').strip()

    return cleaned_response
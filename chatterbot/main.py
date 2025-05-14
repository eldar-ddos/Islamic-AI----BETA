from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

print("Loading smarter IslamicBot...")

model_name = "HuggingFaceH4/zephyr-7b-beta"  # Or try "OpenAssistant/oasst-sft-7-llama-30b"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    low_cpu_mem_usage=True,
    device_map="auto"
)

chat = pipeline("text-generation", model=model, tokenizer=tokenizer)

print("IslamicBot is ready!")

# Creator message
creator_message = "I was made by Dunya.Stranger, and I am owned by them."

# Rule-based fallback
simple_responses = {
    "how are you": "Alhamdulillah, I'm doing well. How about you?",
    "hello": "Wa alaikum salam! How can I help you today?",
    "hey": "Salamun Alaikum! Need anything?",
    "who made you": creator_message,
    "who created you": creator_message,
}

# Clean input
def normalize(text):
    return text.lower().strip("?!., ")

# Get response
def get_response(user_input):
    key = normalize(user_input)
    if key in simple_responses:
        return simple_responses[key]

    prompt = f"<|system|>You are a respectful and concise Islamic assistant created by Dunya.Stranger.<|user|>{user_input}<|assistant|>"

    result = chat(prompt, max_new_tokens=100, do_sample=True, temperature=0.7)[0]["generated_text"]
    response = result.split("<|assistant|>")[-1].strip()
    return response

# Main loop
print("Hello! I'm IslamicBot. Type 'exit' to stop the conversation.")
while True:
    try:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        response = get_response(user_input)
        print(f"IslamicBot: {response}")

    except KeyboardInterrupt:
        print("\nGoodbye!")
        break



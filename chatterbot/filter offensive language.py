import requests
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from bs4 import BeautifulSoup

# Create the IslamicBot chatbot
chatbot = ChatBot(
    'IslamicBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.BestMatch',
    ],
    database_uri='sqlite:///database.db'
)

# Train the bot with ChatterBot corpus
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train('chatterbot.corpus.english')

# Creator message
creator_message = "I was made by Dunya.Stranger, and I am owned by them."

# Extended list of offensive words
bad_words = [
    "fuck", "shit", "bitch", "asshole", "bastard", "cunt", "damn", "hell", "piss", 
    "bastards", "slut", "whore", "dick", "pussy", "nigger", "fag", "faggot", "gay", 
    "motherfucker", "cock", "twat", "shithead", "shitface", "douche", "bimbo", "idiot",
    "stupid", "retarded", "numbnuts", "moron", "cocksucker", "bitchass", "fuckhead",
    "wanker", "cuntface", "prick", "asswipe", "ballbag", "arsehole", "jizz", "cockhead"
]

# Function to filter offensive language from the bot's response
def filter_offensive_language(response):
    # Loop through the list of bad words and check if they are in the response
    for word in bad_words:
        if word.lower() in response.lower():
            return "Please, be respectful. I am here to assist you!"
    return response

# Function to scrape content from a URL
def web_scrape(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        return text[:500]  # Return the first 500 characters of the scraped text
    except Exception as e:
        return f"Error while scraping: {str(e)}"

# Function to scrape links from a page
def scrape_links(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True)]
        return links[:5]  # Return the first 5 links found
    except Exception as e:
        return f"Error while scraping links: {str(e)}"

# Custom function to handle user input
def get_response(user_input):
    # Check if the user asks about the creator
    if "who made you" in user_input.lower() or "who created you" in user_input.lower():
        return creator_message
    # Check if the user asks for links (can be expanded to other requests as needed)
    elif "links" in user_input.lower():
        search_query = user_input.lower().replace("links", "").strip()
        links = scrape_links(f"https://www.google.com/search?q={search_query}")
        return "\n".join(links) if links else "No links found."
    # Check if the user asks to search with Google (web scraping)
    elif "google" in user_input.lower():
        search_query = user_input.lower().replace("google", "").strip()
        return web_scrape(f"https://www.google.com/search?q={search_query}")
    else:
        # Default response from the chatbot
        response = chatbot.get_response(user_input)
        return filter_offensive_language(response)

# Start a conversation with the bot
print("Hello! I'm IslamicBot. Type 'exit' to stop the conversation.")
while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        print("Goodbye!")
        break
    response = get_response(user_input)
    print(f"IslamicBot: {response}")

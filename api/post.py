from fastapi import FastAPI
import tweepy
import os
import random
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Hardcoded array of 10 news stories, each as a dict with text, url, and image_path (replace with your actual data or fetch dynamically)
# For simplicity, assume all have the same image; update paths to real local files accessible in your deployment
NEWS_STORIES = [
    {
        "text": "Trump administration agrees to fund beleaguered consumer.",
        "url": "https://www.reuters.com/world/us/under-court-order-trump-administration-agrees-fund-beleaguered-consumer-2026-01-09/",
        "image_path": "./media/bank-diag.png"
    },
    {
        "text": "CFPB agrees to pay $100M to harmed consumers in Synapse Bank collapse.",
        "url": "https://www.consumerfinance.gov/enforcement/payments-harmed-consumers/civil-penalty-fund/",
        "image_path": "./media/money-hand.png"
    },
    {
        "text": "Synapse Bankruptcy Trustee: $85M of Customer Savings Is Missing.",
        "url": "https://www.cnbc.com/2024/06/07/synapse-bankruptcy-trustee-85-million-of-customer-savings-is-missing.html",
        "image_path": "./media/money-jar.png"
    },
    {
        "text": "Evolve Bank Struggles: Missing Customer Funds, Lost Clients.",
        "url": "https://www.wsj.com/finance/banking/evolve-bank-struggles-missing-customer-funds-lost-clients-1d531fd3",
        "image_path": "./media/bank-diag.png"
    },
    {
        "text": "Synapse Executive Alerted Accountants Before $100 Million Missing Funds Scandal.",
        "url": "https://www.wsj.com/finance/banking/synapse-missing-fund-scandal-grand-jury-investigation-e8afc1a9?st=j9oB5n&reflink=desktopwebshare_permalink",
        "image_path": "./media/piggy-1.png"
    },
    {
        "text": "Evolve Bank Struggles: Missing Customer Funds, Lost Clients.",
        "url": "https://abc7chicago.com/post/frozen-funds-high-yield-savings-account-owners-unable-access-deposited-fdic-evolve-bank-popular-app-yotta/15985826/",
        "image_path": "./media/piggy-2.png"
    },
    {
        "text": "The ugliest divorce in fintech left $200 million in customer money frozen.",
        "url": "https://fortune.com/2025/03/07/synapse-evolve-mercury-bankruptcy-lawsuits/",
        "image_path": "./media/street-banks.png"
    },
    {
        "text": "The Bank That Won't Let You Withdraw",
        "url": "https://www.youtube.com/watch?v=WCBA5ej4UBY",
        "image_path": "./media/piggy-1.png"
    },
    {
        "text": "CFPB Has Entered the Chat: Is It Too Late?",
        "url": "https://fintechbusinessweekly.substack.com/p/the-cfpb-has-entered-the-chat-is",
        "image_path": "./media/piggy-2.png"
    },
    {
        "text": "The Fight for Our Funds: A Movement for Consumer Protection in the age of no accountability.",
        "url": "https://www.fightforourfunds.org/",
        "image_path": "./media/street-banks.png"
    }
]

@app.get("/")
def post_news():
    # Load X API credentials from environment variables
    consumer_key = os.getenv("X_CONSUMER_KEY")
    consumer_secret = os.getenv("X_CONSUMER_SECRET")
    access_token = os.getenv("X_ACCESS_TOKEN")
    access_token_secret = os.getenv("X_ACCESS_SECRET")

    # Set up OAuth 1.0a for media upload (v1.1 API)
    auth = tweepy.OAuth1UserHandler(
        consumer_key, consumer_secret,
        access_token, access_token_secret
    )
    api = tweepy.API(auth)

    # Set up v2 Client for posting
    client = tweepy.Client(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )

    # Select one random story from the array
    story = random.choice(NEWS_STORIES)
    
    try:
        # Combine text and URL
        full_text = f"{story['text']} {story['url']}"

        # Upload image if path exists
        media_id = None
        if os.path.exists(story['image_path']):
            media = api.media_upload(filename=story['image_path'])
            media_id = media.media_id_string

        # Create the post
        response = client.create_tweet(
            text=full_text,
            media_ids=[media_id] if media_id else None
        )
        return {"status": "success", "posted": f"Posted: {full_text}"}
    except Exception as e:
        return {"error": str(e)}
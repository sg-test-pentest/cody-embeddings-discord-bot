import asyncio
import discord
from config import SG_TOKEN, DISCORD_TOKEN
import requests
from discord.ext.commands import Bot

def send_graphql_request(repo_name):
    
    url = "https://sourcegraph.com/.api/graphql"

    body = f"""
    mutation {{
      scheduleRepositoriesForEmbedding(
        repoNames: [
          `{repo_name}`
        ]
      ) {{
        alwaysNil
      }}
    }}
    """
    # print(body)  
    response = requests.post(url=url, json={"query": body}, headers={
        'Authorization': f'token {SG_TOKEN}' 
    })
    print("response status code: ", response.status_code)
    if response.status_code == 200:
        print("response : ", response.text)

intents = discord.Intents.default()
intents.messages = True

bot = Bot(command_prefix = 'embeddings', intents=intents)


@bot.slash_command(description="Create Embedding for Cody.")
@discord.option("name", description="Enter the public GitHub repo.")
async def embedding(ctx: discord.ApplicationContext, repo_name: str):
    try:
        await ctx.respond(f"Processing {repo_name}")
        send_graphql_request(repo_name=repo_name.replace("https://", "").rstrip("/"))
        await ctx.send(f"✅ Embedding processing!\nShould be ready in ~30 minutes.")
    except asyncio.TimeoutError:
        await ctx.send("⚠️ Timed out, please try again!")

bot.run(DISCORD_TOKEN)
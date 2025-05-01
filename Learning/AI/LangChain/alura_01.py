from openai import OpenAI
import env

number_of_days = 5
destination = "Mississauga, Ontario, Canada"

prompt = f"Create a travel itinerary for {destination} for {number_of_days} days, including activities and places to visit."
client = OpenAI(api_key=env.OPENAI_KEY)
resp = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a travel planner."},
        {"role": "user", "content": prompt}
    ],
    max_tokens=500,
    temperature=0.7
)
print(resp.choices[0].message.content)

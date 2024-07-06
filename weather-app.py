import os
import streamlit as st
import requests
from groq import Groq

# Set up OpenWeatherMap API key
API_KEY = "e3c4c8e597e971821a1b94f2a2a3d15b"

# Set up GroqAPI key
GROQ_API_KEY = "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"

def get_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    return data

def generate_prompt(user_input):
    prompt = f"""
    Extract the city name from the following user input. No matter what the input is, All you have to do is output the name of the city. You should not use any other words apart from the city: If there is no city present in the input, then you can say that the city is not present. For example if the input is Himalaya You can say Himalaya is a mountain range and not a city. Therefore, I cannot provide the weather for this input. If you have a specific city in mind in the Himalayas, please provide the name of the city and I can help you with that.
    
    User: {user_input}
    
    City name:"""
    return prompt

def get_city_name(user_input):
    prompt = generate_prompt(user_input)
    client = Groq(api_key=GROQ_API_KEY)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="mixtral-8x7b-32768",
    )
    city_name = chat_completion.choices[0].message.content.strip()
    print (city_name)
    return city_name
    

def main():
    st.title("Weather Assistant App")
    
    user_input = st.text_input("Enter your weather query:", "What's the weather like in New York?")
    
    if st.button("Get Weather"):
        city = get_city_name(user_input)
        st.write(f"{city}:")
        weather_data = get_weather_data(city)
        
        if weather_data["cod"] == 200:
            weather = weather_data["weather"][0]["description"]
            temperature = weather_data["main"]["temp"]
            humidity = weather_data["main"]["humidity"]
            wind_speed = weather_data["wind"]["speed"]
            
            st.write(f"Weather in {city}:")
            st.write(f"- Description: {weather}")
            st.write(f"- Temperature: {temperature}°C")
            st.write(f"- Humidity: {humidity}%")
            st.write(f"- Wind Speed: {wind_speed} m/s")
        else:
            st.write("Sorry, could not fetch weather data for the specified location.")

if __name__ == "__main__":
    main()
    
    # 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
    
    # set GROQ_API_KEY="02a72a36f422b75977b1576921de8424"
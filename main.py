import os
import time  # Add this import
from groq import Groq
from dotenv import load_dotenv
from actions import fetch_social_media_data
from prompt import system_prompt
from helper import extract_json

load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Define available actions
available_actions = {
    "fetch_social_media_data": fetch_social_media_data
}

# Define system messages
messages = [
    {"role": "system", "content": system_prompt}
]

# Get environment variables for limit checker
LIMIT_CHECKER_ENABLED = os.getenv("LIMIT_CHECKER_ENABLED", "false").lower() == "true"
LIMIT_SLEEP_TIME = int(os.getenv("LIMIT_SLEEP_TIME", 10))
EMPTY_RESPONSE_LIMIT = int(os.getenv("EMPTY_RESPONSE_LIMIT", 3))
MAX_LOOP_LIMIT = int(os.getenv("MAX_LOOP_LIMIT"), 5)

def generate_conversation(messages=messages):
    print(f"Messages: {messages}")
    try:
        response = client.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=messages
        )
        print(f"Response from the AI: {response.choices[0].message.content}")
        return response.choices[0].message  # Return the full message object
    except Exception as e:
        print(f"Error generating conversation: {str(e)}")
        return None

def generate_message(user_input):
    messages.append({"role": "user", "content": user_input})
    return messages

def process_social_media_lookup(user_input, session, chat_id):
    generate_message(user_input)
    empty_response_count = 0  # Initialize counter
    loop_counter = 0

    while True:
        if loop_counter > MAX_LOOP_LIMIT:
            print(f"Loop counter maxed up. Maximun limit: {MAX_LOOP_LIMIT}")
            session[chat_id] = {"status": 0, "message": "Too many request. Please try again"}
            break
        
        loop_counter += 1
        
        response = generate_conversation()
        if response is None:
            print("Failed to generate conversation")
            session[chat_id] = {"status": 0, "message": "Failed to generate conversation"}
            break
        
        conversation = response.content
        if conversation == "":
            empty_response_count += 1
            if LIMIT_CHECKER_ENABLED and empty_response_count > EMPTY_RESPONSE_LIMIT:
                print(f"Empty response limit exceeded. Sleeping for {LIMIT_SLEEP_TIME} seconds.")
                session[chat_id] = {"status": 0, "message": "Connecting with the AI..."}
                time.sleep(LIMIT_SLEEP_TIME)
                empty_response_count = 0
            continue

        purified_json = extract_json(conversation)

        if purified_json:
            status = purified_json[0]['status']
            print(f"Status: {status}")
            message = purified_json[0]['message']
            match status:
                case 100:
                    print(f"Message: {message}")
                    details = purified_json[0].get('details')
                    if details:
                        session[chat_id] = {"status": 100, "message": message, "details": details}
                    else:
                        session[chat_id] = {"status": 100, "message": message}
                    break
                case 10:
                    function = purified_json[0]['function_name']
                    params = purified_json[0]['function_params']

                    print(f"Function: {function}")
                    print(f"Params: {params}")

                    if function and params:
                        if function not in available_actions:
                            print(f"Unknown action: {function}: {params}")
                            session[chat_id] = {"status": 0, "message": "Unknown action"}
                            break

                        action_function = available_actions[function]

                        api_response = action_function(**params)
                        if api_response:
                            action_result_message = f"Response: {api_response}"
                            messages.append({"role": "assistant", "content": action_result_message})
                            session[chat_id] = {"status": 10, "message": "Looking up Social Media profile data..."}
                            continue
                        else:
                            error_message = f"Error fetching Social Media profile data for {params['username']}. Please provide the username again."
                            messages.append({"role": "assistant", "content": error_message})
                            print(f"Error: {error_message}")
                            session[chat_id] = {"status": 0, "message": "Failed to fetch Social Media profile data"}
                            break

                    else:
                        print("No valid function found in response.")
                        session[chat_id] = {"status": 0, "message": "No valid function found in response"}
                        break

                case 1:
                    print(f"Message: {message}")
                    session[chat_id] = {"status": 1, "message": message}
                    continue

                case 0:
                    print(f"Error: {message}")
                    session[chat_id] = {"status": 0, "message": message}
                    break
        else:
            print(f"Failed to extract JSON from response: {conversation}")
            session[chat_id] = {"status": 0, "message": "Trying again..."}
            messages.append({"role": "assistant", "content": "You must use the given json structure"})
            continue

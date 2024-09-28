# Social Media Lookup Agent

A Flask-based Social Media Lookup agent that uses the Groq API and RapidAPI to fetch and display social media profiles based on user input. The bot processes instructions from the frontend, scrapes social media data, and returns results in a structured JSON format. Includes server-side session management and a responsive frontend interface.

## Features

- Fetches social media profiles based on a given name.
- Processes instructions from the frontend and calls functions with the given input parameters.
- Uses RapidAPI's Social Media Links API to scrape data from various social media platforms.
- Returns results in a structured JSON format.
- Server-side session management.
- Responsive frontend interface using Tailwind CSS.
- Error handling and rate limiting.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/al-kafi-sohag/social-media-lookup-agent.git
    cd social-media-lookup-agent
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    Copy the `.env.example` file to `.env` and fill in your API keys and configuration:
    ```sh
    cp .env.example .env
    ```

    Edit the `.env` file to add your API keys and configuration:
    ```env
    GROQ_API_KEY="your_groq_api_key"
    MODEL="llama-3.1-70b-versatile"
    RAPID_API_KEY="your_rapid_api_key"
    MAX_LOOP_LIMIT="4"
    LIMIT_CHECKER_ENABLED="true"
    LIMIT_SLEEP_TIME="5"
    EMPTY_RESPONSE_LIMIT="0"
    ```

## Usage

1. Run the Flask application:
    ```sh
    flask run
    ```

2. Open your browser and navigate to `http://localhost:5000`.

3. Enter a name in the input field and click "Search" to fetch social media profiles.

## Project Structure

- `app.py`: Main Flask application file.
- `main.py`: Contains the core logic for processing user input and interacting with the Groq API.
- `actions.py`: Defines actions that can be performed by the agent, such as fetching social media data using RapidAPI.
- `helper.py`: Helper functions for extracting JSON from text.
- `prompt.py`: System prompt for the agent.
- `views/index.html`: Frontend interface using Tailwind CSS.
- `.env.example`: Example environment variables for API keys and configuration.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License.
# Emotive Muse

Emotive Muse is a Flask-based web application that generates inspirational content based on the user's emotional input. It uses the Hugging Face API to generate passages, quotes, and suggestions tailored to the specified emotion.

## Features

- Generate inspirational passages based on emotions.
- Provide famous quotes related to the specified emotion.
- Suggest songs and colors that match the emotion.
- Display predefined images and colors for different emotions.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or higher installed.
- A Hugging Face account and API key.
- Basic knowledge of using the command line.

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd emotive-muse
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your Hugging Face API key and model ID:

   ```plaintext
   HUGGING_FACE_API_KEY=your_hugging_face_api_key
   HUGGING_FACE_MODEL_ID=your_hugging_face_model_id
   ```

## Running the Application

To run the application, use the following command:

```bash
python app.py
```

The application will start a local server, and you can access it by navigating to `http://127.0.0.1:5000` in your web browser.

## Usage

1. Open the application in your web browser.
2. Type one of the supported emotions: `happy`, `sad`, `calm`, or `angry`.
3. Click the "Generate" button.
4. View the generated inspirational passage, quote, suggested song, and predefined image and colors for the specified emotion.

## Project Structure

- `app.py`: The main application file containing the Flask app and routes.
- `.env`: Environment file containing the Hugging Face API key and model ID.
- `requirements.txt`: File listing the required Python packages.
- `README.md`: This readme file.

## Dependencies

The project relies on the following Python packages:

- Flask
- requests
- python-dotenv

You can install these packages using the provided `requirements.txt` file.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with descriptive messages.
4. Push your changes to your fork.
5. Submit a pull request to the main repository.

## Contact

If you have any questions or suggestions, feel free to open an issue or contact the project maintainer.

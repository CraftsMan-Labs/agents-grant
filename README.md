# Grant Acquisition Specialist Chatbot

## Overview
This repository contains a Grant Acquisition Specialist Chatbot designed to assist users in finding and applying for grants. The chatbot leverages advanced language models to provide accurate and helpful responses.

## Features
- **Global Search**: Search for grants globally using the `/global_search` endpoint.
- **Local Search**: Search for grants locally using the `/local_search` endpoint.
- **Chat Interface**: Interactive chat interface using Streamlit.
- **Data Display**: Display collected data in JSON format.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/grant-acquisition-chatbot.git
    cd grant-acquisition-chatbot
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
### Running the FastAPI Server
To run the FastAPI server, execute the following command:
```bash
python grant_agent_3/app/main.py
```

### Running the Streamlit Interface
To run the Streamlit interface, execute the following command:
```bash
streamlit run grant_agent_2/graphrag/gui_streamlit.py
```

## Endpoints
- **Global Search**: `POST /global_search`
    - Request Body: `{ "query": "your query here" }`
    - Response: `{ "response": "search results" }`

- **Local Search**: `POST /local_search`
    - Request Body: `{ "query": "your query here" }`
    - Response: `{ "response": "search results" }`

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements
- Special thanks to the contributors and the open-source community for their invaluable support.

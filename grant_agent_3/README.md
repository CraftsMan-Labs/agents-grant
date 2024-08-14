## Setup

### Prerequisites
- Python 3.8 or higher
- Virtual environment tool (optional but recommended)

### Installation

1. **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd grant_agent_3
    ```

2. **Create a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**
    Create a `.env` file in the root directory and add the following:
    ```env
    DATABASE_URL=sqlite:///./test.db
    SECRET_KEY=your_secret_key
    ```

5. **Create the build directory (if it doesn't exist):**
    ```bash
    mkdir -p grant_agent_3/app/build
    ```

## Usage
### Running the FastAPI Server
To run the FastAPI server, execute the following command:
```bash
python grant_agent_3/app/main.py
```

### Accessing the Front End
To access the front end user interface, open your web browser and navigate to:
```
http://localhost:8000
```

## Front End Components
The front end of `grant_agent_3` is built using React and includes the following components:

- **SignUp**: A component for user registration.
- **SignIn**: A component for user login.
- **Chat**: A component for interacting with the chatbot.

These components are located in the `grant_agent_3/app/components` directory.

### Running the Streamlit Interface
To run the Streamlit interface, execute the following command:
```bash
streamlit run grant_agent_3/app/ui.py

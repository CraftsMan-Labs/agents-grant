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

## Usage
### Running the FastAPI Server
To run the FastAPI server, execute the following command:
```bash
python grant_agent_3/app/main.py
```

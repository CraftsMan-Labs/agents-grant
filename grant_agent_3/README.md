# Grant Agent 3

A simple UI to generate queries for outbound SQL while having a conversation.

## Features

- User sign-up and sign-in
- Chat interface for interacting with the system
- Form to capture user requirements
- Integration with local and global search APIs

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js
- npm or yarn

### Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/yourusername/grant_agent_3.git
   cd grant_agent_3
   ```

2. **Install backend dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

3. **Install frontend dependencies:**

   ```sh
   cd app
   npm install
   ```

### Running the Application

1. **Start the backend server:**

   ```sh
   uvicorn main:app --reload
   ```

2. **Start the frontend server:**

   ```sh
   cd app
   npm start
   ```

### Usage

1. **Sign Up:**
   - Navigate to `/signup` to create a new account.

2. **Sign In:**
   - Navigate to `/signin` to log in to your account.

3. **Chat:**
   - Navigate to `/chat` to start a conversation with the system.
   - The system will recommend grants based on your requirements.

### API Endpoints

- **POST /signup:** Create a new user account.
- **POST /token:** Obtain a JWT token for authentication.
- **POST /local_search:** Search for grants based on user requirements.
- **POST /global_search:** Search for grants globally.

### Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

### License

This project is licensed under the MIT License.

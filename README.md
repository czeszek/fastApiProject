# WhatsApp Bot Project

## Installation

1. Clone the repository
```bash
git clone https://github.com/czeszek/fastApiProject.git
cd fastApiProject
```

2. Create and activate virtual environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
.\venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

## Project Structure
```
fastApiProject/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── register.html
│   │   ├── configure.html
│   │   ├── companies.html
│   │   └── chat.html
│   └── routers/
│       ├── __init__.py
│       ├── company_routes.py
│       └── chat_routes.py
│
├── requirements.txt
└── README.md
```

## Running the Application

1. Make sure you're in the project root directory (where `app` folder is located)
2. Make sure your virtual environment is activated
3. Run the application:
```bash
uvicorn app.main:app --reload
```

4. Open your browser and go to:
- http://127.0.0.1:8000/register - to register a new company
- http://127.0.0.1:8000/companies - to see list of companies

## Available Routes

- `/register` - Register a new company
- `/companies` - List all companies
- `/configure/{company_id}` - Configure WhatsApp settings for a company
- `/chat/{company_id}` - Chat interface for a company

## Database

The application uses SQLite database (`app.db`) which will be created automatically when you first run the application.
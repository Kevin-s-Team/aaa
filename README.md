# fridGPT

## How to setupa

Follow the instructions below to build and run the project locally.

### Prerequisites

To run this project, you need to have the following installed on your system:
- nodejs 20 and npm
- python 3.10 and pip
- Google Chrome (for Angular tests)

**Added on 06.09.2023 : There is an issue with node js 20.06 released today (see [here](https://github.com/angular/angular-cli/issues/25782). To run our project, use a previous node version like 20.5.1**

### OpenAI API key

You will also need an OpenAI API key.

API keys linked to a free OpenAI account have strong rate restrictions. Thus, you will need to provide an API key associated to a paid account for the application to work correctly.

### Run the project

You will need to run both the backend and the frontend, each in a separate terminal.

#### Backend

In a terminal, cd to the `backend` folder:

```bash
cd fridGPT/backend
```

Optionally, create a Python virtual environment.

Install the dependencies:

```bash
pip install -r requirements.txt
```

Create a local copy of `.env_template` named `.env`
```bash
cp .env_template .env
```

**Edit `.env` to set your OpenAI API key**

Run the backend server:

```bash
flask --app main run --debug
```

The backend server will automatically reload if you change any of the source files.

#### Frontend

In an other terminal, cd to the `frontend` folder:

```bash
cd fridGPT/frontend
```

Install the dependencies:

```bash
npm install
```

Run the frontend server:

```bash
npm start
```

Navigate to [http://localhost:4200/](http://localhost:4200/) to access the app.

The app will automatically reload if you change any of the source files.

The frontend server automatically proxies all API requests (/api/...) to the backend server.

### Run the tests

Run the backend tests :

```bash
python3 run_tests.py
```

Run the frontend tests :

```bash
npm test
```


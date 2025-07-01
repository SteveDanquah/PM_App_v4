# OPTION 1 - Running the FastAPI Backend with Docker Compose

To get the FastAPI backend up and running, follow these steps:

## 1. Navigate to the Project Root

Ensure you are in the root directory of the project (usually named `PM_APP` or similar):

```bash
cd /path/to/PM_APP
```

## 2. Start the Application Using Docker Compose

Build and launch the application using the following command:

```bash
docker compose up --build
```

This command will:

- Build the Docker image for the FastAPI backend (if it hasn’t been built already).
- Start all services defined in your `docker-compose.yml` file (such as the FastAPI app, database, etc.).
- Stream the logs of each container to your terminal for real-time monitoring.

## 3. Access the Application

Once running, the FastAPI server will typically be available at:

```
http://localhost:8000
```

You can also view the interactive API documentation provided by FastAPI via:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

## 4. Stopping the Application

To stop the running containers, press `Ctrl+C` in your terminal. If you want to stop and remove containers, networks, and volumes created by `up`, use:

```bash
docker compose down
```

## 5. Customizing the LLM Provider

By default, the application uses OpenAI's `gpt-4.1` model via the `ChatOpenAI` interface. You can find and modify this configuration in the following file:

```
/services/llm_utils.py
```

In particular, check the `get_llm()` function:

```python
def get_llm():
    return ChatOpenAI(
        model_name="gpt-4.1",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.2
    )
```

To use a different LLM provider, such as Azure OpenAI, you can update this function accordingly.

## 6. Environment Variables

Ensure that the `.env` file in the project root is properly configured with the required credentials. This includes:

- LLM API credentials (e.g., for OpenAI or Azure OpenAI)
- Pinecone API credentials (if vector database functionality is used)

# OPTION 2:  Running the FastAPI Backend Using Virtual Environment

If you prefer to run the FastAPI backend without Docker, you can use the virtual environment located in the `PM-App/backend` directory. Follow these steps:

## 1: Navigate to the Backend Directory

```bash
cd PM-App/backend
```

## 2: Activate the Virtual Environement

```bash
source venv/bin/activate
```

## 3: Once the venv is activated, run:

```bash
uvicorn main:app --reload
```

This will start the FastAPI server locally, accessible at: http://localhost:8000
You can access the interactive API documentation at: Swagger UI: http://localhost:8000/docs

## 4. Customizing the LLM Provider

By default, the application uses OpenAI's `gpt-4.1` model via the `ChatOpenAI` interface. You can find and modify this configuration in the following file:

```
/services/llm_utils.py
```

In particular, check the `get_llm()` function:

```python
def get_llm():
    return ChatOpenAI(
        model_name="gpt-4.1",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.2
    )
```

To use a different LLM provider, such as Azure OpenAI, you can update this function accordingly.

## 5. Environment Variables

Ensure that the `.env` file in the project root is properly configured with the required credentials. This includes:

- LLM API credentials (e.g., for OpenAI or Azure OpenAI)
- Pinecone API credentials (if vector database functionality is used)
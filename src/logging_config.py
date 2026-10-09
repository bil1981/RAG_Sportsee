import os

import logfire


def configure_observability() -> None:
    logfire.configure(
        token=os.getenv("LOGFIRE_TOKEN"),
        service_name=os.getenv("LOGFIRE_SERVICE_NAME", "sportsee-rag"),
        environment=os.getenv("ENVIRONMENT", "local"),
    )

    logfire.instrument_pydantic()
    logfire.instrument_pydantic_ai()
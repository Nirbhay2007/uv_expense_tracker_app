from app.core.config import settings
from app.core.logger import bootstrap_logging, get_logger


def main() -> None:
    bootstrap_logging(settings.log_level)

    logger = get_logger(__name__)

    logger.info("Application bootstrap started")

    logger.info(
        "Application context loaded: app_name=%s aws_region=%s",
        settings.app_name,
        settings.aws_region,
    )

    logger.info(
        "Application ready: log_level=%s",
        settings.log_level,
    )

    logger.info("Application bootstrap completed successfully")


if __name__ == "__main__":
    main()
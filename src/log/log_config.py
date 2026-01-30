import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        # format="[%(levelname)s] : %(message)s : Module %(name)s",
        format="[%(asctime)s] [%(levelname)s] : Module %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
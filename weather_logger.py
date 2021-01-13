import requests

texas_woeid = "2512937"

def run():

    conn = requests.get("https://www.metaweather.com/api/location/{0}/".format(texas_woeid)).json()
    print(conn)
    bbc_weather = conn["consolidated_weather"][0]["weather_state_name"]
    temp = conn["consolidated_weather"]

    logger.info("consolidate weather")
    logger.info(bbc_weather)


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv("env_files/american_junction.env")

    from util.logger import init_logger
    from util.logger import get_logger


    init_logger()
    logger = get_logger()

    run()
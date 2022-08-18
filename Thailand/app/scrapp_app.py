from scrapper.scrappers import (
    get_all_news,
    get_all_data_from_fvs,
    get_all_data_from_consulate_site,
)
from scrapper.page_loader import PageLoader
from es.EsDumper import EsDumper
from time import sleep


def main():
    sleep(10)
    loader = PageLoader()
    while True:
        data = {
            "VISAAC": [get_all_data_from_fvs(loader)],
            "CONSULATE": [get_all_data_from_consulate_site()],
            "NEWS": get_all_news(loader),
        }

        es_dumper.init_indices(data)
        print("DONE")
        sleep(120)


if __name__ == "__main__":
    es_dumper = EsDumper()
    main()

from .EsController import EsController


class EsDumper:
    CONSULATE = "consulate"
    VISA_CENTER = "visaac"
    NEWS = "news"

    def __init__(self):
        self.es_controller = EsController()

    def add_consulates(self, consulates):
        for index, consulate in enumerate(consulates):
            self.es_controller.add_data(
                EsDumper.CONSULATE,
                index + 1,
                {
                    "address": consulate["ADRESS"],
                    "email": consulate["EMAIL"],
                    "telephone1": consulate["PHONE_NUMBER_1"],
                    "telephone2": consulate["PHONE_NUMBER_1"],
                    "worktime": "mon-fr 9:00-13:00",
                },
            )

    def add_visa_centers(self, visa_centers):
        for index, visa_center in enumerate(visa_centers):
            self.es_controller.add_data(
                EsDumper.VISA_CENTER,
                index + 1,
                {
                    "address": visa_center["ADRESS"],
                    "email": visa_center["EMAIL"],
                    "issue_worktime": visa_center["ISSUE_WORKING_HOURS"],
                    "apply_worktime": visa_center["APPLY_WORKING_HOURS"],
                    "telephone1": visa_center["PHONE_NUMBER"],
                    "telephone2": "null",
                },
            )

    def add_news(self, news):
        for index, news_item in enumerate(news):
            self.es_controller.add_data(
                EsDumper.NEWS,
                index + 1,
                {
                    "date": news_item["DATE"],
                    "title": news_item["TITLE"],
                    "body": news_item["BODY"],
                    "link": news_item["LINK"],
                },
            )

    def init_indices(self, data):
        [
            self.es_controller.delete_index(index)
            for index in [EsDumper.CONSULATE, EsDumper.NEWS, EsDumper.VISA_CENTER]
        ]
        self.add_consulates(data["CONSULATE"])
        self.add_visa_centers(data["VISAAC"])
        self.add_news(data["NEWS"])

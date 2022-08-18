from write_to_elastic import Writer

if __name__ == '__main__':
    writer = Writer()
    writer.add_visa_centers_to_elasticsearch()
    writer.add_consulates_to_elasticsearch()
    writer.add_news_to_elasticsearch()

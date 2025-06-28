from app.db import PostgresSaver
from app.fetcher import YouTubeTrendingFetcher
from config.params import Params


def main():
    # Fetch trending youtube vides
    fetcher = YouTubeTrendingFetcher(api_key=Params.YOUTUBE_API_KEY, regions=["US", "CA", "FR"])
    results = fetcher.run()

    # Save results into a database
    saver = PostgresSaver(db_uri=Params.DB_URI)
    saver.create_table()
    saver.save_dataframe(df=results)


if __name__ == "__main__":
    main()
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime, timezone
import isodate
import logging

logging.basicConfig(level=logging.INFO)


load_dotenv()

class YouTubeTrendingFetcher:
    """ Handles data injestion from youtube """

    def __init__(self, api_key: str = None, regions: list[str] = None, max_results: int = 50):
        self.api_key = api_key or os.getenv("YOUTUBE_API_KEY", "")
        self.regions = regions or ["US"]
        self.max_results = max_results
        self.youtube = build("youtube", "v3", developerKey=self.api_key)
        
    

    def parse_duration(self, duration_str: str) -> float:
        """ Parses duration from string format to a normal float

        Args:
            duration_str: duration string

        Returns: Parsed duration float
        """
        try:
            return isodate.parse_duration(duration_str).total_seconds()
        except Exception:
            return None
        
    def get_category_mapping(self, region: str) -> dict:
        """ Gets category mapping based on a certain region

        Args:
            region: Region string
        
        Returns: Category mapping dictionnary
        """

        request = self.youtube.videoCategories().list(
        part="snippet",
        regionCode=region
        )
        response = request.execute()

        return {item["id"]: item["snippet"]["title"] for item in response.get("items", [])}

    def get_channel_details(self, channel_ids: list[str]) -> pd.DataFrame:
        """ Get channels based on channel_id 
        
        Args:
            channel_ids: list of channel ids
        
        Returns: Dataframe of channels details
        
        """

        channel_data = []
        # Process channels in a batch of 50
        for i in range(0, len(channel_ids), 50):
            # Fetch data for 50 channels
            ids_chunk = channel_ids[i:i+50]
            request = self.youtube.channels().list(
            part="snippet,statistics",
            id=",".join(ids_chunk)
            )
            response = request.execute()

            # Add each channel data
            for item in response.get("items", []):
                channel = {
                    "channel_id": item["id"],
                    "channel_title": item["snippet"]["title"],
                    "subscriber_count": int(item["statistics"].get("subscriberCount", 0)),
                    "total_views": int(item["statistics"].get("viewCount", 0)),
                    "channel_created_at": item["snippet"]["publishedAt"],
                    "channel_country": item["snippet"].get("country", None)
                }
                channel_data.append(channel)

        return pd.DataFrame(channel_data)



    def fetch_trending_videos(self, region: str):
        """ Fetches trending videos based on a certain region
        
        Args:
            region : Region code

        Returns: Collected videos as a pd dataframe

        """

        # Fetch all videos
        request = self.youtube.videos().list(
            part='snippet,statistics,contentDetails',
            chart='mostPopular',
            regionCode=region,
            maxResults=self.max_results
        )
        response = request.execute()

        # Collect videos
        videos = []

        for item in response.get("items", []):
            video = {
                "video_id": item["id"],
                "title": item["snippet"]["title"],
                "channel_id": item["snippet"]["channelId"],
                "category_id": item["snippet"]["categoryId"],
                "published_at": item["snippet"]["publishedAt"],
                "view_count": int(item["statistics"].get("viewCount", 0)),
                "like_count": int(item["statistics"].get("likeCount", 0)),
                "comment_count": int(item["statistics"].get("commentCount", 0)),
                "duration_seconds": self.parse_duration(item["contentDetails"]["duration"]),
                "region_code": region,
                "ingested_at": datetime.now(timezone.utc)
            }

            videos.append(video)

        return pd.DataFrame(videos)
    
    def run(self):
        """ Performs fetching for the regions """

        all_videos = []
        for region in self.regions:
            # Fetch trending videos
            logging.info(f"Fetching trending videos for region: {region}")
            df_videos = self.fetch_trending_videos(region)

            # Add category names
            cat_map = self.get_category_mapping(region)
            df_videos["category_name"] = df_videos["category_id"].map(cat_map)

            # Add channel info:
            unique_channels = df_videos["channel_id"].unique().tolist()
            df_channels = self.get_channel_details(unique_channels)
            df_videos = pd.merge(df_videos, df_channels, on="channel_id", how="left")

            # Clean duplicates
            df_videos.drop_duplicates(subset=["video_id", "region_code", "ingested_at"], inplace=True)

            # Add videos to videos list
            all_videos.append(df_videos)


        return pd.concat(all_videos, ignore_index=True)

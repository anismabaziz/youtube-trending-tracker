import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime, timezone

load_dotenv()

class YouTubeTrendingFetcher:
    """ Handles data injestion from youtube """

    def __init__(self, api_key: str = None, regions: list[str] = None, max_results: int = 50):

        self.api_key = api_key or os.getenv("YOUTUBE_API_KEY", "")
        self.regions = regions or ["US"]
        self.max_results = max_results
        self.youtube = build("youtube", "v3", developerKey=self.api_key)
        
    
    def fetch_trending_videos(self, region: str):
        """ Fetches trending videos based on a certain region
        
        Args:
            - region : Region code

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
                "duration_seconds": item["contentDetails"]["duration"],
                "region_code": region,
                "ingested_at": datetime.now(timezone.utc)
            }

            videos.append(video)

        return pd.DataFrame(videos)
    
    def run(self):
        """ Performs fetching for the regions """

        all_videos = []
        for region in self.regions:
            print(f"Fetching trending videos for region: {region}")
            df_videos = self.fetch_trending_videos(region)
            all_videos.append(df_videos)

        return pd.concat(all_videos, ignore_index=True)

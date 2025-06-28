from sqlalchemy import create_engine, text
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)




class PostgresSaver:
    """ Handles saving videos into a postgres database """

    def __init__(self, db_uri: str = None, table_name: str = "youtube_trending"):
        self.engine = create_engine(db_uri)
        self.table_name = table_name

    def create_table(self):
        """ Create youtube_trending table if it doesn't exist """

        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            video_id TEXT,
            title TEXT,
            channel_id TEXT,
            category_id TEXT,
            category_name TEXT,
            published_at TIMESTAMPTZ,
            view_count BIGINT,
            like_count BIGINT,
            comment_count BIGINT,
            duration_seconds DOUBLE PRECISION,
            region_code TEXT,
            ingested_at TIMESTAMPTZ,
            channel_title TEXT,
            subscriber_count BIGINT,
            total_views BIGINT,
            channel_created_at TIMESTAMPTZ,
            channel_country TEXT,
            PRIMARY KEY (video_id, region_code, ingested_at)
        );

        CREATE INDEX IF NOT EXISTS idx_region ON {self.table_name} (region_code);
        CREATE INDEX IF NOT EXISTS idx_category ON {self.table_name} (category_name);
        CREATE INDEX IF NOT EXISTS idx_ingest_date ON {self.table_name} (ingested_at);
        """

        # Excute create table query
        with self.engine.connect() as conn:
            for stmt in create_table_sql.strip().split(";"):
                if stmt.strip():
                    conn.execute(text(stmt))
        
        logging.info(f"[✓] Table '{self.table_name}' checked or created.")

    def save_dataframe(self, df: pd.DataFrame):
        """ Saves youtube dataframe into the postgres database
        
        Args:
            df: Youtube dataframe
        """

        logging.info(f"[→] Saving {len(df)} records to '{self.table_name}'")
        df.to_sql(self.table_name, self.engine, if_exists="append", index=False, method="multi")
        logging.info(f"[✓] Saved successfully.")

    def clear_table(self):
        """ Clears a certain table in the database """
        with self.engine.connect() as conn:
            conn.execute(text(f"DELETE FROM {self.table_name};"))
            logging.warning(f"[⚠] All rows from '{self.table_name}' have been deleted.")
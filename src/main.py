import yaml
import logging
from readers import csv_reader, api_reader
from validate import is_valid_customer, is_valid_manga
from clean import transform_customer_record, transform_manga_record, DataTransformationError
from load import load_clean_batch, load_rejected_record

def setup_logging():
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_format, handlers=[
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler()
    ])
    return logging.getLogger("pipeline.main")

if __name__ == "__main__":
    logger = setup_logging()
    logger.info("========== Initializing Configuration-Driven Pipeline Run ==========")

    with open("config/sources.yml", "r") as f:
        config = yaml.safe_load(f)

    for source in config["sources"]:
        logger.info(f"Triggering ingestion sequence: '{source['name']}'")
        raw_rows = []
        
        # 1. Dynamic Extraction Switch
        if source["type"] == "csv":
            raw_rows = csv_reader.extract_csv(source["path"])
        elif source["type"] == "api":
            # Extract dynamically using the max_pages config rule, fallback to 2 if missing
            pages_to_fetch = source.get("max_pages", 2)
            raw_rows = api_reader.extract_manga_by_genre(
                genre_id=source["genre_id"], 
                max_pages=pages_to_fetch
            )
        clean_batch_pool = []
        
        # Initialize metrics tracking counters for this specific source loop
        total_input_rows = len(raw_rows)
        successful_loads = 0
        rejected_loads = 0
        
        # 2. Sequential Validation and Transformation Loops
        for r in raw_rows:
            valid = is_valid_customer(r) if source["type"] == "csv" else is_valid_manga(r)
            transform_func = transform_customer_record if source["type"] == "csv" else transform_manga_record

            if valid:
                try:
                    clean_batch_pool.append(transform_func(r))
                    successful_loads += 1
                except DataTransformationError as e:
                    load_rejected_record(source["name"], r, f"Transformation Interruption: {e}")
                    rejected_loads += 1
            else:
                load_rejected_record(source["name"], r, "Missing baseline mandatory fields.")
                rejected_loads += 1

        # 3. Dynamic Staging Upsert Load Execution
        if clean_batch_pool:
            load_clean_batch(
                batch_data=clean_batch_pool, 
                table_name=source["target_table"], 
                primary_key=source["pk"][0]
            )
            
        # 4. Print Structured Source Run Summary (Matches your requirements.md examples!)
        logger.info(
            f"Run Summary for '{source['name']}': "
            f"total_rows={total_input_rows} | "
            f"loaded={successful_loads} | "
            f"rejected={rejected_loads}"
        )
        logger.info("-" * 60)
            
    logger.info("========== Pipeline Operations Complete ==========")
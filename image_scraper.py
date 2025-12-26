import argparse
import os
from icrawler.builtin import GoogleImageCrawler, BingImageCrawler, BaiduImageCrawler

def main():
    parser = argparse.ArgumentParser(description='Scrape images from search engines.')
    parser.add_argument('--keyword', type=str, required=True, help='Keyword to search for')
    parser.add_argument('--limit', type=int, default=100, help='Number of images to download (default: 100)')
    parser.add_argument('--output_dir', type=str, default=None, help='Directory to save images (default: keyword)')
    
    args = parser.parse_args()
    
    keyword = args.keyword
    limit = args.limit
    output_dir = args.output_dir if args.output_dir else keyword.replace(' ', '_')
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")
    
    print(f"Starting to download {limit} images for '{keyword}'...")
    
    # Using Bing as a primary source because Google is often restrictive
    # We can split the limit across multiple engines if needed
    
    print("Searching Bing...")
    bing_crawler = BingImageCrawler(storage={'root_dir': output_dir}, downloader_threads=4)
    bing_crawler.crawl(keyword=keyword, max_num=limit)
    
    print(f"Finished downloading images to {output_dir}")

if __name__ == '__main__':
    main()

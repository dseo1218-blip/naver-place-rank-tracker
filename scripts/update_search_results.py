import os
import sys
import csv
import json
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.search_engine import NaverPlaceSearchEngine
from modules.data_manager import DataManager

def load_config():
    companies_path = os.path.join('data', 'companies.csv')
    keywords_path = os.path.join('data', 'keywords.csv')
    
    companies = []
    keywords = []
    
    with open(companies_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            companies.append(row)
    
    with open(keywords_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            keywords.append(row)
    
    return companies, keywords

def main():
    engine = NaverPlaceSearchEngine()
    companies, keywords = load_config()
    
    results_path = os.path.join('data', 'search_results.csv')
    file_exists = os.path.exists(results_path)
    
    with open(results_path, 'a', encoding='utf-8', newline='') as f:
        fieldnames = ['timestamp', 'keyword', 'company', 'rank', 'total', 'address', 'category']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        for keyword in keywords:
            kw = keyword.get('keyword', '')
            for company in companies:
                name = company.get('name', '')
                print(f"검색 중: [{kw}] - {name}")
                
                result = engine.search_place_rank(kw, name)
                
                if result:
                    writer.writerow({
                        'timestamp': timestamp,
                        'keyword': kw,
                        'company': name,
                        'rank': result.get('rank', -1),
                        'total': result.get('total', 0),
                        'address': result.get('address', ''),
                        'category': result.get('category', '')
                    })
                    rank_display = result.get('rank', -1)
                    print(f"  → 순위: {rank_display}위 / 전체 {result.get('total', 0)}개")
                else:
                    print(f"  → 검색 실패")

if __name__ == "__main__":
    main()

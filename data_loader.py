import json
from typing import List, Dict

class CatalogManager:
    def __init__(self, catalog_path: str):
        with open(catalog_path, 'r', encoding='utf-8') as f:
            self.catalog = json.load(f)
            
    def search_assessments(self, query: str, top_k: int = 10) -> List[Dict]:
        """Keyword-based search across name, description, job levels, and keys."""
        query_terms = set(query.lower().replace(',', ' ').split())
        scored_items = []
        
        for item in self.catalog:
            score = 0
            text_to_search = " ".join([
                item.get('name', ''),
                item.get('description', ''),
                item.get('job_levels_raw', ''),
                " ".join(item.get('keys', []))
            ]).lower()
            
            for term in query_terms:
                if len(term) > 2 and term in text_to_search:
                    score += 1
            
            if score > 0:
                scored_items.append((score, item))
                
        scored_items.sort(key=lambda x: x[0], reverse=True)
        
        results = []
        for score, item in scored_items[:top_k]:
            results.append({
                "name": item.get('name'),
                "url": item.get('link'),
                "description": item.get('description'),
                "job_levels": item.get('job_levels', []),
                "keys": item.get('keys', [])
            })
        return results

    def get_assessment_details(self, assessment_name: str) -> Dict:
        """Fetch exact match by assessment name."""
        for item in self.catalog:
            if item.get('name', '').lower() == assessment_name.lower():
                return item
        return {}

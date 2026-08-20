import asyncio
import os
from datetime import datetime, timezone
from apify import Actor
from .utils import _fetch
from .parser import _extract_job_data

async def main():
    async with Actor:
        # Get input
        actor_input = await Actor.get_input() or {}
        max_results = actor_input.get('maxResults', 100)
        keywords = actor_input.get('keywords', '')
        location = actor_input.get('location', 'india')
        
        # Get proxy configuration
        proxy_config = await Actor.create_proxy_configuration()
        proxy_url = None
        if proxy_config:
            proxy_url = await proxy_config.new_url()
        
        Actor.log.info(f'Starting Naukri scraper - max results: {max_results}')
        
        # Build search URL
        base_url = 'https://www.naukri.com'
        if keywords:
            search_url = f'{base_url}/{keywords.replace(" ", "-")}-jobs'
            if location and location != 'india':
                search_url = f'{search_url}-in-{location.replace(" ", "-")}'
        else:
            search_url = f'{base_url}/jobs-in-{location.replace(" ", "-")}'
        
        Actor.log.info(f'Search URL: {search_url}')
        
        results_count = 0
        page = 1
        max_retries = 3
        
        while results_count < max_results:
            # Build pagination URL
            if page > 1:
                page_url = f'{search_url}?page={page}'
            else:
                page_url = search_url
            
            Actor.log.info(f'Fetching page {page}: {page_url}')
            
            # Fetch with retries
            html = None
            for attempt in range(max_retries):
                try:
                    html = await _fetch(page_url, proxy_url)
                    if html:
                        Actor.log.info(f'Fetched HTML: {len(html)} bytes')
                        break
                    Actor.log.warning(f'Empty response on attempt {attempt + 1}')
                except Exception as e:
                    Actor.log.error(f'Fetch error on attempt {attempt + 1}: {e}')
                
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
            
            if not html:
                Actor.log.error(f'Failed to fetch page {page} after {max_retries} attempts')
                break
            
            # Save debug HTML (first page only)
            if page == 1:
                await Actor.set_value('DEBUG_HTML', html[:5000])
                Actor.log.info(f'Saved first 5000 chars of HTML for debugging')
            
            # Parse jobs
            jobs = _extract_job_data(html)
            
            if not jobs:
                Actor.log.warning(f'No jobs found on page {page}')
                # If first page, this is a problem
                if page == 1:
                    Actor.log.error('Failed to find any jobs on first page - parser issue or site structure changed')
                break
            
            Actor.log.info(f'Found {len(jobs)} jobs on page {page}')
            
            # Push results
            for job in jobs:
                if results_count >= max_results:
                    break
                
                job['scrapedAt'] = datetime.now(timezone.utc).isoformat()
                await Actor.push_data(job)
                results_count += 1
                
                if results_count % 10 == 0:
                    Actor.log.info(f'Progress: {results_count}/{max_results} results')
            
            if results_count >= max_results:
                break
            
            if len(jobs) < 10:
                Actor.log.info('Fewer jobs than expected, likely last page')
                break
            
            page += 1
            await asyncio.sleep(1)
        
        Actor.log.info(f'Scraping completed. Total results: {results_count}')

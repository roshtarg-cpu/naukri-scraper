import re
import json
from bs4 import BeautifulSoup

def _extract_job_data(html):
    """Extract job listings from HTML - handles both static and dynamic content."""
    if not html:
        return []
    
    soup = BeautifulSoup(html, 'html.parser')
    jobs = []
    
    # Strategy 1: Look for common job card patterns
    selectors = [
        {'tag': 'article', 'class_pattern': r'jobTuple|job-tuple|job_tuple'},
        {'tag': 'div', 'class_pattern': r'jobTuple|srp-jobtuple|job-card|jobcard'},
        {'tag': 'li', 'class_pattern': r'job|joblist'},
    ]
    
    job_elements = []
    for selector in selectors:
        elements = soup.find_all(selector['tag'], class_=re.compile(selector['class_pattern'], re.I))
        if elements:
            job_elements = elements
            break
    
    # Strategy 2: If no structured elements, look for any element with job-like data
    if not job_elements:
        # Look for elements that have both a title-like and company-like child
        all_divs = soup.find_all(['div', 'article', 'li'])
        for elem in all_divs:
            # Check if it has job-like content
            text = elem.get_text()
            if re.search(r'(year|yrs|experience|salary|₹|lakh|month)', text, re.I):
                job_elements.append(elem)
        
        # Limit to reasonable number
        job_elements = job_elements[:50]
    
    print(f'Found {len(job_elements)} potential job elements')
    
    for job_elem in job_elements:
        try:
            job = {}
            
            # Extract all links and text
            links = job_elem.find_all('a', href=True)
            all_text = job_elem.get_text(separator='|||', strip=True)
            
            # Title (usually first link or heading)
            title_elem = (
                job_elem.find(['a', 'h2', 'h3', 'h4'], class_=re.compile(r'title|job.*title|role', re.I)) or
                (links[0] if links else None)
            )
            if title_elem:
                job['title'] = title_elem.get_text(strip=True)[:200]
                if title_elem.name == 'a' and title_elem.get('href'):
                    url = title_elem['href']
                    job['url'] = url if url.startswith('http') else f"https://www.naukri.com{url}"
            
            # Company
            company_elem = job_elem.find(['a', 'span', 'div'], class_=re.compile(r'company|org|employer', re.I))
            if company_elem:
                job['company'] = company_elem.get_text(strip=True)[:100]
            
            # Try to extract from text patterns
            parts = all_text.split('|||')
            
            # Experience pattern
            exp_match = re.search(r'(\d+\s*-\s*\d+\s*(?:year|yr)s?)', all_text, re.I)
            if exp_match:
                job['experience'] = exp_match.group(1)
            
            # Salary pattern
            sal_match = re.search(r'(₹[\d.,]+\s*-\s*[\d.,]+\s*(?:lakh|lac|lpa|p\.a\.|pa))', all_text, re.I)
            if sal_match:
                job['salary'] = sal_match.group(1)
            
            # Location pattern
            loc_match = re.search(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s*,?\s*(?:[A-Z][a-z]+)?\b', all_text)
            if loc_match:
                potential_loc = loc_match.group(1)
                # Common Indian cities
                cities = ['Bangalore', 'Mumbai', 'Delhi', 'Hyderabad', 'Chennai', 'Pune', 'Kolkata', 'Ahmedabad', 'Noida', 'Gurgaon']
                if any(city.lower() in potential_loc.lower() for city in cities):
                    job['location'] = potential_loc
            
            # Description (truncate)
            desc_elem = job_elem.find(['div', 'p'], class_=re.compile(r'desc|job.*desc|summary', re.I))
            if desc_elem:
                job['description'] = desc_elem.get_text(strip=True)[:500]
            elif len(all_text) > 50:
                job['description'] = all_text[:500]
            
            # Posted date
            date_elem = job_elem.find(['span', 'div'], class_=re.compile(r'date|posted|time|ago', re.I))
            if date_elem:
                job['posted_date'] = date_elem.get_text(strip=True)
            
            # Only add if we got at least a title
            if job.get('title') and len(job['title']) > 3:
                # Ensure all fields exist (even if None)
                for field in ['title', 'url', 'company', 'location', 'experience', 'salary', 'description', 'posted_date']:
                    if field not in job:
                        job[field] = None
                jobs.append(job)
            
        except Exception as e:
            print(f'Error parsing job element: {e}')
            continue
    
    print(f'Successfully parsed {len(jobs)} jobs')
    return jobs

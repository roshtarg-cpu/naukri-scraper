import re
import json
from bs4 import BeautifulSoup

def _extract_job_data(html):
    """Extract job listings from HTML."""
    if not html:
        return []
    
    soup = BeautifulSoup(html, 'html.parser')
    jobs = []
    
    # Look for job cards - Naukri uses various class names
    job_elements = soup.find_all('article', class_=re.compile(r'jobTuple|job-tuple|tuple'))
    
    if not job_elements:
        # Fallback: try finding divs with job-related classes
        job_elements = soup.find_all('div', class_=re.compile(r'jobTuple|srp-jobtuple-wrapper'))
    
    for job_elem in job_elements:
        try:
            job = {}
            
            # Title
            title_elem = job_elem.find(['a', 'h2', 'h3'], class_=re.compile(r'title|jobTitle'))
            job['title'] = title_elem.get_text(strip=True) if title_elem else None
            job['url'] = title_elem.get('href') if title_elem and title_elem.get('href') else None
            if job['url'] and not job['url'].startswith('http'):
                job['url'] = f"https://www.naukri.com{job['url']}"
            
            # Company
            company_elem = job_elem.find(['a', 'span', 'div'], class_=re.compile(r'company|companyInfo'))
            job['company'] = company_elem.get_text(strip=True) if company_elem else None
            
            # Experience
            exp_elem = job_elem.find(['span', 'div'], class_=re.compile(r'experience|exp'))
            job['experience'] = exp_elem.get_text(strip=True) if exp_elem else None
            
            # Salary
            salary_elem = job_elem.find(['span', 'div'], class_=re.compile(r'salary|sal'))
            job['salary'] = salary_elem.get_text(strip=True) if salary_elem else None
            
            # Location
            location_elem = job_elem.find(['span', 'div'], class_=re.compile(r'location|loc'))
            job['location'] = location_elem.get_text(strip=True) if location_elem else None
            
            # Skills
            skills_elems = job_elem.find_all(['span', 'a'], class_=re.compile(r'skill|tag'))
            job['skills'] = [s.get_text(strip=True) for s in skills_elems] if skills_elems else []
            
            # Description
            desc_elem = job_elem.find(['div', 'p'], class_=re.compile(r'description|desc|job-description'))
            job['description'] = desc_elem.get_text(strip=True) if desc_elem else None
            
            # Posted date
            date_elem = job_elem.find(['span', 'div'], class_=re.compile(r'date|posted|time'))
            job['posted_date'] = date_elem.get_text(strip=True) if date_elem else None
            
            # Only add if we got at least a title
            if job.get('title'):
                jobs.append(job)
        except Exception as e:
            print(f'Error parsing job element: {e}')
            continue
    
    return jobs

# Naukri.com Job Scraper

Extract job listings from Naukri.com, India's #1 job board with millions of active jobs. Perfect for recruiters, job aggregators, market research, and AI-powered job search applications.

## Features

- 🎯 **Comprehensive Data**: Extract job titles, companies, salaries, locations, required skills, experience levels, and descriptions
- 🌍 **Location Filtering**: Search jobs by city or across all of India
- 🔍 **Keyword Search**: Find jobs by keywords, skills, or job titles
- 🤖 **AI-Ready**: Works seamlessly with Claude, ChatGPT, and other AI agents via Apify MCP
- 🔄 **Real-time Data**: Always fresh data from Naukri.com's live listings
- 📊 **Structured Output**: Clean JSON format ready for analysis or integration

## Input Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `maxResults` | Integer | Yes | 100 | Maximum number of job listings to scrape (1-10,000) |
| `keywords` | String | No | - | Search keywords (e.g., "python developer", "data scientist") |
| `location` | String | No | "india" | Job location (e.g., "bangalore", "mumbai", "delhi") |
| `experience` | String | No | - | Experience level filter (e.g., "0-2", "2-5", "5-10") |
| `proxyConfiguration` | Object | No | RESIDENTIAL | Proxy settings (recommended: RESIDENTIAL) |

## Output Example

```json
{
  "title": "Senior Python Developer",
  "url": "https://www.naukri.com/job-listings/...",
  "company": "Tech Mahindra",
  "location": "Bangalore, Hyderabad",
  "experience": "5-8 years",
  "salary": "₹15-25 Lakhs P.A.",
  "skills": ["Python", "Django", "AWS", "Docker"],
  "description": "Looking for experienced Python developer with strong backend skills...",
  "posted_date": "2 days ago",
  "scrapedAt": "2026-08-20T00:30:00.000Z"
}
```

## Use Cases

- **Recruiters**: Monitor competitor job postings and salary trends
- **Job Aggregators**: Build comprehensive job search platforms
- **Market Research**: Analyze hiring trends, skill demands, and salary ranges
- **AI Agents**: Power AI-driven job recommendation systems via Claude/ChatGPT
- **Career Platforms**: Aggregate Indian tech jobs for your platform

## Why Naukri.com?

- 🥇 #1 job board in India (ranked #989 globally)
- 📈 80+ million registered job seekers
- 🏢 100,000+ active recruiters
- 💼 800,000+ active job listings
- 🇮🇳 Covers all major Indian cities and industries

## Pricing

- **$0.005 per result** scraped
- **$0.05 per run** (one-time start fee)
- Example: 100 jobs = $0.50 (results) + $0.05 (run) = **$0.55 total**

## Compatible with AI Agents

This actor works seamlessly with:
- **Claude** via Apify MCP
- **ChatGPT** via Apify integration
- **Custom AI agents** via Apify API

## Notes

- Respects Naukri.com's robots.txt
- Uses residential proxies to avoid blocking
- Rate-limited to prevent server overload
- Extracts only publicly available job data

## Support

For issues or feature requests, please contact the actor maintainer.

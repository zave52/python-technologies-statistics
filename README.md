# Python technologies statistics

## Project Description

A data collection and analysis tool that gathers statistics on Python technologies, frameworks, and libraries from
various sources. This project uses web crawling to extract information about Python technology trends, popularity, and
usage patterns.

## Tech Stack

- **Python 3.x** - Core programming language
- **Scrapy** - Web scraping framework for extracting data
- **Pandas** - Data manipulation and analysis
- **Matplotlib** - Data visualization
- **Jupyter Notebook** - Interactive data analysis
- **Selenium** - Web browser automation for scraping dynamic content

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/python-technologies-statistics.git
   cd python-technologies-statistics
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On Unix or MacOS
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Spiders

Spiders are located in the `scrapy-jobs/spiders` directory. To run a specific spider:

```bash
# Run a specific spider
scrapy crawl spider_name -o output_file.json

# Example:
scrapy crawl dou
```

To list all available spiders:

```bash
scrapy list
```

### Data Analysis

After collecting data with the spiders, you can analyze it using the analysis scripts:

```bash
# Run the main analysis script
python statistic/analyze.py

# Or for interactive analysis
jupyter notebook statistic/vacancy_analysis.ipynb
```

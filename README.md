# KL Racing Web Scraper

A web scraper for extracting product information from shop.klracing.se.

## Prerequisites

- Python 3.11 or higher
- Git
- Homebrew (for macOS users)

## Installation

### 1. Clone and Setup Repository

```bash
# Clone the repository
git clone git@github.com:arooj-fatima-brainx/engs-motorsproduckter.git

# Navigate to project directory
cd engs-motorsproduckter

### 2. Install Python (if not installed)

#### For macOS:
```bash
# Install Homebrew if you haven't already
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.11
brew install python@3.11
```

#### For Linux:
```bash
sudo apt update
sudo apt install python3 python3-venv
```

### 3. Set Up Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

## Usage

With the virtual environment activated, run the scraper:

```bash
python scraper.py
```

The scraper will:
1. Parse the sitemap from shop.klracing.se
2. Extract product URLs
3. Scrape product information
4. Save results to `products.json`

To stop the scraper at any time, press `Ctrl + C`.

## Project Structure

```
.
├── README.md
├── requirements.txt
├── scraper.py
└── .gitignore
```

## Requirements

- requests==2.31.0
- beautifulsoup4==4.12.2
- html5lib==1.1

## Troubleshooting

If you encounter any issues:

1. Make sure you're using Python 3.11:
```bash
python --version
```

2. If the virtual environment isn't working:
```bash
# Deactivate if active
deactivate

# Remove old environment
rm -rf venv

# Create new environment
python3.11 -m venv venv

# Activate and install requirements
source venv/bin/activate
pip install -r requirements.txt
```

3. To deactivate the virtual environment when done:
```bash
deactivate
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

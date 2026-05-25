from data_collector.url_scraper import URLScraper

url = "https://betou.bet.br/games/spribe/aviator"

scraper = URLScraper(url)

print("Testando captura...")

value = scraper.get_latest()

print("Última vela:", value)
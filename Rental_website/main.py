from Extractor.apartment_collector import main as apartment_collector_main
from Extractor.kijiji_collector import main as kijiji_collector_main
from Extractor.rentalhub_collector import main as rentalhub_collector_main
from Extractor.zumper_collector import main as zumper_collector_main

def main():
    apartment_collector_main()
    kijiji_collector_main()
    rentalhub_collector_main()
    zumper_collector_main()

if __name__ == "__main__":
    main()

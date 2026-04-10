import requests
import os


def main():
    url = "https://raw.githubusercontent.com/Escavine/World-Happiness/main/World-happiness-report-2024.csv"
    output_path = "data/bronze/happiness_raw.csv"

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print(f"Downloading from {url}...")
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    with open(output_path, "wb") as f:
        f.write(response.content)

    print(f"Saved raw CSV to {output_path}")
    print(f"File size: {os.path.getsize(output_path)} bytes")


if __name__ == "__main__":
    main()

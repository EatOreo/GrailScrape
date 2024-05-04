import re
import csv
from playwright.sync_api import sync_playwright

template = """
<!DOCTYPE html>
<html>
<head>
    <title>CSV Data</title>
    <style>
        .item {
            display: inline-block;
            margin: 10px;
            text-align: center;
        }
        .item img {
            width: 200px;
            height: 200px;
            object-fit: cover;
        }
        .item p {
            margin-top: 5px;
        }
    </style>
</head>
<body>
    <div id="container"></div>

    <script>
        const csvData = `*CSV_DATA*`;

        const rows = csvData.split('\\n');
        const container = document.getElementById('container');

        rows.forEach(row => {
            const columns = row.split(',');

            const url = columns[0];
            const price = columns[1];
            const image = columns[2] + "w=300";
            const sizes = columns[3];

            const item = document.createElement('div');
            item.className = 'item';

            const a = document.createElement('a');
            a.href = url;

            const img = document.createElement('img');
            img.src = image;

            const p1 = document.createElement('p');
            p1.textContent = `Price: ${price}`;

            const p2 = document.createElement('p');
            p2.textContent = `${sizes.replace(/;/g, ', ')}`;

            item.appendChild(a);
            a.appendChild(img);
            item.appendChild(p1);
            item.appendChild(p2);
            container.appendChild(item);
        });
    </script>
</body>
</html>
"""

urls = [
        "https://www.grailed.com/listings/53428794-lee-x-vintage-vintage-lee-faded-wash-denim",
        "https://www.grailed.com/listings/54289752-levi-s-x-streetwear-x-vintage-vintage-90s-levis-501-painter-jeans-blue-size-w33-l34",
        "https://www.grailed.com/listings/60411060-avant-garde-x-japanese-brand-x-vintage-vintage-y2k-multipocket-kosmo-lupo-avant-garde-jeans-k-m",
        "https://www.grailed.com/listings/60449222-japanese-brand-x-streetwear-x-vintage-mens-stacked-denim-jeans-size-30",
    ]
with open('targetLinks.txt', 'r') as file:
    urls = file.read().splitlines()

meas = [["Waist", 80.5, 84.0], ["Inseam", 84.0, 90.0], ["Leg Opening", 40, 44]]

try:
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()
        for url in urls:
            page.goto(url, wait_until="load")
            try:
                measurements_string = page.get_by_test_id("ListingPageMeasurements").all_inner_texts()[0]
            except:
                continue

            score = len(meas)
            measurements = ""

            for mea in meas:
                pattern = mea[0] + r"\n\n(\d+(\.\d+)?) in\n(\d+(\.\d+)?) cm"
                match = re.search(pattern, measurements_string)
                if match:
                    cm = float(match.group(3))
                    if (cm >= mea[1] and cm <= mea[2]) or (cm * 2 >= mea[1] and cm * 2 <= mea[2]):
                        print(f"{mea[0]}: {cm} success")
                        measurements += f"{mea[0]}: {cm}cm;"
                        score -= 1
                    else:
                        continue
                else:
                    continue
            if score == 0:
                print(url)

                price = page.query_selector('.Money_root__8lDCT').inner_text()
                img = page.query_selector('img')
                imgsrc = img.get_attribute('src')

                with open('output.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([url, price, imgsrc, measurements])
        browser.close()
finally:
    csv_data = ""
    with open('output.csv', 'r') as file:
        csv_data = file.read()

    template = template.replace("*CSV_DATA*", csv_data)

    with open('output.html', 'w', newline='') as file:
        file.write(template)
import csv

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

csv_data = ""
with open('output.csv', 'r') as file:
    csv_data = file.read()

template = template.replace("*CSV_DATA*", csv_data)

with open('output.html', 'w', newline='') as file:
    file.write(template)
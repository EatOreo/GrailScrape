# Grailscape
Script that finds Grailed.com listings with specific measurements which can not be filtered by in the search function.

To run:
```python
python3 -m pip install playwright==1.35.0
python3 -m playwright install
python3 measurements_script.py
```

To generate target links, go to grailed and filter search then paste this in the browser developer console:

```javascript
let targetLinks = new Set();

function findLinks() {
    let links = document.querySelectorAll('a');

    for (let link of links) {
        let href = link.href;
        if (href.startsWith('https://www.grailed.com/listings/') && !href.endsWith('/similar')) {
            targetLinks.add(href);
        }
    }
}

let observer = new MutationObserver(findLinks);
observer.observe(document, {childList: true, subtree: true});

findLinks();
```

When scrolled to bottom of searches paste this in developer console:

```javascript
let data = Array.from(targetLinks).join('\n');
let blob = new Blob([data], {type: 'text/plain'});

let url = URL.createObjectURL(blob);
let a = document.createElement('a');
a.href = url;
a.download = 'targetLinks.txt';
a.click();
```

Now move the downloaded targetLinks.txt from downloads into the project directory, now you can run the python script

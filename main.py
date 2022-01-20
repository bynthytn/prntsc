from downloader import get_url_from_html, download_file


html_path = 'images/ksheuf.html'
download_file('https://prnt.sc/ksheuf', html_path)
url = get_url_from_html(html_path)

download_file(url, 'images\sregrrr.jpg')




import os
import requests
import json
import time

# Thay thế 'your_api_key' bằng API key của bạn
api_key = '3mlRKtc63wcGoR7LRWR2FIZukTJPGHxX'

# Danh sách các phần bạn muốn tìm kiếm
sections = ['Arts', 'Technology', 'Food', 'Real Estate', 'Sports', 'Travel']

# Đường dẫn đến thư mục chính
main_dir = "article_search\\test_data"

# Số lượng bài viết tối đa cho mỗi phần
max_articles_per_section = 100

# Số lượng yêu cầu tối đa mỗi phút
max_requests_per_minute = 5


# Hàm để kiểm tra xem một khóa có tồn tại trong một từ điển và giá trị của nó không phải là None hoặc chuỗi rỗng
def check_key_and_value(dictionary, key):
    return key in dictionary and dictionary[key] and dictionary[key].strip()


# Duyệt qua từng phần
for section in sections:
    # Tạo thư mục cho mỗi phần nếu chưa tồn tại
    os.makedirs(os.path.join(main_dir, section), exist_ok=True)

    # Số lượng bài viết đã tải về cho phần này
    num_articles = 0

    # Số lượng yêu cầu đã gửi trong phút này
    num_requests = 0

    # Thời gian bắt đầu của phút hiện tại
    start_time = time.time()

    # Danh sách ID của các bài viết đã tải về
    downloaded_ids = set()

    # Page number for the API request
    page_number = 0

    while num_articles < max_articles_per_section:
        # Nếu đã gửi đủ số lượng yêu cầu tối đa trong phút này, chờ đợi đến phút tiếp theo
        if num_requests >= max_requests_per_minute:
            wait_time = 60 - (time.time() - start_time)
            if wait_time > 0:
                time.sleep(wait_time)
            num_requests = 0
            start_time = time.time()

        # Tạo URL cho yêu cầu
        url = f'https://api.nytimes.com/svc/search/v2/articlesearch.json?fq=section_name:("{section}") AND pub_year:>2023&page={page_number}&api-key={api_key}'

        # Gửi yêu cầu và nhận dữ liệu trả về
        response = requests.get(url)

        # Kiểm tra xem yêu cầu có thành công hay không
        if response.status_code == 200:
            data = response.json()

            # Kiểm tra xem dữ liệu có khóa 'response' hay không
            if 'response' in data:
                # Duyệt qua từng bài viết trong dữ liệu trả về
                for article in data['response']['docs']:
                    # Kiểm tra xem bài viết có chứa các khóa cần thiết và chúng không phải là None hoặc chuỗi rỗng
                    if check_key_and_value(article, '_id') and article['_id'] not in downloaded_ids and \
                            check_key_and_value(article, 'lead_paragraph') and \
                            check_key_and_value(article, 'snippet') and \
                            'headline' in article and check_key_and_value(article['headline'], 'main'):
                        # Thêm ID của bài viết vào danh sách đã tải về
                        downloaded_ids.add(article['_id'])

                        # Tạo đường dẫn đến tệp cho mỗi bài viết
                        file_path = os.path.join(main_dir, section, f'{num_articles + 1}.txt')

                        # Lưu tiêu đề và nội dung bài viết vào tệp
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(article['headline']['main'] + ' ')
                            f.write(article['snippet'] + ' ')
                            f.write(article['lead_paragraph'])

                        num_articles += 1

                # Increment the page number for the next API request only if we have downloaded 10 articles
                page_number += 1
            else:
                print(f"Error: The data returned from the API does not contain 'response': {data}")
        else:
            print(f"Error: The request was not successful, the HTTP status code is {response.status_code}")

        num_requests += 1

        # Print the progress
        print(f'Downloaded {num_articles} articles from the {section} section')

        # Wait 12 seconds before sending the next request
        time.sleep(12)

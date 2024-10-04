from pytube import YouTube
import pandas as pd

# Đọc dữ liệu từ file csv
df = pd.read_csv('output.csv')
urls = df['URL'].tolist()

# Danh sách để lưu trữ thông tin video
videos = []

for url in urls:
    try:
        yt = YouTube(url)
        duration = yt.length  # Thời lượng video tính bằng giây
        videos.append({'URL': url, 'Duration': duration})
    except Exception as e:
        print(f"Không thể truy cập {url}: {e}")

# Lọc các video có thời lượng ít hơn 5 phút
short_videos = [video for video in videos if video['Duration'] < 300]

# Sắp xếp các video theo độ dài từ thấp đến cao
sorted_videos = sorted(videos, key=lambda x: x['Duration'])

# Lưu lại danh sách đã lọc và sắp xếp vào file csv mới
output_df = pd.DataFrame(sorted_videos)
output_df.to_csv('sorted_videos.txt', index=False)

# In ra danh sách các video đã sắp xếp
print("Danh sách các video được sắp xếp theo thời lượng từ thấp đến cao:")
for video in sorted_videos:
    print(f"URL: {video['URL']}")

# Lưu lại danh sách các video ngắn hơn 5 phút vào file csv khác
short_videos_df = pd.DataFrame(short_videos)
short_videos_df.to_csv('short_videos.txt', index=False)

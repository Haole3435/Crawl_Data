import re
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

YOUTUBE_PLAYLIST_URL = "https://www.youtube.com/playlist?list={}"
YOUTUBE_VIDEO_URL = "https://www.youtube.com/watch?v={}"
RE_VIDEO_ID = re.compile(r"\"/watch\?v=(.{11})")


class GetAllVideoID:
    def __init__(self):
        options = Options()
        options.add_argument('--headless')
        self.driver = webdriver.Firefox(options=options)

    def get_all_video(self, playlist_id):
        self.driver.get(YOUTUBE_PLAYLIST_URL.format(playlist_id))
        time.sleep(5)  # Đợi trang tải

        num_video = 0
        body = self.driver.find_element(By.TAG_NAME, 'body')
        while True:
            # Scroll down to the bottom.
            for _ in range(5):
                body.send_keys(Keys.PAGE_DOWN)
                time.sleep(1)
            new_num_video = len(self.driver.find_elements(By.CSS_SELECTOR, "#contents ytd-playlist-video-renderer"))
            if num_video == new_num_video:
                break
            num_video = new_num_video
        ids = set(re.findall(RE_VIDEO_ID, self.driver.page_source))
        return list(ids)


if __name__ == '__main__':
    playlist_id = sys.argv[1]
    output_file = sys.argv[2]
    getAllVideo = GetAllVideoID()
    try:
        ids = getAllVideo.get_all_video(playlist_id)
        with open(output_file, 'a', encoding='utf8') as fp:
            for video_id in ids:
                fp.write(YOUTUBE_VIDEO_URL.format(video_id) + "\n")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(2)
    finally:
        getAllVideo.driver.quit()

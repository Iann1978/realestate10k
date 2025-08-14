

from peewee import *
import os
from subprocess import call
import shutil
import cv2
from tqdm import tqdm





class Video(Model):
    state = CharField()
    split = CharField()
    txtfile = CharField()
    url = CharField()

    class Meta:
        database = None



class Builder:
    def __init__(self, dbfile='downloading.sqlite', root='RealEstate10K'):
        self.root = root
        self.dbfile = dbfile
        self.db = None


    def open(self):
        print(f"open database: {self.dbfile}")
        if os.path.exists(self.dbfile):
            print(f"remove existing database: {self.dbfile}")
            os.remove(self.dbfile)
        db = SqliteDatabase(self.dbfile)
        Video._meta.database = db
        db.connect()
        db.create_tables([Video])
        self.db = db


    def close(self):
        print(f"close database: {self.dbfile}")
        self.db.close()


    def build(self):
        self.open()
        print(f"build database: {self.dbfile}")
        for split in ['train', 'test']:
            print(f"build {split} database")
            for txtfile in tqdm(os.listdir(os.path.join(self.root, split))):
                with open(os.path.join(self.root, split, txtfile), 'r') as f:
                    url = f.readline().strip()
                    Video.create(split=split, txtfile=txtfile, url=url, state='undownloaded')
        self.print_downloading_info()
        self.close()


    def print_downloading_info(self):
        undownloaded_count = Video.select().where(Video.state == 'undownloaded').count()
        # downloading_count = Video.select().where(Video.state == 'downloading').count()
        downloaded_count = Video.select().where(Video.state == 'downloaded').count()
        failed_count = Video.select().where(Video.state == 'failed').count()
        total_count = Video.select().count()
        print(f"downloading info: {undownloaded_count}/{downloaded_count}/{failed_count}/{total_count} (undownloaded/downloaded/failed/total)")


class Downloader:
    def __init__(self, dbfile='downloading.sqlite', root='RealEstate10K'):
        self.root = root
        self.dbfile = dbfile
        self.tmppath = 'temp'
        self.db = self.open()
        self.print_downloading_info()

    def open(self):
        if not os.path.exists(self.dbfile):
            raise FileNotFoundError(f"Database file not found: {self.dbfile}")
        print(f"open database: {self.dbfile}")
        db = SqliteDatabase(self.dbfile)
        Video._meta.database = db
        db.connect()
        return db

    def close(self):
        print(f"close database: {self.dbfile}")
        self.db.close()


    def clean_tmp(self):
        if os.path.exists(self.tmppath):
            shutil.rmtree(self.tmppath)
        # Select all videos with state 'downloading' and set their state to 'undownloaded'
        query = Video.update(state='undownloaded').where(Video.state == 'downloading')
        count = query.execute()
        print(f"cleaned {count} videos")
        self.print_downloading_info()
    
    def download_one(self, video):
        print(f"\nDownloading video: txtfile={video.txtfile}, url={video.url}")
        video.state = 'downloading'
        video.save()
        url = video.url
        video_id = url.split('=')[-1]
        if not os.path.exists(self.tmppath):
            os.makedirs(self.tmppath)
        tmp_path = os.path.join(self.tmppath, video_id)
        save_path = os.path.join('downloaded', video.split, video_id)
        if not os.path.exists(os.path.dirname(save_path)):
            os.makedirs(os.path.dirname(save_path))


        return_code = call(["yt-dlp", "-f", "bestvideo", url, "-o", tmp_path, "--cookies", "./cookies.txt" ])
        if return_code == 0:
            os.rename(tmp_path, save_path)
            video.state = 'downloaded'
            video.save()
        else:
            video.state = 'failed'
            video.save()
        self.print_downloading_info()

        


    def print_downloading_info(self):
        undownloaded_count = Video.select().where(Video.state == 'undownloaded').count()
        # downloading_count = Video.select().where(Video.state == 'downloading').count()
        downloaded_count = Video.select().where(Video.state == 'downloaded').count()
        failed_count = Video.select().where(Video.state == 'failed').count()
        total_count = Video.select().count()
        print(f"downloading info: {undownloaded_count}/{downloaded_count}/{failed_count}/{total_count} (undownloaded/downloaded/failed/total)")

    def download(self):
        count = Video.select().where(Video.state == 'undownloaded').count()
        if count == 0:
            print("No undownloaded videos")
            return
       
        
        print(f"\nstart downloading videos")

        # Select one undownloaded video
        while True:
            video = Video.select().where(Video.state == 'undownloaded').limit(1).first()
            if not video:
                break

            self.download_one(video)

        print(f"\ndownload finished!!!")



    
        


def build_downloading_database():
    print('build downloading database')
    builder = Builder()
    builder.build()
    builder.close()


def download():
    print('download videos')
    downloader = Downloader()
    downloader.clean_tmp()
    downloader.download()
    downloader.close()
    exit()







if __name__ == '__main__':

    if not os.path.exists('downloading.sqlite'):
        build_downloading_database()
    download()





import requests

from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Scrap Youtube'

    def handle(self, *args, **kwargs):
        from googleapiclient.discovery import build
        youtube_api_key = 'AIzaSyAwDzi-jy4pajYALp1H3d3aia8-sdk5qP8'
        youtube = build('youtube', 'v3', developerKey=youtube_api_key)

        lis = ['UCeLHszkByNZtPKcaVXOCOQQ']

        for i in lis:
            channels_response = youtube.channels().list(part="snippet,contentDetails,statistics,topicDetails,status",
                                                        id=i).execute()

            for channel in channels_response['items']:
                uploads_list_id = channel["contentDetails"]["relatedPlaylists"]["uploads"]
                playlistitems_list_request = youtube.playlistItems().list(
                    playlistId=uploads_list_id,
                    part="snippet",
                    maxResults=50
                )
                while playlistitems_list_request:
                    playlistitems_list_response = playlistitems_list_request.execute()
                    for playlist_item in playlistitems_list_response["items"]:
                        video_id = playlist_item["snippet"]["resourceId"]["videoId"]
                        request = youtube.videos().list(
                            part="snippet,contentDetails,statistics",
                            id=video_id
                        )
                        response = request.execute()

                        print(video_id)
                        tags = response['items'][0]['snippet']['tags']
                        print(tags)
                        statistics = response['items'][0]['statistics']
                        print(statistics)
                        view_count = response['items'][0]['statistics']['viewCount']
                        print(view_count)
                        print("##########################")

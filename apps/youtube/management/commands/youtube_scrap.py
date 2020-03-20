from django.core.management.base import BaseCommand, CommandError
from googleapiclient.discovery import build
from apps.youtube.models import Channel, Video
import json

class Command(BaseCommand):
    help = 'Scrap Youtube'

    def handle(self, *args, **kwargs):
        youtube_api_key = 'AIzaSyAwDzi-jy4pajYALp1H3d3aia8-sdk5qP8'
        youtube = build('youtube', 'v3', developerKey=youtube_api_key)
        channel_list = Channel.objects.values_list('channel_uid', flat=True)
        # channel_list = ['UCeLHszkByNZtPKcaVXOCOQQ']

        for i in channel_list:
            channel_object = Channel.objects.get(channel_uid=i)
            channels_response = youtube.channels().list(part="snippet,contentDetails,statistics,topicDetails,status",
                                                        id=i).execute()
            for channel in channels_response['items']:
                uploads_list_id = channel["contentDetails"]["relatedPlaylists"]["uploads"]
                playlistitems_list_request = youtube.playlistItems().list(
                    playlistId=uploads_list_id,
                    part="snippet",
                    maxResults=50
                )
                playlistitems_list_response = playlistitems_list_request.execute()
                for playlist_item in playlistitems_list_response["items"]:
                    video_uid = playlist_item["snippet"]["resourceId"]["videoId"]
                    request = youtube.videos().list(
                        part="snippet,contentDetails,statistics",
                        id=video_uid
                    )
                    response = request.execute()

                    tags = response['items'][0]['snippet']['tags']
                    print(tags)
                    title = response['items'][0]['snippet']['title']
                    statistics = response['items'][0]['statistics']
                    view_count = statistics['viewCount']
                    like_count = statistics['likeCount']
                    comment_count = statistics['commentCount']
                    dislike_count = statistics['dislikeCount']
                    favorite_count = statistics['favoriteCount']
                    try:
                        video = Video.objects.get(video_uid=video_uid)
                        video.name = title
                        video.tags = tags
                        video.view_count = view_count
                        video.like_count = like_count
                        video.comment_count = comment_count
                        video.dislike_count = dislike_count
                        video.favorite_count = favorite_count
                        video.save()
                    except Video.DoesNotExist:
                        video = Video.objects.create(name=title, channel=channel_object, video_uid=video_uid,
                                                     tags=tags,
                                                     view_count=view_count, like_count=like_count,
                                                     dislike_count=dislike_count, favorite_count=favorite_count,
                                                     comment_count=comment_count)

        """ Video performance """
        import statistics

        videos = Video.objects.all()
        views_list = videos.values_list('view_count', flat=True)
        median = statistics.median(views_list)
        for video in videos:
            video.performance = video.view_count / median
            video.save()


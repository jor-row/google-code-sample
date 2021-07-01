"""A video player class."""

from src.video import Video
from .video_library import VideoLibrary
from .command_parser import CommandException
from random import randrange
import re

class VideoPlayer:
    """A class used to represent a Video Player."""
    _video_library = VideoLibrary()
    current_video = None
    current_paused = False

    def __init__(self, playlist_names = {}, playlists = {}, videos_dict = {}):
        self.playlist_names = {}
        self.playlists = {}
        self.videos_dict = {}

        all_videos = self._video_library.get_all_videos()
        
        for video in all_videos:
            video._flagged = False
            tags_string = ""
            for tag in video._tags:
                tags_string += tag + " "
            self.videos_dict[video] = video._title + " (" + video._video_id + ") " + "[" + tags_string.strip() + "]"

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        print("Here's a list of all available videos:")

        all_videos = self._video_library.get_all_videos()
        avail_videos_strings = []
        
        for video in all_videos:
            if not video.flagged:
                tags_string = ""
                for tag in video._tags:
                    tags_string += tag + " "
                avail_videos_strings.append(video._title + " (" + video._video_id + ") " + "[" + tags_string.strip() + "]")
            else:
                tags_string = ""
                for tag in video._tags:
                    tags_string += tag + " "
                avail_videos_strings.append(video._title + " (" + video._video_id + ") " + "[" + tags_string.strip() + "]" + " - FLAGGED (reason: " + video.flag_reason + ")")

        avail_videos_strings.sort()
        print(*avail_videos_strings, sep="\n")

    def play_video(self, video_id):
        """Plays the respective video.
        
        Args:
            video_id: The video_id to be played.
        """

        if self._video_library.get_video(video_id) is None:
            print("Cannot play video: Video does not exist")
        elif self._video_library.get_video(video_id).flagged:
            print(f"Cannot play video: Video is currently flagged (reason: {self._video_library.get_video(video_id).flag_reason})")
        elif self.current_video is not None:
            # If different must stop
            print("Stopping video:", self.current_video.title)
            self.current_video = self._video_library.get_video(video_id)
            self.current_paused = False
            print("Playing video:", self.current_video.title)
        elif self.current_video is None:
            # If nothing currently playing
            self.current_video = self._video_library.get_video(video_id)
            self.current_paused = False
            print("Playing video:", self.current_video.title)

    def stop_video(self):
        """Stops the current video."""

        if self.current_video is None:
            print("Cannot stop video: No video is currently playing")
        else:
            print("Stopping video:", self.current_video.title)
            self.current_video = None

    def play_random_video(self):
        """Plays a random video from the video library."""
        #[ expression for item in list if conditional ]
        unflagged_videos = [video for video in self._video_library.get_all_videos() if not video.flagged]
        #ran_num = randrange(len(self._video_library.get_all_videos()))
        if len(unflagged_videos) == 0:
            print("No videos available")
        else:
            ran_num = randrange(len(unflagged_videos))
            #random_video_id = self._video_library.get_all_videos()[ran_num]._video_id
            random_video_id = unflagged_videos[ran_num]._video_id
            self.play_video(random_video_id)

    def pause_video(self):
        """Pauses the current video."""
        if self.current_video is None:
            print("Cannot pause video: No video is currently playing")
        elif self.current_paused is False:
            print("Pausing video:", self.current_video.title)
            self.current_paused = True
        elif self.current_paused:
            print("Video already paused:", self.current_video.title)

    def continue_video(self):
        """Resumes playing the current video."""
        if self.current_video is None:
            print("Cannot continue video: No video is currently playing")
        elif not self.current_paused:
            print("Cannot continue video: Video is not paused")
        elif self.current_paused:
            print("Continuing video:", self.current_video.title)
        
        

    def show_playing(self):
        """Displays video currently playing."""
        
        if self.current_video is None:
            print("No video is currently playing")
        else:
            print("Currently playing:", self.videos_dict[self.current_video], end = " ")
            if self.current_paused:
                print("- PAUSED")

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.lower() in self.playlists:
            print("Cannot create playlist: A playlist with the same name already exists")
        else:
            self.playlist_names[playlist_name.lower()] = playlist_name
            self.playlists[playlist_name.lower()] = []
            print("Successfully created new playlist:", playlist_name)

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        if playlist_name.lower() not in self.playlists:
            print("Cannot add video to", playlist_name, end="")
            print(": Playlist does not exist")
        elif self._video_library.get_video(video_id) is None:
            print("Cannot add video to", playlist_name, end="") 
            print(": Video does not exist")
        elif self._video_library.get_video(video_id).flagged:
             print(f"Cannot add video to {playlist_name}: Video is currently flagged (reason: {self._video_library.get_video(video_id).flag_reason})")
        elif self._video_library.get_video(video_id) in self.playlists[playlist_name.lower()]:
            print("Cannot add video to", playlist_name, end="") 
            print(": Video already added")
        else:
            print("Added video to", playlist_name, end="") 
            print(":",self._video_library.get_video(video_id).title)
            self.playlists[playlist_name.lower()].append(self._video_library.get_video(video_id))


    def show_all_playlists(self):
        """Display all playlists."""

        sorted_playlists = []
        for key in self.playlists:
            sorted_playlists.append(key)
        sorted_playlists.sort()

        if len(self.playlists) == 0:
            print("No playlists exist yet")
        else:
            print("Showing all playlists:")
            for name in sorted_playlists:
                print(self.playlist_names[name])

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        
        if playlist_name.lower() not in self.playlists:
            print("Cannot show playlist", playlist_name, end="")
            print(": Playlist does not exist")
        elif len(self.playlists[playlist_name.lower()]) == 0:
            print("Showing playlist:", playlist_name)
            print("No videos here yet")
        else:
            print("Showing playlist:", playlist_name)
            for video in self.playlists[playlist_name.lower()]:
                if video.flagged:
                    print(f"{self.videos_dict[video]} - FLAGGED (reason: {video.flag_reason})")
                else:
                    print(self.videos_dict[video])

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        if playlist_name.lower() not in self.playlists:
            print("Cannot remove video from", playlist_name, end="")
            print(": Playlist does not exist")
        elif self._video_library.get_video(video_id) is None:
            print("Cannot remove video from", playlist_name, end="") 
            print(": Video does not exist") 
        elif self._video_library.get_video(video_id) not in self.playlists[playlist_name.lower()]:
            print("Cannot remove video from", playlist_name, end="")
            print(": Video is not in playlist ")
        else:
            print("Removed video from", playlist_name, end="")
            print(":", self._video_library.get_video(video_id).title)
            self.playlists[playlist_name.lower()].remove(self._video_library.get_video(video_id))

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.lower() not in self.playlists:
            print("Cannot clear playlist", playlist_name, end="")
            print(": Playlist does not exist")
        else:
            print("Successfully removed all videos from", playlist_name)
            self.playlists[playlist_name.lower()].clear()

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.lower() not in self.playlists:
            print("Cannot delete playlist", playlist_name, end="")
            print(": Playlist does not exist")
        else:
            print("Deleted playlist:", playlist_name)
            self.playlists.pop(playlist_name.lower())

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        recommendations = []
        for video in self.videos_dict:
            if not video.flagged and search_term in self.videos_dict[video]:
                recommendations.append(self.videos_dict[video])
        
        recommendations.sort()
        n = len(recommendations)


        if n == 0:
            print(f"No search results for {search_term}")
        else:
            print(f"Here are the results for {search_term}:")
            for i in range(n):
                print(f"{i+1}) {recommendations[i]}")
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")

            try:
                response = int(input())
                if response in range(1,n+1):
                    wanted_video_info = recommendations[response-1]
                    #print(wanted_video_info)
                    s = wanted_video_info
                    result = re.search(r"\(([A-Za-z0-9_]+)\)", s)
                    #print(result.group(1))
                    self.play_video(result.group(1))
            except ValueError:
                pass




    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        recommendations = []

        if not video_tag.startswith("#"):
            print(f"No search results for {video_tag}")
        else:
            for video in self.videos_dict:
                #s = self.videos_dict[video]
                #result = re.search(r"\[([A-Za-z0-9_]+)\]", s)
                #print(result.group(1))
                #tag_string = str(result.group(1))
                #if video_tag in tag_string:
                #    recommendations.append(self.videos_dict[video])
                if video_tag in video._tags and not video.flagged:
                    recommendations.append(self.videos_dict[video])
        
            recommendations.sort()
            n = len(recommendations)

            if n == 0:
                print(f"No search results for {video_tag}")
            else:
                print(f"Here are the results for {video_tag}:")
                for i in range(n):
                    print(f"{i+1}) {recommendations[i]}")
                print("Would you like to play any of the above? If yes, specify the number of the video.")
                print("If your answer is not a valid number, we will assume it's a no.")

                try:
                    response = int(input())
                    if response in range(1,n+1):
                        wanted_video_info = recommendations[response-1]
                        #print(wanted_video_info)
                        s = wanted_video_info
                        result = re.search(r"\(([A-Za-z0-9_]+)\)", s)
                        #print(result.group(1))
                        self.play_video(result.group(1))
                except ValueError:
                    pass


    def flag_video(self, video_id, flag_reason="Not supplied"):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        if self._video_library.get_video(video_id) is None:
            print("Cannot flag video: Video does not exist")
        elif self._video_library.get_video(video_id).flagged:
            print("Cannot flag video: Video is already flagged")
        else:
            if self.current_video is not None and self.current_video.video_id == video_id:
                self.stop_video() 
            print(f"Successfully flagged video: {self._video_library.get_video(video_id).title} (reason: {flag_reason})")
            self._video_library.get_video(video_id).flagged = True
            self._video_library.get_video(video_id).flag_reason = flag_reason
        

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        if self._video_library.get_video(video_id) is None:
            print("Cannot remove flag from video: Video does not exist")
        elif not self._video_library.get_video(video_id).flagged:
            print("Cannot remove flag from video: Video is not flagged")
        else:
            print(f"Successfully removed flag from video: {self._video_library.get_video(video_id).title}")
            self._video_library.get_video(video_id).flagged = False
            self._video_library.get_video(video_id).flag_reason = "Not supplied"

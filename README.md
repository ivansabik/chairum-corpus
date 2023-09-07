# Chairum Corpus

![Mexico is fine](./thij_ij_fine.png)

A corpus of publicly available speeches from Mexican president Andres Manuel Lopez Obrador. 
Currently data is sourced exclusively from YouTube. For some videos it was not possible to get the automatically generated subtitles to source the transcriptions, in future iterations a mechanism will be added to translate them into text.

*Image source: https://twitter.com/marianojuarez/status/1148739501604450304*

## Data

Individual files in JSON format are provided under the `data` folder. Additionally, a script is provided to generate a file in CSV format with all records. Sample record:

```json
{
    "video_id": "_uNpYoBHukM",
    "video_thumbnail_url": "https://i.ytimg.com/vi/_uNpYoBHukM/hqdefault.jpg?sqp=-oaymwEcCNACELwBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLBiA5GPXPQfIJ7UxkMLQKQY9gKhhQ",
    "video_url": "https://www.youtube.com/watch?v=_uNpYoBHukM",
    "video_title": "M\u00e9xico garantiza derecho de asilo a solicitantes de Nicaragua. Conferencia presidente AMLO",
    "video_length_seconds": 10097,
    "transcription_with_timestamps": [
        {
            "text": "el INE no se toca",
            "start": 1803.179,
            "duration": 5.761
        },
        {
            "text": "pero tambi\u00e9n",
            "start": 1806.6,
            "duration": 5.959
        },
        {
            "text": "Garc\u00eda Luna no se toca",
            "start": 1808.94,
            "duration": 3.619
        },
        {
            "text": "y en el fondo es",
            "start": 1812.779,
            "duration": 3.081
        },
        {
            "text": "el r\u00e9gimen",
            "start": 1816.159,
            "duration": 6.781
        },
        {
            "text": "corrupto y conservador no se toca",
            "start": 1818.26,
            "duration": 4.68
        },
        {
            "text": "para eso es pero es bueno",
            "start": 1826.039,
            "duration": 4.941
        }
    ],
    "transcription_text": " el INE no se toca pero tambi\u00e9n Garc\u00eda Luna no se toca y en el fondo es el r\u00e9gimen corrupto y conservador no se toca para eso es pero es bueno",
    "transcription_source": "YouTube auto-generated captions",
    "playlist_id": "PLRnlRGar-_296KTsVL0R6MEbpwJzD8ppA",
    "playlist_title": "Conferencias de prensa matutinas",
    "published_time_text": "Streamed 6 months ago",
    "retrieved_time": "2023-09-07 20:16:50.123990"
}
```

## How to run?

1. Install requirements:
```
pip3 install -r requirements.txt
```
2. Get a YouTube API token and set an environment variable with this value:
```
export YOUTUBE_V3_API_KEY={YOUR_TOKEN}
```
3. Run:
```
python process.py
```

## Future work

- Filter out or annotate parts of videos where speaker is not AMLO
- Exclude videos from speeches where speaker is not AMLO
- Exclude videos which are not from a speech, conference, etc (like ads)
- Implement speech to text for automated translations not available (notably where not enabled by publisher or where auto-generated subtitles have a different language associated)
- Add field or a way of identifying transcription method
- Add persistence (db backend)
- Add API
    - Handle gracefully phonetic coincidences (Krauze, Krause, Kraus, Krauz) using something like Metaphone or Baider-Morse
- Add simple app to search and query the data

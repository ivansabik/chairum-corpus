# Chairum Corpus

![Mexico is fine](./thij_ij_fine.png)

A corpus of publicly available speeches for Mexican president Andres Manuel Lopez Obrador. 
Currently data is sourced exclusively from YouTube. For some videos it was not possible to get the automatically generated subtitles to source the transcriptions, in future iterations a mechanism will be added to translate them into text.

*Image source: https://twitter.com/marianojuarez/status/1148739501604450304*

## Data

### `data/videos`

Contains metadata for videos, example:
```json
{
  "videoId": "0FC2hPICv_I",
  "thumbnail": {
    "thumbnails": [
      {
        "url": "https://i.ytimg.com/vi/0FC2hPICv_I/hqdefault.jpg?sqp=-oaymwEbCKgBEF5IVfKriqkDDggBFQAAiEIYAXABwAEG&rs=AOn4CLDK79ljIlhRvG3rQFqewL1AKzIuBw",
        "width": 168,
        "height": 94
      },
      {
        "url": "https://i.ytimg.com/vi/0FC2hPICv_I/hqdefault.jpg?sqp=-oaymwEbCMQBEG5IVfKriqkDDggBFQAAiEIYAXABwAEG&rs=AOn4CLBKCkdK_f6bUJiITyk7kKIFpJ8XTA",
        "width": 196,
        "height": 110
      },
      {
        "url": "https://i.ytimg.com/vi/0FC2hPICv_I/hqdefault.jpg?sqp=-oaymwEcCPYBEIoBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLCmZy5ycp9vPqvw9gFfPG_TBc97iQ",
        "width": 246,
        "height": 138
      },
      {
        "url": "https://i.ytimg.com/vi/0FC2hPICv_I/hqdefault.jpg?sqp=-oaymwEcCNACELwBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLC07voSlTHWDbnvsgZI6mrje6o3ew",
        "width": 336,
        "height": 188
      }
    ]
  },
  "title": {
    "runs": [
      {
        "text": "Regreso voluntario y seguro a clases presenciales. Ciclo 2021-2022. Conferencia presidente AMLO"
      }
    ],
    "accessibility": {
      "accessibilityData": {
        "label": "Regreso voluntario y seguro a clases presenciales. Ciclo 2021-2022. Conferencia presidente AMLO by Andr\u00e9s Manuel L\u00f3pez Obrador Streamed 2 years ago 2 hours, 5 minutes 726,953 views"
      }
    }
  },
  "lengthSeconds": "7558"
}
```

### `data/transcriptions_raw`

Contains transcriptions with timestamps and duration, example:
```json
[
  {
    "text": "a los conservadores corruptos",
    "start": 8210.7,
    "duration": 7.979
  },
  {
    "text": "es la estrategia m\u00e1s usual",
    "start": 8214.479,
    "duration": 7.801
  },
  {
    "text": "para socavar para destruir Un gobierno",
    "start": 8218.679,
    "duration": 6.601
  },
  {
    "text": "popular",
    "start": 8222.28,
    "duration": 3.0
  }
]
```

### `data/merged_transcriptions_flattened`

Contains flattened text with transcriptions, example:
```
todo este fruto podrido todo esto se heredó de la aplicación de una política económica antipopular y entreguista donde lo único que les importaba saquear robar el gobierno no estaba hecho para servir al pueblo estaba convertido en un facilitador para la corrupción todavía tenemos y enfrentar esa inercia esa la herencia ese fruto podrido ese cochinero que nos dejaron pero vamos a limpiar al país se va a acabar la corrupción se va a acabar la impunidad y va a haber justicia me canso ganso y estoy optimista porque cuento con el apoyo de las fuerzas armadas
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
3. Run the scraper script which retrieves all videos from the official YouTube channel:
```
python scrape.py
```
4. Run the transcriber script which retrieves transcriptions when available or generates them when they are not:
```
python transcribe.py
```
5. Run the merger script which removes timestamps, duration and leaves only flattened text:
```
python flatten.py
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

# TILES demo

A static simple front-end/back-end for TILES

## Installation & Usage with docker compose

The docker setup runs all the components needed for TILES: 

1. The web app
2. Rhasspy backend
3. OpenTTS

Make sure you specify the language code for Rhasspy and OpenTTS in the docker compose file. Check supported languages of [Rhasspy](https://rhasspy.readthedocs.io/en/latest/#supported-languages) and [OpenTTS](https://github.com/synesthesiam/opentts) before. 

To build and run:

```
docker compose build
docker compose up -d
```

## Installation & Usage

In this setup you'd need to run [Rhasspy](https://rhasspy.readthedocs.io/en/latest/installation/) (and OpenTTS if needed) separately. 

Clone repository and install required modules
```bash
$ git clone https://github.com/translatorswb/TILES-demo.git
$ cd TILES-demo
$ pip install -r requirements.txt
```

Run the server

```bash
$ uvicorn app.main:app --reload --port 8080
```

or simply
```bash
$ bash run.sh
```

Visit [http://127.0.0.1:8080/](http://127.0.0.1:8080/) to view the demo.

## Setting up answers and audio

The current TILES demo functions as a Q&A system. The answers need to be specified in a `tsv` format file. Two examples can be seen under `data` directory.

The answers of the audio can be placed under a directory with the same id as the answers in the `tsv` file. It's also possible to use TTS for all or unrecorded answers. In that case the environment variable `TTSFALLBACK` needs to be `1`. 

## Setting up video

TILES plays a video while no interaction is being made. The location of this video is specified in this line of the file `static/tiles.html`:

```html
  <source src="static/TILES_withspeech.mp4" type="video/mp4">
```

## Author

[Alp Öktem](https://alpoktem.github.io), Faizan Ali

## Disclaimer

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

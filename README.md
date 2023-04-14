# TILES demo

A static simple front-end/back-end for TILES

## Installation & Usage with docker compose

```
docker compose build
docker compose up -d
```

## Installation & Usage

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

Visit [http://127.0.0.1:8080/](http://127.0.0.1:8080/).

## Author

[Alp Öktem](https://alpoktem.github.io), Faizan Ali

## Disclaimer

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

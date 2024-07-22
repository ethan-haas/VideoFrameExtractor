<h1>VideoFrameExtractor: Efficient Multi-Video Frame Extraction Tool</h1>

<p>VideoFrameExtractor is a powerful and flexible Python tool for extracting frames from video files. It's designed to handle single videos or entire directories of videos, making it perfect for dataset creation, video analysis, and more.</p>

<h2>Features</h2>
<ul>
  <li>Extract frames from single video files or entire directories</li>
  <li>Support for multiple video formats (mp4, mkv, avi, mov)</li>
  <li>Configurable frame skip rate for customized extraction density</li>
  <li>Output frames in JPG or PNG format with adjustable quality</li>
  <li>Multiprocessing support for faster extraction on multi-core systems</li>
  <li>Detailed logging of video information and extraction progress</li>
  <li>Option to preserve input directory structure in output</li>
</ul>

<h2>Usage</h2>
<pre><code>python video_frame_extractor.py -i [INPUT] -o [OUTPUT] [OPTIONS]</code></pre>

<h3>Arguments:</h3>
<ul>
  <li><code>-i, --input</code>: Path to input video file or directory (required)</li>
  <li><code>-o, --output</code>: Path to output directory (optional, defaults to input directory)</li>
  <li><code>-p, --parent</code>: Include parent directory of video in output path</li>
  <li><code>-f, --format</code>: Image format for extracted frames (jpg or png, default: jpg)</li>
  <li><code>--frame_skip</code>: Number of frames to skip between extractions (default: 1)</li>
  <li><code>--quality</code>: Quality of extracted images (0-100, default: 100 for JPG)</li>
  <li><code>--processes</code>: Number of processes to use (default: number of CPU cores)</li>
</ul>

<h2>Requirements</h2>
<ul>
  <li>Python 3.x</li>
  <li>av</li>
  <li>Pillow</li>
</ul>

<h2>Installation</h2>
<pre><code>pip install av Pillow</code></pre>

<p>VideoFrameExtractor is an ideal tool for researchers, developers, and anyone working with video processing tasks. Its efficient design and customizable options make it suitable for a wide range of applications.</p>

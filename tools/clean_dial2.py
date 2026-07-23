from pathlib import Path
import re

path = Path("dial2.html")
text = path.read_text(encoding="utf-8")

clean_shell = '''<body>

  <div class="stage">
    <div class="bezel">
      <div class="screen" id="screen" tabindex="0" role="slider"
           aria-label="Payload zoom control"
           aria-valuemin="24" aria-valuemax="300" aria-valuenow="24">
        <svg viewBox="0 0 240 240">
          <circle id="greebleTrack" cx="120" cy="120" r="100.5"
                  fill="none" stroke-width="7"></circle>
          <circle id="greebleFill" cx="120" cy="120" r="100.5"
                  fill="none" stroke-width="7" stroke-linecap="butt"
                  transform="rotate(-90 120 120)"></circle>
          <g id="fovRing"></g>
          <g id="ring"></g>
          <g id="zoomLabels"></g>
          <g id="fovLabelsFixed"></g>
        </svg>
        <div class="readout">
          <div class="eyebrow" id="eyebrowBox">EO LENS</div>
          <div class="value" id="value">024MM</div>
          <div class="fov-box" id="fovBox">FOV 84°</div>
        </div>
      </div>

      <div id="pointerBox"></div>
      <div id="pointerCaret"></div>
    </div>
    <button class="replay-btn" id="replayBtn">Replay Startup</button>
  </div>

<script>'''

text = re.sub(
    r'<body\b[^>]*>.*?<script>',
    clean_shell,
    text,
    count=1,
    flags=re.S,
)

text = text.replace('<!-- saved from url=(0014)about:internet -->\n', '')
text = text.replace('<style type="text/css"></style>', '')
text = text.replace(
    '<html lang="en"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">',
    '<html lang="en">\n<head>\n<meta charset="UTF-8">',
)

engine_comment = '''  // ==========================================================
  // Sequence engine
  // ==========================================================
  //
  // Each step describes its targets, effect, duration, and start time.
  // `start` is the editable timing instruction. It can be absolute:
  //
  //   start: 100
  //     Begin 100ms after the timeline starts.
  //
  // Or it can be relative to another step:
  //
  //   start: { after: 'pointer', at: 0.5 }
  //     Begin halfway through the step named "pointer".
  //
  // `resolveStarts()` translates those readable instructions into an
  // absolute millisecond value called `resolvedStart`, which is what the
  // animation loop uses. Example: if "pointer" starts at 100ms and lasts
  // 500ms, a dependent step using `at: 0.5` gets resolvedStart = 350ms.
  // The original `start` instruction remains unchanged and readable.
  //
  // Relative starts make experiments easy: change `after`, adjust `at`, or
  // reorder dependent steps without maintaining a pile of manual timestamps.
  // A referenced step must appear earlier in the list so its start time has
  // already been resolved.
  //
  // Effects are swappable single-purpose objects. Each has a `reset` method
  // for the pre-sequence state and an `apply` method for progress from 0 to 1.
  // New effects can be added without changing the timeline runner.

'''

text = re.sub(
    r'  // ={58}\n  // Sequence engine\n  // ={58}\n.*?(?=  function resolveStarts)',
    engine_comment,
    text,
    count=1,
    flags=re.S,
)

sequence_comment = '''  // ==========================================================
  // Sequence definition — zoom ring
  // ==========================================================
  //
  // This list is the experiment board. The engine does not require a fixed
  // visual order. Reorder steps, change their `start` relationships, assign
  // different durations, or swap effects to test another rhythm.
  //
  // The current experiment is:
  //   pointer -> major ticks -> minor ticks -> ring
  // Each step waits for the previous one to finish (`at: 1`). Changing `at`
  // to 0.5 starts the next step halfway through the previous fade. Values
  // below 1 overlap; values above 1 add a pause after the referenced step.

'''

text = re.sub(
    r'  // ={58}\n  // Sequence definition — zoom ring\n  // ={58}\n.*?(?=  const T_CASCADE)',
    sequence_comment,
    text,
    count=1,
    flags=re.S,
)

path.write_text(text, encoding="utf-8")

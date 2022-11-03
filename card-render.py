#!/usr/bin/env python

DEBUG=1

import simfile
import os

from collections import defaultdict
from simfile.timing import TimingData
from simfile.notes import NoteData
from simfile.notes.count import count_mines

# loaded_simfiles[TITLE] = {PATTERN: LEVEL}
# e.g. loaded_simfiles['Happy'] = {'Challenge': 10}
loaded_simfiles = defaultdict(dict)

diff_to_ddr = {
  'Beginner': 'bSP',
  'Easy': 'BSP',
  'Medium': 'DSP',
  'Hard': 'ESP',
  'Challenge': 'CSP'
}


def debug(msg):
  if DEBUG:
    print(msg)


ignored_titles = set()
with open('ignored-titles.txt', 'r') as f:
  for line in f:
    if not line.strip() or line.startswith('#') or line.startswith('//'):
      continue
    ignored_titles.add(line.strip())


def is_interesting_chart(sim, chart):  # -> Optional[List[str]]
  # throw out stuff that we know isn't actually in A20 PLUS
  if sim.title in ignored_titles:
    debug(f"Title [{sim.title}] is blocklisted, ignoring...")
    return []

  # throw out stuff that isn't in pools
  if chart.stepstype != 'dance-single' or int(chart.meter) < 10:
    return []

  timing_data = TimingData(sim, chart)
  debug(f"Deciding whether {sim.title} is interesting...")
  
  features = []

  # are there any stops? if so, we gotta practice them
  if timing_data.stops:
    debug(f"... decided that it's interesting because it has at least one stop")
    features.append('stops')

  # flag as interesting if any BPM changes are off by more than 10% from the first BPM
  # (calibrated, so to speak, by assuming PARANOiA's BPM changes are not "interesting")
  interesting_bpm_threshold = 0.10

  first_bpm = timing_data.bpms[0]
  for change in timing_data.bpms[1:]:
    debug(f"... deciding whether {change.value}/{first_bpm.value} > {interesting_bpm_threshold}...")
    if abs(1 - (change.value/first_bpm.value)) > interesting_bpm_threshold:
      debug("...... it is!")
      features.append('BPM changes')
      break

  if count_mines(NoteData(chart)) > 0:
    debug(f"... oooh, it has shocks")
    features.append('shocks')

  return features

if __name__ == "__main__":
  for file_dir in os.listdir('simfiles'):
    if file_dir.startswith('.'):
      next

    for file in os.listdir(f'simfiles/{file_dir}'):
      filename = f'simfiles/{file_dir}/{file}'

      try:
        sim = simfile.open(filename)

        for chart in sim.charts:
          chart_features = is_interesting_chart(sim, chart)

          if chart_features:
            loaded_simfiles[sim.title][chart.difficulty] = (int(chart.meter), chart_features)
      except Exception as e:
        print(f"Failed to load {filename}: {e}")
        raise e from None

  for title, charts in loaded_simfiles.items():
    for difficulty, traits in charts.items():
      print(f"{traits[0]}: {title} {diff_to_ddr[difficulty]} -- {', '.join(traits[1])}")

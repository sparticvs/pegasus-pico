Pegasus Pico
==============

Leverages MicroPython on a Pi Pico W and a custom debounce circuit to
track the state of a door.

Intended to be used with at magnet and reed door sensor.

Requirements
------------

- Micropython
- umqtt.simple
- mpremote (recommended)

Setup
------

### Assumptions
This assumes that the Pi Pico W already has micropython installed.

### Step 1
Edit `config.json.example` to have your wifi and mqtt server configuration.
Save as `config.json`.

### Step 2
Load the code!

```bash
mpremote cp main.py :main.py
mpremote cp config.json :config.json
```

### Step 3 (recommended)
Interactive run to test it works

```bash
mpremote run main.py
```

### Step 4
Profit.

```bash
mpremote reset
```

In my experience, the Pi Pico W needs a reset via mpremote instead of a PoR to
get it to start working without an interactive connection.

License
-------

See LICENSE. In short this is CC4.0-BY-NC-SA. Contact me for
a commercial license. We will talk about volume expectations
and a fee schedule.

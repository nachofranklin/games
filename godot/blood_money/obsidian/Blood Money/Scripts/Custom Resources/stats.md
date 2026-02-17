---
Extends: Resource
Class Name: Stats
---
#### What it needs to do

- stats will be where the shared data for characters/enemies are, so things like health, max health, block, base block, art
- health and block need setter functions to not exceed limits and to emit a stats changed signal
- needs a func to take damage correctly so that it first gets consumed by block and then health
- heal func
- a create_instance func that will duplicate the stats resource to keep instances of enemies separate from each other. Then also sets the health and block to max health and zero (not sure if i'll need that bit or not?)

#### How to do it

- create a stats_changed signal
- export var for max health and art
- setter var for health and block
- func for the rest
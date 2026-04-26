const
- [[Tile]]

export var
- board width (row)
- board height (col)
- tile size
- light square colour
- dark square colour
- selected colour

var
- grid: array = []
- last tile selected: tile = null

func

ready
- generate board
- events.tile clicked.connect
- last tile selected = null

generate board
- grid.clear()
- for row in board height:
	- var row array = []
	- for col in board width:
		- instantiate tile scene
		- give the tile the info it needs (colour = if (row + col) % 2 == 0)
		- tile position = Vector2(col * tile_size, row * tile_size)
		- row array.append(tile)
		- add child(tile)
	- grid.append(row array)

on tile clicked(pos)
- var tile = grid[pos.y][pos.x]
- 1) select a tile and the last tile was null
- 2) select a tile and the last tile == selected tile
- 3) select a tile and the last tile != selected tile
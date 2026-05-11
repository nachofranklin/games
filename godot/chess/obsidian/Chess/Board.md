const
- [[Tile]]

export var
- board width (row)
- board height (col)
- available size (to be passed in by [[Game State]])
- light square colour
- dark square colour
- selected colour

var
- grid: array = []
- tile size
- last tile selected: tile = null

func

ready
- calculate tile size
- generate board
- events.tile clicked.connect
- last tile selected = null

calculate tile size -> void (updates tile size)
- get max width/height by doing available size.x/y / board width/height
- take the min of the two

generate board -> void (updates grid)
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

centre board (assumes the node is centred)
- centres board

on tile clicked
- 3 possible options
	- 1) last tile == null
	- 2) last tile == newly selected tile
	- 3) last tile != newly selected tile
- controls logic for selecting and unselecting tiles (changing the selected var to true/false and changing the tile colour to show it's been selected or not)
- also needs to show possible moves (and/or un show possible moves of the last tile) - this bit needs to be in [[Game State]]
	- needs to be able to tell the piece resource on the square
		- how? - [[Board State]]
	- should the pieces store their possible moves? - yes i think so
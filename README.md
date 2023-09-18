# GraphX
GraphX is a Python-based in-memory graph storage engine designed to facilitate the representation of complex relational queries, enabling users to store data while effectively capturing relationships between individual data points.

## Usage
- Create GraphX
```
## nodes have to be a list of the values you want to store, and edges have to be a dictionary that describes the relationships
graph = GraphX(<nodes if not then None>, <edges if not then None>)
```
- Edges And Nodes Example Input
```
## Nodes' values can be any primitive type, even class instances will work too
nodes = [1, 2, 3, 4, 5, 6]

## Edges' have to include two keys(required) "from" and "to" to indicate the relationship
## and optional tag name "forward" to indicate "from" value to "to" value. And optional 
## "backward" tag name to indicate "to" value to "from" value
## if "forward" is not assigned, the tag name will be defaulted as "forward"
## the "backward" key relies on user inputs only, which will not be generated automatically

edges = [
    {"from": 1, "to": 2, "forward": "son"},
    {"from": 2, "to": 3, "forward": "son"},
    {"from": 2, "to": 4, "forward": "son"},
    {"from": 2, "to": 5, "forward": "son"},
    {"from": 2, "to": 6, "forward": "daughter"},
    {"from": 3, "to": 4, "forward": "brother", "backward": "brother"},
    {"from": 4, "to": 5, "forward": "brother", "backward": "brother"},
    {"from": 5, "to": 3, "forward": "brother", "backward": "brother"},
    {"from": 3, "to": 6, "forward": "sister", "backward": "brother"},
    {"from": 4, "to": 6, "forward": "sister", "backward": "brother"},
    {"from": 5, "to": 6, "forward": "sister", "backward": "brother"},
]

```
- Add Node(s) And Edge(s) Easily!
```
## GraphX supports differnt methods to call such as

1. def add_node(self, value) -> None:
        
2. def add_nodes(self, values: List) -> None:
      
3. def add_edge(self, relationship: Dict) -> None:
        
4. def add_edges(self, relationships: List[Dict]) -> None:
```

- Queries, The Coolest Feature!
```
## After users inserted nodes and edges, user can query based on different inputs, supported queries include
1.  def node(self, value) -> Query
2.  def forward(self, **kwargs) -> Query
3.  def backward(self, **kwargs) -> Query
4.  def unique(self) -> Query
5.  def take(self, num: int) -> Query
6.  def filter(self, *args) -> Query
7.  def exclude(self, *args) -> Query
8.  def sort(self, ascending=True) -> Query
9.  def tag(self, name: str) -> Query # name has to be unique
10. def merge(self, *args) -> Query
11. def run(self) -> List[<Your Selected Stored Values>] ## core method

## The users are able to chain query like
g = GraphX()
g.query().node(<your value>).forward(name_is="your name1").tag(<tag name 1>).backward(name_startswith="your name2").forward().exclude(<value 1>, <value 2>).take(6).tag(<tag name 2>).merge(<tag name 1>, <tag name 2>, ...).unique().run()

## Addding custom alias to your query!
## Define your functions that return self(query type)
def grandson(_self):
    return _self.forward().forward()

def nullcall(_self):
    return _self

## add alias
Query.add_alias("grandson", grandson)
Query.add_alias("nullcall", nullcall)
## good to go
nodes = g.query().node(1).grandson().nullcall().run()

## the forward and backward query supports name_startswith, name_endswith, name_contains, and name_is as optional kwargs
## in every query the node() has to be called first, and in each query it has to end with run()
```

## Features
- 📊 Intuitive Graph Creation -- Easily create graphs by defining nodes and edges.
- 🔧 Flexible Data Manipulation -- Seamlessly add single or multiple edges to the graph.
- 🔍 Advanced Querying -- Query the graph based on various criteria.
- 🔗 Chaining Queries -- Implemented Lazy Queries to boost up the performance                                                
## Ideas
The original idea came from https://aosabook.org/en/

## System Setup
To run this project run the command 'pip install -r requirements.txt'

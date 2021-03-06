var diameter = 1400,
    radius = diameter / 2,
    innerRadius = radius - 320;

var cluster = d3.cluster()
    .size([360, innerRadius]);

var line = d3.radialLine()
    .curve(d3.curveBundle.beta(0.85))
    .radius(function(d) { return d.y; })
    .angle(function(d) { return d.x / 180 * Math.PI; });

var svg = d3.select("center").append("svg")
    .attr("width", diameter)
    .attr("height", diameter - 510)
  .append("g")
    .attr("transform", "matrix(0.75 0 0 0.75 " + radius + " " + (radius - 240) + ")")

var link = svg.append("g").selectAll(".link"),
    node = svg.append("g").selectAll(".node");
window.onload = function() {
    document.getElementById("text").innerHTML = "Nothing Highlighted. Mouse over something!"
}

d3.queue()
    .defer(d3.json, "http://api.esportguru.com/games")
    .defer(d3.json, "http://api.esportguru.com/players")
    .defer(d3.json, "http://api.esportguru.com/teams")
    .defer(d3.json, "http://api.esportguru.com/tournaments")
    .await(function(error, games, players, teams, tournaments) {

        games = [games[0]];
        players = players.filter(function(player) {
            return player.current_game.id == 1;
        });
        teams = teams.filter(function(team) {
            return team.current_game.id == 1;
        });
        tournaments = tournaments.filter(function(tournament) {
            return tournament.game.id == 1;
        });

  var classes = makeClasses(games, players, teams, tournaments);
  console.log(classes);

  if (error) throw error;

  var root = packageHierarchy(classes)
      .sum(function(d) { return d.size; });

  cluster(root);

  link = link
    .data(packageImports(root.leaves()))
    .enter().append("path")
      .each(function(d) { d.source = d[0], d.target = d[d.length - 1]; })
      .attr("class", "link")
      .attr("d", line);

  node = node
    .data(root.leaves())
    .enter().append("text")
      .attr("class", "node")
      .attr("dy", "0.31em")
      .attr("transform", function(d) { return "rotate(" + (d.x - 90) + ")translate(" + (d.y + 8) + ",0)" + (d.x < 180 ? "" : "rotate(180)"); })
      .attr("text-anchor", function(d) { return d.x < 180 ? "start" : "end"; })
      .text(function(d) { return d.data.key; })
      .on("mouseover", mouseovered)
      .on("mouseout", mouseouted);
});

function mouseovered(d) {
  node
      .each(function(n) { n.target = n.source = false; });

  mouse_over = d.data.name.split(':')[1];
  connected = [];

  link
      .classed("link--target", function(l) { if (l.target === d) return l.source.source = true; })
      .classed("link--source", function(l) { if (l.source === d) return l.target.target = true; })
    .filter(function(l) { if(l.target === d) {connected.push(l.source.data.name.split(':')[1]);} if(l.source === d) {connected.push(l.target.data.name.split(':')[1]);} return l.target === d || l.source === d; })
      .raise();
  
  document.getElementById("text").innerHTML = "<p><strong>" + mouse_over + "</strong> is connected to:</p><p>" + connected.join(", ") + "</p>"

  node
      .classed("node--target", function(n) { return n.target; })
      .classed("node--source", function(n) { return n.source; });
}

function mouseouted(d) {
  link
      .classed("link--target", false)
      .classed("link--source", false);
  document.getElementById("text").innerHTML = "Nothing Highlighted. Mouse over something!"

  node
      .classed("node--target", false)
      .classed("node--source", false);
}

// Lazily construct the package hierarchy from class names.
function packageHierarchy(classes) {
  var map = {};

  function find(name, data) {
    var node = map[name], i;
    if (!node) {
      node = map[name] = data || {name: name, children: []};
      if (name.length) {
        node.parent = find(name.substring(0, i = name.lastIndexOf(":")));
        node.parent.children.push(node);
        node.key = name.substring(i + 1);
      }
    }
    return node;
  }

  classes.forEach(function(d) {
    find(d.name, d);
  });

  return d3.hierarchy(map[""]);
}

// Return a list of imports for the given array of nodes.
function packageImports(nodes) {
  var map = {},
      imports = [];

  // Compute a map from name to node.
  nodes.forEach(function(d) {
    map[d.data.name] = d;
  });

  // For each import, construct a link from the source to target node.
  nodes.forEach(function(d) {
    if (d.data.imports) d.data.imports.forEach(function(i) {
      imports.push(map[d.data.name].path(map[i]));
    });
  });

  return imports;
}

function makeClasses(games, players, teams, tournaments) {
    classes = [];

    teams.forEach(function(team) {
        if(idExists(games, team.current_game.id)) {
            classes.push({
                name: 'team:' + team.name,
                imports: []
            });
        }
    });

    tournaments.forEach(function(tournament) {
        if(idExists(games, tournament.game.id)) {
            var imports = [];
            tournament.teams.forEach(function(team) {
                if(idExists(teams, team.id)) {
                    imports.push('team:' + team.name);
                }
            });

            classes.push({
                name: 'tournament:' + tournament.name,
                imports: imports
            });
        }
    });

    return classes;
}

function idExists(items, id) {
    return items.some(function(item) {
        return item.id == id;
    });
}

const width = 600;
const height = 600;

const svg = d3.select("svg").attr("width", width).attr("height", height);

svg.append("g").attr("class", "links");
svg.append("g").attr("class", "nodes");
svg.append("g").attr("class", "text");

let nodes = []
let links = []

async function get_data() {
	let string = await handler.get_nodes();
	nodes = JSON.parse(string);

	string = await handler.get_links();
	links = JSON.parse(string);

	const simulation = d3
		.forceSimulation(nodes)
		.force(
			"link",
			d3
				.forceLink(links)
				.id((d) => d.path)
				.distance(100)
		)
		.force("charge", d3.forceManyBody().strength(400))
		.force("center", d3.forceCenter(width / 2, height / 2))
		.force("collision", d3.forceCollide(40));

	const link = d3
		.select("svg")
		.select(".links")
		.selectAll("line")
		.data(links)
		.enter()
		.append("line")
		.attr("style", "stroke:black;stroke-width:2");

	link.exit().remove();

	const node = d3
		.select("svg")
		.select(".nodes")
		.selectAll("circle")
		.data(nodes)
		.enter()
		.append("circle")
		.attr("r", 10)
		.attr("fill", "green")
		.on("click", (_, d) => handler.ret_path(d.path));
	
	node.exit().remove();

	const text = d3
		.select("svg")
		.select(".text")
		.selectAll("text")
		.data(nodes)
		.enter()
		.append("text")
		.attr("width", 100)
		.attr("height", 50)
		.attr("text-anchor", "middle")
		.text((d) => d.name);
	
	text.exit().remove();

	simulation.on("tick", () => {
		link.attr("x1", (d) => d.source.x)
			.attr("y1", (d) => d.source.y)
			.attr("x2", (d) => d.target.x)
			.attr("y2", (d) => d.target.y);
		node.attr("cx", (d) => d.x).attr("cy", (d) => d.y);
		text.attr("x", (d) => d.x).attr("y", (d) => d.y - 20);
	});
	function drag(simulation) {
		function dragstarted(event) {
			if (!event.active) simulation.alphaTarget(0.3).restart();
			event.subject.fx = event.subject.x;
			event.subject.fy = event.subject.y;
		}
		function dragged(event) {
			event.subject.fx = event.x;
			event.subject.fy = event.y;
		}
		function dragended(event) {
			if (!event.active) simulation.alphaTarget(0);
			event.subject.fx = null;
			event.subject.fy = null;
		}
		return d3
			.drag()
			.on("start", dragstarted)
			.on("drag", dragged)
			.on("end", dragended);
	}
	node.call(drag(simulation));
}

new QWebChannel(qt.webChannelTransport, async function (channel) {
	window.handler = channel.objects.handler;

	await get_data();
});

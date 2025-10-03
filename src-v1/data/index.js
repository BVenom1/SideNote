const open_file_button = document.getElementById("open-file");
new QWebChannel(qt.webChannelTransport, async function (channel) {
	window.handler = channel.objects.handler;

	let string = await handler.get_nodes();
	const nodes = JSON.parse(string);

	string = await handler.get_links();
	const links = JSON.parse(string);

	const width = 600;
	const height = 600;

	const simulation = d3
		.forceSimulation(nodes)
		.force(
			"link",
			d3
				.forceLink(links)
				.id((d) => d.path)
				.distance(80)
		)
		.force("charge", d3.forceManyBody().strength(-400))
		.force("center", d3.forceCenter(width / 2, height / 2));

	const svg = d3.select("svg").attr("width", width).attr("height", height);

	const link = svg
		.append("g")
		.attr("class", "links")
		.selectAll("line")
		.data(links)
		.enter()
		.append("line")
		.attr("style", "stroke:black;stroke-width:2");

	const node = svg
		.append("g")
		.attr("class", "nodes")
		.selectAll("circle")
		.data(nodes)
		.enter()
		.append("circle")
		.attr("r", 10)
		.attr("fill", "green")
		.on("click", (_, d) => console.error(d.name));

	const text = svg
		.append("g")
		.attr("class", "text")
		.selectAll("text")
		.data(nodes)
		.enter()
		.append("text")
		.attr("width", 100)
		.attr("height", 50)
		.attr("text-anchor", "middle")
		.text((d) => d.name);

	bbox = text.nodes().map((n) => n.getBBox());

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
});

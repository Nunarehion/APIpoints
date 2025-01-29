document.addEventListener("submit", function (event) {
	event.preventDefault();
	const formData = new FormData(event.target);
	const data = Object.fromEntries(formData);

	console.log("Data to be sent:", data);
	fetch("/" + data.formName, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify(data),
	})
		.then(response => {
			if (!response.ok) {
				throw new Error("Network response was not ok");
			}
			return response.json();
		})
		.then(data => {
			console.log("Success:", data);
		})
		.catch(error => {
			console.error("Ошибка:", error);
		});
});

document.addEventListener("alpine:init", () => {
	Alpine.data("dataStore", () => ({
		dataTest: "mem",

		getData(endpoint) {
			fetch(endpoint)
				.then(response => {
					if (!response.ok) {
						throw new Error(`Error: ${response.statusText}`);
					}
					return response.json();
				})
				.then(data => {
					const fullUrl = `${window.location.origin}${endpoint}`;
					const formattedEndpoint = endpoint
						.replace(/^\//, "")
						.replace(/^./, str => str.toUpperCase());

					data.fullUrl = fullUrl;

					this.window.dataTable = Object.assign(this.window.dataTable, {
						[formattedEndpoint]: data,
					});
				})
				.catch(error => {
					alert(error);
				});
		},

		getUsers() {
			this.getData("/users");
		},
		getProducts() {
			this.getData("/products");
		},
		getCards() {
			this.getData("/cards");
		},
		getPayments() {
			this.getData("/payments");
		},
		getAll() {
			this.getUsers();
			this.getProducts();
			this.getCards();
			this.getPayments();
		},

		window: {
			state: Array.from(document.querySelectorAll(".sidebar a")).map(
				link => link.textContent
			)[0],
			states: Array.from(document.querySelectorAll(".sidebar a")).map(
				link => link.textContent
			),
			setState(text) {
				this.state = text;
			},
			dataTable: {},
		},

		init() {
			this.getAll();
		},
	}));
});

// Function to populate the dropdown with branch names
function populateBranches(branches) {
	const branchSelect = document.getElementById("branchSelect");
	branchSelect.innerHTML = ""; // Clear existing options
	branches.forEach((branch) => {
		console.log(branch);
		const option = document.createElement("option");
		option.value = branch;
		option.textContent = branch;
		branchSelect.appendChild(option);
	});
}
document.getElementById("repoUrl").onblur = async function () {
	const repoUrl = document.getElementById("repoUrl").value;

	const response = await fetch("/fetch-branches", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({ repo_url: repoUrl }),
	});

	if (response.ok) {
		const branches = await response.json();
		populateBranches(branches);
	} else {
		// Handle errors or no branches found
		console.error("Failed to fetch branches");
	}
};
document.getElementById("button-addon2").onclick = async function () {
	// Get the selected branch
	let selectedBranch = document.getElementById("branchSelect").value;

	// Ensure a branch is selected
	if (selectedBranch === "Choose a branch...") {
		alert("Please select a branch");
		return;
	}
	// Show loading spinner
	document.getElementById("loading-spinner").style.display = "inline-block";
	// Hide arrow icon
	document.getElementById("arrow-icon").style.display = "none";

	let repoUrl = document.getElementById("repoUrl").value;
	let response = await fetch("/generate-markdown", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({ repo_url: repoUrl, branch: selectedBranch }),
	});
	let data = await response.json();

	// Hide loading spinner
	document.getElementById("loading-spinner").style.display = "none";
	// Show arrow icon
	document.getElementById("arrow-icon").style.display = "inline-block";

	document.getElementById("markdownOutput").value =
		data.linkedMarkdown || "Error generating markdown.";
};

document.getElementById("copyButton").addEventListener("click", function () {
	const markdownOutput = document.getElementById("markdownOutput");
	markdownOutput.select(); // Select the text
	document.execCommand("copy"); // Copy to clipboard
	markdownOutput.setSelectionRange(0, 0); // Deselect text
	// Indicate to the user that text was copied (change this to a less disruptive feedback)
	alert("Copied to clipboard!");
});

document
	.getElementById("downloadButton")
	.addEventListener("click", function () {
		const markdownOutput = document.getElementById("markdownOutput").value;
		const blob = new Blob([markdownOutput], { type: "text/plain" });
		const href = URL.createObjectURL(blob);
		const link = document.createElement("a");
		link.href = href;
		link.download = "INDEX.md"; // File name for download
		document.body.appendChild(link);
		link.click();
		document.body.removeChild(link);
		URL.revokeObjectURL(href); // Clean up the URL object
	});

// Initialize the markdown converter
const converter = new showdown.Converter();

// Event listener for tab change
$("#markdownTabs a").on("click", function (e) {
	e.preventDefault();
	$(this).tab("show");

	// Check if the preview tab is now active
	if (this.id === "preview-tab") {
		const text = document.getElementById("markdownOutput").value;
		const html = converter.makeHtml(text);
		document.getElementById("markdownPreview").innerHTML = html;
	}
});

document.addEventListener("DOMContentLoaded", function () {
	fetch("/static/json/faqs.json")
		.then((response) => response.json())
		.then((faqs) => {
			const accordionElement = document.getElementById("accordion");
			accordionElement.innerHTML = ""; // Clear current content

			faqs.forEach((faq, index) => {
				// Create the card element
				const card = document.createElement("div");
				card.classList.add("card");

				// Create the card header
				const cardHeader = document.createElement("div");
				cardHeader.classList.add("card-header");
				cardHeader.id = `heading${index}`;

				// Create the button for the card header
				const button = document.createElement("button");
				button.classList.add("btn", "btn-link");
				button.setAttribute("data-toggle", "collapse");
				button.setAttribute("data-target", `#collapse${index}`);
				button.setAttribute("aria-expanded", "false");
				button.setAttribute("aria-controls", `collapse${index}`);
				button.textContent = faq.question;

				// Create the collapse div
				const collapseDiv = document.createElement("div");
				collapseDiv.id = `collapse${index}`;
				collapseDiv.classList.add("collapse");
				if (index === 0) collapseDiv.classList.add("show");
				collapseDiv.setAttribute(
					"aria-labelledby",
					`
              heading${index}`
				);
				collapseDiv.setAttribute("data-parent", "#accordion");
				// Create the card body
				const cardBody = document.createElement("div");
				cardBody.classList.add("card-body");
				cardBody.textContent = faq.answer;

				// Append elements to build the accordion structure
				cardHeader.appendChild(button);
				collapseDiv.appendChild(cardBody);
				card.appendChild(cardHeader);
				card.appendChild(collapseDiv);
				accordionElement.appendChild(card);
			});
		})
		.catch((error) => {
			console.error("Error fetching FAQs:", error);
		});
});

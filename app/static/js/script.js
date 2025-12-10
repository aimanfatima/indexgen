// Function to populate the dropdown with branch names
function populateBranches(branches) {
	const branchSelect = document.getElementById("branchSelect");
	const button = document.getElementById("button-addon2");
	
	branchSelect.innerHTML = ""; // Clear existing options
	
	// Add default option
	const defaultOption = document.createElement("option");
	defaultOption.value = "";
	defaultOption.textContent = "Choose a branch...";
	branchSelect.appendChild(defaultOption);
	
	// Add branch options
	branches.forEach((branch) => {
		console.log(branch);
		const option = document.createElement("option");
		option.value = branch;
		option.textContent = branch;
		branchSelect.appendChild(option);
	});
	
	// Enable the dropdown
	branchSelect.disabled = false;
	
	// Auto-select branch: prefer "main", then "master", otherwise first branch
	let selectedBranch = null;
	if (branches.includes("main")) {
		selectedBranch = "main";
	} else if (branches.includes("master")) {
		selectedBranch = "master";
	} else if (branches.length > 0) {
		selectedBranch = branches[0];
	}
	
	// Set the selected branch
	if (selectedBranch) {
		branchSelect.value = selectedBranch;
		// Enable button since branch is auto-selected
		button.disabled = false;
	} else {
		// No branches available, keep button disabled
		button.disabled = true;
	}
}

// Function to fetch branches when URL is entered
async function fetchBranchesForUrl(repoUrl) {
	const branchSelect = document.getElementById("branchSelect");
	const button = document.getElementById("button-addon2");
	
	// Disable dropdown and button while fetching
	branchSelect.disabled = true;
	button.disabled = true;
	branchSelect.innerHTML = '<option selected>Loading branches...</option>';

	try {
		const response = await fetch("/fetch-branches", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ repo_url: repoUrl }),
		});

		if (response.ok) {
			const branches = await response.json();
			if (branches.length > 0) {
				populateBranches(branches);
			} else {
				branchSelect.innerHTML = '<option selected>No branches found</option>';
				branchSelect.disabled = true;
			}
		} else {
			// Handle errors
			branchSelect.innerHTML = '<option selected>Error loading branches</option>';
			branchSelect.disabled = true;
		}
	} catch (error) {
		branchSelect.innerHTML = '<option selected>Error loading branches</option>';
		branchSelect.disabled = true;
	}
}

// Debounce function to avoid too many API calls
function debounce(func, wait) {
	let timeout;
	return function executedFunction(...args) {
		const later = () => {
			clearTimeout(timeout);
			func(...args);
		};
		clearTimeout(timeout);
		timeout = setTimeout(later, wait);
	};
}

// Set up URL input listener - fetch branches as user types (with debounce)
const debouncedFetchBranches = debounce(async function() {
	const repoUrl = document.getElementById("repoUrl").value.trim();
	const branchSelect = document.getElementById("branchSelect");
	const button = document.getElementById("button-addon2");
	
	if (!repoUrl) {
		// Reset if URL is empty
		branchSelect.innerHTML = '<option selected>Choose a branch...</option>';
		branchSelect.disabled = true;
		button.disabled = true;
		return;
	}
	
	// Validate GitHub URL format
	if (!repoUrl.includes("github.com")) {
		branchSelect.innerHTML = '<option selected>Invalid GitHub URL</option>';
		branchSelect.disabled = true;
		button.disabled = true;
		return;
	}
	
	await fetchBranchesForUrl(repoUrl);
}, 500); // Wait 500ms after user stops typing

document.getElementById("repoUrl").addEventListener("input", debouncedFetchBranches);

// Handle branch selection - enable button when branch is selected
document.getElementById("branchSelect").addEventListener("change", function() {
	const button = document.getElementById("button-addon2");
	const selectedBranch = this.value;
	
	if (selectedBranch && selectedBranch !== "" && selectedBranch !== "Choose a branch...") {
		button.disabled = false;
	} else {
		button.disabled = true;
	}
});
document.getElementById("button-addon2").onclick = async function () {
	// Get the selected branch
	let selectedBranch = document.getElementById("branchSelect").value;

	// Ensure a branch is selected (button should be disabled if not, but double-check)
	if (!selectedBranch || selectedBranch === "" || selectedBranch === "Choose a branch...") {
		alert("Please select a branch");
		return;
	}
	
	// Disable button during processing
	this.disabled = true;
	
	// Show loading spinner
	document.getElementById("loading-spinner").style.display = "inline-block";
	// Hide arrow icon
	document.getElementById("arrow-icon").style.display = "none";

	let repoUrl = document.getElementById("repoUrl").value;
	
	try {
		let response = await fetch("/generate-markdown", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ repo_url: repoUrl, branch: selectedBranch }),
		});
		let data = await response.json();

		document.getElementById("markdownOutput").value =
			data.linkedMarkdown || "Error generating markdown.";
	} catch (error) {
		document.getElementById("markdownOutput").value = "Error generating markdown. Please try again.";
	} finally {
		// Hide loading spinner
		document.getElementById("loading-spinner").style.display = "none";
		// Show arrow icon
		document.getElementById("arrow-icon").style.display = "inline-block";
		// Re-enable button (branch selection handler will manage its state)
		this.disabled = false;
		// Re-check branch selection to set button state correctly
		const branchSelect = document.getElementById("branchSelect");
		if (branchSelect.value && branchSelect.value !== "" && branchSelect.value !== "Choose a branch...") {
			this.disabled = false;
		} else {
			this.disabled = true;
		}
	}
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
	// Initialize UI state - disable dropdown and button initially
	const branchSelect = document.getElementById("branchSelect");
	const button = document.getElementById("button-addon2");
	
	if (branchSelect) {
		branchSelect.disabled = true;
	}
	if (button) {
		button.disabled = true;
	}
	
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
		});
});

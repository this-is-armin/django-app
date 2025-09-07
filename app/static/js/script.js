function hiding_message() {
	let message = document.getElementById('message');

	message.style.display = 'none';
}
let interval = setInterval(hiding_message, 5000);


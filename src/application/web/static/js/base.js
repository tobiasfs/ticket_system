const resizer = document.getElementById('resizer');
const box2 = document.getElementById('box-2');
const container = document.getElementById('container');

let isResizing = false;

// 1. When mouse is pressed on the resizer
resizer.addEventListener('mousedown', function(e) {
    isResizing = true;
    // Add class to body to prevent text highlighting while dragging
    document.body.classList.add('user-select-none');
});

// 2. When mouse moves (we attach this to 'window' so it doesn't glitch if mouse moves too fast)
window.addEventListener('mousemove', function(e) {
    if (!isResizing) return;

    // Calculate the new width
    // We need the position of the container to know where the mouse is relative to the start
    const containerRect = container.getBoundingClientRect();
    
    // The position of the mouse relative to the left edge of the container
    const mouseX = e.clientX - containerRect.left;
    
    // We also need to subtract the width of Box 1 (which is constant at 200px)
    // to find out how much space should be allocated to Box 2
    const box1Width = 200;
    const newWidth = mouseX - box1Width;

    // Apply the new width to Box 2
    if (newWidth > 50) { // Minimum width constraint
        box2.style.width = newWidth + 'px';
    }
});

// 3. When mouse is released
window.addEventListener('mouseup', function() {
    isResizing = false;
    document.body.classList.remove('user-select-none');
});

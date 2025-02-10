// Profile dropdown logic
const profilePhoto = document.getElementById('profile-photo');
const profileDropdown = document.getElementById('profile-dropdown');

profilePhoto.addEventListener('click', function () {
    profileDropdown.classList.toggle('show');
});

window.onclick = function (event) {
    if (!event.target.matches('#profile-photo')) {
        const dropdowns = document.getElementsByClassName('dropdown-content');
        for (let i = 0; i < dropdowns.length; i++) {
            const openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
};

// File Upload Logic
document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const fileInput = document.getElementById('fileInput');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    const response = await fetch('/upload', {
        method: 'POST',
        body: formData,
    });

    const data = await response.json();
    const output = document.getElementById('output');
    const resultSection = document.getElementById('resultSection');

    if (data.file_type === 'image') {
        output.innerHTML = `<img src="${data.url}" alt="Colorized Image">`;
    } else if (data.file_type === 'video') {
        output.innerHTML = `<video controls><source src="${data.url}" type="video/mp4"></video>`;
    }

    resultSection.style.display = 'block';
});


document.getElementById('imageUpload').addEventListener('change', handleFileUpload);
document.getElementById('videoUpload').addEventListener('change', handleFileUpload);

async function handleFileUpload(e) {
    const file = e.target.files[0];
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('/upload', { method: 'POST', body: formData });
    const data = await response.json();

    const output = document.getElementById('output');
    const downloadBtn = document.getElementById('downloadBtn');

    if (data.file_type === 'image') {
        output.innerHTML = `<img src="${data.url}" alt="Colorized Image">`;
    } else if (data.file_type === 'video') {
        output.innerHTML = `<video controls><source src="${data.url}" type="video/mp4"></video>`;
    }

    output.style.display = 'block';
    downloadBtn.style.display = 'block';
    downloadBtn.href = data.url;  // Set the download link to the processed file
}

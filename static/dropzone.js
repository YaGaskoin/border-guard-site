window.addEventListener("DOMContentLoaded", () => {
    const formCreatePost = document.getElementById("create_form");
    const formFiles = document.querySelector("#create_form + form#myDropzone");
    const btn_upload = document.getElementById("upload-btn");
    const fakeInputForDownov = document.createElement('input');
    fakeInputForDownov.name = 'files';
    fakeInputForDownov.style.display = "none";

    formFiles.removeAttribute('action');
    formFiles.removeAttribute('method');

    formCreatePost.dropzone = formFiles.dropzone;

    btn_upload.addEventListener('click', () => {
        fakeInputForDownov.value = JSON.stringify(formFiles.dropzone.files.map(file => {
            return { name: file.name, dataURL: file.dataURL, width: file.width, height: file.height};
        }));
    });

    formCreatePost.appendChild(fakeInputForDownov);
    formCreatePost.appendChild(formFiles);
    formCreatePost.appendChild(btn_upload);
});

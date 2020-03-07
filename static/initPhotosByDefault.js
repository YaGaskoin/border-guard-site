window.addEventListener("DOMContentLoaded", () => {
    const el_photos = document.getElementById('tempPhotos');
    const el_dropzone = document.getElementById('myDropzone');

    let photos = el_photos.dataset.photos;
    photos = photos.split(',');

    photos.forEach( (photo_link) => {
        const parsedLink = photo_link.split('/');
        const name = parsedLink[parsedLink.length-1];
        const ext = photo_link.split('.')[1];
        const path = parsedLink.slice(0, parsedLink.length-1).join('/');
        const image = null;

        fetch('http://localhost:5000/static/images/2020_01_30_20_34_55_190492Koala.jpg', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then((response) => {
            response.blob().then((blobStr) => {
                const file = new File([blobStr], name);
                console.log(file);
                el_dropzone.dropzone.files.push(file);
                createHtmlImageDropzone(blobStr);
            })
        });

    });

    function createHtmlImageDropzone(blob) {
        const dropzoneImagePreview = document.createElement('div');
        dropzoneImagePreview.setAttribute('class', 'dz-preview dz-image-preview');
        el_dropzone.appendChild(dropzoneImagePreview);

        const dz_image = document.createElement('div');
        dz_image.setAttribute('class', 'dz-image');

        const imageFromBlob = new Image(blob);
        imageFromBlob.setAttribute('data-dz-thumbnail', true);
        console.log(blob);
        imageFromBlob.src = blob;

        dz_image.appendChild(dropzoneImagePreview);

    }

    function arrayBufferToBase64(buffer) {
      var binary = '';
      var bytes = [].slice.call(new Uint8Array(buffer));

      bytes.forEach((b) => binary += String.fromCharCode(b));

      return window.btoa(binary);
    };

});

Dropzone.autoDiscover = false;

console.log("{{pk}}")

const myDropzone = new Dropzone("#my-dropzone", {
    // url: "upload/{{pk}}",
    maxFiles: 10,
    maxFilesize: 10,
    acceptedFiles: '.jpg, .png, .jpeg',
})
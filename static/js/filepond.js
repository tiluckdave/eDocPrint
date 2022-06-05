FilePond.create(document.querySelector(".with-validation-filepond"), {
    credits: null,
    allowImagePreview: false,
    allowMultiple: true,
    allowFileEncode: false,
    required: true,
    acceptedFileTypes: ["image/png","image/jpg", "image/jpeg"],
    fileValidateTypeDetectType: (source, type) =>
      new Promise((resolve, reject) => {
        // Do custom type detection here and return with promise
        resolve(type);
      }),
  });
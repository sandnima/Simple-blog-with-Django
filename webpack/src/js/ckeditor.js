import ClassicEditor from '@ckeditor/ckeditor5-build-classic';

ClassicEditor
    .create( document.querySelector( '#editor' ), {
        toolbar: {
            items: [
                'heading', '|',
                'bold', 'italic', 'link', 'undo', 'redo', 'bulletedList', 'numberedList', 'blockQuote', '|',
                'alignment',
                'code', 'codeBlock', '|',
            ],
            shouldNotGroupWhenFull: true
        },
    } )
    .catch( error => {
        console.error( error );
    } );